# vs-tipi — Repo Guidelines

## Prime directive

`vs-tipi` is the VS Code-flavored enclosure. It consumes `tipi` via git submodule and wires it into the VS Code Agents app. **Never duplicate logic that lives in `tipi`** — add a new tool/wrapper there and reference it from here.

## Fleet architecture (required reading)

The vault's `=notes/docs/architecture/fleet-architecture-guidelines.md` is the spine. `vs-tipi` must mirror the current Agentic OS doctrine, not the older per-bot transport model.

### Current doctrine

`vs-tipi` is an enclosure over the original consciousness substrate. It does not own the substrate, the ledger, the workflow engine, or the tool gateway.

- **Consciousness substrate**: Body is the vault/repos/runtime state; Mind is Cortex/OBn/Khoj-style retrieval and working context; Spirit is belief/proof/meaning.
- **Sinew**: the connection tissue between work records, tools, health, routes, context, and proof. Sinew includes Linear/Beads links, ContextForge/Bifrost MCP routes, Uptime Kuma service checks, Cortex context, n8n workflows, rbitr traces, Dramatis cues, RepoWeaver/GitNexus code intelligence, Telegram ingress, and VS Code enclosure state.
- **Compatibility rule**: Dramatis decides. Linear and Beads remember. Sinew connects. n8n executes. rbitr records and spawns. ContextForge and Bifrost expose tools. Uptime Kuma observes service health. Cortex carries working memory/context. RepoWeaver explains the fleet. GitNexus explains symbols when healthy. VS Tipi is an enclosure, not the substrate.

For vs-tipi work, the sections that matter most:

- **§1 Three-layer consciousness** — vs-tipi is an enclosure; never writes to Body/Mind/Spirit.
- **§2 Fleet Identity & Surfaces** — runtimes (Hermes, OLIVIER_MBP, KimiClaw, PT, Claude Code) map to agents in `plugins/tipi/agents/`. Keep rosters in sync.
- **§3 Shared contract** — `consciousness-interface.json` is LOCKED. Schema changes go through `~/Documents/Coordination/2026-04-21-infra-context-dashboard-coordination.md` first.
- **§13 Agentic OS Addendum + ADR-0014** — work flows Linear/Beads → Dramatis → Sinew/Conduit/n8n/rbitr → workers → proof. Do not recreate ClawHub inside VS Code.
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

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **vs-tipi** (734 symbols, 971 relationships, 7 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> If any GitNexus tool warns the index is stale, run `npx gitnexus analyze` in terminal first.

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `gitnexus_impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `gitnexus_detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `gitnexus_query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `gitnexus_context({name: "symbolName"})`.

## Never Do

- NEVER edit a function, class, or method without first running `gitnexus_impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `gitnexus_rename` which understands the call graph.
- NEVER commit changes without running `gitnexus_detect_changes()` to check affected scope.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/vs-tipi/context` | Codebase overview, check index freshness |
| `gitnexus://repo/vs-tipi/clusters` | All functional areas |
| `gitnexus://repo/vs-tipi/processes` | All execution flows |
| `gitnexus://repo/vs-tipi/process/{name}` | Step-by-step execution trace |

## Cross-Repo Groups

This repository is listed under GitNexus **group(s): fleet** (see `~/.gitnexus/groups/`). For cross-repo analysis, use MCP tools `impact`, `query`, and `context` with `repo` set to `@<groupName>` or `@<groupName>/<memberPath>` (paths match keys in that group’s `group.yaml`). Use `group_list` / `group_sync` for membership and sync. From the terminal: `npx gitnexus group list`, `npx gitnexus group sync <name>`, `npx gitnexus group impact <name> --target <symbol> --repo <group-path>`.

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->
