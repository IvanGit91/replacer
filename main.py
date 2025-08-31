import sys
import time

from prompt_toolkit.shortcuts import radiolist_dialog, message_dialog

from cmd_utils.utils import checkboxlist_dialog
from config import load_config
from enums import Operation, Configuration
from processor import process_files
from utils import normalize_number_text

def main():
    confs, list_conf_bool, data_json = load_config()
    op_type = confs.get(Configuration.OP_TYPE.value, 1)

    # Optional GUI dialogs
    op_names = Operation.to_list_name()
    if confs.get(Configuration.SHOW_GUI_CONFIG.value, False):
        op_type = radiolist_dialog(
            values=[(i + 1, op) for i, op in enumerate(op_names)],
            title="Operation Type",
            text="Select the type of operation:"
        )
        results = checkboxlist_dialog(
            title="Options",
            text="Select available options",
            values=list_conf_bool,
        )
        if results:
            confs.update(results)
        else:
            message_dialog(title="Operation cancelled", text="Exiting...")
            sys.exit(0)

    if op_type not in [1, 2, 3]:
        print(f"Invalid operation type {op_type}. Exiting...")
        sys.exit(0)

    # Show banner
    print(normalize_number_text(""))
    print(normalize_number_text("YOU ARE USING"))
    print(normalize_number_text(op_names[op_type - 1]))
    print(normalize_number_text(""))
    time.sleep(1)

    process_files(op_type, data_json)


if __name__ == "__main__":
    main()
