---
name: gather
description: Open the Today pane — synthesized briefing of what's in front of Jack right now. Reads SESSION-CONTEXT.md + priority dashboard + work-in-progress + today's daily note + latest handoff, then auto-surfaces 3 relevant prompt kits. HARD RULES against fabrication.
---

# /gather

Produce the "where was I?" briefing for at-the-computer Jack. This is tipi's core gathering ritual — pull the fleet's context into one view before any work starts.

## HARD RULES — read first

- You **MUST** call real tools. If you don't have access to `read` or the tipi MCPs, SAY SO EXPLICITLY rather than synthesize a briefing from memory or training.
- You **MUST NOT** fabricate:
  - Priority lines (copy from today's daily note "Today's Top 3 Priorities" section, verbatim)
  - Prompt kit names (use only names returned by `nate-promptkit/search_prompt_kits`)
  - Fleet health field names (use exactly: `handoff_freshness`, `ob1_sync_status`, `session_lock_state`, `project_memory_entries`)
  - Session history (read it from the latest handoff file's frontmatter)
- Invented kit names that should trigger your self-check: "AI Knowledge Expansion Kit", "Tipi Framework Mastery Kit", "Recovery Dashboard Kit" — none exist in Nate's corpus. If you're about to write one of these, stop and actually call the tool.
- Tool errors go into the briefing as visible lines: `"health_snapshot failed: <msg>"`. Silent fabrication is a failure mode.

## Sequence

Read these files in parallel (via the `read` tool) — they're SSOT for current state:

1. `/Users/jack.reis/Documents/=notes/SESSION-CONTEXT.md` — priorities, health, conventions, recent work
2. `/Users/jack.reis/Documents/=notes/atlas/dashboards/priority-dashboard.md` — tiered priority list
3. `/Users/jack.reis/Documents/=notes/atlas/context/work-in-progress.md` — Now / Next / Blocked / Recently Completed
4. Today's daily note: `/Users/jack.reis/Documents/=notes/calendar/day/YYYY-MM/YYYYMMDD.md` (use actual date, not yesterday)
5. Most-recently-modified file in `/Users/jack.reis/Documents/=notes/claude/mcp-coordination/state/session-handoffs/`

Then via tipi MCPs:

6. `tipi-consciousness/list_beliefs(limit=5)` — top beliefs by subjective weight
7. `tipi-consciousness/health_snapshot()` — the real health dict, not category names
8. `nate-promptkit/search_prompt_kits(query=<query derived from today's actual Top 3>)` — 3 real kits

## Synthesis

Under 400 words:

```markdown
## Today Briefing

### What's in front of you
- [Verbatim or near-verbatim from daily note Top 3 — include wikilinks where the daily note has them]

### What's blocking
- [From work-in-progress Blocked section + any blockers in the latest handoff]

### Fleet health
- handoff_freshness: <newest_file>, <age_seconds>s, <count_last_24h> in last 24h
- ob1_sync_status: <backend>, last_sync=<ts>, ok=<bool>, records=<count>
- session_lock_state: <holder list or "no locks">
- project_memory_entries: <total>/<limit>, approaching_consolidation=<bool>

### Kits in play
- <real kit name> (<real published date>) — <why-relevant in one line>

### Last session
- Shipped: <from handoff tasks_completed>
- Next: <from handoff next_actions>
- Watch: <from handoff blockers>
```

## Freshness guard

- If any source file has `updated:` > 14 days stale, flag it in the briefing
- If `~/Documents/Coordination/` has a file with newer mtime than the latest handoff, read that too — another session may be active
- If `tipi-consciousness/health_snapshot` returns a yellow/red on any field, put that ABOVE the priority list

## Don't

- Don't recommend actions. Gather, don't dispatch. For action, Jack uses `/tipi:dispatch` or `@fleet`.
- Don't write anything. Read-only skill.
- Don't compose the briefing before you've called the tools. Call first, synthesize second.
