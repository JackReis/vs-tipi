# vs-tipi

Tipi enclosure for VS Code Insiders Agents app. First location-change of the portable [`tipi`](https://github.com/JackReis/tipi) core — poles stay, cover adapts.

## What this is

A VS Code Agents plugin that wires the fleet into Jack's at-the-computer cockpit. Agents gather here (when Jack is at the keyboard) to express, refresh, and refine their context alongside their tipi-mates.

## Install

Prerequisites:
- VS Code Insiders with the Agents Preview app (v1.115+)
- `~/Documents/tipi/` cloned and its venv set up (`python3 -m venv .venv && .venv/bin/pip install -e '.[dev]'`)

Install the plugin:

```
In VS Code Insiders → Command Palette → "Chat: Install Plugin From Source"
→ enter: https://github.com/JackReis/vs-tipi
```

The plugin pulls the `tipi` submodule automatically. The MCP servers assume `tipi/.venv/` exists inside the submodule — run the install script if needed:

```bash
cd <plugin-root>/tipi
python3 -m venv .venv && .venv/bin/pip install -e '.[dev]'
.venv/bin/pytest tests/  # should be 46 passed
```

## What's inside

| Component | Purpose |
|---|---|
| `plugin.json` | VS Code Agents plugin manifest |
| `.mcp.json` | Wires the 6 tipi MCP servers (consciousness, dizzy, hermes, openclaw, claude_spawn, epigenetics) |
| `agents/` | Custom agents — `@hermes`, `@zolivier`, `@kimiclaw`, `@claude-new`, `@fleet` |
| `skills/` | Slash commands — `/gather`, `/dispatch`, `/inbox`, `/handoff`, `/resume`, `/kit` |
| `chatmodes/` | Today mode (auto-surfaces briefing + 3 relevant kits on session start) |
| `tipi/` | Submodule — the portable fleet core |

## The shelter metaphor

Jack (2026-04-21): *"the movable shelter and gathering place for the agents to express, refresh and refine their context — this is where the agents can have their richest 'dreams' because of the influences of their tipi-mates."*

`vs-tipi` is the first pitched location. Future enclosures (`cursor-tipi`, `zed-tipi`) reuse the `tipi` submodule unchanged — poles travel, cover changes.

## Related

- Core: [github.com/JackReis/tipi](https://github.com/JackReis/tipi)
- Plan: `=notes/docs/plans/2026-04-21-tipi-vs-tipi.md`
- ADR: `=notes/docs/architecture/three-layer-consciousness.md`
