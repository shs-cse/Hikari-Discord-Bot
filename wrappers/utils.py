class FormatText:
    print_indentation_level = 0
    """
    Use ANSI color codes/graphics mode to emphasize changes
    reference: https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
    """
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    DIM_BOLD_RESET = '\033[22m'
    ITALICS = '\033[3m'
    UNDERLINE = '\033[4m'
    
    
    # dim yellow
    def wait(text):
        return f"\n{FormatText.YELLOW}{FormatText.DIM} {text}{FormatText.RESET}"

    # cyan
    def status(text, add_to_indentation_level=0):
        # remove extra indentation from this point onward
        if add_to_indentation_level < 0:
            FormatText.print_indentation_level += add_to_indentation_level
        if FormatText.print_indentation_level < 1:
            FormatText.print_indentation_level = 1
        indentation = '\t' * FormatText.print_indentation_level
        msg = f"\n{FormatText.CYAN}{indentation}• {text}{FormatText.RESET}"
        # add extra indentation after this point onward
        if add_to_indentation_level >= 0:
            FormatText.print_indentation_level += add_to_indentation_level
        return msg
        
    # green
    def success(text):
        return f"\n{FormatText.GREEN}✔ {text}{FormatText.RESET}"

    # yellow
    def warning(text):
        return f"\n{FormatText.YELLOW}{FormatText.BOLD}‼️ {text}{FormatText.RESET}"

    # red
    def error(text):
        return f"\n\n{FormatText.RED}{FormatText.BOLD}✘ {text}{FormatText.RESET}"