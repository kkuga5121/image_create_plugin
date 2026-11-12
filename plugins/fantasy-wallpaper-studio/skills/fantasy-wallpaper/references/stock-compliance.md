# Stock Compliance and Readiness

Record each check as `VERIFIED`, `UNVERIFIED`, or `FAILED`, with evidence and an
exact blocker. `VERIFIED` means evidence was actually examined. No known issue
is not verified permission. Unknown tool terms, reference rights, or releases
must stay `UNVERIFIED`; never automatically pass them.

## Policy sources

Official sources checked on **12 November 2026, Asia/Bangkok**:

- [Generative AI guidelines](https://helpx.adobe.com/stock/contributor/submit-your-content/submit-generative-ai-content/generative-ai-content-guidelines.html): tool rights, prohibited prompts, labels, releases, and asset classification.
- [Illustration requirements](https://helpx.adobe.com/stock/contributor/submit-your-content/submit-illustrations/technical-legal-requirements-illustration-submission.html): technical and legal requirements.
- [AI illustration guidelines](https://helpx.adobe.com/stock/contributor/submit-your-content/submit-generative-ai-content/generative-ai-illustrations-submission-guidelines.html): image quality and originality.
- [Distinct AI submissions](https://helpx.adobe.com/stock/contributor/submit-your-content/submit-generative-ai-content/distinct-generative-ai-submission-best-practices.html): similarity and selective curation.

Reopen relevant official documentation for each Stock production/submission
review when requirements may have changed. Record URLs, actual date checked,
applicable rules, and any conflict with this snapshot. Prefer current official
policy over a permissive old snapshot. If unavailable, explain that policy
verification remains pending; do not imply a current check occurred.

## Evidence checklist

1. **Origin and references:** record independent creation and every supplied
   image/reference, source, license, and permission for this use. Historical
   wallpaper inspiration and unknown web images are not automatically cleared.
2. **Generator and upscaler terms:** verify the actual provider, tool/model,
   account tier where relevant, current terms, and whether commercial stock
   licensing is allowed. Record the terms URL/document and applicability.
   Availability of an image tool or general commercial use language alone does
   not establish all contributor rights. Contributor evidence may be necessary.
3. **IP and identity:** inspect prompts and actual pixels for protected
   characters, distinctive franchise designs, logos, brands, signatures,
   artwork, and recognizable people or property. A Stock request for a
   copyrighted anime character must receive an original alternative, not a
   reproduction or a lightly renamed lookalike. Review that alternative again.
4. **People/property and releases:** record whether subjects are fully invented,
   based on real references, recognizable, or uncertain. A real identifiable
   person or recognizable protected real property requires the applicable
   clearance/release and current restrictions check. Record reviewed evidence
   or pending requirements. Do not invent a release or mark unknowns exempt.
5. **Declarations:** instruct the Contributor to select `Created using
   generative AI tools` for fully AI-generated assets. Select `People and
   Property are fictional` when fictional people or fictional property are
   actually present. Do not apply it as a blanket waiver for real subjects.
   Record the recommended selection and rationale; the user must perform it
   in the portal. Preparation readiness may include these explicit portal steps;
   never claim the checkboxes were already selected without observed evidence.
6. **Classification and accuracy:** default painterly fantasy art to
   `Illustrations`. Consider `Photos` only for camera-like realism of subjects
   that could exist in real life. A photorealistically rendered impossible
   fantasy scene remains an illustration. Never imply fictional people are
   real individuals or that invented scenes document news. No illustrative
   editorial classification for generative AI content.
7. **Final file and quality:** require measured final-file technical evidence
   and actual-image visual review. Review exports/upscales again. Check metadata
   against the final image; prompts alone cannot certify quality or content.
8. **Distinctiveness:** compare accessible candidates and known prior outputs.
   Record what was compared and collection-wide search limits; do not claim
   exhaustive uniqueness. Only recommend a differentiated, commercially useful
   strongest candidate. Escalate unresolved similarity for manual review.

For each rights/release check, return status, supporting source, applicable
subject/tool/reference, evidence reviewed, and unresolved action. Verified
not-applicable releases require a reason (for example, independently invented
scene with no real-person/property basis); absence of evidence is not that reason.

## Quality over quantity

Maintain a conservative internal ceiling of three potential candidates per
similar concept, subject to stricter current Adobe rules. This is not an Adobe
entitlement or a recommendation to submit all three. Current AI guidance rejects
multiple versions from the same or similar prompt. Select the strongest image;
retain others privately unless they add clearly different commercial value.
Color changes, mirroring, filters, simple crops, and ratio changes alone do not
create distinct submissions. Diversify subject, environment, concept, buyer use,
and composition; never generate large batches solely for upload volume.

## Readiness decision, in priority order

Report all blockers even when one higher-priority verdict applies.

| Verdict | Required decision rule |
| --- | --- |
| `BLOCKED_RIGHTS` | A known failed rights/IP/release check or prohibited reference/identity prevents commercial licensing. Stop that Stock branch and offer an original cleared alternative. Unknown rights alone are not a known failure. |
| `NOT_READY_TECHNICAL` | Final file missing/inaccessible, decoding failed, any required format/pixel/size/profile check failed or remains unverified, or no supported successful resolution recovery exists. |
| `NEEDS_CORRECTION` | Actual-image review finds fixable defects or `REJECT`, metadata/declarations are wrong, or known similarity/other correctable compliance failures remain. Explain whether editing or a new concept is needed. |
| `PENDING_MANUAL_VERIFICATION` | No known blocking failure remains, but rights, releases, current policy, visual inspection, or other required evidence is still unverified. `NOT_INSPECTED` can never yield ready. |
| `READY_FOR_SUBMISSION` | All required final-file checks verified, actual final-image visual review is `PASS`, metadata and declaration instructions are accurate, IP/licensing/reference rights and necessary releases are verified or justified not applicable, and current policy/similarity review has no unresolved blocker. |

The bundled technical validator is deliberately limited to technical evidence.
Even its successful result remains `PENDING_MANUAL_VERIFICATION` until the other
checks are completed. Only the main agent can combine all verified evidence into
the final readiness report. Do not upload, publish, or guarantee moderation approval.
