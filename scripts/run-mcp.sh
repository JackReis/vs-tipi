#!/usr/bin/env bash
# run-mcp.sh — self-healing MCP server launcher for tipi submodule.
#
# On first run (after plugin clone), creates ${PLUGIN_ROOT}/tipi/.venv and
# `pip install -e '.[dev]'`. Subsequent runs just exec the Python module.
#
# Usage (from .mcp.json):
#   command: "${CLAUDE_PLUGIN_ROOT}/scripts/run-mcp.sh"
#   args:    ["tipi.mcp.consciousness.server"]
#
# Exit codes:
#   - exits with whatever the MCP server exits with
#   - 20: tipi submodule missing (submodule init failed)
#   - 21: venv creation failed
#   - 22: pip install failed

set -euo pipefail

MODULE="${1:?need python module as first arg, e.g. tipi.mcp.consciousness.server}"

# PLUGIN_ROOT resolves via ${CLAUDE_PLUGIN_ROOT} when VS Code Agents sets it;
# falls back to the script's directory when run standalone.
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
TIPI_DIR="${PLUGIN_ROOT}/tipi"
VENV_DIR="${TIPI_DIR}/.venv"

if [ ! -d "${TIPI_DIR}" ]; then
  echo "run-mcp.sh: tipi submodule not found at ${TIPI_DIR}" >&2
  echo "  try: cd ${PLUGIN_ROOT} && git submodule update --init" >&2
  exit 20
fi

if [ ! -x "${VENV_DIR}/bin/python" ]; then
  echo "run-mcp.sh: venv not found; bootstrapping at ${VENV_DIR}..." >&2
  python3 -m venv "${VENV_DIR}" >&2 || exit 21
  "${VENV_DIR}/bin/pip" install --quiet --upgrade pip >&2 || exit 22
  "${VENV_DIR}/bin/pip" install --quiet -e "${TIPI_DIR}[dev]" >&2 || exit 22
  echo "run-mcp.sh: venv bootstrap complete" >&2
fi

exec "${VENV_DIR}/bin/python" -m "${MODULE}"
