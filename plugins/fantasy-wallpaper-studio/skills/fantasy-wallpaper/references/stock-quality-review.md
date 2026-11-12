# Stock Actual-Image Quality Review

Assign this checklist to the Visual Quality Reviewer for Stock editions. Supply
the real final image in a child-supported form, its concept/brief, and any
earlier review/correction evidence. A filename, prompt, parent-only image,
historical manifest, or claimed completion does not grant image access.

## Access and resolution

List the actual accessible image reference(s) inspected. If none can be opened,
return `access=UNAVAILABLE`, `status=NOT_INSPECTED`, and the reason. Stop visual
judgment: do not return `PASS` or invent defects. Main-agent review may substitute
only if the main agent can actually inspect the image; record that attribution.
If nobody has access, readiness stays non-ready under the compliance rules.

Inspect full composition and thumbnail hierarchy, then 100% resolution when
available. Include important detailed regions: hands, face/eyes/ears, joints,
clothing/hair crossings, architecture/rail connections, reflections, textures,
and crop boundaries. Record which regions and resolution were available. A
downsampled preview cannot establish a full-resolution pass; record the partial
review with `access=PARTIAL`, `status=NOT_INSPECTED` for the incomplete final-asset
inspection, keep full-resolution review pending, and request final pixels. Record
any actually observed preview findings separately; do not invent a defect to
force `NEEDS_CORRECTION`.

## Inspection checklist

- **Human anatomy, when present:** appropriate visible finger count and natural
  structure, hand poses, plausible joints and limbs, consistent face, eye/ear
  placement, natural hair and clothing intersections. Account for occlusion;
  do not demand five visibly exposed fingers on a closed or hidden hand.
- **Environment:** coherent perspective, plausible architecture, rail/bridge/
  object connections, stable supports, placement and scale, consistent light
  direction, reflections, contact shadows, and physical construction.
- **AI artifacts:** duplicated/merged objects, distorted geometry, accidental
  text/symbols, blurry or melted detail, repeated texture artifacts, broken edge
  transitions, oversharpening, halos, compression, and upscale distortion.
- **Commercial presentation:** clear subject/hierarchy at thumbnail size,
  professional composition, consistent rendering, useful design space where
  appropriate, safe object margins, no unintended borders, signatures, logos,
  watermarks, or branding. Compare accessible submission candidates for meaningful
  differentiation; do not infer collection-wide uniqueness.

Distinguish deliberate painterly brushwork and fantasy invention from accidental
artifact or incoherent construction. Mark nonapplicable anatomy checks explicitly.
Do not claim file format, MP, ICC, or exact dimensions from visual estimation.

## Required review report

1. **Access:** actual image reference, reviewer, full-resolution/preview access,
   regions inspected, and limitations.
2. **Findings:** for every issue, location, observable defect, severity
   (`minor`, `major`, `critical`), and recommended targeted correction.
3. **Corrections:** requested edits, observed corrections actually applied, and
   accepted continuity anchors to preserve. Unknown edit history stays unknown.
4. **Remaining issues:** explicit unresolved findings and checks still unverified.
5. **Status:** `PASS`, `NEEDS_CORRECTION`, or `REJECT`. Use `NOT_INSPECTED` for
   missing image access or incomplete final-resolution inspection.
   Any unresolved visible defect requires correction;
   inaccessible detail checks remain pending even if the preview has no defects.

`PASS` requires actual inspection with no unresolved quality issue and adequate
detail access. `NEEDS_CORRECTION` means targeted edits can repair the image.
`REJECT` means severe, pervasive, or unrepairable defects require a fresh output
or concept. Every later export/upscale/edit requires review of that final output.
The coordinator owns all editing/generation and translates this visual result
into the overall [readiness verdict](stock-compliance.md).
