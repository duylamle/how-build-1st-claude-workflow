"""Launcher shim — lets `python server.py` work without installing the package.

For production / pip installs, use the `sidekick-agent-mcp` console script
defined in pyproject.toml (which calls sidekick_agent.server:main directly).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sidekick_agent.server import main

if __name__ == "__main__":
    main()
