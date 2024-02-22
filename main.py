# from consts import Color
from wrappers.json import read_json, update_json
from wrappers.pygs import check_google_creds
from pprint import pprint
    

def main():
    # info = read_json("info.jsonc")
    # pprint(info, sort_dicts=False)
    # update_json(info, "info.jsonc")
    check_google_creds()
    
if __name__ == "__main__":
    main()