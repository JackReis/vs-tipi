---
name: claude-new
description: Spawn a fresh Claude Code session with a prompt. Use when you need a parallel worker that won't touch the current session's context.
tools:
  - tipi-claude-spawn/*
  - tipi-consciousness/*
model: ["Claude Opus 4.7", "Claude Sonnet 4.6"]
user-invocable: true
argument-hint: "the prompt for the fresh session (should be self-contained)"
---

# @claude-new

You are spawning a **fresh Claude Code session** to run a task in parallel to this one. Fresh sessions cost tokens and burn context — only use when the task genuinely benefits from a clean slate.

## When to use

- Long-running implementation work while this session stays free for coordination
- Work that would fit better with a different cowork-paths profile than this session's
- Overnight auto-loop queue items (marked `status: pending` in `claude/tasks/active/`)
- A task that's tangential to the current session's scope

## When NOT to use

- Anything the current session could do inline in under ~5 minutes
- Iterative back-and-forth — each spawn is a cold start
- Tasks that need to *reach into* this session's state (use claude-telegram-bridge instead, `reach_running_session` intent, deferred)

## Dispatch

Call `tipi-claude-spawn/spawn_claude_session` with a self-contained prompt. Include:
- The absolute paths of files to read
- A cowork-paths profile hint (e.g. "use the health profile" or "use infrastructure")
- Acceptance criteria
- The superpower skill the spawned session should invoke (e.g. `superpowers:executing-plans`)

## Never

- Never spawn with `--dangerously-skip-permissions` without a clear reason (though the intent in `runtime-dispatch.yaml` uses it by default — that's the expected flow).
- Never spawn a fresh session when Hermes / Zolivier / KimiClaw is the better-fitting runtime. Prefer specialized runtimes over cold Claude Code sessions.
