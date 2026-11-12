# Adobe Stock Production

Load this guide with [roles](agent-roles.md), [compliance](stock-compliance.md),
[quality review](stock-quality-review.md), and [metadata](stock-metadata.md).
This is an additional production mode; [wallpaper production](pair-production.md)
keeps its existing sequence and defaults.

## Production sequence

1. **Concept selection.** For new ideas, delegate commercial concept curation.
   For an already selected original concept, skip ideation. An ideas-only request
   returns concepts; generation begins only when requested. Resolve protected
   identities with an original alternative before Stock generation.
2. **Art direction.** Delegate one Stock brief per concept. Choose 3:2 horizontal,
   16:9 panoramic, 4:5 portrait, 2:3 vertical, or 1:1 square for the buyer use.
   Retain painterly semi-realistic fantasy treatment. Define coherent spatial
   layers, lighting, materials, subject placement, crop margins, and useful copy
   space. Do not inherit device ratios automatically.
3. **Generate actual artwork.** The main agent calls available image tools using
   their documented arguments and any required host skill. Prefer native high
   resolution, targeting approximately 12 MP. A prompt is preparation, never an
   image output. Record each real tool result and accessible image reference.
4. **Visual review.** Supply actual output to the Visual Quality Reviewer. Apply
   focused edits for concrete defects and review the resulting image again.
   Retain accepted anchors; stop unproductive cosmetic loops and report residual
   defects. No image access means `NOT_INSPECTED`.
5. **Export and validate.** Inspect actual metadata, prepare a high-quality JPEG
   with embedded sRGB through supported tools, and validate the final file.
   Review the final encoded image, not only the earlier source. Keep originals;
   avoid repeated lossy encoding. Check compression, fine detail, and edges
   visually; the technical validator cannot score artistic quality.
6. **Compliance review.** Delegate the specialist to assess final pixels, prompt
   provenance, references, licensing terms, releases, labeling, and similarity.
   Refresh current official policy before a submission-readiness claim.
7. **Metadata.** Have the specialist prepare English metadata from the accepted
   final image. After edits, recheck all descriptions, declarations, and keywords.
8. **Deliver.** Provide the final artwork using the host's supported artifact
   mechanism plus the full contract below. Assign readiness from evidence and
   state every blocker. Never automatically upload or submit to Adobe Stock.

At most three active children, or the lower host limit, across all roles and
editions. Queue dependent work; close finished workers where supported. Children
must not recursively delegate, generate/edit images, modify repository files,
or publish. Native-agent failure retains the existing explicit fallback gate.

## Resolution and technical evidence

The production target is about 12 MP, not a promise about tool capabilities.
4000 × 3000 is a 12 MP arithmetic example, not the default aspect ratio. For a
3:2 brief, 4242 × 2828 is approximately 12 MP; choose native supported dimensions
near the intended ratio. Final acceptance uses measured pixels, not prompt text.
Never claim 4K, 8K, native resolution, or 12 MP without reading the actual file.
DPI metadata does not add pixels.

The bundled checker implements JPEG, RGB, embedded sRGB ICC, full decoding,
4–100 MP inclusive, and a conservative 45,000,000-byte limit. These limits follow
[Adobe's illustration specifications](https://helpx.adobe.com/stock/contributor/submit-your-content/submit-illustrations/technical-legal-requirements-illustration-submission.html),
checked on 12 November 2026. Recheck before submission if policy may have changed.

With local file access, Python 3.10+ and Pillow with LittleCMS are required for
the bundled [validator](../scripts/validate_stock_asset.py). Install dependencies
in a suitable isolated environment using [requirements](../scripts/requirements.txt).
From this skill directory, invoke:

```bash
python3 scripts/validate_stock_asset.py /actual/path/to/final.jpg
```

Use an actual existing output path, not the example path. The read-only command
prints JSON and exits 0 only for verified technical checks; it never returns
`READY_FOR_SUBMISSION`. Record its real output. It does not export, upscale,
perform visual inspection, clear rights, or inspect policy updates. ICC evidence
uses parsing, an sRGB description, and sampled color-transform agreement; it is
conservative, not exhaustive ICC certification. Unsupported profiles need a
trusted color-managed workflow, not a renamed label.

If local execution is unavailable, equivalent real metadata/decoder evidence
is acceptable. A preview, declared filename, RGB mode without an embedded ICC,
or inaccessible download cannot establish technical compliance. Mark missing
checks `UNVERIFIED` and use `NOT_READY_TECHNICAL` until measurements exist.

If resolution is insufficient:

1. Report actual dimensions and MP first (1068 × 736 = 0.786048 MP).
2. Prefer a higher native-resolution output. Otherwise discover an actual
   supported high-quality upscaler and check its commercial terms. This plugin
   does not bundle one. Do not invent an endpoint or silently use basic resize.
3. Record original dimensions, upscaler/tool and settings, final dimensions,
   and that the output was upscaled rather than natively generated at that size.
4. Inspect the actual upscaled final image at 100% for artificial texture,
   halos, repeated patterns, distortion, and loss of detail. Rerun file checks.
5. Without a supported successful recovery, use `NOT_READY_TECHNICAL`. A larger
   file with unresolved visual artifacts is still not submission-ready.

## BOTH and partial progress

Use shared original identity, materials, palette, atmosphere, and storytelling
anchors. Produce the requested wallpaper editions with the unchanged vivo-first,
actual-reference iPad sequence, then a separately composed commercial Stock
edition. Use accessible accepted images as continuity references when needed
and supported, with verified rights. A pair plus Stock means three separate
outputs. Do not copy, stretch, mirror, crop, or merely resize a wallpaper to
claim a new Stock composition. Device editions are personal wallpaper outputs,
not additional Stock submission candidates.

Track `concept / mode / edition / output reference / review / dimensions /
technical status / rights status / readiness`. Preserve completed wallpaper
outputs if Stock fails and completed Stock outputs if another requested item
fails. Report exact requested/completed counts and blocked dependencies. Every
edit, export, or upscale invalidates earlier file checks; revalidate and review
the final version. Tie reports to the exact inspected image reference.

## Required per-Stock-image delivery contract

All fields are required; unavailable values must be explicitly `unverified`,
`UNVERIFIED`, `NOT_INSPECTED`, or a reasoned not-applicable value, never invented.

| Section | Required fields |
| --- | --- |
| Asset | Concept ID; final accessible image reference; measured width and height; actual MP; format; exact bytes and MB; embedded color-profile evidence; generation status/tool and source dimensions; upscaling status/tool/settings and resulting dimensions |
| Visual review | Inspected reference and reviewer; access and resolution limits; `PASS`, `NEEDS_CORRECTION`, `REJECT`, or `NOT_INSPECTED`; location/defect/severity/correction findings; corrections applied; remaining issues |
| Adobe Stock metadata | English title; ordered English keywords and count; asset type; category; AI checkbox instruction; fictional people/property declaration; model/property release requirements |
| Compliance | Technical validation and evidence; visual quality evidence; IP-risk assessment; commercial stock-licensing verification; reference rights; release status; labeling/declaration checks; similarity assessment; official policy sources and check date |
| Readiness | One verdict from the compliance guide; exact reasons for every blocker; required manual steps; strongest candidate recommendation |

Use `READY_FOR_SUBMISSION`, `PENDING_MANUAL_VERIFICATION`, `NEEDS_CORRECTION`,
`NOT_READY_TECHNICAL`, or `BLOCKED_RIGHTS` under the decision rules. Readiness is
an evidence-backed preparation status, not a guarantee of Adobe acceptance.
