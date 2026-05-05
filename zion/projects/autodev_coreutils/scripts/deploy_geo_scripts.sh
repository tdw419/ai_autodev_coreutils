#!/bin/bash
# Deploy GeOS preflight scripts from autodev_coreutils to ~/.hermes/scripts/
# Source of truth: autodev_coreutils/scripts/geo/
# Runtime location: ~/.hermes/scripts/ (Hermes scheduler enforces this)

set -euo pipefail
SRC="$(cd "$(dirname "$0")/geo" && pwd)"
DST="$HOME/.hermes/scripts"

for f in "$SRC"/*.py; do
    name=$(basename "$f")
    cp "$f" "$DST/$name"
    echo "  deployed $name"
done

echo "Done. $(ls "$SRC"/*.py | wc -l) scripts deployed to $DST"
