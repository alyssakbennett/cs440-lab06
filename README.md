# CS440 Lab 6: Contribution agent for TheAlgorithms/Python

A Claude Code agent that fixes a TheAlgorithms/Python issue by following
the repo's `CONTRIBUTING.md`, then opens the PR on **my fork only**, never upstream.

**Result:** [alyssakbennett/Python PR 1](https://github.com/alyssakbennett/Python/pull/1)
fixes upstream issue 15635 (`hashes/adler32.py` checksummed Unicode code points
instead of UTF-8 bytes).

## Code features

| File | Type | What it does |
|---|---|---|
| [`.claude/skills/contribute/SKILL.md`](.claude/skills/contribute/SKILL.md) | Skill (`/contribute <issue>`) | The workflow: read the issue and CONTRIBUTING.md, reproduce the bug, fix it with doctests, run pre-commit, get a review, then commit, push to the fork, and open the PR with the upstream PR template. |
| [`.claude/agents/contributing-reviewer.md`](.claude/agents/contributing-reviewer.md) | Subagent | A read-only reviewer that checks the diff for correctness, doctests and CONTRIBUTING.md rules. It answers `READY` or `CHANGES NEEDED`. |
| [`.claude/hooks/guard_upstream.py`](.claude/hooks/guard_upstream.py) | PreToolUse hook (Bash) | Denies `git push upstream` and any `gh` write command aimed at TheAlgorithms. |
| [`.claude/hooks/check_python.sh`](.claude/hooks/check_python.sh) | PostToolUse hook (Edit/Write) | After every `.py` edit in the fork, runs `ruff check`, `ruff format --check` and the doctests, and sends any failures back to the agent. |
| [`.claude/settings.json`](.claude/settings.json) | Config | Registers both hooks. |

## Design decisions

- **Hooks enforce the rules, not just the prompt.** The skill *tells* the agent
  not to go upstream, but `guard_upstream.py` *blocks* it at runtime. The
  upstream remote's push URL is also set to `DISABLED` in the clone.
- **The quality checks run automatically.** `check_python.sh` runs on every edit,
  so style or doctest failures get caught right away, not at PR time.
- **The reviewer is separate and read-only.** A fresh subagent that can't edit files
  reviews the change against CONTRIBUTING.md, so the fix doesn't approve itself.
- **No `#N` references.** On a fork, a bare `#N` can link to the upstream issue
  and leave a cross-reference there. The skill and the reviewer both check for this.

## Setup

```sh
gh repo fork TheAlgorithms/Python --clone        # creates ./Python
git -C Python remote set-url --push upstream DISABLED
python3 -m venv .venv && .venv/bin/pip install ruff pre-commit
claude                                           # then: /contribute <issue-number>
```
