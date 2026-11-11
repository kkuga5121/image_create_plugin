# Fantasy Wallpaper Studio verification

Date: 11 November 2026, Asia/Bangkok.

## Scope

The [design](../design/2026-11-11-design-fantasy-wallpaper-plugin.md) and
[plan](../plan/2026-11-11-plan-fantasy-wallpaper-plugin.md) distinguish source
checks, observed native delegation, installed-plugin activation, and real image
creation. This record does not treat instruction review as live image testing.

## Skill baseline, before authoring

A fresh native child received the coastal-station pair request without the new
skill. It proposed portrait followed by reference-based landscape, but explicitly
said `ไม่แบ่งให้เอเจนต์ เพราะภาพ iPad ต้องอ้างอิงภาพ vivo` and added
`เหลือพื้นที่สำหรับไอคอน`. The missing delegation and stale icon-space default
are the baseline failures. The new workflow separates delegated planning/review
from main-agent sequential generation and uses the current full-frame brief.

## Manual acceptance scenarios

| ID | Scenario | Expected | Observation |
| --- | --- | --- | --- |
| S1 | Six ideas across women, scenes, animals | Real bounded native delegation; six ideas; no images | Not run |
| S2 | Bare `ข้อ 4 แบบคู่`, no active set | Clarify catalog before generation | Not run |
| S3 | `latest-18 / 9` pair; missing portrait reference or landscape failure | Portrait precedes reference-based landscape; report incomplete dependency | Not run |
| S4 | Reviewer lacks image access; metadata unavailable | No invented visual findings or dimensions; attribute main-agent review | Not run |
| S5 | Delegation or generation tools absent | Report blocked capability; do not silently fall back | Not run |
| S6 | Two pairs with one landscape failure | Account for four outputs and label partial results | Not run |
| S7 | Lighting revision of an accepted pair | Preserve references, edit and review; skip ideation | Not run |

## Verification results

- Metadata parsing: initial manifests and JSON-compatible YAML parsed successfully.
- Automated validator and archive tests: Not run.
- Packaged-role native delegation: Not run.
- Target-client installation/activation: Not run.
- Actual image creation/editing, dimension measurement, and device testing: Not run.
- Remote source delivery: Pending.
