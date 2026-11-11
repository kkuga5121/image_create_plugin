# Fantasy Wallpaper Studio

A skills-only plugin for Codex and ChatGPT Work. It turns the recorded wallpaper
workflow into reusable instructions for original fantasy ideas, image production,
and matching vivo/iPad pairs.

## Requirements

Use a host/account that exposes native subagents. Image creation and editing also
require the host's image tools and a supported way to supply image references.
An ideas-only request does not require image generation. The plugin supplies
instructions, not its own model, server, tools, or API credentials.

The main agent generates the portrait, supplies that actual image to the
landscape call, and delivers two separate outputs. Child agents handle ideation,
art direction, and review. Targets are approximately 9:20 and 1.45:1; exact output
dimensions depend on the tool and must be measured rather than assumed.

## Usage

Select this plugin in your host's plugin picker, or invoke its skill where
supported. The skill is [fantasy-wallpaper](skills/fantasy-wallpaper/SKILL.md).

- `คิดไอเดียใหม่ 6 แบบ แบ่งหญิง ฉาก และสัตว์ โดยใช้ subagent`
- `ขยายไอเดียชุด 18 แบบ ข้อ 1, 3, 7`
- `ทำชุด 18 แบบ ข้อ 9 แบบคู่ vivo + iPad`
- `ทำสถานีปลายรางที่ทะเลมาถึงเป็นกลางคืน แบบคู่`
- `ปรับแสงภาพคู่นี้ให้นุ่มขึ้น โดยคงตัวเอกและฉากเดิม`

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
