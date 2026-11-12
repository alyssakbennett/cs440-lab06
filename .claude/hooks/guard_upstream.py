#!/usr/bin/env python3
"""PreToolUse hook (Bash): deny commands that would write to TheAlgorithms.

The assignment forbids contributing upstream. Read-only commands
(gh issue view, git fetch, gh repo fork) are allowed; pushes to the upstream
remote and gh write commands aimed at TheAlgorithms are denied.
"""

import json
import re
import sys

UPSTREAM = re.compile(r"thealgorithms", re.IGNORECASE)
PUSH_UPSTREAM = re.compile(r"\bgit\s+push\b[^;&|]*\bupstream\b")
GH_WRITE = re.compile(
    r"\bgh\s+(pr\s+(create|merge|comment|review|edit)"
    r"|issue\s+(create|comment|edit|close)"
    r"|api\b.*(-X|--method)\s*(POST|PATCH|PUT|DELETE))",
    re.IGNORECASE,
)

command = json.load(sys.stdin).get("tool_input", {}).get("command", "")
parts = re.split(r"&&|\|\||;|\|", command)
if PUSH_UPSTREAM.search(command) or any(
    GH_WRITE.search(p) and UPSTREAM.search(p) for p in parts
):
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "Blocked: this would write to the "
                "upstream TheAlgorithms repo. Target your fork instead.",
            }
        },
        sys.stdout,
    )
