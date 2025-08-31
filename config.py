import json
import os

from dotenv import load_dotenv

load_dotenv()

# -------------------------------
# Global Constants & Config
# -------------------------------
CONF_FILE = os.environ.get("CONF_FILE")
EXTENSION = os.environ.get("EXTENSION")
SUB_EXTENSION = os.environ.get("SUB_EXTENSION")
PARSED_FOLDER = os.environ.get("PARSED_FOLDER")
TEMPLATES_CONF = os.environ.get("TEMPLATES_CONF")
TARGET_FOLDER = os.environ.get("TARGET_FOLDER")
TEMPLATE_FOLDER = os.environ.get("TEMPLATE_FOLDER")

_config = {}

# -------------------------------
# Configuration
# -------------------------------
def load_config(read_conf_file=True):
    global _config
    list_conf_bool = []
    data_json = []

    if read_conf_file and os.path.exists(CONF_FILE):
        with open(CONF_FILE, encoding="utf-8") as f:
            data_json = json.load(f)
            for conf in data_json['configuration']:
                for k, v in conf.items():
                    if v["enabled"]:
                        _config[k] = v["value"]
                        if isinstance(v["value"], bool) and v["menu"]:
                            list_conf_bool.append((k, v["value"]))
    return _config, list_conf_bool, data_json


def save_config(confs, data_json):
    with open(CONF_FILE, 'w', encoding="utf-8") as f:
        for k, v in confs.items():
            data_json['configuration'][0][k]['value'] = v
        json.dump(data_json, f, indent=4)

def get_config():
    return _config