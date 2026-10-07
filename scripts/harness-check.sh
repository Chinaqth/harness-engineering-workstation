#!/usr/bin/env bash
set -euo pipefail
root="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
python_bin="${HARNESS_PYTHON:-python3}"
export PYTHONDONTWRITEBYTECODE=1
"$python_bin" "$root/scripts/validate_repository.py" "$root"
"$python_bin" "$root/scripts/validate_protocol_versions.py" "$root"
"$python_bin" "$root/scripts/validate_routing.py" "$root"
"$python_bin" "$root/scripts/validate_change.py" "$root"
"$python_bin" "$root/scripts/knowledge-garden.py" "$root"
"$python_bin" -m unittest discover -s "$root/tests"
printf 'Harness check passed.\n'
