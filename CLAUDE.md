# vs-tipi — Repo Guidelines

## Prime directive

`vs-tipi` is the VS Code-flavored enclosure. It consumes `tipi` via git submodule and wires it into the VS Code Agents app. **Never duplicate logic that lives in `tipi`** — add a new tool/wrapper there and reference it from here.

## Fleet architecture (required reading)

The vault's `=notes/docs/architecture/fleet-architecture-guidelines.md` is the spine. For vs-tipi work, the sections that matter most:

- **§1 Three-layer consciousness** — vs-tipi is an enclosure; never writes to Body/Mind/Spirit.
- **§2 Fleet Identity & Surfaces** — runtimes (Hermes, OLIVIER_MBP, KimiClaw, PT, Claude Code) map to agents in `plugins/tipi/agents/`. Keep rosters in sync.
- **§3 Shared contract** — `consciousness-interface.json` is LOCKED. Schema changes go through `~/Documents/Coordination/2026-04-21-infra-context-dashboard-coordination.md` first.
- **§6.5 Runtime instruction cascade** *(v1.6.0)* — each runtime reads its own native cascade file. This `CLAUDE.md` is Claude Code's cascade for this repo. Don't invent `<RUNTIME>-MEMORY.md` files; per-runtime archival earns its place by content, not naming.

When a fleet-visible change lands in the vault's fleet-arch guidelines, mirror the minimum here so cold-start Claude Code sessions in this repo pick it up.

## Layout rules

- Agent definitions go in `agents/*.agent.md`. Frontmatter fields: `name`, `description`, `tools`, `model`, `user-invocable` (boolean), optional `handoffs`.
- Slash commands go in `skills/<name>/SKILL.md`.
- MCP servers are declared in `.mcp.json` ONLY. Don't add per-agent MCP wiring.
- The Today chat mode is at `chatmodes/today.chatmode.md`.

## Submodule hygiene

- `tipi/` submodule pinned to a specific commit. Bump deliberately (`cd tipi && git pull && cd .. && git add tipi`).
- Never edit files inside `tipi/` from this repo. Open a separate session against the tipi repo.

## Testing

- No Python tests in this repo — `tipi` owns that.
- Validate plugin structure with `scripts/validate_plugin.py` (parses plugin.json, each .agent.md, each SKILL.md; reports issues).
- Full smoke test requires VS Code Insiders + the Agents app installed. Record the smoke in a dated file under `docs/smoke-tests/` per plan Task 8.2.

## Vault plan that governs this repo

`=notes/docs/plans/2026-04-21-tipi-vs-tipi.md` (Phases 4-9 apply to this repo).
