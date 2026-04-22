"""Validate the vs-tipi plugin structure without needing VS Code installed.

Checks:
- plugin.json has required top-level fields
- Each *.agent.md has valid YAML frontmatter with required fields
- Each skills/*/SKILL.md has valid YAML frontmatter
- .mcp.json is valid JSON and references exist
- Tools listed in agents resolve to mcpServers in .mcp.json (prefix match)
- Each agent's tools list is a subset of tool-manifest.yaml's `allowed` for that agent
  (agents with extra tools = CI failure; prevents silent privilege creep)

Exit code 0 on success, 1 on any error.

Usage: python3 scripts/validate_plugin.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _plugin_json_path() -> Path:
    """Plugin manifest moved from root to .claude-plugin/ in marketplace layout."""
    a = ROOT / ".claude-plugin" / "plugin.json"
    b = ROOT / "plugin.json"
    return a if a.exists() else b

REQUIRED_PLUGIN_FIELDS = {"name", "description", "version"}
REQUIRED_AGENT_FRONTMATTER = {"name", "description"}
REQUIRED_SKILL_FRONTMATTER = {"name"}


def _read_frontmatter(path: Path) -> dict:
    """Minimal YAML-frontmatter parser (no pyyaml dependency).

    Handles:
    - key: value
    - key: [a, b, c] (inline list — stored as str, not parsed)
    - nested blocks (multi-line list under key — stored as str block)
    """
    text = path.read_text()
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: no frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError(f"{path}: frontmatter not closed")
    block = text[4:end]
    data: dict[str, str | list] = {}
    current_key: str | None = None
    current_list: list | None = None
    for raw in block.splitlines():
        if not raw.strip():
            continue
        if raw.startswith("  - ") and current_key and current_list is not None:
            current_list.append(raw[4:].strip())
            continue
        if ": " in raw and not raw.startswith(" "):
            key, val = raw.split(": ", 1)
            current_key = key.strip()
            current_list = None
            if val.strip() == "":
                current_list = []
                data[current_key] = current_list
            else:
                data[current_key] = val.strip()
        elif raw.endswith(":") and not raw.startswith(" "):
            current_key = raw[:-1].strip()
            current_list = []
            data[current_key] = current_list
    return data


def check_plugin_json(errors: list[str]) -> dict | None:
    path = _plugin_json_path()
    if not path.exists():
        errors.append("plugin.json missing (checked .claude-plugin/ and root)")
        return None
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        errors.append(f"plugin.json invalid JSON: {exc}")
        return None
    missing = REQUIRED_PLUGIN_FIELDS - data.keys()
    if missing:
        errors.append(f"plugin.json missing fields: {sorted(missing)}")
    return data


def check_mcp_json(errors: list[str]) -> dict | None:
    path = ROOT / ".mcp.json"
    if not path.exists():
        errors.append(".mcp.json missing")
        return None
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        errors.append(f".mcp.json invalid JSON: {exc}")
        return None
    servers = data.get("mcpServers", {})
    if not servers:
        errors.append(".mcp.json has no mcpServers")
    return data


def _load_tool_manifest() -> dict | None:
    """Load tool-manifest.yaml (no pyyaml dependency — minimal parser)."""
    path = ROOT / "agents" / "tool-manifest.yaml"
    if not path.exists():
        return None
    # Minimal YAML parser: handles nested {agents: {name: {description, allowed: [list]}}}
    manifest: dict = {"agents": {}}
    current_agent: str | None = None
    current_list: list | None = None
    in_agents = False
    for raw in path.read_text().splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        if stripped == "agents:":
            in_agents = True
            continue
        if not in_agents:
            continue
        if indent == 2 and stripped.endswith(":"):
            current_agent = stripped[:-1]
            manifest["agents"][current_agent] = {"allowed": []}
            current_list = None
        elif indent == 4 and stripped == "allowed:":
            current_list = manifest["agents"][current_agent]["allowed"]
        elif indent == 6 and stripped.startswith("- "):
            if current_list is not None:
                current_list.append(stripped[2:].strip())
    return manifest


def check_agents(errors: list[str], mcp: dict) -> None:
    agents_dir = ROOT / "agents"
    if not agents_dir.exists():
        errors.append("agents/ directory missing")
        return
    servers = set((mcp or {}).get("mcpServers", {}).keys())
    manifest = _load_tool_manifest()
    files = sorted(agents_dir.glob("*.agent.md"))
    if not files:
        errors.append("agents/ has no *.agent.md files")
        return
    for path in files:
        try:
            fm = _read_frontmatter(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        missing = REQUIRED_AGENT_FRONTMATTER - fm.keys()
        if missing:
            errors.append(f"{path.name}: missing frontmatter {sorted(missing)}")
        tools = fm.get("tools", [])
        if not isinstance(tools, list):
            continue
        # MCP-server existence check
        for tool in tools:
            server = tool.split("/", 1)[0]
            if server.startswith("tipi-") and server not in servers:
                errors.append(
                    f"{path.name}: tool {tool!r} references unregistered server {server!r}"
                )
        # Tool-manifest permission check (privilege-creep guard)
        if manifest:
            agent_name = fm.get("name") or path.stem.removesuffix(".agent")
            policy = manifest.get("agents", {}).get(agent_name)
            if policy is None:
                errors.append(
                    f"{path.name}: agent {agent_name!r} has no entry in tool-manifest.yaml"
                )
            else:
                allowed = set(policy.get("allowed", []))
                for tool in tools:
                    if tool in allowed:
                        continue
                    # Check wildcard match: allowed entry "foo/*" covers "foo/bar"
                    wildcard_match = any(
                        a.endswith("/*") and tool.startswith(a[:-1])
                        for a in allowed
                    )
                    if not wildcard_match:
                        errors.append(
                            f"{path.name}: tool {tool!r} not in manifest `allowed` for agent {agent_name!r}"
                        )


def check_skills(errors: list[str]) -> None:
    skills_dir = ROOT / "skills"
    if not skills_dir.exists():
        return  # skills are optional; Phase 6 will add them
    for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"skills/{skill_dir.name}/: missing SKILL.md")
            continue
        try:
            fm = _read_frontmatter(skill_md)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        missing = REQUIRED_SKILL_FRONTMATTER - fm.keys()
        if missing:
            errors.append(f"skills/{skill_dir.name}/SKILL.md: missing frontmatter {sorted(missing)}")


def check_chatmodes(errors: list[str], mcp: dict) -> None:
    """Verify chat-mode tool lists reference only registered MCP servers.

    This exists because tipi-epigenetics/* leaked into today.chatmode.md after
    the epigenetics MCP was deleted — the validator only scanned agents/ and
    skills/, so the stale reference shipped and Today mode hallucinated.
    """
    chatmodes_dir = ROOT / "chatmodes"
    if not chatmodes_dir.exists():
        return
    servers = set((mcp or {}).get("mcpServers", {}).keys())
    for path in sorted(chatmodes_dir.glob("*.chatmode.md")):
        try:
            fm = _read_frontmatter(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        tools = fm.get("tools", [])
        if not isinstance(tools, list):
            continue
        for tool in tools:
            server = tool.split("/", 1)[0]
            if server.startswith("tipi-") and server not in servers:
                errors.append(
                    f"{path.name}: tool {tool!r} references unregistered server {server!r}"
                )


def main() -> int:
    errors: list[str] = []
    plugin = check_plugin_json(errors)
    mcp = check_mcp_json(errors)
    check_agents(errors, mcp or {})
    check_skills(errors)
    check_chatmodes(errors, mcp or {})
    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1
    n_agents = len(list((ROOT / "agents").glob("*.agent.md")))
    n_skills = sum(1 for p in (ROOT / "skills").iterdir() if p.is_dir()) if (ROOT / "skills").exists() else 0
    n_chatmodes = len(list((ROOT / "chatmodes").glob("*.chatmode.md"))) if (ROOT / "chatmodes").exists() else 0
    n_servers = len(mcp.get("mcpServers", {})) if mcp else 0
    manifest = _load_tool_manifest()
    manifest_note = f"+ tool-manifest ({len(manifest['agents'])} policies)" if manifest else "(no manifest)"
    print(f"OK — plugin={plugin['name']} version={plugin['version']}")
    print(f"     {n_agents} agents, {n_skills} skills, {n_chatmodes} chatmodes, {n_servers} MCP servers {manifest_note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
