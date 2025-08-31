from prompt_toolkit.application import get_app
from prompt_toolkit.layout import HSplit
from prompt_toolkit.shortcuts.dialogs import _run_dialog
from prompt_toolkit.widgets import Dialog, Label, Button

from cmd_utils.CheckboxList import CheckboxList


def checkboxlist_dialog(title='', text='', ok_text='Ok', cancel_text='Cancel',
                        values=None, style=None, async_=False):
    """
    Display a simple checkbox-list of element the user can choose amongst.

    More than one element can be selected at a time using Arrow keys and Enter.
    The focus can be moved between the list and the Ok/Cancel button with tab.
    """
    def ok_handler():
        get_app().exit(check_list.current_checked_values)

    def ko_handler():
        get_app().exit()

    check_list = CheckboxList(values)
    #checkbox1 = Checkbox("singola")  Singola checkbox

    dialog = Dialog(
        title=title,
        body=HSplit([
            Label(text=text, dont_extend_height=True),
            check_list,
        ]),
        buttons=[
            Button(text=ok_text, handler=ok_handler),
            Button(text=cancel_text, handler=ko_handler),
        ],
        with_background=True)

    return _run_dialog(dialog, style, async_=async_)