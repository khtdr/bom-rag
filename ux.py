import shutil


def info(*args):
    return RESET + DIM + " ".join(args) + RESET


def status(*args):
    return "\n" + RESET + BOLD + " ".join(args) + RESET


def prompt(*args):
    return "\n" + RESET + BOLD + " ".join(args) + "\n>> " + RESET


def answer(*args):
    text = " ".join(args)
    indented = _indent_text(text, 3)
    prefix = RESET + BOLD + "=>" + RESET
    return RESET + prefix + BLUE + BOLD + indented[2:] + RESET


def cite(*args):
    text = " ".join(args)
    indented = _indent_text(text, 3)
    prefix = RESET + DIM + "->" + RESET
    return RESET + prefix + indented[2:] + "\n" + RESET


# Text Styles
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
REVERSE = "\033[7m"
UNDERLINE = "\033[4m"
BLUE = "\033[34m"


def _get_term_width():
    try:
        return int(shutil.get_terminal_size().columns)
    except ValueError:
        return 80


def _indent_text(text, desired_indent=2):
    term_width = _get_term_width()
    indent = " " * desired_indent

    words = text.split()
    lines = [indent]  # Initialize with the desired indent
    current_line_length = 0

    for word in words:
        if current_line_length + len(word) + 1 > term_width - desired_indent:
            lines.append(indent)  # Start a new line with the indent
            current_line_length = 0

        lines[-1] += f"{word} "
        current_line_length += len(word) + 1  # +1 for space

        if current_line_length >= term_width - desired_indent:
            lines.append(indent)  # Ensure the last line starts with the indent
            current_line_length = 0

    return "\n".join(lines)
