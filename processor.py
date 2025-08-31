# -------------------------------
# File Processing
# -------------------------------
import os
import sys
from os import listdir

import pyperclip

from config import save_config, PARSED_FOLDER, SUB_EXTENSION, EXTENSION, TEMPLATE_FOLDER, TARGET_FOLDER, get_config
from enums import Configuration, Operation
from replacer import substitute
from utils import write_vars_from_json

def process_files(op_type, data_json):
    if not os.path.exists(PARSED_FOLDER):
        os.makedirs(PARSED_FOLDER)

    confs = get_config()
    target = TEMPLATE_FOLDER if confs[Configuration.USE_TEMPLATE_FOLDER.value] and op_type == Operation.TEMPLATE_MANAGER.value else TARGET_FOLDER
    files = listdir(target)
    if not files:
        print("No files found in the folder")
        return

    for file_name in files:
        in_file = os.path.join(target, file_name)
        out1 = os.path.join(PARSED_FOLDER, file_name.replace(SUB_EXTENSION, "") + "_parsed_1" + EXTENSION)
        out2 = os.path.join(PARSED_FOLDER, file_name.replace(SUB_EXTENSION, "") + "_parsed_2" + EXTENSION)
        out3 = os.path.join(PARSED_FOLDER, file_name.replace(SUB_EXTENSION, "") + "_parsed" + EXTENSION)

        with open(in_file, "r", encoding="utf-8") as f_in, \
             open(out1, "w+", encoding="utf-8") as f1_out, \
             open(out2, "w+", encoding="utf-8") as f2_out, \
             open(out3, "w+", encoding="utf-8") as f3_out:

            if op_type == Operation.REPLACE_EQUALS.value:
                loaded_vars = write_vars_from_json("equals")
            elif op_type == Operation.HIBERNATE_MODEL_GENERATOR.value:
                loaded_vars = write_vars_from_json("getter-setter")
            elif op_type == Operation.TEMPLATE_MANAGER.value:
                loaded_vars = write_vars_from_json(confs["template_json_name"])
            else:
                print("Invalid operation type")
                sys.exit(0)

            substitute(file_name, f_in, f1_out, f2_out, f3_out, *loaded_vars)

        os.remove(out1)
        os.remove(out2)
        print("Parsed file saved in: " + str(out3))

        if confs.get(Configuration.DELETE_INPUT_FILE, False):
            os.remove(in_file)
            print(f"Input file {in_file} successfully deleted")

        if confs.get(Configuration.OPEN_FILE, False):
            os.startfile(out3)
            print(f"File {out3} successfully opened in editor")

        if confs.get(Configuration.COPY_TO_CLIPBOARD, False):
            with open(out3, 'r', encoding="utf-8") as fo:
                pyperclip.copy(fo.read())
                print(f"File {out3} successfully copied to clipboard")

    if confs.get(Configuration.OVERWRITE_CONFIG, False):
        save_config(confs, data_json)
