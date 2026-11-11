# Fantasy Wallpaper Studio

Portable wallpaper plugin for **Codex and ChatGPT Work**, derived from the
[source session](docs/wallpaper-project-summary.md). The main agent creates
matching vivo/iPad artwork with native subagents for ideas, art direction, and
review. No hosted service or API key is added by this plugin.

## Install and use

```bash
codex plugin marketplace add kkuga5121/image_create_plugin --ref main
```

Use your supported client's install/refresh flow, select **Fantasy Wallpaper
Plugins**, and install **Fantasy Wallpaper Studio**. The repository marketplace
is `.agents/plugins/marketplace.json`; its source resolves from the repository
root. Registration is not account installation. Client/account capabilities
determine whether native subagents and image tools are available.

Try: `ทำชุด 18 แบบ ข้อ 9 แบบคู่ vivo + iPad โดยใช้ subagent`.

See the [plugin guide](plugins/fantasy-wallpaper-studio/README.md) for requirements,
Thai examples, and the differences between local installation, account import,
and public submission. This repository does not install into an account or
publish to the public directory automatically.

## Develop and package

Python 3.10+ is needed for author tooling; there are no third-party dependencies.

```bash
python3 -m unittest discover -s tests -p 'test_plugin_tools.py' -v
python3 scripts/validate_plugin.py --plugin-dir plugins/fantasy-wallpaper-studio --marketplace .agents/plugins/marketplace.json
python3 scripts/package_plugin.py --plugin-dir plugins/fantasy-wallpaper-studio --output-dir dist
python3 -m zipfile -t dist/fantasy-wallpaper-studio-0.1.0.zip
```

The ZIP is written outside the plugin and ignored by Git. An existing archive
is preserved: remove your previous generated archive explicitly before rebuilding.
Skill frontmatter uses single-line JSON-quoted YAML scalars for `name` and
`description`; `agents/openai.yaml` uses JSON syntax, which is a YAML subset.
The project validator supports that authoring subset, not arbitrary YAML.

The [design](docs/design/2026-11-11-design-fantasy-wallpaper-plugin.md),
[implementation plan](docs/plan/2026-11-11-plan-fantasy-wallpaper-plugin.md), and
[verification record](docs/test/2026-11-11-test-fantasy-wallpaper-plugin.md)
describe scope and test evidence. Static package checks do not prove real image
generation, target-client installation, or on-device wallpaper behavior.
