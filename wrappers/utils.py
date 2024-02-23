class FormatText:
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


    def success(text):
        return f"\n{FormatText.GREEN}✔ {text}{FormatText.RESET}"

    def warning(text):
        return f"\n{FormatText.YELLOW}{FormatText.BOLD}‼️ {text}{FormatText.RESET}"

    def error(text):
        return f"\n{FormatText.RED}{FormatText.BOLD}✘ {text}{FormatText.RESET}"