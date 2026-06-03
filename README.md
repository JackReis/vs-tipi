# vs-tipi

Tipi enclosure for VS Code Insiders Agents app. It is the VS Code surface for the Agentic OS consciousness substrate and the sinew that connects the fleet.

## What this is

A VS Code Agents plugin that wires the fleet into Jack's at-the-computer cockpit. Agents gather here to read the substrate, route through the sinew layer, and return proof through the real work ledger.

The key principle: **VS Tipi is an enclosure, not the substrate.** It presents the fleet inside VS Code, but the durable architecture lives across the vault, Linear, Beads, ContextForge, Bifrost, Uptime Kuma, Cortex, n8n, rbitr, Dramatis, RepoWeaver, GitNexus, and the runtime workers.

## Install

Prerequisites:
- VS Code Insiders with the Agents Preview app (v1.115+)
- Python 3.11+ on PATH
- Node.js + npx (for the remote MCPs, including `nate-promptkit` and `agentic-coding-school`)

### Env var for `/tipi:kit` (optional)

The `/tipi:kit` slash command + Today-mode kit auto-surface use Nate's PromptKit, which requires a subscriber URL (private credential, not in this repo). If you have a subscription:

```bash
# One-time — add to ~/.zshenv or equivalent, then reload shell:
export NATE_PROMPTKIT_URL="https://www.contentmasterpro.limited/api/mcp/subscriber/<YOUR-TOKEN>"

# For GUI apps (VS Code Insiders launched from Finder), also:
launchctl setenv NATE_PROMPTKIT_URL "$NATE_PROMPTKIT_URL"
```

Reload VS Code Insiders after setting. Without this, `/tipi:kit` will fail gracefully with a message telling you to set the env var (never hallucinate a kit).

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
├── agents-app/                   # generated separate VS Code Agents app projection
├── scripts/
│   └── generate-agents-app-projection.py
└── plugins/
    └── tipi/
        ├── .claude-plugin/
        │   └── plugin.json       # plugin manifest
        ├── .mcp.json             # 7 tipi MCP servers
        ├── agents/               # @hermes, @olivier_mbp, @kimiclaw, @pt, @claude-new, @fleet
        ├── skills/               # /gather, /dispatch, /inbox, /handoff, /resume, /kit
        ├── chatmodes/            # Today mode
        ├── scripts/
        │   └── run-mcp.sh        # self-healing MCP launcher
        └── tipi/                 # submodule — the portable fleet core
```

## The architecture

Jack (2026-04-21): *"the movable shelter and gathering place for the agents to express, refresh and refine their context — this is where the agents can have their richest 'dreams' because of the influences of their tipi-mates."*

That shelter now has a precise systems role:

- **Consciousness substrate** is the ground: Body (vault/repos/runtime state), Mind (Cortex/OBn/Khoj-style retrieval and working context), and Spirit (belief/proof/meaning).
- **Sinew** is the connection tissue: Linear/Beads work links, ContextForge/Bifrost MCP routes, Uptime Kuma service checks, Cortex context, n8n workflows, rbitr traces, Dramatis cues, RepoWeaver/GitNexus code intelligence, Telegram ingress, and VS Code enclosure state.
- **Actors** are runtimes and humans inside a Dramatis scene. They do not own transport identities or the work ledger.

`vs-tipi` is the first pitched location. Future enclosures (`cursor-tipi`, `zed-tipi`) reuse the `tipi` submodule unchanged — poles travel, cover changes.

## Fleet architecture — the spine

vs-tipi consumes the posture defined in the vault's **`=notes/docs/architecture/fleet-architecture-guidelines.md`** and **ADR-0014**. Cold-starting in this repo? Read §0 and the Agentic OS addendum first.

Compatibility rule:

> Dramatis decides. Linear and Beads remember. Sinew connects. n8n executes. rbitr records and spawns. ContextForge and Bifrost expose tools. Uptime Kuma observes service health. Cortex carries working memory/context. RepoWeaver explains the fleet. GitNexus explains symbols when healthy. VS Tipi is an enclosure, not the substrate.

The older per-agent transport framing is deprecated. Telegram should be one fleet ingress, Discord is an observation/broadcast surface, and VS Code agents are actor views over the same substrate.

- **Three-layer consciousness** — Body (vault) → Mind (OBn/Khoj) → Spirit (belief-ledger, future). Epigenetics (PromptKit) is adjacent input, not a fourth layer.
- **Sinew / connection** — routes and evidence across Linear, Beads, ContextForge, Bifrost, Uptime Kuma, Cortex, n8n, rbitr, Dramatis, RepoWeaver, GitNexus, Telegram, and VS Code.
- **Fleet identity** — Hermes, OLIVIER_MBP, KimiClaw, PT, Claude Code, Codex, and other runtimes are actors. Their old Wings/Zoe/Mara/Kopi/Neo names are surfaces, not ownership boundaries.
- **Runtime instruction cascade** (§6.5) — Claude reads `CLAUDE.md`, Codex reads `AGENTS.md`, Gemini-CLI/PT reads `GEMINI.md`. Each runtime owns its own cascade file only.
- **Enclosure invariant** (§1) — vs-tipi consumes the three layers via MCP, never writes back to the substrate.

The `tipi` submodule is the portable fleet core; vs-tipi is its first pitched location.

## Separate Agents app projection

The VS Code Agents app is a separate enclosure from the plugin bundle. Its workspace lives in `agents-app/` and is generated from the coordination roster in `~/Documents/Coordination/2026-04-23-vscode-agents-app-roster.json` by `scripts/generate-agents-app-projection.py`.

That projection keeps the same fleet agent set and MCP surface aligned with the SSOT, while still letting the separate app have its own workspace settings and discovery path.

## Related

- Core: [github.com/JackReis/tipi](https://github.com/JackReis/tipi)
- Plan: `=notes/docs/plans/2026-04-21-tipi-vs-tipi.md`
- ADR: `=notes/docs/architecture/three-layer-consciousness.md`
