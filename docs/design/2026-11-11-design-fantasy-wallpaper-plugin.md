# Fantasy Wallpaper Studio plugin design

Date: 11 November 2026, Asia/Bangkok.

Status: Proposed design; awaiting approval before implementation.

## Purpose and source

Create a reusable plugin for the wallpaper workflow recorded in
[the source session summary](../wallpaper-project-summary.md). The plugin should
help users explore ideas, create matching vivo and iPad wallpapers, and review
the resulting artwork. Its instructions explicitly delegate bounded tasks to
native subagents.

The user selected a skills-based plugin for Codex and ChatGPT Work. They
authorized delivery to the existing Git repository on `main`:
`https://github.com/kkuga5121/image_create_plugin.git`.

The plugin uses the tools and permissions available in its host. It does not
provide its own image model, agent runtime, hosted service, or API credentials.

## Approaches considered

1. **Skills with native subagents — selected by the user.** Package the workflow,
   visual brief, catalogs, and delegation instructions. This uses the host's
   existing image and subagent capabilities without another server. Availability
   depends on the host and account.
2. **MCP service with API-backed agents — not selected.** A separate service could
   manage agents and image generation, but would require hosting, authentication,
   credentials, and operational work beyond the selected scope.

## Proposed structure

Use `fantasy-wallpaper-studio` as the plugin identity and **Fantasy Wallpaper
Studio** as its display name. These names are implementation proposals.

```text
.agents/plugins/marketplace.json
plugins/fantasy-wallpaper-studio/
  plugin.json
  README.md
  skills/fantasy-wallpaper/
    SKILL.md
    agents/openai.yaml
    references/
      visual-brief.md
      concept-catalog.md
      agent-roles.md
      pair-production.md
scripts/
  validate_plugin.py
  package_plugin.py
```

The portable manifest uses the Agent Plugins 1.0 schema. The repository
marketplace points to the plugin directory. The optional skill metadata declares
compatibility with `CODEX` and `CHAT`; it does not create a separate agent runtime.
A legacy manifest is unnecessary unless target-client verification demonstrates
that it is needed. No MCP configuration or app dependency is required.

The installable package contains only the self-contained plugin directory.
Repository development documents, private image links, generated pictures, and
build artifacts do not become plugin dependencies. Packaging scripts write the
archive outside the plugin directory. Generated archives are ignored by Git.

## User-facing behavior

The skill recognizes Thai or English requests for fantasy wallpaper ideas,
expanding an existing idea, making vivo or iPad artwork, producing matching pairs,
and revising or reviewing a pair. It responds in the user's language.

The latest brief overrides historical experiments. Defaults are painterly,
semi-realistic fantasy concept art throughout both subject and environment,
controlled oil/gouache brushwork, deliberate materials and lighting, and
atmospheric depth. Anime cel shading is historical context, not the default.

Support adult female human subjects, landscapes without people, animals,
spirits, robots, and expressive objects. Compose across the full frame. Do not
reinstate the superseded clock-space or Depth Effect requirements. Deliver
artwork without UI, text, logos, or watermarks.

Maintain the latest 18 concepts and the earlier 12- and 10-concept catalogs with
explicit set names. Historical generation status means only that the session
summary recorded it; it is not proof that those files are accessible now.
Resolve names and set-qualified numbers before generation. For bare numbers
without an active set, ask which set the user means.

Inspiration titles describe provenance and broad ideas. Invent the requested
scene rather than presenting invented events as facts from those works. Use
research tools when the user requests source research or factual verification.

## Delegation and ownership

The main agent owns the user's request, shared brief, image generation calls,
reference selection, final checks, and delivery. It uses native delegation
tools exposed by the current host rather than hardcoded tool names or shell
commands. All child agents inherit the host's available permissions and tools.

The role prompts are supporting Markdown references, not automatically registered
custom-agent definitions. They work as task instructions in both target hosts.

| Role | Assigned task | Required return |
| --- | --- | --- |
| Concept curator | For an ideation request, explore one bounded subject category. Independent categories may run in parallel. | Original scene ideas, storytelling moment, palette, category, and source provenance when applicable. |
| Pair art director | For a selected concept, define shared visual anchors and two compositions. | One continuity brief plus portrait and landscape generation prompts. |
| Visual reviewer | After the two outputs exist, compare actual images with the continuity brief. | Concrete defects, image evidence, and proposed corrections, or an explicit statement that images could not be inspected. |

Use no more than three active child agents, and respect any lower host limit.
Queue work if necessary. Do not let child agents recursively delegate, publish,
modify the repository, or generate images independently. Wait for required
results before the dependent step. Do not spawn ideation agents for a request
that already specifies the concept.

Give each child the relevant brief, requested output, constraints, and accessible
references. Do not assume child agents can see private library URLs or the
parent's conversation images. If actual image access cannot be passed to a
reviewer, the main agent performs the visual check if possible and accurately
records that limitation.

If native delegation is unavailable, report that the requested subagent workflow
is blocked. Offer a single-agent alternative without claiming that delegation
occurred; use it only if the user chooses it. If image generation is unavailable,
provide clearly labeled preparation material and report generation as blocked.
Never describe prompts, roleplay, or a source-session status as newly generated
images or actual child-agent execution.

## Pair production

1. Resolve the selected concept and record one storytelling moment. Obtain the
   art director's shared identity, costume, props, materials, palette, lighting,
   time, environment, and rendering treatment.
2. Generate the vivo portrait first. Target approximately `9:20`, with breathing
   room around important objects. This is a composition target, not a promise
   that the image tool supports an exact pixel size.
3. Inspect the returned image. Use the actual vivo output as a visual reference
   for a separate iPad landscape image, targeting approximately `1.45:1`.
   Recompose the scene for the wider frame rather than stretching the portrait.
4. Preserve the same protagonist, scene, event, costume, props, palette,
   materials, time, and painting treatment. Do not generate both orientations
   independently from text and claim reference-based continuity.
5. Review anatomy where applicable, subject count, props, perspective, scene
   continuity, visual style, and important objects near the edges. Apply focused
   corrections through the host's image-editing tools when needed. Keep any
   accepted reference image available throughout revisions.
6. Verify that there are two separate image outputs per selected concept.
   Inspect actual dimensions using available file or image metadata tools. If
   dimensions cannot be measured, mark them unverified. Report ratio deviations
   and possible crop effects without silently changing or distorting artwork.
7. Deliver both images with clear concept and orientation labels. State any
   remaining defect or tool limitation. Do not claim native screen resolution or
   device testing from the historical summary's dimensions.

Generate sequentially within a pair so the portrait reference exists before the
landscape call. A batch of N concepts requires 2N outputs. Track progress by set,
concept, orientation, and review status; do not silently omit failed items.

On tools with conversation-image references but no local paths, use their
documented reference mechanism. If the portrait cannot be supplied to the next
call, report the reference limitation instead of claiming it was supplied.

## Distribution and verification

Include repository installation instructions and representative Thai commands.
Document that desktop/repository marketplace installation differs from account
import and public directory publication. Git delivery does not prove that the
plugin is installed or that an account supports native subagents.

Verification must cover manifest and metadata parsing, contained references,
marketplace paths, archive contents, and the absence of private source-library
URLs in the package. Run a native subagent smoke check against the packaged role
instructions if the current environment permits it. Record static checks,
observed delegation, image-generation checks, and host installation separately.

Do not generate wallpapers merely to validate packaging. Full image creation and
installation in each target client remain explicitly unverified unless actually
performed. Include manual acceptance scenarios for idea selection, ambiguous
numbers, reference-dependent pairs, unavailable tools, and partial batches.

After approval and implementation, validate the final artifact, commit the
plugin source and supporting files, and push to `origin/main`. Do not force-push,
overwrite remote work, install into the user's account, or publish a public
directory listing as part of this Git-only delivery.

## Acceptance criteria

- The plugin and repository marketplace parse and resolve to a usable skill.
- The package works without files outside its own directory.
- The skill explicitly requests real native delegation with bounded role tasks.
- The latest session brief and distinct concept numbering survive packaging.
- Pair production preserves the portrait-reference dependency and requires two
  independently deliverable files, with honest verification status.
- Missing capabilities and inaccessible historical images are handled explicitly.
- README and validation results distinguish source delivery from installed and
  end-to-end verified behavior.
- The final source commit is present on the existing remote's `main` branch.

## Decisions left to the builder

Exact wording, file organization within the listed references, archive naming,
and dependency-free validation implementation are routine builder decisions.
Do not add a service, API credentials, model override, custom agent installation,
or client configuration changes without a new requirement.

## References

- [OpenAI: Package your plugin](https://developers.openai.com/plugins/build/plugins)
- [OpenAI: Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)

The accompanying [workflow diagram](../diagram/2026-11-11-design-fantasy-wallpaper-plugin.puml)
shows the dependency between planning, generation, and review.
