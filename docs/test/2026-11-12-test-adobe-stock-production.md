# Adobe Stock Production upgrade and verification

Date: 12 November 2026, Asia/Bangkok.

## Implemented scope

Implemented the user-supplied Adobe Stock Production Mode specification in the
existing repository plugin. The source plugin is now version **0.2.0**. Identity,
marketplace source/policy, product availability, plugin default prompt, and
skill default prompt remain unchanged. No installed cache was edited, no account
plugin was published, and no Adobe submission was made.

`WALLPAPER` retains existing visual defaults, device ratios, bounded native
delegation, and sequential vivo/reference-based iPad generation. `ADOBE_STOCK`
adds one independent commercial composition per selected concept. `BOTH` adds
a separate Stock composition to the requested wallpaper editions. Stock targets
approximately 12 MP, while readiness depends on measured final files and verified
rights rather than a target-resolution claim.

## Files changed or created

Under `plugins/fantasy-wallpaper-studio/`:

- Updated `plugin.json` to 0.2.0 and extended description/keywords.
- Updated `README.md` with modes, invocation, dependencies, validation, and limits.
- Updated `skills/fantasy-wallpaper/SKILL.md` for mode routing and Stock gates.
- Updated `skills/fantasy-wallpaper/agents/openai.yaml` discovery description.
- Extended `references/agent-roles.md`, `references/pair-production.md`, and
  `references/visual-brief.md` inside the skill without replacing pair behavior.
- Added skill references `stock-production.md`, `stock-compliance.md`,
  `stock-quality-review.md`, and `stock-metadata.md`.
- Added skill `scripts/validate_stock_asset.py` and `scripts/requirements.txt`.

Repository changes: updated root `README.md`, added
`tests/test_stock_validation.py`, and added this dated verification report.
The generated `dist/fantasy-wallpaper-studio-0.2.0.zip` is ignored by Git.
Pre-existing `.DS_Store` changes were not part of the implementation.

## Roles and invocation

Concept Curator gains buyer intent, commercial use, originality, and IP screening.
Pair Art Director adds a single-image Stock brief with buyer-oriented framing.
Visual Reviewer adds actual-image anatomy, construction, artifact, and commercial
quality checks. A fourth role, Stock Compliance and Metadata Specialist, handles
technical evidence, licensing/releases, current policy, and English metadata.
Four role types do not change the maximum of three active native children or a
lower host limit. The main agent alone generates/edits images and executes file
operations; children remain bounded and cannot recursively delegate or publish.

Invoke with `Create an original fantasy railway station illustration for Adobe
Stock.` or `mode=ADOBE_STOCK`. Request Vivo, iPad, and Adobe Stock together, or
specify `mode=BOTH`, for three separately composed editions. Existing wallpaper
requests still select `WALLPAPER`. English metadata accompanies Stock editions.

## Automated verification

Executed on Python **3.12.16**, Pillow **13.0.0**, using an isolated uv environment:

```bash
uv run --with 'Pillow>=10' python -m unittest discover -s tests -v
python3 scripts/validate_plugin.py --plugin-dir plugins/fantasy-wallpaper-studio --marketplace .agents/plugins/marketplace.json
python3 scripts/package_plugin.py --plugin-dir plugins/fantasy-wallpaper-studio --output-dir dist
python3 -m zipfile -t dist/fantasy-wallpaper-studio-0.2.0.zip
git diff --check
```

- **35 tests passed:** 21 existing authoring/archive tests and 14 new Stock
  tests. The initial Stock test run failed because the helper did not yet exist.
- Measured-file tests cover valid 4 MP JPEG, 1068 × 736 below-minimum output even
  with 1200 DPI, below-4 MP and above-100 MP boundaries, actual PNG disguised as
  JPEG, missing/broken ICC, forged sRGB description with altered color transform,
  CMYK, exact 45,000,000-byte acceptance and one-byte-over rejection, missing/
  directory/corrupt files, truncated JPEG decoding, JSON/exit behavior, absent
  Pillow, unavailable LittleCMS, and inaccessible ancestor-directory diagnostics.
- A LittleCMS-unavailable regression was observed raising `ImportError` before
  the fix. It now reports `UNVERIFIED` and `NOT_READY_TECHNICAL` without crashing.
- Actual repository plugin and marketplace validation passed.
- ZIP integrity passed. Independently extracted all **14 packaged files** into
  a temporary directory, validated the extracted plugin without the repository
  marketplace, and executed its bundled validator against a synthetic 4 MP
  sRGB JPEG. It returned technical `VERIFIED`, visual `NOT_INSPECTED`, and
  `PENDING_MANUAL_VERIFICATION`, never submission-ready.
- Whitespace checks passed.

Independent read-only review found no Critical/Important issue and one minor
permission-error edge: `Path.is_file()` was outside the error handler on supported
Python versions. Its new regression failed before the fix. The helper now checks
existence inside the guarded operation and reports failure without losing JSON.
The final suite includes this fix; no review finding remains deferred.

## Instruction-application acceptance scenarios

A fresh read-only native child first applied the original skill. It reported
that Stock routing, specifications, rights gating, metadata, and readiness were
absent. A different fresh child then read the updated skill/references and applied
the following simulated requests. No image generation or artistic inspection
occurred during these instruction simulations.

| Test | Observed simulated behavior | Evidence level |
| --- | --- | --- |
| A: Matching Vivo/iPad pair | `WALLPAPER`; two compositions; vivo first, actual reference for iPad; existing concept-selection gate retained | Instruction simulation passed; live generation not run |
| B: Original fantasy railway station for Adobe Stock | `ADOBE_STOCK`; one buyer-oriented composition; actual review/file validation, IP/rights, English metadata, readiness required | Instruction simulation passed; live production not run |
| C: 1068 × 736 output | Correctly computed 0.786048 MP; refused Stock-ready claim; `NOT_READY_TECHNICAL` | Instruction simulation and actual synthetic-file regression passed |
| D: Copyrighted anime character for Stock | Blocked protected identity; offered original adult character and distinct concept | Instruction simulation passed; no protected image generated |
| E: Vivo, iPad, and Stock | `BOTH`; three distinct compositions; preserved pair sequence and separate Stock checks | Instruction simulation passed; live triple generation not run |
| F: Filename without accessible image | `NOT_INSPECTED`; no fabricated `PASS`, defects, or dimensions | Instruction simulation passed |

Additional simulations covered unknown rights despite technical/visual success
(`PENDING_MANUAL_VERIFICATION`), preview-only access, and a host cap of two native
children. The preview test found a missing status definition. The guides now
explicitly use `access=PARTIAL` and `NOT_INSPECTED` for incomplete final-asset
review, with observed preview findings reported separately. A follow-up reran
preview/no-access/unknown-rights cases and found them consistent.

## Technical and operational limits

The validator is read-only. It checks actual JPEG/RGB encoding, full decoding,
pixels, bytes, and embedded ICC using profile parsing plus sampled sRGB transform
agreement. ICC verification is conservative, not exhaustive certification.
It cannot inspect artistic quality, identify all IP, establish originality,
clear licensing/releases, determine generator/upscale provenance, or validate
current policy automatically. A successful technical check remains pending.

Python 3.10+ and Pillow with LittleCMS are optional Stock-check dependencies;
authoring/package tools remain standard-library-only. Native subagents, image
generation/editing/reference support, high-quality JPEG export, and any safe
upscaler must come from the host. No exporter or upscaler is bundled. Unknown
rights remain `UNVERIFIED`; insufficient/inaccessible files remain non-ready.

Official Adobe technical, AI, metadata/category, and distinct-content sources
were opened during implementation and linked in the packaged guides. Future
production must refresh relevant policies, inspect final pixels, verify actual
tool/reference/contributor rights and applicable releases, and apply portal AI
and fictional-subject declarations. Adobe moderation remains external.

Real artwork generation, final-art visual review, host JPEG export/upscaling,
installed-plugin activation, account publication, and Adobe upload were not run.
Those are separate integration/manual checks; source tests and simulations do
not prove them.
