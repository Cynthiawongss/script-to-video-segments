# The last label · approved synthetic source

This original miniature scene is for testing the skill, not footage from a real project. The dialogue below is the source of truth. No lines may be added, removed, or reordered for the sample.

## Brief

A quiet packing desk. Mira stands left; Noah sits right. One parcel, a label printer, and a screen showing room 21. Morning light stays constant. They catch an old address before printing. Target: 30 seconds. Provisional planning cap: 10 seconds per generation segment, chosen for this example; it is not a claim about any vendor's API. No reference images or video have been generated.

| ID | Speaker | Exact dialogue |
|---|---|---|
| D1 | MIRA | This is the last label. |
| D2 | NOAH | Check the address before we print. |
| D3 | MIRA | It still has the old room number. |
| D4 | NOAH | Change it to twelve. |
| D5 | MIRA | Twelve. Now it matches. |
| D6 | NOAH | Ready to send. |

## Continuity and production assumptions

Mira wears a teal work shirt; Noah a grey sweater. No names, clothing, screen direction, or light changes. The room number changes from 21 to 12 during segment B. Segment C prints the corrected label and places it beside the parcel. The label's physical location and screen contents are tracked separately.

Dialogue pacing uses a 3 words/second review threshold, not a claim about recorded speech. Read aloud and allow action time before generating. A generation trial must establish whether the requested screen/label text is legible; use a post-production text replacement if it is not, preserving the same story fact.

`plan.json` is editable. `segments.md` is generated from it. Revise JSON, validate, then render again; do not hand-edit the generated document and let it diverge.
