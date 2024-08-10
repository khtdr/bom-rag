import shutil


def info(*args):
    # Join all arguments with a space and print them in dim text, then reset
    return RESET + BOLD + " ".join(args).strip() + RESET


def status(*args):
    # Join all arguments with a space and print them in dim text, then reset
    # ux.status("*> sEaRcHiNg FoR aNsWeRs...")
    return RESET + BOLD + " ".join(args).strip() + RESET


def prompt(*args):
    # Join all arguments with a space and print them in bold text, then reset
    # print("-- ")
    # print("?>", end=" ")
    return BOLD + RESET + " ".join(args).strip() + RESET


# Text Styles
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
UNDERLINE = "\033[4m"

# Colors
# Foregrounds, backgrounds, and bright foregrounds for dark text
BLACK_BG = "\033[40m"
BLACK_FG = "\033[30m"
BLACK_FG_BR = "\033[90m"
BLUE_BG = "\033[44m"
BLUE_FG = "\033[34m"
BLUE_FG_BR = "\033[94m"
CYAN_BG = "\033[46m"
CYAN_FG = "\033[36m"
CYAN_FG_BR = "\033[96m"
GREEN_BG = "\033[42m"
GREEN_FG = "\033[32m"
GREEN_FG_BR = "\033[92m"
MAGENTA_BG = "\033[45m"
MAGENTA_FG = "\033[35m"
MAGENTA_FG_BR = "\033[95m"
RED_BG = "\033[41m"
RED_FG = "\033[31m"
RED_FG_BR = "\033[91m"
WHITE_BG = "\033[47m"
WHITE_FG = "\033[37m"
WHITE_FG_BR = "\033[97m"
YELLOW_BG = "\033[43m"
YELLOW_FG = "\033[33m"
YELLOW_FG_BR = "\033[93m"


def calculate_effective_width(text):
    width = 0
    for char in text:
        if ord(char) >= 32 and ord(char) <= 126:  # ASCII printable range
            width += 1
    return width


def get_terminal_size():
    width = shutil.get_terminal_size((80, 24))
    return width


def adjust_text_for_indentation(text, terminal_width, desired_indent=2):
    effective_width = calculate_effective_width(text)
    max_lines = terminal_width // effective_width

    # Calculate how much text needs to be adjusted
    adjustment_needed = max_lines * desired_indent - effective_width % terminal_width

    # Pad or trim the text based on the adjustment needed
    if adjustment_needed > 0:
        text = text.ljust(len(text) + adjustment_needed)
    else:
        text = text.rstrip(len(text) + adjustment_needed)

    return text
