# vs-tipi

Tipi enclosure for VS Code Insiders Agents app. First location-change of the portable [`tipi`](https://github.com/JackReis/tipi) core — poles stay, cover adapts.

## What this is

A VS Code Agents plugin that wires the fleet into Jack's at-the-computer cockpit. Agents gather here (when Jack is at the keyboard) to express, refresh, and refine their context alongside their tipi-mates.

## Install

Prerequisites:
- VS Code Insiders with the Agents Preview app (v1.115+)
- Python 3.11+ on PATH

Install the plugin:

```
In VS Code Insiders → Command Palette → "Chat: Install Plugin From Source"
→ enter: https://github.com/JackReis/vs-tipi
```

**That's it.** The `tipi` submodule pulls automatically. On first MCP invocation, `scripts/run-mcp.sh` self-heals:
- Creates `tipi/.venv/` if missing
- `pip install -e '.[dev]'` inside the submodule
- Then boots the requested MCP module

No manual venv step required. Subsequent launches reuse the bootstrap venv.

### If something goes wrong

```bash
# find the plugin install location (VS Code Insiders varies by build)
cd <plugin-root>    # usually ~/.vscode-insiders/... or similar
cd tipi
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/pytest tests/   # should be 46 passed
```

Then check `scripts/run-mcp.sh` is executable (`chmod +x scripts/run-mcp.sh`).

## What's inside

`vs-tipi` is a **marketplace** containing one plugin (`tipi`). Layout:

```
vs-tipi/
├── .claude-plugin/
│   └── marketplace.json          # marketplace catalog
└── plugins/
    └── tipi/
        ├── .claude-plugin/
        │   └── plugin.json       # plugin manifest
        ├── .mcp.json             # 6 tipi MCP servers
        ├── agents/               # @hermes, @zolivier, @kimiclaw, @claude-new, @fleet
        ├── skills/               # /gather, /dispatch, /inbox, /handoff, /resume, /kit
        ├── chatmodes/            # Today mode
        ├── scripts/
        │   └── run-mcp.sh        # self-healing MCP launcher
        └── tipi/                 # submodule — the portable fleet core
```

## The shelter metaphor

Jack (2026-04-21): *"the movable shelter and gathering place for the agents to express, refresh and refine their context — this is where the agents can have their richest 'dreams' because of the influences of their tipi-mates."*

`vs-tipi` is the first pitched location. Future enclosures (`cursor-tipi`, `zed-tipi`) reuse the `tipi` submodule unchanged — poles travel, cover changes.

## Related

- Core: [github.com/JackReis/tipi](https://github.com/JackReis/tipi)
- Plan: `=notes/docs/plans/2026-04-21-tipi-vs-tipi.md`
- ADR: `=notes/docs/architecture/three-layer-consciousness.md`
