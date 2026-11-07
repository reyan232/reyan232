"""Tests für Projektstruktur: Agenten, Skills, Schutzregeln, Validator-CLI."""
import io
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from scripts.validate_research_data import (
    AGENT_ALLOWED_TOOLS, BASE, EXPECTED_AGENTS, EXPECTED_SKILLS, check_project_structure,
    main, parse_frontmatter,
)

try:
    import yaml  # noqa: F401
    HAVE_YAML = True
except ImportError:  # pragma: no cover
    HAVE_YAML = False


class RepositoryStructureTests(unittest.TestCase):
    def test_repository_structure_has_no_errors(self):
        self.assertEqual(check_project_structure(BASE).errors, [])

    def test_six_agents_with_valid_frontmatter_and_read_only_tools(self):
        for name in EXPECTED_AGENTS:
            with self.subTest(agent=name):
                text = (BASE / '.claude/agents' / f'{name}.md').read_text(encoding='utf-8')
                fm, _, problem = parse_frontmatter(text)
                self.assertIsNone(problem)
                self.assertEqual(fm['name'], name)
                tools = {t.strip() for t in str(fm['tools']).split(',')}
                self.assertTrue(tools <= AGENT_ALLOWED_TOOLS, tools)

    def test_seven_skills_with_valid_frontmatter(self):
        for name in EXPECTED_SKILLS:
            with self.subTest(skill=name):
                text = (BASE / '.claude/skills' / name / 'SKILL.md').read_text(encoding='utf-8')
                fm, body, problem = parse_frontmatter(text)
                self.assertIsNone(problem)
                self.assertEqual(fm['name'], name)
                self.assertIn('Beispiel', body)

    @unittest.skipUnless(HAVE_YAML, 'PyYAML nicht installiert')
    def test_frontmatter_is_strict_yaml(self):
        files = list((BASE / '.claude/agents').glob('*.md')) + list((BASE / '.claude/skills').glob('*/SKILL.md'))
        self.assertEqual(len(files), 13)
        for path in files:
            with self.subTest(file=path.name):
                raw = path.read_text(encoding='utf-8').split('\n---', 1)[0][3:]
                self.assertIsInstance(yaml.safe_load(raw), dict)

    def test_cli_succeeds_on_repository(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(['--root', str(BASE)])
        self.assertEqual(code, 0, buf.getvalue())


class StructureViolationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        shutil.copytree(BASE / '.claude', self.root / '.claude',
                        ignore=shutil.ignore_patterns('settings.local.json'))

    def tearDown(self):
        self.tmp.cleanup()

    def errors(self):
        return check_project_structure(self.root).errors

    def test_write_tool_in_agent_is_rejected(self):
        path = self.root / '.claude/agents/source-researcher.md'
        text = path.read_text(encoding='utf-8')
        path.write_text(text.replace('tools: Read,', 'tools: Write, Read,', 1), encoding='utf-8')
        self.assertTrue(any('nicht erlaubte Tools' in e for e in self.errors()))

    def test_missing_agent_section_is_rejected(self):
        path = self.root / '.claude/agents/scientific-critic.md'
        text = path.read_text(encoding='utf-8')
        path.write_text(text.replace('## Verbote', '## Hinweise'), encoding='utf-8')
        self.assertTrue(any('"## Verbote"' in e for e in self.errors()))

    def test_broken_yaml_is_rejected(self):
        path = self.root / '.claude/skills/citation-audit/SKILL.md'
        path.write_text('name: citation-audit\nkein frontmatter\n', encoding='utf-8')
        self.assertTrue(any('Frontmatter fehlt' in e for e in self.errors()))

    def test_missing_student_draft_protection_is_rejected(self):
        (self.root / '.claude/settings.json').write_text('{"permissions": {"deny": []}}', encoding='utf-8')
        self.assertTrue(any('06_student_draft' in e for e in self.errors()))


if __name__ == '__main__':
    unittest.main()
