# Agents App Projection

This workspace is the separate VS Code Agents app projection for the fleet.

Architecture:
- VS Tipi is an enclosure, not the substrate.
- Consciousness substrate: Body (vault/repos/runtime state), Mind (Cortex/OBn/Khoj-style retrieval and working context), Spirit (belief/proof/meaning).
- Sinew: Linear/Beads work links, ContextForge/Bifrost MCP routes, Uptime Kuma service checks, Cortex context, n8n workflows, rbitr traces, Dramatis cues, RepoWeaver/GitNexus code intelligence, Telegram ingress, and VS Code enclosure state.
- Compatibility rule: Dramatis decides. Linear and Beads remember. Sinew connects. n8n executes. rbitr records and spawns. ContextForge and Bifrost expose tools. Uptime Kuma observes service health. Cortex carries working memory/context. RepoWeaver explains the fleet. GitNexus explains symbols when healthy.

Source of truth:
- Fleet architecture: `/Users/jack.reis/Documents/=notes/docs/architecture/fleet-architecture-guidelines.md`
- Identity map: `/Users/jack.reis/Documents/Coordination/2026-04-22-identity-mapping.md`
- Projection roster: `/Users/jack.reis/Documents/Coordination/2026-04-23-vscode-agents-app-roster.json`

Generated surfaces:
- `hermes.agent.md`
- `olivier_mbp.agent.md`
- `kimiclaw.agent.md`
- `pt.agent.md`
- `claude-new.agent.md`
- `fleet.agent.md`

Notes:
- `vs-tipi` is the generator boundary.
- The built-in VS Code Codex agent stays app-native; it is not duplicated here as a custom agent file.
- Telegram, Discord, and VS Code are surfaces; they do not own work records or fleet identity.
- Regenerate this bundle with `scripts/generate-agents-app-projection.py`.
