from wrappers.json import read_json, update_json
from pprint import pprint

def main():
    info = read_json("info.jsonc")
    pprint(info, sort_dicts=False)
    update_json(info, "info.jsonc")
    
if __name__ == "__main__":
    main()