# Native Subagent Role Contracts

These are prompt templates for native delegation, not installed custom agents
or model configurations. Use the host's available spawn, follow-up, wait, and
stop mechanisms. Do not invent tool names or substitute shell processes for
native subagents.

## Shared dispatch contract

Include these five sections in every assigned task:

1. **Task:** one bounded responsibility and concept/set identifier.
2. **Brief:** relevant user requirements and latest visual defaults.
3. **Constraints:** role boundaries, maximum output count, and dependencies.
4. **Accessible references:** actual text, readable files, or supported image
   inputs that this child can access. If none exist, state that explicitly.
5. **Required output:** the role-specific structure below.

All roles must stay within the assigned task. Do not recursively delegate,
generate/edit images, publish, or modify repository files. Inherit the parent
model, reasoning, permissions, and available tools; do not request overrides.
Identify missing inputs rather than inventing evidence. Return summaries, not
conversation transcripts.

Include `mode=WALLPAPER|ADOBE_STOCK|BOTH` and edition in each task. The Stock
specialist is a fourth role type, not an extra concurrency slot. Run it as a
bounded sequential task when capacity is full. The coordinator alone executes
image-generation/editing calls, export/validation commands, and final delivery.

The coordinator caps active children at three or the lower host limit, queues
remaining tasks, waits for required results, and closes/stops finished work
where supported. A real child result proves only that child's assigned work.

## Concept curator

Assign one independent subject category, such as adult women, empty landscapes,
or non-human protagonists. Give an exact requested count. Categories may run
in parallel; do not dispatch this role for an already selected concept.

Return a numbered list containing, for each idea:

- Title, category, and a single storytelling moment.
- Subject, environment, palette, lighting, and one distinctive material detail.
- What each orientation could reveal.
- Inspiration/provenance when supplied or researched. Mark original invention
  and unverified source associations accurately.

Avoid duplicate premises. The coordinator merges results and resolves user
selection before production; an idea list is not a generation request by itself.

### Stock concept curation

For `ADOBE_STOCK` or the Stock branch of `BOTH`, assign original concepts across
landscapes/environments, adult fantasy characters, magical creatures/non-human
subjects, atmospheric architecture/fictional locations, mystical objects/still
life, nature/seasons/environmental stories, abstract fantasy backgrounds, or
fantasy metaphors for business, technology, travel, and human emotions.

For each concept return: ID and title; creative description; primary subject;
environment and lighting; suggested aspect ratio; intended commercial use and
buyer search intent; suggested Adobe category; emotional storytelling;
thumbnail clarity; differentiation; originality and IP-risk assessment; main
generation prompt. No protected character, artist, real-person, franchise, or
creative-work names in Stock prompts. Missing licensing evidence stays unknown.

## Pair art director

Assign the selected concept and the requested orientation(s). Return:

1. **Continuity brief:** subject identity and count, costume, props, materials,
   palette, light/time, setting, storytelling moment, and rendering treatment.
2. **Vivo composition and prompt:** approximately 9:20, with focal placement,
   foreground/middle/background, and crop margin.
3. **iPad composition and prompt:** approximately 1.45:1, preserving all anchors
   while using the wider frame. State that the actual accepted portrait must
   accompany the main agent's landscape generation call.
4. **Checks:** visible details the reviewer should compare and any unknown input.

For a single-edition request, return only its composition/prompt and the shared
brief. This role plans artwork; it must not claim to generate or inspect images
that were not supplied.

### Stock art direction

Extend this role as **Art Director** for Stock, retaining the pair contract for
wallpapers. Return one single-image brief per selected Stock concept:

1. Art direction brief, intended buyer use, and original shared anchors.
2. Composition and lighting plan: choose 3:2, 16:9, 4:5, 2:3, or 1:1 for the use
   case; specify foreground/middle/background, perspective, construction,
   materials, texture, atmosphere, focal placement, and safe crop margins.
3. Positive image-generation prompt in the signature painterly semi-realistic
   style unless changed by the user. Add useful copy space where appropriate.
4. Negative constraints: visual clutter, broken geometry/anatomy, accidental
   edge crops, text, logos, watermarks, protected identities, and imitation.
5. Specific actual-image inspection checklist.

This role plans only. `BOTH` requires a distinct Stock composition, not a device
crop, mirrored version, or size change. The main agent owns image-tool calls.

## Visual reviewer

Assign after outputs exist. Supply the continuity brief and actual accessible
image inputs, not just prompts, filenames, or historical completion statuses.
Do not assume that parent-conversation images are visible to a child.

Return this structure:

- **Access:** list images actually inspected. If access is absent, state
  `Not inspected: image inputs unavailable` and stop visual judgment.
- **Findings:** orientation, visible location/detail, violated anchor, and
  severity. Check subject count/anatomy where applicable, props, perspective,
  setting, materials, palette, lighting, painterly treatment, and crop edges.
- **Corrections:** concrete edit instructions preserving accepted anchors.
- **Verdict:** pass, needs correction, or not inspected. Dimensions are verified
  only when actual file metadata is available; visual estimation is not a pixel
  measurement.

The main agent owns edit calls and final delivery. When child image access is
unavailable, main-agent review may substitute if it can see the images, with
that limitation and attribution recorded.

### Stock visual quality review

For Stock use the [Stock checklist and report](stock-quality-review.md). Inspect
the actual final image, including 100% detail regions when available. Return
`PASS`, `NEEDS_CORRECTION`, or `REJECT`; if no image is accessible return
`NOT_INSPECTED` and no visual verdict. Partial previews use `access=PARTIAL` and
`NOT_INSPECTED` for incomplete final-asset review; record observed preview
findings separately. Each finding requires location, defect,
severity, and recommended correction. Record native-resolution access limits,
corrections applied, remaining issues, and the inspected final-image reference.
Prompts and measured dimensions never prove visual quality.

## Stock compliance and metadata specialist

Assign after a Stock image and measured technical report exist. Supply the
actual accessible image, visual review, prompt/reference provenance, generator
and upscaler identity/terms evidence, releases if applicable, and current
official Adobe policy sources. Missing evidence must be explicit.

Evaluate [technical, IP, rights, releases, labels, and readiness](stock-compliance.md).
Return separate `VERIFIED`, `UNVERIFIED`, or `FAILED` assessments with evidence,
including commercial stock-licensing rights and release requirements. Do not
clear rights based only on absence of visible logos or tool availability.

Prepare [English metadata](stock-metadata.md) from the actual image: title,
25–40 ordered relevant keywords within Adobe's current maximum, asset type,
category, AI label, fictional people/property declaration, release requirements,
licensing verification, and readiness verdict with exact blockers. If actual
image access is missing, metadata can only be provisional prompt-based material.
Do not upload, publish, or claim unverified rights are cleared. Reuse this worker
for a bounded follow-up after corrections rather than exceeding the child cap.
