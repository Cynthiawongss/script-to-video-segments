# Script to Video Segments

English · [简体中文](README.zh-CN.md)

**Split approved scripts into generation-ready segments with dialogue coverage and continuity checks.**

![Script to Video Segments](assets/hero.png)

## What you receive

Integrated segment prompts, source dialogue mapping, opening and closing states, timing checks, and edit notes.

[Read the skill](skills/script-to-video-segments/SKILL.md) · [中文指令](skills/script-to-video-segments/SKILL.zh-CN.md)

## Try the example

The Last Label is a synthetic 30-second scene planned as three connected segments. Its 10-second cap is a planning assumption, not a vendor claim.

[Example notes](skills/script-to-video-segments/examples/the-last-label/script.md) · [Interactive example](skills/script-to-video-segments/examples/the-last-label/index.html) · [中文示例](skills/script-to-video-segments/examples/the-last-label/index.zh-CN.html)

Download the repository and open the example HTML in a browser. GitHub displays HTML source rather than running the example. Examples work offline and use synthetic material.

## Install

Give this URL to your GitHub-capable skill installer and install the complete skill folder:

```text
https://github.com/Cynthiawongss/script-to-video-segments/tree/main/skills/script-to-video-segments
```

Keep `references/`, `examples/`, and any `scripts/` and `agents/` subfolders together. `SKILL.md` is the default English entry; `SKILL.zh-CN.md` is its Chinese equivalent. The workflow follows the requested output language.

Alternatively, download an English or Chinese skill ZIP from the [v0.1.0 release](https://github.com/Cynthiawongss/script-to-video-segments/releases/tag/v0.1.0). Install one language variant.

## Example request

```text
Use $script-to-video-segments to split this approved script into generation segments. Preserve every line and integrate camera, action, dialogue, and sound on one timeline per segment.
```

## Verify

From the repository root:

```sh
python3 tools/build_examples.py
python3 -m unittest discover -s tests -v
```

See [validation scope and limits](validation/README.md) for browser checks. Python checkers require only Python 3.10+ and its standard library.

## Scope

This is a production plan, not rendered footage. Declared state checks cannot guarantee visual or voice continuity in generated video.

The cover illustrates continuity with a fictional character; it is not generated footage from the example.
