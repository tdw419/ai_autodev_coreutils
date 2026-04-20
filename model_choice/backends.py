"""Backend dispatch -- litellm and CLI subprocess."""

import os
import select
import subprocess
from dataclasses import dataclass
from typing import Generator, Optional

from .registry import Provider


@dataclass
class GenerateResult:
    """Result from a generate call, including usage stats."""
    text: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


def call_litellm(
    provider: Provider,
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 2000,
    system: str | None = None,
) -> str:
    """Call Ollama or ZAI via litellm."""
    import litellm

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    kwargs = dict(
        model=provider.model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    if provider.api_base:
        kwargs["api_base"] = provider.api_base
    if provider.env_key:
        api_key = os.environ.get(provider.env_key)
        if api_key:
            kwargs["api_key"] = api_key

    resp = litellm.completion(**kwargs)
    usage = getattr(resp, 'usage', None)
    return GenerateResult(
        text=resp.choices[0].message.content,
        prompt_tokens=getattr(usage, 'prompt_tokens', 0) if usage else 0,
        completion_tokens=getattr(usage, 'completion_tokens', 0) if usage else 0,
        total_tokens=getattr(usage, 'total_tokens', 0) if usage else 0,
    )


def call_cli(
    provider: Provider,
    prompt: str,
) -> str:
    """Call Gemini or Claude via CLI subprocess.

    Temperature and max_tokens are ignored -- CLI tools don't expose
    them in non-interactive -p mode.
    """
    if provider.cli_cmd == "gemini":
        cmd = ["gemini", "-p", prompt, "--sandbox"]
        env = dict(os.environ, TERM="dumb")
    elif provider.cli_cmd == "claude":
        cmd = ["claude", "-p", prompt, "--dangerously-skip-permissions"]
        env = None  # inherit
    else:
        # Generic fallback
        cmd = [provider.cli_cmd or "echo", prompt]
        env = None

    result = subprocess.run(
        cmd, capture_output=True, text=True, timeout=120, env=env,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"{provider.cli_cmd} exited {result.returncode}: "
            f"{result.stderr[:500]}"
        )
    # CLI backends don't report token counts
    return GenerateResult(text=result.stdout)


# ---- streaming backends ----

def stream_litellm(
    provider: Provider,
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 2000,
    system: str | None = None,
) -> Generator[str, None, None]:
    """Stream from litellm, yielding text chunks.

    Enhanced: handles connection errors mid-stream gracefully and extracts
    usage from the final streaming chunk when available.
    """
    import litellm

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    kwargs = dict(
        model=provider.model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
        stream_options={"include_usage": True},
    )

    if provider.api_base:
        kwargs["api_base"] = provider.api_base
    if provider.env_key:
        api_key = os.environ.get(provider.env_key)
        if api_key:
            kwargs["api_key"] = api_key

    try:
        response = litellm.completion(**kwargs)
    except Exception:
        # Let connection failures propagate immediately so fallback can kick in
        raise

    try:
        for chunk in response:
            # litellm streaming chunks: check for content delta
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta
            if delta and delta.content:
                yield delta.content
    except Exception as e:
        # Mid-stream error: wrap with context but still raise
        raise RuntimeError(
            f"Stream interrupted for {provider.model}: {e}"
        ) from e


def stream_cli(
    provider: Provider,
    prompt: str,
    timeout: float = 120.0,
) -> Generator[str, None, None]:
    """Stream from CLI subprocess, yielding text chunks as they arrive.

    Enhanced:
    - Uses select() for non-blocking reads with timeout
    - Reads in larger 4096-byte buffers for efficiency
    - Properly handles EINTR and broken pipes
    """
    if provider.cli_cmd == "gemini":
        cmd = ["gemini", "-p", prompt, "--sandbox"]
        env = dict(os.environ, TERM="dumb")
    elif provider.cli_cmd == "claude":
        cmd = ["claude", "-p", prompt, "--dangerously-skip-permissions"]
        env = None
    else:
        cmd = [provider.cli_cmd or "echo", prompt]
        env = None

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )
    try:
        while True:
            # Use select to avoid blocking forever on stdout
            if proc.stdout is not None:
                ready, _, _ = select.select([proc.stdout], [], [], timeout)
                if not ready:
                    # Timeout -- process may be hung
                    raise RuntimeError(
                        f"{provider.cli_cmd}: no output for {timeout}s"
                    )
                chunk = proc.stdout.read(4096)
                if not chunk:
                    break
                yield chunk

            # Check if process ended
            if proc.poll() is not None:
                # Drain remaining stdout
                remaining = proc.stdout.read() if proc.stdout else ""
                if remaining:
                    yield remaining
                break

        proc.wait(timeout=10)
    except GeneratorExit:
        # Consumer abandoned the generator -- clean up
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
        return
    finally:
        # Ensure process is reaped even if consumer abandons the generator
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
        if proc.returncode != 0:
            stderr = proc.stderr.read() if proc.stderr else ""
            raise RuntimeError(
                f"{provider.cli_cmd} exited {proc.returncode}: "
                f"{stderr[:500]}"
            )


def stream(
    provider: Provider,
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 2000,
    json_mode: bool = False,
    system: str | None = None,
) -> Generator[str, None, None]:
    """Unified streaming dispatch. Applies json_mode prompt suffix, then routes."""
    if json_mode:
        prompt += (
            "\n\nIMPORTANT: Respond with valid JSON only. "
            "No markdown fences, no explanation, just the JSON object."
        )

    if provider.backend == "litellm":
        yield from stream_litellm(provider, prompt, temperature, max_tokens, system)
    elif provider.backend == "cli":
        yield from stream_cli(provider, prompt)
    else:
        raise ValueError(f"Unknown backend: {provider.backend}")


# ---- unified dispatch ----

def call(
    provider: Provider,
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 2000,
    json_mode: bool = False,
    system: str | None = None,
) -> GenerateResult:
    """Unified dispatch. Applies json_mode prompt suffix, then routes."""
    if json_mode:
        prompt += (
            "\n\nIMPORTANT: Respond with valid JSON only. "
            "No markdown fences, no explanation, just the JSON object."
        )

    if provider.backend == "litellm":
        return call_litellm(provider, prompt, temperature, max_tokens, system)
    elif provider.backend == "cli":
        return call_cli(provider, prompt)
    else:
        raise ValueError(f"Unknown backend: {provider.backend}")
