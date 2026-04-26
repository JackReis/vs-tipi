# Agents App Projection

This workspace is the separate VS Code Agents app projection for the fleet.

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
- Regenerate this bundle with `scripts/generate-agents-app-projection.py`.
