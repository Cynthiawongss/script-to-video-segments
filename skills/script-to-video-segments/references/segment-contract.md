# Segment plan v1

JSON is the editable source. `render_plan.py` creates Markdown from it. The checker does not run video generation or access a network.

## Root

- `schema_version`: 1.
- `title`: scene name.
- `planning`: `target_seconds`, `max_segment_seconds`, `limit_basis` (source or provisional), `speech_unit`, `max_units_per_second`. Supported speech units: `whitespace_words`, `cjk_characters`. The latter is intentionally a simple non-whitespace-character estimate; mixed-language content needs manual review.
- `locks`: nonempty map of stable IDs to actual character/setting/style descriptions.
- `source_dialogue`: ordered list of `{id, speaker, text}`. Split an approved line into ordered phrase IDs before planning if it spans segments; preserve the parent ID, exact original text, and ordered-part mapping in the source script. Review reassembly separately: the checker compares only the supplied source map, not the original script file.
- `omissions`: list of `{id, authorization}`. Empty unless the user approved a cut. A filled authorization field is a record for human review, not proof of consent.
- `segments`: ordered list described below.

## Segment

`id`, `duration`, `lock_ids`, `opening_state`, `closing_state`, `beats`, and `bridge`.

`opening_state` and `closing_state` are nonempty maps with the same keys across the sequence, such as `location`, `person_position`, `prop_state`, `screen_state`. Keep trackable state separate from style prose. `bridge` is an empty string for continuous action, otherwise the concrete reason for a changed boundary (e.g. a labelled next-day cut).

Every segment includes all root lock IDs; a lock may describe how an off-screen person remains absent. Avoid irrelevant locks by keeping the root set limited to the sequence.

Each beat has `start`, `end`, `camera`, `action`, `audio`, `dialogue`, `state_in`, and `state_out`. Beat states use the same keys as the segment. They form a chain from segment opening to segment closing. `dialogue` is a list of `{id, speaker, text}` referencing source lines. Silent beats use `[]`.

Time intervals cover exactly `[0, duration]`, consecutively, without overlap or gaps. Dialogue IDs occur in source order, exactly once, excluding approved omissions. The sum of segment durations equals the supplied target. A deliberate duration change requires updating that target and the brief, not hiding a mismatch.

## Review beyond the checker

The script checks schema, arithmetic time coverage, exact dialogue references, and declared state continuity. It flags estimated speech load above the supplied threshold. It cannot inspect source images, infer whether “picks up the mug” matches `mug=on_table`, detect natural-language contradictions, prove permission for a cut, or judge a performance. It does not guarantee visual consistency or voice/lip sync.

For a revision, update root locks first, then the changed beats, then downstream opening/closing states until the original state is re-established. Render the prompt document again. Check the edited scene's meaning and timing with a person or a generation trial.
