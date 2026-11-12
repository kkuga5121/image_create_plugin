---
name: "fantasy-wallpaper"
description: "Use when the user requests fantasy wallpaper ideas, concept expansion, vivo portrait or iPad landscape artwork, matching wallpaper pairs, Adobe Stock illustrations, commercial stock artwork, stock submission preparation, or revisions and visual reviews of those images, in Thai or English."
---

# Fantasy Wallpaper

Use real native subagents for bounded art tasks. The main agent owns generation,
references, verification, and delivery. Respond in the user's language.

## Route the request

Select the production mode before loading defaults:

| Mode | Trigger | Deliverables and references |
| --- | --- | --- |
| `WALLPAPER` | Default; wallpaper, vivo, iPad, matching pair | Existing requested device edition(s); use routing below |
| `ADOBE_STOCK` | Adobe Stock, stock illustrations, commercial stock artwork, stock submission; ภาพสต็อก, ขายบน Adobe Stock | One independently composed artwork per selected concept; load all four Stock guides below |
| `BOTH` | Wallpaper/device editions and Stock requested for the same concept | Separate requested device editions plus one Stock composition; preserve pair order and apply Stock checks only to Stock |

An explicit mode takes precedence. Conflicting explicit mode and requested
deliverables require clarification. Stock wording alone never requests a
wallpaper pair. Ideas, metadata-only work, and validation-only work do not
authorize unsolicited image generation. If the concept is already selected,
skip ideation in every mode.

| Request | Load | Delegate |
| --- | --- | --- |
| New ideas | Visual brief and role templates | Concept curators for independent categories |
| Existing concept or expansion | Brief, catalog if relevant, role templates | Pair art director; skip ideation |
| Create pair or single edition | Above plus production guide | Art director, then reviewer after generation |
| Revise or review existing images | Production guide and roles | Reviewer with actual accessible images |

References: [visual brief](references/visual-brief.md),
[catalog](references/concept-catalog.md), [roles](references/agent-roles.md),
[production](references/pair-production.md).

Stock references: [production and output contract](references/stock-production.md),
[compliance and readiness](references/stock-compliance.md),
[actual-image quality review](references/stock-quality-review.md),
[English metadata](references/stock-metadata.md).

## Capability and input gates

Check available native delegation tools and only the image capabilities needed
by this request. Ideas and prompt preparation need no image generator.
If native delegation is unavailable, report that the subagent workflow is
blocked. Offer a single-agent alternative and wait for the user's choice.
Missing generation tools permit clearly labeled preparation material, not a
claim of completed artwork.

Resolve catalog, concept, and requested orientations. Without an active set,
bare numbers require clarification. Historical completion is not current file
access. Request an accessible image when an old image is needed.

## Delegate and produce

Explicitly spawn native child agents using the role contracts. Provide task,
brief, constraints, accessible references, and required output. Use at most three
active children and honor lower host limits. Queue remaining work and wait for
dependent results. Children must not recursively delegate, generate images,
publish, or modify repository files.

For new ideas, delegate independent subject categories and combine results.
For a selected concept, delegate shared anchors and compositions to the art
director. Main-agent image calls remain sequential: generate and inspect vivo,
then supply that actual output as reference for a separate iPad composition.
Use approximately 9:20 portrait and 1.45:1 landscape; do not stretch one image
into the other. Single-edition requests produce only the requested orientation.

The preceding device sequence applies to `WALLPAPER` and the wallpaper branch
of `BOTH`. In `ADOBE_STOCK`, delegate a single-image Stock brief, then generate
the Stock composition using the [Stock workflow](references/stock-production.md).
Stock uses buyer-oriented ratios, not device ratios. In `BOTH`, complete the
unchanged requested wallpaper sequence, then generate a separate Stock edition
from shared original anchors. Delegate the Stock compliance/metadata specialist
after actual output evidence exists. Four role types do not allow four active
children: release finished workers or queue the specialist under the same cap.

Delegate visual review only with images the child can access. If access fails,
record that and inspect as the main agent when possible. Correct concrete
defects through the host's image-editing tools. Keep accepted references.

## Deliver with evidence

Report actual child activity, output count, visual-review status, and measured
dimensions or `unverified`. A pair needs two separate outputs; N pairs need 2N.
Identify failed items and reference limitations. Deliver images with concept and
orientation labels. Prompts and imagined reviews are not generated images or
observed checks. Compose full-frame artwork using the latest brief; superseded
clock and icon-space conventions do not override it.

For each Stock deliverable, use the full Stock output contract and a readiness
verdict with reasons. Run the bundled [read-only technical validator](scripts/validate_stock_asset.py)
when local Python/Pillow and the actual file are available, or record equivalent
measured evidence. Technical success alone never means `READY_FOR_SUBMISSION`.
Missing actual images mean `NOT_INSPECTED`; unknown rights remain `UNVERIFIED`.
Never automatically upload, submit, or publish Stock content.
