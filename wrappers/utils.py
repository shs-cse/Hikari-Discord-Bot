class Color:
    MAGENTA = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_CYAN = '\033[96m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def format_success_msg(text):
    return f"\n{Color.OK_GREEN}✔ {text}{Color.RESET}"

def format_warning_msg(text):
    return f"\n{Color.WARNING}{Color.BOLD}‼️ {text}{Color.RESET}"

def format_error_msg(text):
    return f"\n{Color.FAIL}{Color.BOLD}✘ {text}{Color.RESET}"