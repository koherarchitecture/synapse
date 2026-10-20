#!/usr/bin/env bash
# Run before every release, from anywhere. It refuses when the method page is missing,
# when a check fails, or when anything that looks like a key is in the tree.
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -s METHOD.md ]; then
  echo "refused: METHOD.md is missing or empty"
  exit 1
fi

python3 scaffold/test_layers.py

if grep -rInE "(hf_[A-Za-z0-9]{10}|sk-[A-Za-z0-9-]{20}|password[[:space:]]*[:=])" --exclude-dir=.git --exclude=check.sh .; then
  echo "refused: something above looks like a key or a password"
  exit 1
fi

echo "release checks pass"
