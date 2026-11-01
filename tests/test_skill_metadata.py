"""Regression cases for metadata errors and existing repository formats."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_skill_metadata import check_file, validate


class MetadataTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def skill(self, directory="example", metadata=None, body="\n# Example\n"):
        if metadata is None:
            metadata = "name: example\ndescription: Example skill\n"
        path = self.root / "skills" / directory / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"---\n{metadata}---\n{body}", encoding="utf-8")
        return path

    def test_current_metadata_formats(self):
        for tags in ("[news, rss]", "news, rss"):
            with self.subTest(tags=tags):
                path = self.skill(metadata=f'''name: Daily News Digest
description: |
  A multi-line description: valid YAML.
  Another line.
tags: {tags}
compatibility: openclaw | claude-code | any-agent
trigger: [news]
triggers: [digest]
metadata: {{"openclaw": {{"emoji": "📰", "requires": {{"bins": []}}}}}}
displayName: Example
acceptLicenseTerms: true
custom-extension: whatever
''')
                self.assertEqual(check_file(path), ("Daily News Digest", []))

    def test_duplicate_names_across_nested_directories(self):
        self.skill("first")
        self.skill("nested/second")
        count, errors = validate(self.root)
        self.assertEqual(count, 2)
        self.assertEqual(len(errors), 1)
        self.assertIn("duplicate skill name", errors[0])

    def test_distinct_display_names_and_directory_mismatch(self):
        self.skill("different-dir", "name: Self-Improving + Proactive Agent\ndescription: Fine\n")
        self.skill("other", "name: brain\ndescription: Fine\n")
        self.assertEqual(validate(self.root), (2, []))

    def test_duplicate_yaml_keys(self):
        cases = (
            "tags: [a]\ntags: [b]\n",
            "metadata:\n  openclaw:\n    emoji: a\n    emoji: b\n",
            'metadata: {"openclaw": {"emoji": "a", "emoji": "b"}}\n',
            "metadata:\n  <<: {emoji: a, emoji: b}\n",
        )
        for suffix in cases:
            with self.subTest(suffix=suffix):
                path = self.skill(metadata="name: example\ndescription: Fine\n" + suffix)
                self.assertIn("duplicate YAML key", check_file(path)[1][0])

    def test_merge_overrides_and_reused_aliases_are_valid(self):
        path = self.skill(metadata='''name: example
description: Fine
defaults: &defaults {emoji: a, enabled: true}
metadata: {<<: *defaults, emoji: b}
other: {<<: *defaults, enabled: false}
''')
        self.assertEqual(check_file(path), ("example", []))

    def test_yaml_syntax_error(self):
        path = self.skill(metadata="name: example\ndescription: invalid: colon\n")
        errors = check_file(path)[1]
        self.assertIn(f"{path}:3: invalid YAML", errors[0])

    def test_unsafe_yaml_tag_is_rejected(self):
        path = self.skill(metadata="name: example\ndescription: Fine\nextra: !!python/object:os.system {}\n")
        self.assertIn("invalid YAML", check_file(path)[1][0])

    def test_missing_delimiters(self):
        for text in ("name: example\n", "---\nname: example\n"):
            with self.subTest(text=text):
                path = self.skill()
                path.write_text(text, encoding="utf-8")
                self.assertIn("delimiter", check_file(path)[1][0])

    def test_empty_and_non_mapping_frontmatter(self):
        for metadata in ("", "- example\n", "example\n"):
            with self.subTest(metadata=metadata):
                self.assertIn("must be a YAML mapping", check_file(self.skill(metadata=metadata))[1][0])

    def test_required_string_fields(self):
        for metadata in ("name: example\n", "description: Fine\n", "name: []\ndescription: 42\n"):
            with self.subTest(metadata=metadata):
                self.assertTrue(check_file(self.skill(metadata=metadata))[1])

    def test_original_four_field_residue(self):
        path = self.skill(
            metadata="name: example\ndescription: Fine\ntags: [old]\ncompatibility: openclaw\nlicense: MIT\nsource: https://example.org\n",
            body="\ntags:\n  - new\ncompatibility: openclaw\nlicense: MIT\nsource: https://example.org\n\n# Example\n",
        )
        errors = check_file(path)[1]
        self.assertEqual(len(errors), 4)
        self.assertTrue(all("repeated metadata field" in error for error in errors))

    def test_extra_delimiter_does_not_hide_residue(self):
        errors = check_file(self.skill(body="\n---\nname: example\n---\n# Example\n"))[1]
        self.assertIn("repeated metadata field 'name'", errors[0])

    def test_markdown_examples_are_not_metadata(self):
        for body in (
            "```yaml\nname: example\n```\n",
            "~~~yaml\nname: example\n~~~\n",
            "    name: example\n",
            "# Example\nname: example\n",
            "An example follows:\nname: example\n",
            "> name: example\n",
        ):
            with self.subTest(body=body):
                self.assertEqual(check_file(self.skill(body=body))[1], [])

    def test_bom_and_crlf(self):
        path = self.skill()
        text = path.read_text()
        path.write_bytes(b"\xef\xbb\xbf" + text.replace("\n", "\r\n").encode())
        self.assertEqual(check_file(path), ("example", []))

    def test_invalid_utf8(self):
        path = self.skill()
        path.write_bytes(b"\xff")
        self.assertIn("cannot read UTF-8", check_file(path)[1][0])

    def test_empty_repository_fails(self):
        self.assertIn("no SKILL.md files found", validate(self.root)[1][0])

    def test_cli_exit_codes(self):
        script = Path(__file__).resolve().parents[1] / "scripts/validate_skill_metadata.py"
        for valid, expected in ((True, 0), (False, 1)):
            with self.subTest(valid=valid):
                self.skill(metadata="name: example\ndescription: Fine\n" if valid else "name: []\n")
                result = subprocess.run([sys.executable, str(script), str(self.root)], capture_output=True, text=True)
                self.assertEqual(result.returncode, expected, result.stderr)


if __name__ == "__main__":
    unittest.main()
