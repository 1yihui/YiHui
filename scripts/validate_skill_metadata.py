#!/usr/bin/env python3
"""Check SKILL.md metadata without executing skills or interpreting their bodies."""

import argparse
from pathlib import Path
import re
import sys

try:
    import yaml
except ImportError:
    raise SystemExit(
        "Missing PyYAML. Run: python -m pip install -r scripts/requirements-metadata.txt"
    )


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject repeated explicit keys, including nested/flow mappings.

    Check before SafeLoader expands YAML merges so a legitimate explicit override
    of an inherited key is not mistaken for a duplicate.
    """

    def __init__(self, stream):
        super().__init__(stream)
        self.checked_mappings = set()

    def flatten_mapping(self, node):
        if id(node) not in self.checked_mappings:
            self.checked_mappings.add(id(node))
            seen = {}
            for key_node, _ in node.value:
                if key_node.tag == "tag:yaml.org,2002:merge":
                    key = "<<"
                else:
                    key = self.construct_object(key_node)
                try:
                    if key in seen:
                        raise yaml.constructor.ConstructorError(
                            "while constructing a mapping", seen[key],
                            f"duplicate YAML key {key!r}", key_node.start_mark,
                        )
                    seen[key] = key_node.start_mark
                except TypeError:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping", node.start_mark,
                        "unhashable YAML key", key_node.start_mark,
                    ) from None
        super().flatten_mapping(node)


FIELD = re.compile(r"^([A-Za-z][A-Za-z0-9_.-]*):(?:\s|$)")


def leading_body_fields(lines, start):
    """Inspect only an unfenced metadata-like preamble, never prose/examples.

    A heading, fence, blockquote, or ordinary paragraph ends this check. Blank
    lines, indented YAML continuations and stray delimiters may separate fields.
    """
    fields = []
    for index in range(start, len(lines)):
        line = lines[index]
        if not line.strip() or line.rstrip() == "---":
            continue
        match = FIELD.match(line)
        if match:
            fields.append((match.group(1), index + 1))
        elif fields and line.startswith((" ", "\t")):
            continue
        else:
            break
    return fields


def check_file(path):
    """Return (name, errors); errors contain a file path and 1-based line."""
    errors = []

    def error(line, message):
        errors.append(f"{path}:{line}: {message}")

    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except (OSError, UnicodeError) as exc:
        error(1, f"cannot read UTF-8: {exc}")
        return None, errors
    if not lines or lines[0].rstrip() != "---":
        error(1, "missing opening frontmatter delimiter '---'")
        return None, errors
    end = next((i for i in range(1, len(lines)) if lines[i].rstrip() == "---"), None)
    if end is None:
        error(1, "missing closing frontmatter delimiter '---'")
        return None, errors
    try:
        metadata = yaml.load("\n".join(lines[1:end]), Loader=UniqueKeyLoader)
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        error(mark.line + 2 if mark else 1, f"invalid YAML: {getattr(exc, 'problem', str(exc))}")
        return None, errors
    if not isinstance(metadata, dict):
        error(2, "frontmatter must be a YAML mapping")
        return None, errors
    for key in ("name", "description"):
        value = metadata.get(key)
        if not isinstance(value, str) or not value.strip():
            error(2, f"{key} must be a non-empty string")
    for key, line in leading_body_fields(lines, end + 1):
        if key in metadata:
            error(line, f"repeated metadata field {key!r} after closing frontmatter")
    name = metadata.get("name")
    return name.strip() if isinstance(name, str) and name.strip() else None, errors


def validate(root):
    """Return (number of SKILL.md files, errors), including cross-file duplicates."""
    paths = sorted((root / "skills").rglob("SKILL.md"))
    if not paths:
        return 0, [f"{root / 'skills'}:1: no SKILL.md files found"]
    errors = []
    names = {}
    for path in paths:
        name, file_errors = check_file(path)
        errors.extend(file_errors)
        if name:
            if name in names:
                errors.append(f"{path}:2: duplicate skill name {name!r}; first declared in {names[name]}")
            else:
                names[name] = path
    return len(paths), errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1],
        help="repository root (defaults to this script's repository)",
    )
    count, errors = validate(parser.parse_args(argv).root)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"FAIL: {count} SKILL.md files; {len(errors)} error(s).", file=sys.stderr)
        return 1
    print(f"OK: {count} SKILL.md files; unique names, valid YAML, no leading metadata residue.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
