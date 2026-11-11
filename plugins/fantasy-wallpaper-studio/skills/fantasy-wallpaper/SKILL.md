---
name: "fantasy-wallpaper"
description: "Use when the user requests fantasy wallpaper ideas, concept expansion, vivo portrait or iPad landscape artwork, matching wallpaper pairs, or revisions and visual reviews of those images, in Thai or English."
---

# Fantasy Wallpaper

Use real native subagents for bounded art tasks. The main agent owns generation,
references, verification, and delivery. Respond in the user's language.

## Route the request

| Request | Load | Delegate |
| --- | --- | --- |
| New ideas | Visual brief and role templates | Concept curators for independent categories |
| Existing concept or expansion | Brief, catalog if relevant, role templates | Pair art director; skip ideation |
| Create pair or single edition | Above plus production guide | Art director, then reviewer after generation |
| Revise or review existing images | Production guide and roles | Reviewer with actual accessible images |

References: [visual brief](references/visual-brief.md),
[catalog](references/concept-catalog.md), [roles](references/agent-roles.md),
[production](references/pair-production.md).

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
