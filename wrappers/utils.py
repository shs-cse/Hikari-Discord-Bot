import re
from bot_variables.config import RegexPattern

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
    
    
# folder id -> link
def get_link_from_folder_id(folder_id):
    return f"https://drive.google.com/drive/folders/{folder_id}"
    
# sheet id -> link
def get_link_from_sheet_id(sheet_id):
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}"

# destination sheet id + source sheet id -> allow access link
def get_allow_access_link_from_sheet_id(dest_sheet_id, src_sheet_id):
    dest_sheet_url = get_link_from_sheet_id(dest_sheet_id)
    return f"{dest_sheet_url}/externaldata/addimportrangepermissions?donorDocId={src_sheet_id}"

# link -> sheets/folder id
def get_drive_id_from_link(link):
    return re.search(RegexPattern.GOOGLE_DRIVE_LINK_ID, link).group()