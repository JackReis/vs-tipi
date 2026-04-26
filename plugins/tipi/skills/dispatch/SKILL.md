---
name: dispatch
description: Dispatch a task to a specific fleet runtime. `/dispatch hermes <task>` routes to @hermes; likewise for olivier_mbp, kimiclaw, claude. Resolves the intent via tipi's runtime-dispatch.yaml.
---

# /dispatch

Thin wrapper — resolves agent slug → correct MCP tool → fires. This skill exists so Jack can type `/dispatch hermes finish the refactor` and not think about which tool name maps to which runtime.

## Sequence

1. Parse args into `<slug> <task-text>`.
2. Validate slug against known runtimes: `hermes`, `olivier_mbp`, `kimiclaw`, `claude`.
3. Refuse if no task text — don't dispatch bare agents.
4. Resolve to MCP tool:
   - `hermes` → `tipi-hermes/dispatch_to_hermes`
   - `olivier_mbp` → `tipi-openclaw/dispatch_to_olivier_mbp`
   - `kimiclaw` → `tipi-openclaw/dispatch_to_kimiclaw`
   - `claude` → `tipi-claude-spawn/spawn_claude_session`
5. Call the tool with `text=<task-text>`.
6. Report `{ok, returncode, stdout, stderr}` back.

## If `ok=false`

Surface stderr. Don't retry silently — that's how Zoe got kicked from Discord on 2026-04-21 (rate-limit loop). Surface the error, let Jack decide.

## Coordination

Write a one-line entry in `~/Documents/=notes/inbox/agent-coordination.md` after a successful dispatch, so sibling sessions see what's in flight.

## Prefer @fleet for routing decisions

If Jack types `/dispatch` without knowing which runtime fits, route to `@fleet` (the meta-agent) first. `/dispatch` is for when Jack already knows.
