import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "generate-agents-app-projection.py"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "generate_agents_app_projection", SCRIPT_PATH
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class GenerateAgentsAppProjectionTest(unittest.TestCase):
    def test_generates_separate_agents_app_bundle_from_roster(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            roster_path = tmp_path / "agents-app-roster.json"
            roster_path.write_text(
                json.dumps(
                    {
                        "agent_files": [
                            "hermes.agent.md",
                            "olivier_mbp.agent.md",
                            "kimiclaw.agent.md",
                            "claude-new.agent.md",
                            "fleet.agent.md",
                        ]
                    }
                ),
                encoding="utf-8",
            )

            output_root = tmp_path / "agents-app"
            written = module.generate_agents_app_projection(
                vs_tipi_root=ROOT,
                roster_path=roster_path,
                output_root=output_root,
            )

            expected_files = [
                output_root / "README.md",
                output_root / ".mcp.json",
                output_root / ".vscode" / "settings.json",
                output_root / ".github" / "agents" / "hermes.agent.md",
                output_root / ".github" / "agents" / "olivier_mbp.agent.md",
                output_root / ".github" / "agents" / "kimiclaw.agent.md",
                output_root / ".github" / "agents" / "claude-new.agent.md",
                output_root / ".github" / "agents" / "fleet.agent.md",
            ]

            for path in expected_files:
                self.assertTrue(path.exists(), path)

            self.assertEqual(set(expected_files), set(written))

            mcp = json.loads((output_root / ".mcp.json").read_text(encoding="utf-8"))
            self.assertIn("agentic-coding-school", mcp["mcpServers"])
            self.assertTrue(
                str(mcp["mcpServers"]["tipi-consciousness"]["command"]).endswith(
                    "scripts/run-mcp.sh"
                )
            )

            settings = json.loads(
                (output_root / ".vscode" / "settings.json").read_text(encoding="utf-8")
            )
            locations = settings["chat.agentFilesLocations"]
            self.assertIn(".github/agents", " ".join(locations))

            fleet_agent = (output_root / ".github" / "agents" / "fleet.agent.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("handoffs:", fleet_agent)
            self.assertIn("claude-new", fleet_agent)


if __name__ == "__main__":
    unittest.main()
