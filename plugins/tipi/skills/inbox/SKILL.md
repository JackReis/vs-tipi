---
name: inbox
description: Surface the fleet inbox — latest Discord #bots messages + Telegram pings + recent session handoffs — deduped and sorted newest-first. Read-only.
---

# /inbox

Pull the fleet's recent activity into one view. No actions, just "what's been happening while I wasn't at the keyboard?"

## Sources (newest first)

1. `~/Documents/=notes/inbox/bots-transcript.md` — mirrored #bots activity (filesystem freshness signal)
2. `~/Documents/=notes/claude/mcp-coordination/state/session-handoffs/` — recent handoff files (last 3)
3. `~/Documents/=notes/inbox/agent-coordination.md` — cross-agent thread summaries
4. Today's dizzy-inbox in the current session's prompt (if present)

## Dedup + present

- Collapse repeated identical messages (looking at you, Zoe-rate-limit-loop).
- Show most recent 20 entries with timestamp + sender + first-line summary.
- Highlight anything addressed to @ this session's runtime/slug.

## Don't

- Don't fetch live Discord — the filesystem mirror is the SSOT for inbox purposes. If the mirror is stale (> 1hr), flag it.
- Don't mark anything as read — this is a view, not a state-mutator.

## Escalate

If the inbox shows a rate-limit loop in progress (e.g. 10+ identical messages in < 2 min from one bot), surface a big warning and suggest kicking the bot or pausing its launchd job. Do not attempt the kick yourself.
