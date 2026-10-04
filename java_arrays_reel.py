from dataclasses import dataclass
import os

from manim import *


@dataclass(frozen=True)
class Palette:
    background: str
    ink: str
    accent: str
    secondary: str
    muted_accent: str
    code_background: str
    cell_border: str | None = None
    code_keyword: str | None = None
    code_value: str | None = None


BURGUNDY = Palette(
    background="#F7F1E7",
    ink="#1D1A18",
    accent="#8E2432",
    secondary="#625D58",
    muted_accent="#D7B7A9",
    code_background="#EFE5D9",
)

TERRACOTTA = Palette(
    background="#F6EBDD",
    ink="#2B211C",
    accent="#C65D3E",
    secondary="#6B5E55",
    muted_accent="#D5AD62",
    code_background="#EEDCC9",
)

DARK_JAVA = Palette(
    background="#17191C",
    ink="#F4EEE5",
    accent="#A52D3B",
    secondary="#8D98A3",
    muted_accent="#59636D",
    code_background="#23272B",
    cell_border="#66717B",
    code_keyword="#C56A73",
    code_value="#E2A08F",
)


class JavaArraysReel(Scene):
    """Shared animation; subclasses only supply a visual palette."""

    palette = BURGUNDY

    def construct(self):
        p = self.palette
        self.camera.background_color = p.background

        # All geometry is deliberately fixed so both palette variants are identical.
        title = Text(
            "Java Arrays",
            font="Avenir Next",
            weight=BOLD,
            color=p.ink,
            font_size=58,
        ).to_edge(UP, buff=0.9)
        title_rule = Line(LEFT * 3.25, RIGHT * 3.25, color=p.accent, stroke_width=6)
        title_rule.next_to(title, DOWN, buff=0.28)

        eyebrow = Text(
            "A simple way to store many values",
            font="Avenir Next",
            color=p.secondary,
            font_size=24,
        ).next_to(title_rule, DOWN, buff=0.28)

        code_t2c = {}
        if p.code_keyword:
            code_t2c["int"] = p.code_keyword
        if p.code_value:
            code_t2c["91"] = p.code_value
        code = Text(
            "int[] marks = {85, 72, 91, 64, 88};",
            font="Menlo",
            color=p.ink,
            font_size=30,
            t2c=code_t2c,
        )
        code_card = SurroundingRectangle(
            code,
            buff=0.33,
            corner_radius=0.12,
            color=p.code_background,
            fill_color=p.code_background,
            fill_opacity=1,
            stroke_width=0,
        )
        code_group = VGroup(code_card, code).move_to(DOWN * 1.65)
        code_label = Text(
            "JAVA CODE",
            font="Avenir Next",
            weight=BOLD,
            color=p.accent,
            font_size=18,
        ).next_to(code_group, UP, buff=0.23).align_to(code_group, LEFT)

        values = [85, 72, 91, 64, 88]
        cell_w, cell_h = 1.25, 1.05
        array_cells = VGroup()
        value_labels = VGroup()
        for value in values:
            cell = RoundedRectangle(
                width=cell_w,
                height=cell_h,
                corner_radius=0.08,
                color=p.cell_border or p.ink,
                stroke_width=2.5,
                fill_color=p.background,
                fill_opacity=1,
            )
            label = Text(
                value,
                font="Menlo",
                weight=BOLD,
                color=p.ink,
                font_size=31,
            ).move_to(cell)
            array_cells.add(cell)
            value_labels.add(label)
        array = VGroup(*[VGroup(cell, label) for cell, label in zip(array_cells, value_labels)])
        array.arrange(RIGHT, buff=0)
        array.move_to(DOWN * 4.45)

        index_labels = VGroup(
            *[
                Text(
                    str(index),
                    font="Menlo",
                    color=p.secondary,
                    font_size=26,
                )
                for index in range(5)
            ]
        )
        for label, cell in zip(index_labels, array):
            label.next_to(cell, DOWN, buff=0.26)
        index_caption = Text(
            "INDEX",
            font="Avenir Next",
            weight=BOLD,
            color=p.secondary,
            font_size=17,
        ).next_to(index_labels, DOWN, buff=0.2)

        focus_box = SurroundingRectangle(
            array[2],
            buff=0.10,
            corner_radius=0.1,
            color=p.accent,
            stroke_width=5,
        )
        pointer = Triangle(color=p.accent, fill_color=p.accent, fill_opacity=1)
        pointer.scale(0.14).rotate(PI).next_to(index_labels[0], DOWN, buff=0.18)

        result_label = Text(
            "marks[2]",
            font="Menlo",
            weight=BOLD,
            color=p.ink,
            font_size=42,
        )
        arrow = Arrow(
            LEFT,
            RIGHT,
            buff=0.12,
            color=p.accent,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.22,
        ).set_length(0.62)
        result_value = Text(
            "91",
            font="Menlo",
            weight=BOLD,
            color=p.accent,
            font_size=48,
        )
        result = VGroup(result_label, arrow, result_value).arrange(RIGHT, buff=0.22)
        result.move_to(DOWN * 6.85)
        result_card = SurroundingRectangle(
            result,
            buff=0.25,
            corner_radius=0.12,
            color=p.muted_accent,
            stroke_width=2,
        )

        ending = Text(
            "One variable. Many values.",
            font="Avenir Next",
            weight=BOLD,
            color=p.ink,
            font_size=34,
        ).to_edge(DOWN, buff=0.75)

        # Shared timing and motion for both versions.
        self.play(FadeIn(title, shift=UP * 0.15), Create(title_rule), FadeIn(eyebrow), run_time=0.8)
        self.play(FadeIn(code_label, shift=UP * 0.1), FadeIn(code_group, shift=UP * 0.15), run_time=0.8)
        self.wait(0.6)
        self.play(
            FadeOut(code_group, shift=UP * 0.15),
            FadeOut(code_label, shift=UP * 0.15),
            LaggedStart(*[FadeIn(item, shift=UP * 0.15) for item in array], lag_ratio=0.08),
            run_time=0.9,
        )
        self.play(FadeIn(index_labels, shift=UP * 0.1), FadeIn(index_caption), run_time=0.55)
        self.wait(0.6)
        self.play(FadeIn(pointer, shift=UP * 0.12), run_time=0.3)
        self.play(
            pointer.animate.next_to(index_labels[1], DOWN, buff=0.18),
            run_time=0.38,
            rate_func=smooth,
        )
        self.play(
            pointer.animate.next_to(index_labels[2], DOWN, buff=0.18),
            run_time=0.38,
            rate_func=smooth,
        )
        self.play(Create(focus_box), Indicate(array[2], color=p.accent, scale_factor=1.04), run_time=0.65)
        self.play(Create(result_card), FadeIn(result, shift=UP * 0.12), run_time=0.7)
        self.wait(0.35)
        self.play(FadeIn(ending, shift=UP * 0.12), run_time=0.65)
        self.wait(2.5)


class BurgundyJavaArrays(JavaArraysReel):
    palette = BURGUNDY


class TerracottaJavaArrays(JavaArraysReel):
    palette = TERRACOTTA


class DarkJavaArrays(JavaArraysReel):
    palette = DARK_JAVA


class _LegacyJavaArraysExplainer(Scene):
    """Long-form educational explainer using the same visual system."""

    palette = BURGUNDY

    def _text(self, content, size, color=None, weight=None, font="Avenir Next"):
        text_kwargs = {
            "font": font,
            "font_size": size,
            "color": color or self.palette.ink,
        }
        if weight is not None:
            text_kwargs["weight"] = weight
        return Text(content, **text_kwargs)

    def _code_card(self, content, y=0, size=30, t2c=None):
        p = self.palette
        code = Text(
            content,
            font="Menlo",
            font_size=size,
            color=p.ink,
            t2c=t2c or {},
        )
        card = SurroundingRectangle(
            code,
            buff=0.32,
            corner_radius=0.12,
            color=p.code_background,
            fill_color=p.code_background,
            fill_opacity=1,
            stroke_width=0,
        )
        return VGroup(card, code).move_to(DOWN * -y)

    def _array(self, values, center=DOWN * 2.2, value_color=None, cell_width=1.25, cell_height=1.05, value_font=31):
        p = self.palette
        cells = VGroup()
        for value in values:
            cell = RoundedRectangle(
                width=cell_width,
                height=cell_height,
                corner_radius=0.08,
                color=p.cell_border or p.ink,
                stroke_width=2.5,
                fill_color=p.background,
                fill_opacity=1,
            )
            label = Text(
                str(value),
                font="Menlo",
                weight=BOLD,
                color=value_color or p.ink,
                font_size=value_font,
            ).move_to(cell)
            cells.add(VGroup(cell, label))
        cells.arrange(RIGHT, buff=0).move_to(center)
        return cells

    def _indices(self, array, font_size=26):
        p = self.palette
        labels = VGroup(
            *[
                Text(str(index), font="Menlo", color=p.secondary, font_size=font_size)
                for index in range(len(array))
            ]
        )
        for label, cell in zip(labels, array):
            label.next_to(cell, DOWN, buff=0.26)
        return labels

    def _header(self, title, subtitle=None):
        p = self.palette
        heading = self._text(title, 52, p.ink, BOLD).to_edge(UP, buff=0.82)
        rule = Line(LEFT * 3.25, RIGHT * 3.25, color=p.accent, stroke_width=6)
        rule.next_to(heading, DOWN, buff=0.24)
        group = VGroup(heading, rule)
        if subtitle:
            sub = self._text(subtitle, 23, p.secondary).next_to(rule, DOWN, buff=0.25)
            group.add(sub)
        return group

    def construct(self):
        p = self.palette
        self.camera.background_color = p.background
        values = ["85", "72", "91", "64", "88"]

        # Scene 1 — the problem: many separate variables.
        hook = self._header("Need to store 100 values?")
        variable_names = [f"score{i}" for i in range(1, 6)] + ["score6", "score7", "score8", "…", "score100"]
        clutter = VGroup(
            *[
                self._text(
                    name,
                    27,
                    p.ink if i % 3 else p.secondary,
                    font="Menlo",
                )
                for i, name in enumerate(variable_names)
            ]
        ).arrange_in_grid(rows=5, cols=2, buff=(0.35, 0.44)).move_to(DOWN * 1.5)
        messy = self._text("That's a lot of variables.", 34, p.accent, BOLD).to_edge(DOWN, buff=1.15)
        self.play(FadeIn(hook, shift=UP * 0.12), run_time=0.65)
        self.play(LaggedStart(*[FadeIn(item, shift=UP * 0.12) for item in clutter], lag_ratio=0.08), run_time=1.9)
        self.play(FadeIn(messy, shift=UP * 0.12), run_time=0.55)
        self.wait(0.65)

        # Scene 2 — the solution: one clean declaration.
        better = self._header("There's a better way.")
        declaration = self._code_card("int[] scores;", y=1.0, size=42)
        declaration_label = self._text("ONE VARIABLE", 19, p.accent, BOLD).next_to(declaration, UP, buff=0.25)
        self.play(
            FadeOut(hook), FadeOut(clutter), FadeOut(messy),
            FadeIn(better, shift=UP * 0.12),
            run_time=0.75,
        )
        self.play(FadeIn(declaration_label, shift=UP * 0.1), FadeIn(declaration, shift=UP * 0.15), run_time=0.8)
        self.wait(1.0)

        # Scene 3 — an array as one variable holding multiple values.
        array_header = self._header("One variable. Many values.")
        scores_label = self._text("scores", 34, p.accent, BOLD).move_to(UP * 0.05)
        array = self._array(values, center=DOWN * 2.35)
        array_caption = self._text("the values belong to the same variable", 23, p.secondary).to_edge(DOWN, buff=1.05)
        self.play(
            FadeOut(better), FadeOut(declaration), FadeOut(declaration_label),
            FadeIn(array_header, shift=UP * 0.12), FadeIn(scores_label, shift=UP * 0.1),
            run_time=0.8,
        )
        self.play(LaggedStart(*[FadeIn(cell, shift=UP * 0.18) for cell in array], lag_ratio=0.12), run_time=1.3)
        self.play(FadeIn(array_caption, shift=UP * 0.1), run_time=0.55)
        self.wait(1.1)

        # Scene 4 — connect the initialization code directly to the cells.
        init_header = self._header("Creating an array")
        init_code = self._code_card(
            "int[] scores = {85, 72, 91, 64, 88};",
            y=1.0,
            size=27,
            t2c={"int": p.accent, "91": p.accent},
        )
        init_label = self._text("JAVA CODE", 18, p.accent, BOLD).next_to(init_code, UP, buff=0.22).align_to(init_code, LEFT)
        self.play(FadeOut(array_header), FadeOut(scores_label), FadeOut(array_caption), FadeIn(init_header), run_time=0.65)
        self.play(FadeIn(init_label, shift=UP * 0.1), FadeIn(init_code, shift=UP * 0.12), run_time=0.8)
        self.play(array.animate.move_to(DOWN * 2.6), run_time=0.45)
        for cell in array:
            self.play(Indicate(cell, color=p.accent, scale_factor=1.04), run_time=0.34)
        self.wait(0.7)

        # Scene 5 — indexing and accessing a value.
        index_header = self._header("Every value has an index")
        indices = self._indices(array)
        zero_note = self._text("Java starts counting at zero.", 27, p.accent, BOLD).to_edge(DOWN, buff=0.95)
        pointer = Triangle(color=p.accent, fill_color=p.accent, fill_opacity=1)
        pointer.scale(0.14).rotate(PI).next_to(indices[0], DOWN, buff=0.18)
        access = self._text("scores[2]", 39, p.ink, BOLD, font="Menlo")
        arrow = Arrow(LEFT, RIGHT, buff=0.12, color=p.accent, stroke_width=4).set_length(0.62)
        access_value = self._text("91", 45, p.accent, BOLD, font="Menlo")
        access_result = VGroup(access, arrow, access_value).arrange(RIGHT, buff=0.22).move_to(DOWN * 5.05)
        focus = SurroundingRectangle(array[2], buff=0.1, corner_radius=0.1, color=p.accent, stroke_width=5)
        self.play(FadeOut(init_header), FadeOut(init_code), FadeOut(init_label), FadeIn(index_header), run_time=0.65)
        self.play(FadeIn(indices, shift=UP * 0.1), FadeIn(zero_note, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(pointer, shift=UP * 0.1), run_time=0.3)
        self.play(pointer.animate.next_to(indices[1], DOWN, buff=0.18), run_time=0.42, rate_func=smooth)
        self.play(pointer.animate.next_to(indices[2], DOWN, buff=0.18), run_time=0.42, rate_func=smooth)
        self.play(Create(focus), Indicate(array[2], color=p.accent, scale_factor=1.04), run_time=0.65)
        self.play(FadeIn(access_result, shift=UP * 0.12), run_time=0.75)
        self.wait(1.0)

        # Scene 6 — changing a value while preserving the rest of the array.
        change_header = self._header("Changing a value")
        change_code = self._code_card("scores[2] = 95;", y=1.0, size=34, t2c={"95": p.accent})
        change_label = self._text("UPDATE ONE INDEX", 18, p.accent, BOLD).next_to(change_code, UP, buff=0.22).align_to(change_code, LEFT)
        new_value = self._text("95", 31, p.accent, BOLD, font="Menlo").move_to(array[2][1])
        self.play(FadeOut(index_header), FadeOut(indices), FadeOut(pointer), FadeOut(zero_note), FadeOut(access_result), FadeOut(focus), FadeIn(change_header), run_time=0.65)
        self.play(FadeIn(change_label, shift=UP * 0.1), FadeIn(change_code, shift=UP * 0.12), run_time=0.75)
        self.play(Transform(array[2][1], new_value), Indicate(array[2], color=p.accent, scale_factor=1.04), run_time=0.85)
        self.wait(1.0)

        # Scene 7 — process the values together with a loop.
        loop_header = self._header("Why arrays are useful")
        loop_code = self._code_card("for (int i = 0; i < scores.length; i++)", y=0.9, size=21, t2c={"for": p.accent, "int": p.accent})
        loop_label = self._text("WORK WITH THEM TOGETHER", 18, p.accent, BOLD).next_to(loop_code, UP, buff=0.22).align_to(loop_code, LEFT)
        loop_caption = self._text("one highlight can visit every value", 23, p.secondary).to_edge(DOWN, buff=1.0)
        loop_focus = SurroundingRectangle(array[0], buff=0.1, corner_radius=0.1, color=p.accent, stroke_width=5)
        self.play(FadeOut(change_header), FadeOut(change_code), FadeOut(change_label), FadeIn(loop_header), run_time=0.65)
        self.play(FadeIn(loop_label, shift=UP * 0.1), FadeIn(loop_code, shift=UP * 0.12), FadeIn(loop_caption), Create(loop_focus), run_time=0.75)
        for cell in array[1:]:
            self.play(Transform(loop_focus, SurroundingRectangle(cell, buff=0.1, corner_radius=0.1, color=p.accent, stroke_width=5)), run_time=0.38, rate_func=smooth)
        self.wait(0.8)

        # Scene 8 — takeaway.
        takeaway_header = self._header("The takeaway")
        array_word = self._text("ARRAY", 48, p.accent, BOLD).move_to(UP * 1.9)
        one_variable = self._text("One variable", 36, p.ink, BOLD).move_to(UP * 0.35)
        many_values = self._text("Many values", 36, p.ink, BOLD).move_to(DOWN * 1.45)
        down_arrow = Arrow(UP, DOWN, buff=0.14, color=p.accent, stroke_width=5).set_length(0.75).move_to(DOWN * 0.55)
        ending = self._text("One variable. Many values.", 34, p.ink, BOLD).to_edge(DOWN, buff=0.9)
        self.play(
            FadeOut(loop_header), FadeOut(loop_code), FadeOut(loop_label), FadeOut(loop_caption), FadeOut(array), FadeOut(loop_focus),
            FadeIn(takeaway_header), run_time=0.8,
        )
        self.play(FadeIn(array_word, shift=UP * 0.12), FadeIn(one_variable, shift=UP * 0.12), run_time=0.6)
        self.play(GrowArrow(down_arrow), FadeIn(many_values, shift=UP * 0.12), run_time=0.7)
        self.play(FadeIn(ending, shift=UP * 0.12), run_time=0.7)
        self.wait(2.0)


class JavaArraysExplainer(_LegacyJavaArraysExplainer):
    """Composed long-form explainer with phone-first vertical spacing."""

    def construct(self):
        p = self.palette
        self.camera.background_color = p.background
        # Slightly enlarge the complete composition while preserving its framing.
        self.camera.frame_height *= 0.86
        self.camera.frame_width *= 0.86
        values = [85, 72, 91, 64, 88]

        brand = self._text("JAVA ARRAYS", 18, p.secondary, BOLD).to_edge(UP, buff=0.42)
        rule = Line(LEFT * 3.45, RIGHT * 3.45, color=p.accent, stroke_width=4)
        rule.next_to(brand, DOWN, buff=0.16)
        self.add(brand, rule)

        # Problem: give the hook and the clutter separate vertical zones.
        hook = self._text("Need to store 100 values?", 48, p.ink, BOLD).to_edge(UP, buff=1.45)
        names = [
            "int score1 = 89;",
            "int score2 = 78;",
            "int score3 = 90;",
            "int score4 = 84;",
            "int score5 = 76;",
            "…",
            "int score100 = 67;",
        ]
        clutter = VGroup(
            *[self._text(name, 23, p.ink if i % 3 else p.secondary, font="Menlo") for i, name in enumerate(names)]
        ).arrange(DOWN, buff=0.27).move_to(DOWN * 0.55)
        messy = self._text("That's a lot of variables.", 36, p.accent, BOLD).to_edge(DOWN, buff=1.0)
        self.play(FadeIn(hook, shift=UP * 0.12), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(item, shift=UP * 0.12) for item in clutter], lag_ratio=0.08), run_time=1.9)
        self.play(FadeIn(messy, shift=UP * 0.12), run_time=0.55)
        self.wait(0.85)

        # Solution: code is the only focal point.
        better = self._text("There's a better way.", 42, p.ink, BOLD).to_edge(UP, buff=1.45)
        declaration = self._code_card("int[] scores;", y=0.5, size=48)
        declaration_label = self._text("ONE VARIABLE", 20, p.accent, BOLD).next_to(declaration, DOWN, buff=0.35)
        array_caption = self._text("one variable holding many values", 26, p.secondary).to_edge(DOWN, buff=1.05)
        self.play(FadeOut(hook), FadeOut(clutter), FadeOut(messy), FadeIn(better, shift=UP * 0.12), run_time=0.75)
        self.play(
            FadeIn(declaration, shift=UP * 0.18),
            FadeIn(declaration_label, shift=UP * 0.12),
            FadeIn(array_caption, shift=UP * 0.1),
            run_time=0.85,
        )
        self.wait(1.1)

        # Array: make the main educational object substantially larger.
        array = self._array(values, center=DOWN * 0.25, cell_width=1.65, cell_height=1.4, value_font=43)
        scores_label = self._text("scores", 40, p.accent, BOLD).next_to(array, LEFT, buff=0.15)
        scores_array_group = VGroup(scores_label, array)
        scores_array_group.move_to(array.get_center())
        init_code = self._code_card("int[] scores = {85, 72, 91, 64, 88};", y=2.05, size=35, t2c={"int": p.accent, "91": p.accent})
        init_label = self._text("JAVA CODE", 18, p.accent, BOLD).next_to(init_code, UP, buff=0.2).align_to(init_code, LEFT)
        self.play(FadeOut(better), FadeOut(declaration), FadeOut(declaration_label), run_time=0.75)
        self.play(
            FadeIn(scores_label, shift=UP * 0.12),
            FadeIn(init_label, shift=UP * 0.1),
            FadeIn(init_code, shift=UP * 0.15),
            LaggedStart(*[FadeIn(cell, shift=UP * 0.18) for cell in array], lag_ratio=0.12),
            run_time=1.35,
        )
        self.wait(1.35)

        # Code is contextual and sits above the array; the array stays visible.
        self.play(FadeOut(array_caption), run_time=0.8)
        for cell in array:
            self.play(Indicate(cell, color=p.accent, scale_factor=1.05), run_time=0.32)
        self.wait(0.9)

        # Indexing: reveal one layer at a time.
        indices = self._indices(array, font_size=36)
        zero_note = VGroup(
            self._text("In Java, indexing is 0-based.", 28, p.secondary, BOLD),
            self._text("first element  →  index 0", 25, p.secondary, font="Menlo"),
            self._text("last element   →  length - 1", 25, p.secondary, font="Menlo"),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(indices, shift=UP * 0.12), FadeIn(zero_note, shift=UP * 0.12), run_time=0.65)
        # Hold the indexing explanation long enough to read before selecting index 2.
        self.wait(2.6)
        pointer = Triangle(color=p.accent, fill_color=p.accent, fill_opacity=1)
        pointer.scale(0.16).rotate(PI).next_to(indices[2], DOWN, buff=0.2)
        focus = SurroundingRectangle(array[2], buff=0.12, corner_radius=0.1, color=p.accent, stroke_width=6)
        access = self._text("scores[2]", 50, p.ink, BOLD, font="Menlo")
        arrow = Arrow(LEFT, RIGHT, buff=0.14, color=p.accent, stroke_width=5).set_length(0.72)
        access_value = self._text(str(values[2]), 58, p.accent, BOLD, font="Menlo")
        access_result = VGroup(access, arrow, access_value).arrange(RIGHT, buff=0.25).move_to(UP * 2.35)
        self.play(
            FadeOut(init_label),
            FadeOut(init_code),
            FadeOut(zero_note, shift=DOWN * 0.08),
            FadeIn(pointer, shift=UP * 0.1),
            Create(focus),
            FadeIn(access_result, shift=UP * 0.15),
            run_time=0.7,
        )
        self.remove(zero_note)
        self.wait(1.0)

        # Update: explain the operation before showing the assignment code.
        modify_note = self._text("You can also modify an element using its index.", 30, p.ink, BOLD).to_edge(DOWN, buff=0.85)
        self.play(FadeOut(access_result), FadeOut(indices), FadeOut(pointer), FadeOut(focus), run_time=0.65)
        self.play(FadeIn(modify_note, shift=UP * 0.1), run_time=0.45)
        self.wait(1.35)
        change_code = self._code_card("scores[2] = 95;", y=2.25, size=43, t2c={"95": p.accent})
        new_value = self._text(str(95), 43, p.accent, BOLD, font="Menlo").move_to(array[2][1])
        self.play(FadeIn(change_code, shift=UP * 0.15), run_time=0.75)
        self.play(FadeIn(indices, shift=UP * 0.1), FadeIn(pointer, shift=UP * 0.1), FadeIn(focus), run_time=0.55)
        self.wait(0.45)
        values[2] = 95
        self.play(Transform(array[2][1], new_value), run_time=0.9)
        self.play(Indicate(array[2][0], color=p.accent, scale_factor=1.06), run_time=0.5)
        self.wait(0.45)
        self.play(FadeOut(focus), FadeOut(pointer), run_time=0.25)
        self.remove(focus, pointer)
        self.play(FadeOut(modify_note, shift=DOWN * 0.08), run_time=0.45)

        # Loop: ask the broader question first, then traverse every element.
        loop_code = self._code_card("for (int i = 0; i < scores.length; i++)", y=2.3, size=32, t2c={"for": p.accent, "int": p.accent})
        loop_question = self._text("What if we want to access every element?", 38, p.ink, BOLD).move_to(DOWN * 0.1)
        loop_focus = SurroundingRectangle(array[0], buff=0.12, corner_radius=0.1, color=p.accent, stroke_width=6)
        self.play(
            FadeOut(change_code), FadeOut(indices),
            FadeOut(array), FadeOut(scores_label),
            FadeIn(loop_question, shift=UP * 0.12),
            run_time=0.8,
        )
        self.remove(focus)
        self.wait(1.2)
        self.play(
            FadeOut(loop_question),
            FadeIn(loop_code, shift=UP * 0.12),
            FadeIn(array), FadeIn(scores_label), FadeIn(indices, shift=UP * 0.1),
            run_time=0.8,
        )
        loop_readout = self._text("i = 0  →  scores[0]  →  85", 27, p.secondary, font="Menlo").to_edge(DOWN, buff=0.95)
        loop_explanation = self._text(
            "A for loop lets us repeat a block of code.",
            30, ManimColor(p.secondary).interpolate(ManimColor(p.ink), 0.35), BOLD,
        ).next_to(loop_readout, DOWN, buff=0.38)
        pointer.next_to(indices[0], DOWN, buff=0.2)
        self.play(
            FadeIn(loop_readout, shift=UP * 0.1),
            FadeIn(loop_explanation, shift=UP * 0.1),
            FadeIn(pointer, shift=UP * 0.1),
            Create(loop_focus),
            run_time=0.55,
        )
        for i, cell in enumerate(array[1:], start=1):
            next_readout = self._text(f"i = {i}  →  scores[{i}]  →  {values[i]}", 27, p.secondary, font="Menlo").to_edge(DOWN, buff=0.95)
            self.play(
                pointer.animate.next_to(indices[i], DOWN, buff=0.2),
                Transform(loop_focus, SurroundingRectangle(cell, buff=0.12, corner_radius=0.1, color=p.accent, stroke_width=6)),
                Transform(loop_readout, next_readout),
                run_time=0.72,
                rate_func=smooth,
            )
        self.wait(1.1)

        # Takeaway: simplify only after the concept has been fully shown.
        takeaway = self._text("ARRAY", 56, p.accent, BOLD).move_to(UP * 1.95)
        one_variable = self._text("One variable.", 40, p.ink, BOLD).move_to(UP * 0.25)
        many_values = self._text("Many values.", 40, p.ink, BOLD).move_to(DOWN * 1.35)
        self.play(FadeOut(loop_code), FadeOut(loop_readout), FadeOut(loop_explanation), FadeOut(indices), FadeOut(pointer), FadeOut(array), FadeOut(scores_label), FadeOut(loop_focus), FadeIn(takeaway, shift=UP * 0.12), run_time=0.8)
        self.play(FadeIn(one_variable, shift=UP * 0.12), run_time=0.65)
        self.play(FadeIn(many_values, shift=UP * 0.12), run_time=0.55)
        self.wait(1.7)

        # One-second creator end card.
        profile = ImageMobject("profile_pic/justdontquit_exe.png").set_height(2.4)
        profile.move_to(UP * 0.75)
        handle = self._text("justdontquit.exe", 34, p.ink, BOLD).next_to(profile, DOWN, buff=0.22)
        follow = self._text("Follow for more", 34, p.accent, BOLD).next_to(handle, DOWN, buff=0.32)
        end_card = Group(profile, handle, follow)
        self.play(
            FadeOut(takeaway),
            FadeOut(one_variable),
            FadeOut(many_values),
            run_time=0.3,
        )
        self.play(FadeIn(end_card, shift=UP * 0.1), run_time=0.35, rate_func=smooth)
        self.wait(2.5)


if __name__ == "__main__":
    # `PALETTE=terracotta python java_arrays_reel.py` is a convenient local hint,
    # while the named Manim scenes remain the canonical two outputs.
    selected = os.environ.get("PALETTE", "burgundy").lower()
    print("Use: manim -pqh java_arrays_reel.py BurgundyJavaArrays TerracottaJavaArrays DarkJavaArrays")
    print(f"Selected palette hint: {selected}")
