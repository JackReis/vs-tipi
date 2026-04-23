#!/usr/bin/env python3
"""Generate the separate VS Code Agents app projection from the fleet SSOT."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any


DEFAULT_VS_TIPI_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROSTER_PATH = Path(
    "/Users/jack.reis/Documents/Coordination/2026-04-23-vscode-agents-app-roster.json"
)
DEFAULT_OUTPUT_ROOT = DEFAULT_VS_TIPI_ROOT / "agents-app"

def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _read_roster(roster_path: Path) -> list[str]:
    roster = _load_json(roster_path)
    agent_files = roster.get("agent_files") or roster.get("agents")
    if not agent_files:
        raise ValueError(
            f"{roster_path} does not list any agent files under 'agent_files' or 'agents'"
        )
    return [Path(name).name for name in agent_files]


def _project_mcp_manifest(vs_tipi_root: Path) -> dict[str, Any]:
    plugin_mcp_path = vs_tipi_root / "plugins" / "tipi" / ".mcp.json"
    run_mcp_script = vs_tipi_root / "plugins" / "tipi" / "scripts" / "run-mcp.sh"

    manifest = _load_json(plugin_mcp_path)
    servers = manifest.get("mcpServers")
    if not isinstance(servers, dict):
        raise ValueError(f"{plugin_mcp_path} is missing the mcpServers object")

    projected = {}
    for name, server in servers.items():
        if not isinstance(server, dict):
            raise ValueError(f"MCP server {name} is not a JSON object")
        rewritten = dict(server)
        command = rewritten.get("command")
        if isinstance(command, str) and "${CLAUDE_PLUGIN_ROOT}" in command:
            rewritten["command"] = str(run_mcp_script)
        projected[name] = rewritten

    return {"mcpServers": projected}


def _write_readme(output_root: Path, roster_path: Path, agent_files: list[str]) -> Path:
    readme = output_root / "README.md"
    agent_lines = "\n".join(f"- `{name}`" for name in agent_files)
    readme.write_text(
        f"""# Agents App Projection

This workspace is the separate VS Code Agents app projection for the fleet.

Source of truth:
- Fleet architecture: `/Users/jack.reis/Documents/=notes/docs/architecture/fleet-architecture-guidelines.md`
- Identity map: `/Users/jack.reis/Documents/Coordination/2026-04-22-identity-mapping.md`
- Projection roster: `{roster_path}`

Generated surfaces:
{agent_lines}

Notes:
- `vs-tipi` is the generator boundary.
- The built-in VS Code Codex agent stays app-native; it is not duplicated here as a custom agent file.
- Regenerate this bundle with `scripts/generate-agents-app-projection.py`.
""",
        encoding="utf-8",
    )
    return readme


def _write_settings(output_root: Path) -> Path:
    settings = output_root / ".vscode" / "settings.json"
    _write_json(
        settings,
        {
            "chat.agentFilesLocations": ["${workspaceFolder}/.github/agents"],
        },
    )
    return settings


def _copy_agent_files(vs_tipi_root: Path, output_root: Path, agent_files: list[str]) -> list[Path]:
    plugin_agent_dir = vs_tipi_root / "plugins" / "tipi" / "agents"
    dest_dir = output_root / ".github" / "agents"
    dest_dir.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for file_name in agent_files:
        source = plugin_agent_dir / file_name
        if not source.exists():
            raise FileNotFoundError(f"Missing source agent file: {source}")
        destination = dest_dir / file_name
        shutil.copy2(source, destination)
        written.append(destination)
    return written


def generate_agents_app_projection(
    *,
    vs_tipi_root: Path | str = DEFAULT_VS_TIPI_ROOT,
    roster_path: Path | str = DEFAULT_ROSTER_PATH,
    output_root: Path | str = DEFAULT_OUTPUT_ROOT,
) -> list[Path]:
    """Generate the projection bundle and return the written files."""

    vs_tipi_root = Path(vs_tipi_root)
    roster_path = Path(roster_path)
    output_root = Path(output_root)

    agent_files = _read_roster(roster_path)

    output_root.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    written.extend(_copy_agent_files(vs_tipi_root, output_root, agent_files))

    mcp_path = output_root / ".mcp.json"
    _write_json(mcp_path, _project_mcp_manifest(vs_tipi_root))
    written.append(mcp_path)

    settings_path = _write_settings(output_root)
    written.append(settings_path)

    readme_path = _write_readme(output_root, roster_path, agent_files)
    written.append(readme_path)

    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vs-tipi-root", default=str(DEFAULT_VS_TIPI_ROOT))
    parser.add_argument("--roster", default=str(DEFAULT_ROSTER_PATH))
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    args = parser.parse_args()

    written = generate_agents_app_projection(
        vs_tipi_root=Path(args.vs_tipi_root),
        roster_path=Path(args.roster),
        output_root=Path(args.output_root),
    )
    for path in written:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
