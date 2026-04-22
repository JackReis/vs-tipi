---
name: handoff
description: Write a v2 session handoff file capturing current session state — tasks completed, files changed, commits, next actions, blockers. Follows the fleet's Session END four-target discipline.
---

# /handoff

End-of-session ritual. Writes the durable baton that cross-session coordination depends on.

## Sequence

1. Determine session id (from conversation context or ask).
2. Collect state:
   - `tasks_completed` — what shipped this session
   - `files_changed` — paths written/edited (include absolute paths for vault files)
   - `commits` — `git log` on relevant branches
   - `next_actions` — pointer to the next session
   - `blockers` — known impediments
   - `real_bugs_caught` — mid-dev discoveries worth preserving
   - `verification_commands` — what re-verifies the claim
3. Write to `~/Documents/=notes/claude/mcp-coordination/state/session-handoffs/YYYY-MM-DD-<slug>-session-end-<session-id-prefix>.md` using v2 YAML frontmatter.
4. If prior handoff from this session exists (e.g. an earlier batch-1 handoff), set `supersedes:` to its path.
5. **Four mandatory wrap-up targets** (per conventions §agreements rule 2 + session-end memory):
   - Daily note — append to Session Achievements (NEVER overwrite)
   - Session handoff file (this skill writes it)
   - `INFRASTRUCTURE-TASKS.md` — add/update active-initiative entry OR explicit N/A
   - Session log file at `logs/sessions/YYYY-MM/session-active-<id>-YYYYMMDD.md` if the harness creates one
6. Commit + push with a narrow-path `git add`. Never `git add -A`.

## Don't

- Don't write a handoff from mid-session state. Handoffs capture COMPLETE work.
- Don't overwrite a sibling session's handoff.

## After writing

Optionally `/dispatch` a self-note via Telegram for the next morning-brief to pick up, or a `#bots` note if other runtimes need to know the baton is placed.
