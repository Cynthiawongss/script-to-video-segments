---
name: script-to-video-segments
description: Convert an approved script into independently generatable video segments with integrated camera/action/dialogue timelines, source-line coverage, and explicit continuity states. Use for splitting or revising a script under generation limits; the output is a production plan, not a new plot or automatically verified footage.
---

# Script to Video Segments

Preserve the approved story while making each generation unit usable on its own. A shot is a camera view; a segment is one generation job. A segment can contain multiple shots when the chosen tool and brief support them. Use the requested language; do not translate approved dialogue without permission.

## 1. Establish the source and real constraints

Read the approved script, corrections, and available references. Record fixed character identities, names, wardrobe, scene layout, significant props, screen direction, and sound requirements. Keep a past project's lens, genre, language, and cut density out of universal rules.

Get target duration and tool limits from supplied constraints or current official documentation. If unavailable, mark a provisional planning cap rather than claiming model support. Confirm from the request whether the output is a plan, prompts, or generated clips.

Assign stable IDs to source dialogue in order. Keep exact wording. If a line must span segments, split at a natural phrase boundary, preserve its parent ID and ordered parts in the source map, and verify that joining them reconstructs the approved line. Do not speed up speech, translate, cut words, or change the target silently.

## 2. Build one timeline per segment

Choose boundaries where an action, gaze, prop, or sound can carry the edit. Avoid cutting a sentence or essential action merely to fill equal-length blocks.

| Part | Include |
|---|---|
| Opening | People, positions, held objects, prop and screen states |
| Locks and references | Applicable character/setting/style descriptions and actual reference assets |
| Local timeline, starting at 0 | Camera/framing, action, dialogue and sound together in each interval |
| Closing | State the next segment must inherit |
| Edit or bridge | Matching action/sound, or an explicit time/scene change |

Do not maintain a competing camera schedule. A copyable prompt must expand the needed shared locks or provide an explicit assembly step. An unresolved reference ID is not an attached asset. The bundled text-only example does not exercise image-reference upload.

## 3. Track continuity as state

Continuous neighboring segments inherit closing state exactly. An intentional time jump, scene change or transformation needs a stated bridge and updated state. Check that the described action can actually produce each declared state; matching JSON values alone do not establish that.

When generating sequentially, use the accepted take as the next reference where the tool supports it. If a take deviates, repair it or propose the downstream story change for approval. Do not claim a text prompt guarantees consistent footage.

For a correction, find every affected lock, source line, beat, and neighboring boundary. Update downstream dependencies until the prior state is restored, then check coverage and boundaries again. Do not update one prompt while leaving the others contradictory.

## 4. Check structure and timing

For structured plans, read [segment-contract.md](references/segment-contract.md). From this skill's directory, using Python 3.10+ and the standard library:

```sh
python3 scripts/check_plan.py path/to/plan.json
python3 scripts/render_plan.py path/to/plan.json --output path/to/segments.md
```

JSON is the editable source; regenerate Markdown after changes. For a brief text-only request, retain the same continuity and dialogue checks without requiring JSON as an extra deliverable.

| Check | What it establishes |
|---|---|
| Script checker | IDs/text/order match the supplied source map; time intervals, planning cap, total duration and declared state chains agree |
| Source review | The source map itself matches the approved script; split lines reconstruct correctly; cuts have actual authorization |
| Timing review | Speech plus pauses, reactions and action can fit; a speech-rate heuristic is only a review flag |
| Footage review | Actual frames, voices, screen text and cuts work together; only possible when clips exist |

The checker cannot prove natural-language consistency, reference compatibility, consent for omissions, or model performance. If the target is infeasible, quantify the shortfall and offer extending duration, splitting with a compatible total, or proposing cuts. Do not treat an empty warning list as proof of performability.

## 5. Deliver with the correct completion status

Provide the requested plan or prompts with integrated timelines, continuity locks, source-line map, reference/generation instructions and edit notes. State which limits were confirmed, whether timing was estimated or read aloud, and whether any footage was generated and reviewed.

A checked plan is ready for a generation trial. Only reviewed clips can support a claim about actual continuity. Do not add a call to action, new plot, or invented reaction to satisfy a generic template.

See [The Last Label](examples/the-last-label/script.md) for a synthetic 30-second, three-segment scene. Its 10-second cap is a planning assumption, not a vendor specification.
