#!/usr/bin/env python3
"""A minimal symbolic algebra system -- parse, simplify, differentiate."""

from __future__ import annotations

# ── Expression tree ──────────────────────────────────────────────

class Expr:
    """Base expression node."""
    def __add__(self, other): return Add(self, _wrap(other))
    def __radd__(self, other): return Add(_wrap(other), self)
    def __mul__(self, other): return Mul(self, _wrap(other))
    def __rmul__(self, other): return Mul(_wrap(other), self)
    def __pow__(self, other): return Pow(self, _wrap(other))
    def __neg__(self): return Mul(Num(-1), self)
    def __sub__(self, other): return Add(self, Mul(Num(-1), _wrap(other)))
    def __rsub__(self, other): return Add(_wrap(other), Mul(Num(-1), self))
    def __truediv__(self, other): return Mul(self, Pow(_wrap(other), Num(-1)))
    def __eq__(self, other): return type(self) is type(other) and self._key() == other._key()
    def __hash__(self): return hash((type(self).__name__, self._key()))

class Num(Expr):
    def __init__(self, v): self.v = v
    def _key(self): return self.v
    def __repr__(self): return str(self.v) if self.v >= 0 else f"({self.v})"

class Var(Expr):
    def __init__(self, name): self.name = name
    def _key(self): return self.name
    def __repr__(self): return self.name

class Add(Expr):
    def __init__(self, a, b): self.a, self.b = a, b
    def _key(self): return (self.a, self.b)
    def __repr__(self):
        sa, sb = _paren_if_add(self.a), _paren_if_add(self.b)
        return f"{sa} + {sb}"

class Mul(Expr):
    def __init__(self, a, b): self.a, self.b = a, b
    def _key(self): return (self.a, self.b)
    def __repr__(self):
        def fmt(e):
            if isinstance(e, Add): return f"({e})"
            return str(e)
        return f"{fmt(self.a)} * {fmt(self.b)}"

class Pow(Expr):
    def __init__(self, base, exp): self.base, self.exp = base, exp
    def _key(self): return (self.base, self.exp)
    def __repr__(self):
        b = f"({self.base})" if isinstance(self.base, (Add, Mul)) else str(self.base)
        e = f"({self.exp})" if isinstance(self.exp, (Add, Mul)) else str(self.exp)
        return f"{b}^{e}"

class Func(Expr):
    def __init__(self, name, arg): self.name, self.arg = name, arg
    def _key(self): return (self.name, self.arg)
    def __repr__(self): return f"{self.name}({self.arg})"

class Ln(Expr):
    def __init__(self, arg): self.arg = arg
    def _key(self): return self.arg
    def __repr__(self): return f"ln({self.arg})"

class Exp(Expr):
    def __init__(self, arg): self.arg = arg
    def _key(self): return self.arg
    def __repr__(self): return f"exp({self.arg})"

def _wrap(x):
    return x if isinstance(x, Expr) else Num(x)

def _paren_if_add(e):
    return f"({e})" if isinstance(e, Add) else str(e)

# ── Simplifier ───────────────────────────────────────────────────

def simplify(e: Expr) -> Expr:
    """Apply algebraic identities until fixed point."""
    prev = None
    while str(e) != str(prev):
        prev = e
        e = _simp(e)
    return e

def _simp(e: Expr) -> Expr:
    if isinstance(e, (Num, Var)):
        return e

    if isinstance(e, Func):
        a = simplify(e.arg)
        if isinstance(a, Num):
            import math
            funcs = {'sin': math.sin, 'cos': math.cos, 'tan': math.tan, 'sqrt': math.sqrt}
            if e.name in funcs:
                return Num(round(funcs[e.name](a.v), 10))
        return Func(e.name, a)

    if isinstance(e, Ln):
        a = simplify(e.arg)
        if isinstance(a, Num): return Num(round(__import__('math').log(a.v), 10))
        return Ln(a)

    if isinstance(e, Exp):
        a = simplify(e.arg)
        if isinstance(a, Num): return Num(round(__import__('math').exp(a.v), 10))
        return Exp(a)

    if isinstance(e, Add):
        a, b = simplify(e.a), simplify(e.b)
        if isinstance(a, Num) and isinstance(b, Num): return Num(a.v + b.v)
        if isinstance(a, Num) and a.v == 0: return b
        if isinstance(b, Num) and b.v == 0: return a
        if isinstance(b, Mul) and isinstance(b.a, Num) and b.a.v == -1 and b.b == a: return Num(0)
        if isinstance(a, Mul) and isinstance(a.a, Num) and a.a.v == -1 and a.b == b: return Num(0)
        return Add(a, b)

    if isinstance(e, Mul):
        a, b = simplify(e.a), simplify(e.b)
        if isinstance(a, Num) and isinstance(b, Num): return Num(a.v * b.v)
        if isinstance(a, Num) and a.v == 0: return Num(0)
        if isinstance(b, Num) and b.v == 0: return Num(0)
        if isinstance(a, Num) and a.v == 1: return b
        if isinstance(b, Num) and b.v == 1: return a
        return Mul(a, b)

    if isinstance(e, Pow):
        a, b = simplify(e.base), simplify(e.exp)
        if isinstance(b, Num) and b.v == 0: return Num(1)
        if isinstance(b, Num) and b.v == 1: return a
        if isinstance(a, Num) and isinstance(b, Num):
            return Num(round(a.v ** b.v, 10))
        return Pow(a, b)

    return e

# ── Differentiator ───────────────────────────────────────────────

def diff(e: Expr, var: str = 'x') -> Expr:
    """Symbolic derivative d/de_{var}(e)."""
    if isinstance(e, Num):
        return Num(0)                                          # dc/dx = 0

    if isinstance(e, Var):
        return Num(1) if e.name == var else Num(0)             # dx/dx = 1

    if isinstance(e, Add):
        return Add(diff(e.a, var), diff(e.b, var))             # (f+g)' = f' + g'

    if isinstance(e, Mul):
        # Product rule: (fg)' = f'g + fg'
        return Add(Mul(diff(e.a, var), e.b), Mul(e.a, diff(e.b, var)))

    if isinstance(e, Pow):
        if not _contains_var(e.exp, var):
            # Power rule: d/dx[f^n] = n * f^(n-1) * f'
            return Mul(Mul(e.exp, Pow(e.base, Add(e.exp, Num(-1)))), diff(e.base, var))
        if not _contains_var(e.base, var):
            # Exponential: d/dx[a^g] = a^g * ln(a) * g'
            return Mul(Mul(e, Ln(e.base)), diff(e.exp, var))
        # General: d/dx[f^g] = f^g * (g' * ln(f) + g * f'/f)
        return Mul(e, Add(Mul(diff(e.exp, var), Ln(e.base)),
                          Mul(e.exp, Mul(diff(e.base, var), Pow(e.base, Num(-1))))))

    if isinstance(e, Func):
        inner = e.arg
        di = diff(inner, var)
        if e.name == 'sin':
            return Mul(Func('cos', inner), di)                 # cos(u)*u'
        if e.name == 'cos':
            return Mul(Mul(Num(-1), Func('sin', inner)), di)   # -sin(u)*u'
        if e.name == 'tan':
            return Mul(Pow(Func('cos', inner), Num(-2)), di)   # sec^2(u)*u'
        if e.name == 'sqrt':
            return Mul(Mul(Num(0.5), Pow(inner, Num(-0.5))), di)
        raise ValueError(f"Unknown function: {e.name}")

    if isinstance(e, Ln):
        return Mul(Pow(e.arg, Num(-1)), diff(e.arg, var))      # (1/u)*u'

    if isinstance(e, Exp):
        return Mul(e, diff(e.arg, var))                         # exp(u)*u'

    raise ValueError(f"Cannot differentiate: {type(e)}")


def _contains_var(e: Expr, var: str) -> bool:
    if isinstance(e, Num): return False
    if isinstance(e, Var): return e.name == var
    if isinstance(e, (Add, Mul, Pow)): return _contains_var(e.a, var) or _contains_var(e.b, var)
    if isinstance(e, (Func, Ln, Exp)): return _contains_var(e.arg, var)
    return False

# ── Recursive-descent parser ────────────────────────────────────

def parse(s: str) -> Expr:
    """Parse a math expression string into an Expr tree."""
    tokens = _tokenize(s)
    pos, expr = _parse_expr(tokens, 0)
    if pos < len(tokens):
        raise SyntaxError(f"Unexpected token: {tokens[pos]}")
    return expr

def _tokenize(s: str):
    tokens, i = [], 0
    while i < len(s):
        if s[i].isspace(): i += 1; continue
        if s[i] in '+-*/^()': tokens.append(s[i]); i += 1
        elif s[i].isdigit() or (s[i] == '.' and i+1 < len(s) and s[i+1].isdigit()):
            j = i
            while j < len(s) and (s[j].isdigit() or s[j] == '.'): j += 1
            tokens.append(float(s[i:j]) if '.' in s[i:j] else int(s[i:j]))
            i = j
        elif s[i].isalpha():
            j = i
            while j < len(s) and s[j].isalpha(): j += 1
            tokens.append(s[i:j])
            i = j
        else:
            raise SyntaxError(f"Unexpected char: {s[i]}")
    return tokens

def _parse_expr(tokens, pos):
    """expr = term (('+' | '-') term)*"""
    pos, left = _parse_term(tokens, pos)
    while pos < len(tokens) and tokens[pos] in ('+', '-'):
        op = tokens[pos]; pos += 1
        pos, right = _parse_term(tokens, pos)
        left = Add(left, right) if op == '+' else Add(left, Mul(Num(-1), right))
    return pos, left

def _parse_term(tokens, pos):
    """term = power (('*' | '/') power)*"""
    pos, left = _parse_power(tokens, pos)
    while pos < len(tokens) and tokens[pos] in ('*', '/'):
        op = tokens[pos]; pos += 1
        pos, right = _parse_power(tokens, pos)
        left = Mul(left, right) if op == '*' else Mul(left, Pow(right, Num(-1)))
    return pos, left

def _parse_power(tokens, pos):
    """power = unary ('^' power)?  (right-associative)"""
    pos, base = _parse_unary(tokens, pos)
    if pos < len(tokens) and tokens[pos] == '^':
        pos += 1
        pos, exp = _parse_power(tokens, pos)
        return pos, Pow(base, exp)
    return pos, base

def _parse_unary(tokens, pos):
    """unary = '-' unary | atom"""
    if pos < len(tokens) and tokens[pos] == '-':
        pos += 1
        pos, e = _parse_unary(tokens, pos)
        return pos, Mul(Num(-1), e)
    return _parse_atom(tokens, pos)

def _parse_atom(tokens, pos):
    FUNCTIONS = {'sin', 'cos', 'tan', 'sqrt', 'ln', 'exp'}
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of expression")

    t = tokens[pos]

    # Function call: name(expr)
    if isinstance(t, str) and t in FUNCTIONS and pos + 1 < len(tokens) and tokens[pos+1] == '(':
        name = t; pos += 2  # skip name and (
        pos, arg = _parse_expr(tokens, pos)
        if pos >= len(tokens) or tokens[pos] != ')':
            raise SyntaxError("Expected ')'")
        pos += 1
        if name == 'ln': return pos, Ln(arg)
        if name == 'exp': return pos, Exp(arg)
        return pos, Func(name, arg)

    # Parenthesized expression
    if t == '(':
        pos += 1
        pos, e = _parse_expr(tokens, pos)
        if pos >= len(tokens) or tokens[pos] != ')':
            raise SyntaxError("Expected ')'")
        return pos + 1, e

    # Number
    if isinstance(t, (int, float)):
        return pos + 1, Num(t)

    # Variable
    if isinstance(t, str) and t.isalpha():
        return pos + 1, Var(t)

    raise SyntaxError(f"Unexpected token: {t}")

# ── Evaluate ─────────────────────────────────────────────────────

def evaluate(e: Expr, env: dict = None) -> float:
    """Numerically evaluate an expression with variable bindings."""
    import math
    env = env or {}
    if isinstance(e, Num): return e.v
    if isinstance(e, Var):
        if e.name in env: return env[e.name]
        raise ValueError(f"Unbound variable: {e.name}")
    if isinstance(e, Add): return evaluate(e.a, env) + evaluate(e.b, env)
    if isinstance(e, Mul): return evaluate(e.a, env) * evaluate(e.b, env)
    if isinstance(e, Pow): return evaluate(e.base, env) ** evaluate(e.exp, env)
    if isinstance(e, Ln): return math.log(evaluate(e.arg, env))
    if isinstance(e, Exp): return math.exp(evaluate(e.arg, env))
    if isinstance(e, Func):
        v = evaluate(e.arg, env)
        return {'sin': math.sin, 'cos': math.cos, 'tan': math.tan, 'sqrt': math.sqrt}[e.name](v)
    raise ValueError(f"Cannot evaluate: {type(e)}")

# ── REPL ─────────────────────────────────────────────────────────

def main():
    print("Symbolic Math Engine")
    print("Commands: <expr>          -- parse and simplify")
    print("          d <expr>        -- differentiate (d/dx)")
    print("          eval <expr> x=N -- evaluate with x=N")
    print("          quit")
    print()

    x = Var('x')  # convenience

    while True:
        try:
            line = input("λ> ").strip()
        except (EOFError, KeyboardInterrupt):
            print(); break

        if not line or line == 'quit':
            break

        try:
            if line.startswith('eval '):
                # eval x^2 + sin(x) x=3.14
                parts = line[5:]
                # find the last x=... assignment
                assign_idx = parts.rfind(' x=')
                if assign_idx < 0:
                    assign_idx = parts.rfind('x=')
                    if assign_idx < 0:
                        print("Usage: eval <expr> x=<value>")
                        continue
                    expr_str = parts[:assign_idx].strip()
                    assign_str = parts[assign_idx:]
                else:
                    expr_str = parts[:assign_idx].strip()
                    assign_str = parts[assign_idx+1:]

                # Parse assignments
                env = {}
                for asgn in assign_str.split():
                    if '=' in asgn:
                        k, v = asgn.split('=', 1)
                        env[k] = float(v)

                expr = simplify(parse(expr_str))
                result = evaluate(expr, env)
                print(f"  {expr}  at {env}")
                print(f"  = {result}")

            elif line.startswith('d ') or line.startswith('d'):
                expr_str = line[1:].strip() if line.startswith('d ') else line[1:]
                if not expr_str:
                    print("Usage: d <expr>")
                    continue
                expr = parse(expr_str)
                deriv = simplify(diff(expr, 'x'))
                print(f"  d/dx({simplify(expr)})")
                print(f"  = {deriv}")

            else:
                expr = simplify(parse(line))
                print(f"  = {expr}")

        except Exception as ex:
            print(f"  Error: {ex}")

    print("Goodbye.")


if __name__ == '__main__':
    main()
