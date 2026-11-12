---
name: contribute
description: Follow TheAlgorithms/Python CONTRIBUTING.md to fix an issue in the fork clone at ./Python and open a PR on the user's fork only. Use when fixing, checking, committing, or opening a PR for a TheAlgorithms/Python issue.
argument-hint: <upstream-issue-number>
---

# Contribute to TheAlgorithms/Python (fork only)

The fork clone is `./Python` (remote `origin` = the user's fork; `upstream` is
fetch-only). Tools are in `./.venv/bin`. Issue: `$ARGUMENTS`.

## Rules (from CONTRIBUTING.md and the PR template)

- Never push, open PRs, or comment on `TheAlgorithms/*`. PRs target the fork:
  `gh pr create -R <user>/Python --base master`.
- Change **one algorithm file**. Do not touch `README.md` or `DIRECTORY.md`.
  Keep the diff minimal and in the file's existing style.
- Type hints on all parameters and return values; descriptive names; a
  docstring with a source URL; raise exceptions (don't print) on bad input.
- Doctests for valid **and** erroneous input. Never invent doctest output: run it.
- Lines ≤ 88 chars; must pass `ruff check` and `ruff format`.
- Do not write `#N` or upstream issue links in commits or the PR: GitHub would
  cross-reference the upstream issue. Say "upstream issue N" instead.

## Steps

1. Read the issue: `gh issue view $ARGUMENTS -R TheAlgorithms/Python`.
   Read `Python/CONTRIBUTING.md` and `Python/AGENTS.md`.
2. Reproduce the bug with the issue's own example before changing code.
3. Make the fix and add doctests. The PostToolUse hook runs ruff + doctests
   after every edit; fix anything it reports.
4. Run the full checks from `Python/`:
   `../.venv/bin/pre-commit run --files <file>` (with `SKIP=uv-lock`, as
   upstream CI does) and `python3 -m doctest -v <file>`. Re-run the issue's
   reproduction; it must now pass.
5. Ask the `contributing-reviewer` subagent to review. Fix every blocking item.
6. Commit with a clear message, push to `origin`, and open the PR on the fork
   using `Python/.github/pull_request_template.md` as the body (tick the boxes
   that honestly apply; at least one "Describe your change" box must be ticked).
