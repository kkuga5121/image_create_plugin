"""Failure-oriented tests for the repository's authoring tools."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_plugin import parse_skill_frontmatter, validate_plugin


class PluginFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.plugin = self.repo / "plugins" / "fantasy-wallpaper-studio"
        self.skill = self.plugin / "skills" / "fantasy-wallpaper"
        (self.skill / "references").mkdir(parents=True)
        (self.skill / "agents").mkdir()
        self.manifest = {
            "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
            "name": self.plugin.name,
            "version": "0.1.0",
            "extensions": {"com.openai": {"interface": {
                "displayName": "Fantasy Wallpaper Studio",
                "shortDescription": "Create matching fantasy art",
                "category": "Productivity", "capabilities": [],
            }}},
        }
        self.write_json(self.plugin / "plugin.json", self.manifest)
        self.skill_text = ('---\nname: "fantasy-wallpaper"\n'
                           'description: "Use when creating wallpaper."\n---\n'
                           '# Wallpaper\n[Brief](references/brief.md#style)\n')
        (self.skill / "SKILL.md").write_text(self.skill_text)
        (self.skill / "references" / "brief.md").write_text('# Style\nFull frame.\n')
        self.metadata = {"interface": {"display_name": "Wallpaper",
                                      "short_description": "Fantasy wallpaper"},
                         "policy": {"products": ["CODEX", "CHAT"],
                                    "allow_implicit_invocation": True}}
        self.meta_path = self.skill / "agents" / "openai.yaml"
        self.write_json(self.meta_path, self.metadata)
        self.market = self.repo / ".agents" / "plugins" / "marketplace.json"
        self.market.parent.mkdir(parents=True)
        self.market_data = {"name": "fantasy-wallpaper-plugins", "plugins": [{
            "name": self.plugin.name,
            "source": {"source": "local", "path": "./plugins/" + self.plugin.name},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "category": "Productivity",
        }]}
        self.write_json(self.market, self.market_data)

    def write_json(self, path, value):
        path.write_text(json.dumps(value), encoding="utf-8")

    def errors(self):
        return "\n".join(validate_plugin(self.plugin, self.market))


class ValidationTests(PluginFixture):
    def test_valid_self_contained_plugin(self):
        self.assertEqual(validate_plugin(self.plugin, self.market), [])
        self.assertEqual(validate_plugin(self.plugin), [])
        self.assertEqual(parse_skill_frontmatter(self.skill_text)["name"], "fantasy-wallpaper")

    def test_invalid_manifest(self):
        path = self.plugin / "plugin.json"
        for bad in ([], {"name": self.plugin.name}, {**self.manifest, "version": "01.2.3"},
                    {**self.manifest, "extensions": []}):
            with self.subTest(bad=bad):
                self.write_json(path, bad)
                self.assertTrue(validate_plugin(self.plugin))
        path.write_text('{bad')
        self.assertIn("plugin.json", self.errors())

    def test_metadata_format(self):
        for text in (self.skill_text.replace('name: "fantasy-wallpaper"', 'name: unquoted'),
                     self.skill_text.replace('---\n#', 'name: "duplicate"\n---\n#'),
                     self.skill_text.replace('description: "Use when creating wallpaper."\n', ''),
                     self.skill_text.replace('name: "fantasy-wallpaper"', 'name: 42')):
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    parse_skill_frontmatter(text)
        self.meta_path.write_text('interface: [')
        self.assertIn("openai.yaml", self.errors())

    def test_invalid_metadata_types(self):
        for bad in ([], {"policy": {"products": "CHAT"}},
                    {"policy": {"products": ["unknown"]}},
                    {"policy": {"allow_implicit_invocation": "false"}},
                    {"interface": {"display_name": ""}}):
            with self.subTest(bad=bad):
                self.write_json(self.meta_path, bad)
                self.assertIn("openai.yaml", self.errors())

    def test_reference_escape_or_missing(self):
        outside = self.repo / "private.md"
        outside.write_text('outside')
        for link in ('references/missing.md', '../../../../private.md', str(outside),
                     'references/%2e%2e/%2e%2e/%2e%2e/%2e%2e/private.md'):
            with self.subTest(link=link):
                (self.skill / "SKILL.md").write_text(self.skill_text + f'\n[Bad]({link})\n')
                self.assertIn("reference", self.errors().lower())

    def test_symlink_rejected(self):
        outside = self.repo / "outside.md"
        outside.write_text('outside')
        (self.skill / "references" / "linked.md").symlink_to(outside)
        self.assertIn("symlink", self.errors().lower())

    def test_private_library_url_rejected(self):
        for private in ('https://chatgpt.com/library?file_id=' + 'libfile_example',
                        'libfile_' + 'example'):
            (self.skill / "references" / "brief.md").write_text(private)
            self.assertIn("private", self.errors().lower())

    def test_marketplace_target_mismatch(self):
        entry = self.market_data["plugins"][0]
        for path in ('./plugins/other', '../../outside', str(self.plugin)):
            with self.subTest(path=path):
                entry["source"]["path"] = path
                self.write_json(self.market, self.market_data)
                self.assertIn("marketplace", self.errors().lower())

    def test_forbidden_package_content(self):
        for name in ('.env', 'node_modules/a.txt', 'dist/output.zip', '.git/config',
                     'wallpaper-output/picture.png', 'backup.tar.gz'):
            with self.subTest(name=name):
                path = self.plugin / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('unrelated')
                self.assertIn("forbidden", self.errors().lower())
                path.unlink()

    def test_oversized_short_description(self):
        self.manifest['extensions']['com.openai']['interface']['shortDescription'] = 'x' * 31
        self.write_json(self.plugin / 'plugin.json', self.manifest)
        self.assertIn('shortDescription', self.errors())

    def test_unreadable_text_and_missing_root(self):
        (self.skill / 'references' / 'bad.md').write_bytes(b'\xff')
        self.assertIn('UTF-8', self.errors())
        self.assertTrue(validate_plugin(self.repo / 'absent'))

    def test_cli_invalid_input_is_diagnostic(self):
        result = subprocess.run([sys.executable, str(Path(__file__).resolve().parents[1] /
                                'scripts/validate_plugin.py'), '--plugin-dir',
                                str(self.repo / 'absent')], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertNotIn('Traceback', result.stderr)

    def test_sensitive_content_in_any_extension_blocks_archive(self):
        from package_plugin import build_archive
        for name, content in (
                ('notes', b'https://chatgpt.com/library?file_id=' + b'libfile_example'),
                ('private.pem', b'-----BEGIN ' + b'PRIVATE KEY-----'),
                ('binary.dat', b'\xff\x00' + b'libfile_' + b'example')):
            with self.subTest(name=name):
                path = self.plugin / name
                path.write_bytes(content)
                self.assertTrue(validate_plugin(self.plugin))
                with self.assertRaises(ValueError):
                    build_archive(self.plugin, self.repo / 'dist')
                self.assertEqual(list((self.repo / 'dist').glob('*')), [])
                path.unlink()

    def test_reference_style_markdown_is_contained(self):
        for reference in ('../../../../private.md', 'references/missing.md'):
            with self.subTest(reference=reference):
                (self.skill / 'SKILL.md').write_text(
                    self.skill_text + f'\n[Required brief][outside]\n[outside]: {reference}\n')
                self.assertIn('reference', self.errors().lower())
        (self.skill / 'SKILL.md').write_text(
            self.skill_text + '\n[Brief][style]\n[style]: <references/brief.md> "Style"\n')
        self.assertEqual(validate_plugin(self.plugin), [])

    def test_metadata_icons_use_skill_relative_contained_paths(self):
        assets = self.skill / 'assets'
        assets.mkdir()
        icon = assets / 'icon.svg'
        icon.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
        for key in ('icon_small', 'icon_large'):
            self.metadata['interface'][key] = './assets/icon.svg'
        self.write_json(self.meta_path, self.metadata)
        self.assertEqual(validate_plugin(self.plugin), [])
        for key in ('icon_small', 'icon_large'):
            for value in ('../../../../private.svg', './assets/missing.svg', str(icon),
                          'https://example.com/icon.svg', '', None):
                with self.subTest(key=key, value=value):
                    self.metadata['interface'][key] = value
                    self.write_json(self.meta_path, self.metadata)
                    self.assertIn('reference', self.errors().lower())
            self.metadata['interface'][key] = './assets/icon.svg'

    def test_backslash_filenames_rejected_for_portable_zip(self):
        from package_plugin import build_archive
        path = self.plugin / ('..' + '\\' + '..' + '\\' + 'outside.txt')
        path.write_text('unsafe Windows path')
        self.assertTrue(validate_plugin(self.plugin))
        with self.assertRaises(ValueError):
            build_archive(self.plugin, self.repo / 'dist')
        self.assertEqual(list((self.repo / 'dist').glob('*')), [])


class ArchiveTests(PluginFixture):
    def build(self, output=None):
        from package_plugin import build_archive
        return build_archive(self.plugin, output or self.repo / 'dist')

    def test_archive_is_self_contained(self):
        archive = self.build()
        self.assertEqual(archive.name, 'fantasy-wallpaper-studio-0.1.0.zip')
        with zipfile.ZipFile(archive) as z:
            names = z.namelist()
            self.assertIn(self.plugin.name + '/plugin.json', names)
            self.assertIn(self.plugin.name + '/skills/fantasy-wallpaper/SKILL.md', names)
            self.assertIn(self.plugin.name + '/skills/fantasy-wallpaper/references/brief.md', names)
            self.assertTrue(all(n.startswith(self.plugin.name + '/') and
                                not Path(n).is_absolute() and '..' not in Path(n).parts
                                for n in names))
            isolated = self.repo / 'extracted'
            z.extractall(isolated)
        self.assertEqual(validate_plugin(isolated / self.plugin.name), [])

    def test_invalid_package_writes_no_archive(self):
        (self.plugin / 'plugin.json').write_text('{}')
        with self.assertRaises(ValueError):
            self.build()
        self.assertEqual(list((self.repo / 'dist').glob('*')), [])

    def test_output_inside_plugin_rejected(self):
        for output in (self.plugin, self.plugin / 'nested'):
            with self.subTest(output=output):
                with self.assertRaises(ValueError):
                    self.build(output)
        self.assertEqual(list(self.plugin.rglob('*.zip')), [])

    def test_existing_archive_preserved(self):
        output = self.repo / 'dist'
        output.mkdir()
        archive = output / 'fantasy-wallpaper-studio-0.1.0.zip'
        archive.write_bytes(b'keep existing bytes')
        with self.assertRaises(ValueError):
            self.build(output)
        self.assertEqual(archive.read_bytes(), b'keep existing bytes')

    def test_failed_write_cleans_temporary_file(self):
        from unittest.mock import patch
        with patch('zipfile.ZipFile.write', side_effect=OSError('test write failure')):
            with self.assertRaises(OSError):
                self.build()
        self.assertEqual(list((self.repo / 'dist').glob('*')), [])


if __name__ == '__main__':
    unittest.main()
