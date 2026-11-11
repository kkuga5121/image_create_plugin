# Fantasy Wallpaper Studio Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Deliver a self-contained skills plugin that delegates wallpaper work to native subagents, produces reference-based vivo/iPad pairs using host tools, and is distributed through the existing Git repository.

**Architecture:** A portable plugin contains one coordinating skill and four supporting references. The main agent owns image generation and delivery; child agents handle bounded ideation, art direction, and review. Repository tooling validates the package and creates a ZIP without adding a runtime service.

**Tech Stack:** Agent Plugins 1.0 JSON, Markdown skills, YAML metadata, Python 3.10+ standard library (`json`, `pathlib`, `unittest`, `tempfile`, `zipfile`), Git, and host-native image/subagent tools.

**Spec:** [Fantasy Wallpaper Studio design](../design/2026-11-11-design-fantasy-wallpaper-plugin.md).

**Source:** [Wallpaper session summary](../wallpaper-project-summary.md).

**Status:** Implemented and source delivery verified on `origin/main`. Execution evidence is recorded in the [verification record](../test/2026-11-11-test-fantasy-wallpaper-plugin.md); client installation and real image generation remain untested.

## Global Constraints

- Plugin identity: `fantasy-wallpaper-studio`; display name: `Fantasy Wallpaper Studio`; initial version: `0.1.0`.
- Skill identity: `fantasy-wallpaper`; product metadata: `CODEX` and `CHAT`.
- Use native host tools and inherited permissions. Add no MCP server, API credentials, model override, or custom-agent installation.
- At most three active child agents; honor any lower host limit. Children must not recursively delegate, generate images independently, publish, or modify the repository.
- The latest painterly semi-realistic brief overrides historical anime and clock-space experiments.
- Target composition: vivo approximately `9:20`; iPad approximately `1.45:1`. These are not guaranteed tool sizes or device-resolution claims.
- Generate vivo first, then supply that actual image as the reference for a separate iPad image. A batch of N concepts needs 2N outputs.
- The plugin must be self-contained. Exclude source-session private library URLs, unrelated documents, secrets, symlinks, generated images, and build artifacts from its ZIP.
- Missing capabilities must be reported honestly. Single-agent fallback requires the user's choice.
- Preserve historical catalogs as distinct sets. Historical completion does not prove present file access.
- Delivery target: `https://github.com/kkuga5121/image_create_plugin.git`, branch `main`. Never force-push or overwrite remote work.
- Git delivery does not authorize account installation or public directory publication.

## Review Focus

1. Bare concept numbers with no active set must trigger clarification; Task 2 scenario S2 covers this.
2. A child unable to access an image must not invent visual findings; Task 2 scenario S4 covers this.
3. A missing portrait reference or failed landscape must leave a visibly incomplete pair; Task 2 scenario S3 covers this.
4. Symlinks, escaping paths, and private library URLs must prevent packaging; Task 3 automated cases cover these.
5. Invalid input or an output path inside the plugin must leave no archive behind; Task 4 automated cases cover these.

## File Responsibilities

| Path | Responsibility |
| --- | --- |
| `plugins/fantasy-wallpaper-studio/plugin.json` | Portable identity, version, repository, and OpenAI presentation metadata. |
| `plugins/fantasy-wallpaper-studio/skills/fantasy-wallpaper/SKILL.md` | Request routing, capability checks, explicit native delegation, and delivery rules. |
| `plugins/fantasy-wallpaper-studio/skills/fantasy-wallpaper/agents/openai.yaml` | Optional skill display and product metadata, not custom-agent registration. |
| `plugins/fantasy-wallpaper-studio/skills/fantasy-wallpaper/references/visual-brief.md` | Latest visual defaults, subject types, device targets, and superseded rules. |
| `plugins/fantasy-wallpaper-studio/skills/fantasy-wallpaper/references/concept-catalog.md` | Named 18-, 12-, and 10-concept sets, names, inspiration, and historical status. |
| `plugins/fantasy-wallpaper-studio/skills/fantasy-wallpaper/references/agent-roles.md` | Three role task templates, input/output requirements, limits, and evidence rules. |
| `plugins/fantasy-wallpaper-studio/skills/fantasy-wallpaper/references/pair-production.md` | Image-reference dependency, generation, correction, verification, and batch tracking. |
| `plugins/fantasy-wallpaper-studio/README.md` | Portable usage, requirements, examples, and installation limitations. |
| `.agents/plugins/marketplace.json` | Repository marketplace entry resolving to the plugin directory. |
| `scripts/validate_plugin.py` | Package and optional marketplace validation; reusable validation functions and CLI. |
| `scripts/package_plugin.py` | Validated ZIP construction outside the plugin directory. |
| `tests/test_plugin_tools.py` | Failure-oriented validation and archive tests using temporary fixtures. |
| `README.md`, `.gitignore` | Repository setup, author commands, install guidance, and generated-output exclusions. |
| `docs/test/2026-11-11-test-fantasy-wallpaper-plugin.md` | Acceptance scenarios and observed/unverified results. |

Use the existing [workflow diagram](../diagram/2026-11-11-design-fantasy-wallpaper-plugin.puml) for generation dependencies; no second architecture is introduced by this plan.

## Task 1: Create the Discoverable Plugin Package

**Files:** Create both manifests, skill metadata, plugin README, repository README, and `.gitignore` from the table. Create the skill entry file in Task 2; the package is complete only after that dependency lands.

**Interfaces:** Consumes the design's identity and directory layout. Produces plugin version `0.1.0`, repository marketplace `fantasy-wallpaper-plugins`, and source path `./plugins/fantasy-wallpaper-studio` for Tasks 2–4.

- [x] **Step 1:** Create root `plugin.json` with `$schema` exactly `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`, the specified identity/version, repository URL, and descriptive metadata under `extensions.com.openai.interface`. Use category `Productivity`, display name `Fantasy Wallpaper Studio`, and short description `Create matching fantasy art` (27 characters). Omit unknown author, license, app, and service fields.
- [x] **Step 2:** Create `.agents/plugins/marketplace.json` with marketplace identity `fantasy-wallpaper-plugins`, the plugin entry, local source path above, `policy.installation: AVAILABLE`, `policy.authentication: ON_INSTALL`, and category `Productivity`. Do not alter user-level configuration or enable/install the plugin automatically.
- [x] **Step 3:** Create `agents/openai.yaml` with display name, short description, one default prompt, and `policy.products: [CODEX, CHAT]`. Use JSON syntax for this YAML document: JSON is a YAML subset and enables dependency-free parsing. Do not add custom agent definitions.
- [x] **Step 4:** Write the two READMEs. Include desktop repository-marketplace discovery, the documented CLI registration example `codex plugin marketplace add kkuga5121/image_create_plugin --ref main`, required host capabilities, and Thai idea/pair/revision examples. Distinguish repository installation, account import, and public publication. Tell users to use their client's supported install/refresh flow; do not promise web access to local files.
- [x] **Step 5:** Ignore `dist/`, Python caches, and generated wallpaper output directories. Keep every file referenced by the plugin inside its directory. Parse both manifests with `python3 -m json.tool PATH` and inspect marketplace source resolution; expected result is valid JSON and the intended plugin path.

No unit tests are needed for this reversible metadata/documentation work. Commit this package together with Task 2 once the skill exists.

## Task 2: Implement the Wallpaper Workflow and Role Instructions

**Files:** Create `SKILL.md`, all four references, and the acceptance document listed above. Update the plugin README if the final example wording changes.

**Interfaces:** Consumes Task 1's skill path and identity plus the source session. Produces a usable skill, role prompts, and manual scenarios S1–S7 for Task 5. A role invocation receives `task`, `brief`, `constraints`, `accessible_references`, and `required_output` as descriptive prompt sections, not a new API schema.

- [x] **Step 1:** Write flat YAML frontmatter with only `name` and `description`, each a single-line JSON-quoted string. Document the validator's supported authoring format; do not claim it parses arbitrary YAML. Route Thai/English requests for ideas, expansion, single orientations, pairs, review, and revision. Load supporting references only when needed.
- [x] **Step 2:** Extract the latest visual defaults and all three concept sets from the session. Assign stable set labels `latest-18`, `japan-12`, and `fantasy-10`; retain Thai titles and original numbering. Preserve historical status with an explicit provenance disclaimer. Do not copy private library URLs. Explain that inspiration is not verification of invented story events.
- [x] **Step 3:** Write the three role templates. The coordinator explicitly calls available native delegation tools, waits for dependent results, and limits concurrency to three or the lower host cap. Ideation can delegate independent categories; an already selected concept skips ideation. Art direction returns shared anchors and both compositions. Visual review returns image-backed findings or an explicit inability to inspect. Do not hardcode host-specific tool names.
- [x] **Step 4:** Write the pair-production instructions: portrait generation and inspection; actual portrait reference supplied to landscape generation; separate image outputs; targeted edits; actual dimension measurement where possible; honest ratio/crop reporting. Track each batch item by set, concept, orientation, and review status. Never replace reference-based generation with two independent text prompts without reporting the limitation.
- [x] **Step 5:** Document capability failure behavior. Check only tools required by the current task: an ideas-only request needs no image generator. Missing native delegation blocks the subagent workflow; offer but do not silently start a single-agent alternative. Missing generation or inaccessible references leave generation blocked or incomplete. The main agent may inspect images when a child cannot, recording who performed the check.
- [x] **Step 6:** Add these manual acceptance scenarios with `Not run` as their initial result. They test instruction behavior, not text-keyword presence:

| ID | Input or condition | Expected observation |
| --- | --- | --- |
| S1 | `คิดไอเดียใหม่ 6 แบบ แบ่งหญิง ฉาก และสัตว์` | Actual native child activity for independent categories; six ideas; no image generation and no invented delegation. |
| S2 | `ทำข้อ 4 แบบคู่` with no active catalog | Ask which set; do not generate. With `latest-18`, resolve the sea-above-crossing concept. |
| S3 | `ทำชุด 18 แบบ ข้อ 9 แบบคู่ vivo + iPad`; then simulate missing portrait reference or landscape failure | Art-direction delegation; portrait before landscape; reference evidence when available; incomplete status on failure; no fabricated pair. |
| S4 | Reviewer has no image access; separately, metadata cannot be measured | No invented visual review or dimensions. Main-agent visual inspection is attributed accurately if possible. |
| S5 | Host has no native delegation, or no generation tool | Report the unavailable capability. Do not claim completion or silently use the single-agent alternative. |
| S6 | Two selected concepts; one landscape fails | Account for four required outputs; identify the failed orientation and deliver available outputs with partial status. |
| S7 | Existing pair needs a lighting change | Preserve accepted identity and references, use image editing, review the changed pair, and do not repeat ideation. |

- [x] **Step 7:** Read the skill and references against the design's acceptance criteria. Verify metadata parsing and link containment once Task 3 is available. Avoid automated tests that only assert prose contains a phrase.
- [x] **Step 8:** Commit Tasks 1–2 with explicit file paths and message `feat: add fantasy wallpaper workflow plugin`.

## Task 3: Add Focused Package Validation

**Files:** Create `scripts/validate_plugin.py` and `tests/test_plugin_tools.py`.

**Interfaces:** Produce `parse_skill_frontmatter(text: str) -> dict[str, str]` and `validate_plugin(plugin_dir: Path, marketplace: Path | None = None) -> list[str]`. The validator returns an empty list for success and diagnostic strings for invalid input; expected malformed-input failures must not leak a traceback. Task 4 imports `validate_plugin`.

- [x] **Step 1:** Write temporary-fixture `unittest` cases: `test_valid_self_contained_plugin` asserts `[]`; `test_invalid_manifest` asserts diagnostics for malformed JSON or missing schema; `test_metadata_format` rejects invalid/duplicate required frontmatter fields and malformed `openai.yaml` JSON. Assert supported product metadata and nonempty strings, not exact prose.
- [x] **Step 2:** Add `test_reference_escape_or_missing` for missing local references, `../` escape, and absolute local paths; `test_symlink_rejected`; `test_private_library_url_rejected`; `test_marketplace_target_mismatch`; and `test_forbidden_package_content` for `.env`, dependency directories, archives, and generated outputs. Assert useful diagnostic substrings identifying the file or condition.
- [x] **Step 3:** Run `python3 -m unittest discover -s tests -p 'test_plugin_tools.py' -v`. Expected initial failure: missing validator module/functions. Confirm the failure comes from the absent implementation before proceeding.
- [x] **Step 4:** Implement the validator using the standard library. Parse manifests with `json`; parse `openai.yaml` as the declared JSON-compatible YAML subset; parse the two frontmatter scalar values with `json.loads`. Reject unsupported formatting clearly rather than implementing a general YAML parser. Validate identity, SemVer, nonblank presentation values, short-description length at most 30, unique skill names, and products `CODEX`/`CHAT`.
- [x] **Step 5:** Validate local Markdown links and local metadata asset references using resolved paths under the plugin root; allow ordinary external HTTPS documentation links. Reject symlinks before reading targets, credential/private-library content, and forbidden files. Resolve marketplace sources relative to repository root, not `.agents/plugins/`. Do not evaluate or execute referenced files.
- [x] **Step 6:** Add CLI options `--plugin-dir PATH` and optional `--marketplace PATH`. Print diagnostics and exit `1` on invalid input; print `Plugin validation passed.` and exit `0` on success. Run the unit command again, then `python3 scripts/validate_plugin.py --plugin-dir plugins/fantasy-wallpaper-studio --marketplace .agents/plugins/marketplace.json`; both must pass.
- [x] **Step 7:** Commit the scripts/tests with message `build: validate plugin metadata and contained references`.

## Task 4: Build and Inspect the ZIP

**Files:** Create `scripts/package_plugin.py`; extend `tests/test_plugin_tools.py`.

**Interfaces:** Consume `validate_plugin` from Task 3. Produce `build_archive(plugin_dir: Path, output_dir: Path) -> Path`, which validates before writing and raises `ValueError` for invalid input, an output inside the plugin, or an existing target archive. Return `<output_dir>/fantasy-wallpaper-studio-0.1.0.zip` for this version.

- [x] **Step 1:** Add `test_archive_is_self_contained` asserting one `fantasy-wallpaper-studio/` wrapper, expected manifest/skill/reference members, safe relative member paths, and successful validation after extraction into a temporary directory without the repository.
- [x] **Step 2:** Add `test_invalid_package_writes_no_archive`, `test_output_inside_plugin_rejected`, and `test_existing_archive_preserved`. Assert that failed builds create no ZIP and preserve existing bytes. Run the unit command from Task 3 and confirm the new cases fail because packaging is absent.
- [x] **Step 3:** Implement `build_archive` with `zipfile`, sorted contained files, validation before writing, and temporary-file cleanup on errors. Include every used plugin file, including intended hidden files if any; reject symlinks and forbidden members rather than silently making a broken package. Do not include repository marketplace or development files.
- [x] **Step 4:** Add CLI options `--plugin-dir PATH` and `--output-dir PATH`. Print the produced path and exit `0`; print actionable validation/build errors and exit `1`. Run the full unit suite; expected result is all tests passing.
- [x] **Step 5:** Run `python3 scripts/package_plugin.py --plugin-dir plugins/fantasy-wallpaper-studio --output-dir dist`, then `python3 -m zipfile -t dist/fantasy-wallpaper-studio-0.1.0.zip` and `python3 -m zipfile -l dist/fantasy-wallpaper-studio-0.1.0.zip`. Expect a valid ZIP containing only the self-contained plugin wrapper and its intended files. Extract to a temporary directory and run the validator there without a marketplace argument.
- [x] **Step 6:** Commit with message `build: package validated wallpaper plugin archives`. Keep `dist/` ignored. Rebuild and inspect again if packaged source changes later; remove only a previously generated archive from this task when intentionally rebuilding.

## Task 5: Verify Observed Behavior and Deliver to Git

**Files:** Update the acceptance/test record and README verification notes. Update the design's implementation status accurately; do not rewrite its historical decisions as test results.

**Interfaces:** Consume Task 2 scenarios, Task 3 validator, and Task 4 archive. Produce a test record separating static checks, native delegation, real image generation, host installation, and remote Git delivery.

- [x] **Step 1:** Run the full unit suite, package validator with marketplace, and `git diff --check`. Record the commands, exit status, and relevant results. Do not repeat successful checks unless source changes or a failure requires it.
- [x] **Step 2:** When native tools are available, run one no-image art-direction smoke check using the actual packaged role instructions and the `latest-18` concept 9 brief. Require a real child-agent result containing shared anchors and both compositions with the correct targets. Record that this proves delegated art direction in the present environment, not installed-plugin activation or visual generation.
- [x] **Step 3:** Walk through S1–S7 as manual scenarios only where the available environment supports observation. Do not generate wallpapers solely for packaging validation. Mark image-dependent scenarios and client installation `Not run` unless actually exercised; distinguish reasoning-through instructions from observed execution. Report blockers without fabricated success.
- [x] **Step 4:** Request a focused whole-change review against the design, then resolve correctness findings. Review catalog numbering, stale visual rules, child image access, reference dependency, archive containment, and honest capability reporting. Run only the checks affected by any corrections, and rebuild the archive after package edits.
- [x] **Step 5:** Commit final verification/documentation with message `docs: record wallpaper plugin verification and usage`. Check `git status --short --branch` and inspect the final commit list. Stage only intended project files; preserve unrelated user work.
- [x] **Step 6:** Run `git fetch origin` and `git log --oneline --left-right HEAD...origin/main`. If the remote has new commits, integrate without overwriting them and rerun affected checks. Push with `git push origin main`; never use a force option.
- [x] **Step 7:** Compare `git rev-parse HEAD` with the hash returned by `git ls-remote --heads origin main`. Matching hashes prove remote delivery. Report repository/commit link, source paths, local ZIP path, checks performed, and remaining unverified host/image behavior. Do not claim account installation or public publication.

## Completion Boundary

The implementation is delivered when source exists on remote `main`, the package checks pass, the ZIP has been inspected independently of the repository, and the verification record states what actually ran. Host installation and real image creation are separate observations, not implied by source delivery. This planning request stops after saving and checking this document.
