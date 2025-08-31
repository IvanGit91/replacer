# -------------------------------
# Substitution Logic
# -------------------------------
import os
import re

from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style

from config import get_config, PARSED_FOLDER, SUB_EXTENSION, EXTENSION
from enums import Configuration
from utils import count_all_special_chars

style = Style.from_dict({
    'normal': '#ffffff',
    'red': '#ff0066',
    'green': '#44ff44 italic',
})

def substitute(file_name, f_in, f1_out, f2_out, f3_out, *args):
    """
    Apply a list of regex substitutions to the input file and write the results.

    Args:
        file_name (str): The name of the file to process.
        f_in: Input file object
        f1_out: First intermediate output file (swap buffer)
        f2_out: Second intermediate output file (swap buffer)
        f3_out: Final output file
        *args: Regex/replacement pairs (regex1, replacement1, regex2, replacement2, ...)
    """
    substitution_count = 0
    num_rules = len(args)

    # Save a copy of the original file
    original_backup = os.path.join(PARSED_FOLDER, file_name.replace(SUB_EXTENSION, "") + "_original" + EXTENSION)
    with open(original_backup, "w", encoding="utf-8") as f_backup:
        for line in f_in:
            f1_out.write(line)
            f_backup.write(line)

    switch = False
    for i in range(0, num_rules, 2):
        # Swap input/output files between passes
        if switch:
            f1_out.seek(0)
            f1_out.truncate()
            file_in, file_out = f2_out, f1_out
            f2_out.seek(0)
        else:
            f2_out.seek(0)
            f2_out.truncate()
            file_in, file_out = f1_out, f2_out
            f1_out.seek(0)

        line_number = 1
        if not get_config().get(Configuration.ENTIRE_FILE.value, False):
            for line in file_in:
                substitution_count = search_and_replace(
                    args, i, line, file_out, line_number, substitution_count
                )
                line_number += 1
        else:
            # Treat entire file as one string
            content = file_in.read()
            substitution_count = search_and_replace(
                args, i, content, file_out, line_number, substitution_count
            )
        switch = not switch

    # Write final result
    file_out.seek(0)
    for line in file_out:
        f3_out.write(line)

    print(f"Number of search patterns: {int(num_rules / 2)}")
    print(f"Number of replacements performed: {substitution_count}")


def search_and_replace(args, i, text, file_out, line_number, substitution_count=0):
    """
    Search and replace using a regex rule.

    Args:
        args: Regex/replacement pairs
        i: Index of the current regex in args
        text: Input text (line or whole file)
        file_out: File object to write output
        line_number: Current line number
        substitution_count: Counter of replacements so far
    """
    regex, replacement = args[i], args[i + 1]
    match = re.search(regex, text)

    if match:
        replaced = re.sub(regex, replacement, match.string)

        # Handle $1, $2... with \U (upper) and \L (lower) transformations
        if len(match.regs) > 1:
            for idx, region in enumerate(match.regs[1:], start=1):
                sub_text = match.string[region[0]:region[1]]
                if f"\\L${idx}" in replaced:
                    replaced = replaced.replace(f"\\L${idx}", sub_text.lower())
                elif f"\\U${idx}" in replaced:
                    replaced = replaced.replace(f"\\U${idx}", sub_text.upper())
                else:
                    replaced = replaced.replace(f"${idx}", sub_text)

        if get_config().get(Configuration.VERBOSE.value, False):
            show_replacement_preview(regex, replacement, text, replaced, line_number, match)

        file_out.write(replaced)
        substitution_count += 1
    else:
        file_out.write(text)

    return substitution_count


def show_replacement_preview(regex, replacement, original, replaced, line_number, match):
    """Prints a formatted preview of a replacement (only in verbose mode)."""
    text_fragments = FormattedText([
        ('class:normal', 'Line '), ('class:red', str(line_number)), ('class:normal', ': '),
        ('class:green', regex), ('class:normal', ' ---> '), ('class:green', replacement),
    ])
    print_formatted_text(text_fragments, style=style)

    start, end = match.regs[0]
    threshold1 = len(regex)
    threshold2 = len(replacement)

    pos_end2 = end + threshold2 - threshold1 + int(count_all_special_chars(regex) / 2)

    preview = FormattedText([
        ('class:normal', 'Original:   '),
        ('class:normal', original[start - threshold1:start]),
        ('class:green', original[start:end]),
        ('class:normal', original[end:end + threshold1]),
        ('class:normal', '\nReplaced:  '),
        ('class:normal', replaced[start - threshold2:start]),
        ('class:green', replaced[start:pos_end2]),
        ('class:normal', replaced[pos_end2:pos_end2 + threshold2]),
        ('class:normal', '\n'),
    ])
    print_formatted_text(preview, style=style)

