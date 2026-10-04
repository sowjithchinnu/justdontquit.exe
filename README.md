# Java Arrays Reel

A vertical Manim animation that explains Java arrays through code, array
values, zero-based indexing, indexed modification, and loop traversal.

## Project contents

- `java_arrays_reel.py` — shared animation logic and palette-specific scenes.
- `profile_pic/` — profile image used by the two-second outro card.
- `renders/` — final video deliverables.
- `docs/VISUAL_STYLE.md` — visual style notes.

The animation logic is shared. Burgundy, terracotta, and dark Java versions
are controlled through palette configuration rather than duplicated scenes.

## Final renders

```text
renders/burgundy_editorial/java_arrays_burgundy.mp4
renders/burgundy_editorial/java_arrays_explainer.mp4
renders/warm_terracotta/java_arrays_terracotta.mp4
renders/dark_java/java_arrays_dark.mp4
```

## Requirements

- Python 3.14+
- Manim Community Edition 0.21+

The project includes a local `.venv`. To render with it:

```bash
./.venv/bin/manim --disable_caching \
  -r 1080,1920 --fps 30 --format mp4 \
  -o java_arrays_explainer_final \
  java_arrays_reel.py JavaArraysExplainer
```

Move the resulting MP4 from Manim's temporary `media/` output into the
appropriate `renders/` subdirectory. Temporary render files are not part of
the project deliverables.

## Palette scenes

```bash
./.venv/bin/manim -pqh java_arrays_reel.py BurgundyJavaArrays
./.venv/bin/manim -pqh java_arrays_reel.py TerracottaJavaArrays
./.venv/bin/manim -pqh java_arrays_reel.py DarkJavaArrays
```

The target format is vertical 9:16 at 1080×1920.
