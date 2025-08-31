from prompt_toolkit import HTML
from prompt_toolkit.formatted_text import to_formatted_text
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout import FormattedTextControl, Window, ScrollbarMargin
from prompt_toolkit.mouse_events import MouseEventType


class CheckboxList(object):
    """
    List of Checkboxes. More than one can be checked at the same time.

    :param values: List of (value, State[True or False]) tuples.
    """

    def __init__(self, values):
        assert isinstance(values, list)
        assert len(values) > 0
        assert all(isinstance(i, tuple) and len(i) == 2 for i in values)

        self.values = values
        self.current_value = values[0][0]
        self.current_checked_values = {}
        self._selected_index = 0

        for i, value in enumerate(self.values):
            self.current_checked_values[value[0]] = value[1]

        # Key bindings.
        kb = KeyBindings()

        @kb.add('up')
        def _(event):
            self._selected_index = max(0, self._selected_index - 1)

        @kb.add('down')
        def _(event):
            self._selected_index = min(
                len(self.values) - 1, self._selected_index + 1)

        @kb.add('pageup')
        def _(event):
            w = event.app.layout.current_window
            self._selected_index = max(
                0,
                self._selected_index - len(w.render_info.displayed_lines)
            )

        @kb.add('pagedown')
        def _(event):
            w = event.app.layout.current_window
            self._selected_index = min(
                len(self.values) - 1,
                self._selected_index + len(w.render_info.displayed_lines)
            )

        @kb.add('enter')
        @kb.add(' ')
        def _(event):
            self.current_value = self.values[self._selected_index][0]
            self.current_checked_values[self.current_value] = not self.current_checked_values[self.current_value]

        @kb.add(Keys.Any)
        def _(event):
            # We first check values after the selected value, then all values.
            for value in self.values[self._selected_index + 1:] + self.values:
                if type(value[0]) == HTML:
                    field_value = value[0].value
                else:
                    field_value = value[0]
                if field_value.startswith(event.data):
                    self._selected_index = self.values.index(value)
                    self.current_checked_values[self.current_value] = not self.current_checked_values[self.current_value]
                    return

        # Control and window.
        self.control = FormattedTextControl(
            self._get_text_fragments,
            key_bindings=kb,
            focusable=True)

        self.window = Window(
            content=self.control,
            style='class:radio-list',
            right_margins=[
                ScrollbarMargin(display_arrows=True),
            ],
            dont_extend_height=True)

    def _get_text_fragments(self):
        def mouse_handler(mouse_event):
            """
            Set `_selected_index` and `current_value` according to the y
            position of the mouse click event.
            """
            if mouse_event.event_type == MouseEventType.MOUSE_UP:
                self._selected_index = mouse_event.position.y
                self.current_value = self.values[self._selected_index][0]
                self.current_checked_values[self.current_value] = not self.current_checked_values[self.current_value]

        result = []
        for i, value in enumerate(self.values):
            selected = (i == self._selected_index)

            style = ''
            if self.current_checked_values[value[0]]:
                style += ' class:radio-checked'
            if selected:
                style += ' class:radio-selected'

            result.append((style, '('))

            if selected:
                result.append(('[SetCursorPosition]', ''))

            if self.current_checked_values[value[0]]:
                result.append((style, '*'))
            else:
                result.append((style, ' '))

            result.append((style, ')'))
            result.append(('class:radio', ' '))
            result.extend(to_formatted_text(value[0], style='class:radio'))
            result.append(('', '\n'))

        # Add mouse handler to all fragments.
        for i in range(len(result)):
            result[i] = (result[i][0], result[i][1], mouse_handler)

        result.pop()  # Remove last newline.
        return result

    def __pt_container__(self):
        return self.window
