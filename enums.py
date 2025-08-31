from enum import Enum

class Operation(Enum):
    REPLACE_EQUALS = 1
    HIBERNATE_MODEL_GENERATOR = 2
    TEMPLATE_MANAGER = 3

    @classmethod
    def to_list_name(cls):
        return list(map(lambda c: c.name, cls))

    @classmethod
    def to_list_value(cls):
        return list(map(lambda c: c.value, cls))


class Configuration(Enum):
    OP_TYPE = "op_type"
    DELETE_INPUT_FILE = "delete_input_file"
    SHOW_GUI_CONFIG = "show_gui_config"
    VERBOSE = "verbose"
    GET_FILE_BY_FIRST_ENTRY = "get_file_by_first_entry"
    OVERWRITE_CONFIG = "overwrite_config"
    OPEN_FILE = "open_file"
    COPY_TO_CLIPBOARD = "copy_to_clipboard"
    USE_TEMPLATE_FOLDER = "use_template_folder"
    TEMPLATE_JSON_NAME = "template_json_name"
    TEMPLATE_FILE_NAME = "template_file_name"
    ENTIRE_FILE = "entire_file"