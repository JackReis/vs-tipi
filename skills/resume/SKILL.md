---
name: resume
description: Pick up where the last session left off — loads latest handoff, opens its files_changed in VS Code, seeds a Claude Code session with the right cowork-paths profile. The "where was I?" compounding move.
---

# /resume

Ends the "where was I?" problem every time Jack sits down. Reads the latest handoff file and re-hydrates the environment around it.

## Sequence

1. Locate latest file in `~/Documents/=notes/claude/mcp-coordination/state/session-handoffs/` (by mtime).
2. Parse v2 frontmatter — pull `files_changed`, `next_actions`, `branch`, `worktree`, `verification_commands`.
3. Open each file in `files_changed` in VS Code (use `code` CLI — absolute paths required).
4. Pick a cowork-paths profile based on tags/topic (read `~/Documents/=notes/claude/config/cowork-paths.json`):
   - infrastructure / tipi / fleet → `infrastructure` profile
   - health / PT / supplements → `health` profile
   - job-search / EDD / resume → `job-search` profile
   - otherwise → `default`
5. Checkout the branch if `branch:` is specified and not currently checked out. If `worktree:` is specified, cd into it.
6. Run the first of `verification_commands` to confirm the world hasn't broken since last session.
7. Summarize in 5 lines: what was last session, what's the first step, any watch-items.

## Don't

- Don't execute `next_actions` automatically — that's the user's call.
- Don't re-run ALL verification commands — first one is enough for a freshness check.
- Don't resume a stale handoff (> 7 days) without flagging. The state may have drifted.

## Compound effect

When this skill works smoothly, "sitting down at the computer" becomes a ~5-second operation instead of a 5-minute context-rebuild. That's the real value of the tipi / vs-tipi stack — not the agents, but this ritual.
