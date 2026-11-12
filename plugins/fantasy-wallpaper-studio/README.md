# Fantasy Wallpaper Studio

A skills-only plugin for Codex and ChatGPT Work. It turns the recorded wallpaper
workflow into reusable instructions for original fantasy ideas, matching
vivo/iPad pairs, and Adobe Stock production preparation. Version 0.2.0 adds
Stock workflows without replacing Wallpaper Mode.

## Requirements

Use a host/account that exposes native subagents. Image creation and editing also
require the host's image tools and a supported way to supply image references.
An ideas-only request does not require image generation. The plugin supplies
instructions, not its own model, server, tools, or API credentials.

The main agent generates the portrait, supplies that actual image to the
landscape call, and delivers two separate outputs. Child agents handle ideation,
art direction, and review. Targets are approximately 9:20 and 1.45:1; exact output
dimensions depend on the tool and must be measured rather than assumed.

## Production modes

| Mode | Result |
| --- | --- |
| `WALLPAPER` | Existing device compositions, pair continuity, visual defaults, and sequential reference workflow |
| `ADOBE_STOCK` | One original commercial composition per selected concept; actual-image review, file validation, rights assessment, English metadata, and readiness verdict |
| `BOTH` | Requested wallpaper editions plus a separately composed Stock edition sharing an original creative identity |

Stock wording automatically routes to Stock Mode. A request mentioning device
editions and Stock selects `BOTH`. An explicit mode takes precedence; conflicting
instructions are clarified. Stock art keeps painterly semi-realistic fantasy
direction, with 3:2, 16:9, 4:5, 2:3, or 1:1 framing chosen for buyer use.

Concept Curator gains commercial ideation and IP screening. Pair Art Director
adds single-image Stock direction. Visual Reviewer gains detailed actual-image
Stock checks. A fourth role, Stock Compliance and Metadata Specialist, assesses
rights, releases, policy, and metadata. The existing maximum remains three active
children, or fewer if the host requires it; all image calls remain with the main
agent. The specialist queues behind dependent work.

## Usage

Select this plugin in your host's plugin picker, or invoke its skill where
supported. The skill is [fantasy-wallpaper](skills/fantasy-wallpaper/SKILL.md).

- `คิดไอเดียใหม่ 6 แบบ แบ่งหญิง ฉาก และสัตว์ โดยใช้ subagent`
- `ขยายไอเดียชุด 18 แบบ ข้อ 1, 3, 7`
- `ทำชุด 18 แบบ ข้อ 9 แบบคู่ vivo + iPad`
- `ทำสถานีปลายรางที่ทะเลมาถึงเป็นกลางคืน แบบคู่`
- `ปรับแสงภาพคู่นี้ให้นุ่มขึ้น โดยคงตัวเอกและฉากเดิม`
- `Create an original fantasy railway station illustration for Adobe Stock.`
- `Create the same original fantasy concept for Vivo, iPad, and Adobe Stock.`
- `สร้างภาพสถานีรถไฟแฟนตาซีต้นฉบับเพื่อขายบน Adobe Stock`

You can also specify `mode=ADOBE_STOCK` or `mode=BOTH`. English Stock titles and
25–40 relevant ordered keywords accompany accepted Stock artwork even when the
conversation is Thai. The complete [Stock workflow and delivery contract](skills/fantasy-wallpaper/references/stock-production.md)
defines the required asset, visual review, metadata, compliance, and readiness fields.

The named catalogs are `latest-18`, `japan-12`, and `fantasy-10`. A bare number
without an active set requires clarification. Recorded historical images are
not bundled; supply an accessible image when you want to edit or use one.

## Installation and verification

For repository distribution, register the repository marketplace in a supported
Codex CLI:

```bash
codex plugin marketplace add kkuga5121/image_create_plugin --ref main
```

Then use the supported client plugin install/refresh flow and select **Fantasy
Wallpaper Plugins**. A local checkout exposes its repository marketplace to
supported desktop clients. Registration alone does not prove installation.

Account import is a separate host-supported workflow using a plugin archive.
Public directory publication requires a separate submission. Neither occurs by
pushing this repository. Local source access does not imply availability in a
web chat. See [OpenAI packaging guidance](https://developers.openai.com/plugins/build/plugins)
and [native subagent availability](https://learn.chatgpt.com/docs/agent-configuration/subagents).

If a required tool is unavailable, the skill reports that limitation. It does
not silently pretend to delegate or label prompts as generated images.

Source validation, observed role delegation, installed-plugin activation, and
real image generation are separate checks. Consult the repository's verification
record for what was actually tested; packaging alone proves none of the latter
three behaviors.

## Stock validation and limits

The read-only bundled validator needs Python 3.10+ and Pillow with LittleCMS.
The authoring/package tools still use only the Python standard library. From
this plugin directory, in an isolated environment with Python available:

```bash
python3 -m pip install -r skills/fantasy-wallpaper/scripts/requirements.txt
python3 skills/fantasy-wallpaper/scripts/validate_stock_asset.py /actual/path/to/final.jpg
```

Replace the sample path with the real generated final file. The command measures
actual JPEG format, RGB mode, embedded sRGB ICC, full decode, dimensions, MP, and
bytes. It uses 4–100 MP and a conservative 45,000,000-byte ceiling. ICC matching
is conservative and uses a sampled transform; unsupported profiles need trusted
color-managed verification. Exit 0 means technical checks passed only.

The native generation target is approximately 12 MP; actual tool limits may be
lower. No upscaler or JPEG exporter is bundled. Supported host workflows must
produce and inspect any conversion/upscale, then rerun validation. Without an
adequate actual file, report `NOT_READY_TECHNICAL`; DPI changes do not add pixels.

Readiness values are `READY_FOR_SUBMISSION`, `PENDING_MANUAL_VERIFICATION`,
`NEEDS_CORRECTION`, `NOT_READY_TECHNICAL`, and `BLOCKED_RIGHTS`. Actual visual
inspection and commercial stock-licensing/reference/release evidence remain
required; the script cannot clear them. Missing image access is `NOT_INSPECTED`.
Unknown rights stay `UNVERIFIED`. Contributors must verify their terms/releases
and apply the required AI/fictional-subject declarations in the portal. Current
policy review and Adobe moderation remain external checks. No automatic upload
or submission occurs. See [compliance sources and decision rules](skills/fantasy-wallpaper/references/stock-compliance.md).
