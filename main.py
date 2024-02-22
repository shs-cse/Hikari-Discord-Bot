import numpy as np
import pandas as pd
import pyjson5

# read and write to json file
def read_json(file):
    with open(file) as f:
        return pyjson5.load(f)

def main():
    print(read_json("info.jsonc"))
    
if __name__ == "__main__":
    main()