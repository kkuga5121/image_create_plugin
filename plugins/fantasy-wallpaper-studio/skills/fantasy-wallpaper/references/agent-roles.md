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
