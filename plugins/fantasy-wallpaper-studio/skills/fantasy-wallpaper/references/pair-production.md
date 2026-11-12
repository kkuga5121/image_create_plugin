# Reference-Based Wallpaper Production

This guide governs `WALLPAPER` and the wallpaper branch of `BOTH`. Its device
ratios, reference dependency, generation order, and failure accounting remain
unchanged. For Stock-only production use [Stock production](stock-production.md).
`BOTH` adds a separately composed Stock artwork after the requested wallpaper
editions; it never turns the wallpaper landscape into a Stock export by resizing.

## Before generation

Resolve concept/set, orientations, and the latest [visual brief](visual-brief.md).
Use [native role contracts](agent-roles.md) for art direction. One named concept
does not need new ideation or another approval unless an outcome-changing input
is missing. Keep the selected moment and all continuity anchors in a short
working brief. Follow host tool documentation, including reference formats and
any required image-generation skill, rather than guessing arguments.

## Sequential pair workflow

1. Delegate the continuity brief and both compositions to the art director;
   wait for its result. Inspect any user-supplied reference before editing it.
2. The main agent generates one standalone full-bleed vivo portrait, targeting
   approximately 9:20. Inspect the actual output and correct major defects
   before treating it as the accepted reference.
3. Supply that actual accepted portrait to the host's image-generation/editing
   tool for a separate iPad landscape, targeting approximately 1.45:1. Preserve
   the brief's identity, scene, moment, wardrobe, props, materials, palette,
   light/time, and painting treatment. Recompose for width; do not stretch.
4. For a local-file reference, verify the path is readable and pass it through
   the tool's documented reference argument. For conversation-only images, use
   its supported conversation-reference mechanism. Include the smallest set
   containing every required reference. Do not assume a file link alone causes
   the tool to consume it. If the portrait cannot be supplied, report that
   dependency as blocked; do not silently proceed with an independent text call.
5. Delegate visual review with the actual outputs when child image access is
   supported. Otherwise record the access limit and review as the main agent
   when possible. Prompts are not evidence that output anatomy or props are
   correct. Follow the host's image-editing workflow for focused corrections.
6. Recheck affected anchors after edits. If the accepted portrait changes,
   check whether the landscape is now stale and update it using the accepted
   reference. Do not run an open-ended cosmetic revision loop; report unresolved
   defects or ask about a meaningful visual choice when needed.
7. Verify two distinct outputs exist. Read actual width/height from accessible
   file metadata; otherwise mark dimensions unverified. Portrait ratio is
   width/height, approximately 0.45; landscape is approximately 1.45. Report
   measured values and deviations without promising exact device support,
   silently cropping, or upscaling and calling it native resolution.
8. Deliver both images, labeled by concept and orientation, using the host's
   supported image/artifact output mechanism. Report concrete residual defects,
   unverified dimensions, and who performed review.

## Single orientations and revisions

Generate only the requested edition when the user requests a single wallpaper.
If asked to make an iPad companion to an existing vivo image, first obtain that
actual image, inspect it, and use it as the reference. A landscape-only new scene
does not require generating an unsolicited portrait.

For revisions, load the accepted accessible image(s), preserve unchanged anchors,
and edit through host image tools. Delegate review rather than repeating ideation.
Explain which partner needs a matching update when a continuity anchor changes.

## Batch progress and failure accounting

Track `set / concept / orientation / output reference / review / dimensions`.
For N requested pairs, account for all 2N image outputs. Schedule native children
within the concurrency cap; image calls inside each pair remain sequential.
Do not lose the portrait reference among unrelated conversation images.

If a call fails, retain successful outputs and identify the missing orientation.
Do not relabel a single file, montage, planned prompt, or historical image as a
completed pair. Do not fabricate attachment links. Continue independent requested
items when possible and report partial results. Native delegation failure is
not permission to silently roleplay the children: offer single-agent work and
wait for the user's choice.

## Example continuity prompt

For `latest-18 / 9`, keep an empty seaside station at dawn, rails gradually
submerged in clear seawater, a wooden bench, one steaming coffee, weathered
materials, warm early light, and painterly atmospheric depth. The landscape
opens the coastline around the same station and event using the actual portrait
as reference. No people, lettering, interface, logo, or watermark.
