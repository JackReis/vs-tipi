---
name: gather
description: Open the Today pane — synthesized briefing of what's in front of Jack right now. Reads SESSION-CONTEXT.md + priority dashboard + work-in-progress + today's daily note + latest handoff, then auto-surfaces 3 relevant prompt kits.
---

# /gather

Produce the "where was I?" briefing for at-the-computer Jack. This is tipi's core gathering ritual — pull the fleet's context into one view before any work starts.

## Sequence

Read these files in parallel — they're SSOT for current state:

1. `~/Documents/=notes/SESSION-CONTEXT.md` — priorities, health, conventions, recent work
2. `~/Documents/=notes/atlas/dashboards/priority-dashboard.md` — tiered priority list
3. `~/Documents/=notes/atlas/context/work-in-progress.md` — Now / Next / Blocked / Recently Completed
4. `~/Documents/=notes/calendar/day/YYYY-MM/YYYYMMDD.md` (today) — schedule, energy, Top 3 Priorities
5. Latest file in `~/Documents/=notes/claude/mcp-coordination/state/session-handoffs/`

Then via tipi MCPs:

6. `tipi-consciousness/list_beliefs(limit=5)` — top beliefs by subjective weight
7. `tipi-consciousness/health_snapshot()` — is the fleet well?
8. `tipi-epigenetics/search_prompt_kits(query=<today's-Top-3-topic>)` — 3 relevant kits

## Synthesis

Under 400 words:

```markdown
## Today Briefing

### What's in front of you
- [From daily note Top 3 Priorities]

### What's blocking
- [From work-in-progress Blocked section + recent handoffs]

### Fleet health
- [From health_snapshot — green/yellow/red per field]

### Kits in play
- [3 auto-surfaced prompt kits — names + 1-line why-now]

### Last session
- [From latest handoff: what shipped, what's next, any watch-items]
```

## Freshness guard

If any source file has `updated:` > 14 days stale, flag it in the briefing. If the coordination file in `~/Documents/Coordination/` has newer mtime than today's handoffs, read that too — another session may be active.

## Don't

- Don't recommend actions. Gather, don't dispatch. For action, Jack uses `/dispatch` or `@fleet`.
- Don't write anything. Read-only skill.
