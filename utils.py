import json
import math
import re

from config import TEMPLATES_CONF


def write_vars_from_json(template_vars, capitalize_first=False, whole_word=False):
    """Load variables to replace from template JSON."""
    print(f"Variables to replace identified with: {template_vars}\n")
    res = ()
    with open(TEMPLATES_CONF, encoding="utf-8") as f:
        data = json.load(f)
        for templ in data[template_vars]:
            for key, value in templ.items():
                if whole_word:
                    key = r"\b(\w*" + key + r"\w*)\b"
                res += key, value
                if capitalize_first:
                    # Capitalize key and value
                    pos = next((i for i, ch in enumerate(key) if ch.isalpha()), 0)
                    res += key[:pos] + key[pos:].capitalize(), value.capitalize()
    return res


def normalize_number_text(text, length=90, sep="*"):
    if text == "":
        return sep * length
    else:
        value1 = value2 = math.ceil((length - text.__len__()) / 2) - 1
        if text.__len__() % 2 == 1:
            value1 -= 1
        return sep * value1 + " " + text + " " + sep * value2


def count_all_special_chars(testo):
    return len(re.sub(r'[\w]+', '', testo))
