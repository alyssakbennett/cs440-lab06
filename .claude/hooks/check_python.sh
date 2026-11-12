#!/usr/bin/env bash
# PostToolUse hook (Edit|Write): after a .py file in the fork clone changes,
# run the checks CONTRIBUTING.md requires on that file. On failure, exit 2 so
# the output is fed back to Claude to fix.
file=$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))')
repo="$CLAUDE_PROJECT_DIR/Python"
case "$file" in "$repo"/*.py) ;; *) exit 0 ;; esac

bin="$CLAUDE_PROJECT_DIR/.venv/bin"
cd "$repo" || exit 0
rel="${file#"$repo"/}"
out=$(
  { "$bin/ruff" check "$rel" && "$bin/ruff" format --check "$rel" \
    && python3 -m doctest "$rel" && echo "doctests passed"; } 2>&1
)
if [ $? -ne 0 ]; then
  echo "CONTRIBUTING.md checks failed for $rel:" >&2
  echo "$out" >&2
  exit 2
fi
