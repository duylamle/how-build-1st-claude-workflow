#!/usr/bin/env python3
"""
Validate YAML frontmatter in .claude/ files.

This is an example hook for Claude Code that runs on PostToolUse -> Write.
It checks whether files in .claude/ have valid YAML frontmatter with
required fields.

Usage as a Claude Code hook (in .claude/settings.local.json):
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "command": "python .claude/hooks/validate-frontmatter.py \"$FILE_PATH\""
      }
    ]
  }
}

How to extend:
- Add new file types to REQUIRED_FIELDS to validate other files
- Add custom validators in the validate_* functions
- Chain multiple hooks in settings.local.json for different checks
"""

import sys
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration: define which files need which frontmatter fields.
# Keys are filename patterns, values are lists of required field names.
# Nested fields use dot notation (e.g., "metadata.agent").
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = {
    "AGENT.md": ["name", "description", "tools", "model", "skills"],
    "SKILL.md": ["name", "description", "metadata.agent", "metadata.input", "metadata.output"],
}


def extract_frontmatter(content: str) -> dict | None:
    """Extract YAML frontmatter from markdown content.

    Returns parsed dict if valid frontmatter exists, None otherwise.
    """
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None

    # Simple YAML parsing without external dependencies.
    # Handles flat keys and one level of nesting (metadata.field).
    # For production use, consider importing pyyaml.
    raw = match.group(1)
    result = {}
    current_parent = None

    for line in raw.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # Detect indented key (nested under parent)
        if line.startswith("  ") and current_parent and ":" in stripped:
            key, _, value = stripped.partition(":")
            full_key = f"{current_parent}.{key.strip()}"
            result[full_key] = value.strip()
            continue

        # Top-level key
        if ":" in stripped:
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip()
            result[key] = value
            # Track parent for nested fields (e.g., "metadata:")
            if not value or value == ">":
                current_parent = key
            else:
                current_parent = None

    return result


def get_nested_value(data: dict, dotted_key: str) -> str | None:
    """Look up a dotted key like 'metadata.agent' in the parsed dict."""
    return data.get(dotted_key)


def validate_file(file_path: str) -> list[str]:
    """Validate a single file. Returns list of error messages (empty = valid)."""
    path = Path(file_path)
    errors = []

    # Only validate files inside .claude/
    if ".claude" not in path.parts:
        return errors

    # Check if this filename has validation rules
    filename = path.name
    if filename not in REQUIRED_FIELDS:
        return errors

    # Read file
    try:
        content = path.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError) as e:
        return [f"Cannot read file: {e}"]

    # Check frontmatter exists
    frontmatter = extract_frontmatter(content)
    if frontmatter is None:
        return [f"{filename} is missing YAML frontmatter (expected --- block at top of file)"]

    # Check required fields
    for field in REQUIRED_FIELDS[filename]:
        value = get_nested_value(frontmatter, field)
        if value is None or value == "" or value.startswith("[TODO"):
            errors.append(f"{filename}: missing or placeholder value for required field '{field}'")

    return errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python hook-validate-example.py <file_path>")
        print("  Validates YAML frontmatter in AGENT.md and SKILL.md files.")
        sys.exit(0)

    file_path = sys.argv[1]
    errors = validate_file(file_path)

    if errors:
        print("Frontmatter validation errors:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        # Silent on success (convention for hooks)
        sys.exit(0)


if __name__ == "__main__":
    main()
