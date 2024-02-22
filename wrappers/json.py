import json

# decoder for json files with comments
class JSONCDecoder(json.JSONDecoder):
    """
    Preserves empty lines and comments by wrapping the with the key "__comment_LineNum__".
    The encoder assumes that data will remain sorted according to insertion order.
    """
    def decode(self, json_str: str):
        json_str = '\n'.join(line if line.lstrip() and not line.lstrip().startswith('//')
                             else f'"__comment_{n+1:03d}__": {json.dumps(line)},'
                             for n,line in enumerate(json_str.split('\n')))
        return super().decode(json_str)

# read json file
def read_json(file):
    with open(file) as f:
        data = f.read()
        return JSONCDecoder().decode(data)



# encoder for json files with comments
class JSONCEncoder(json.JSONEncoder):
    """
    Convert values with "__comment_LineNum__" key to actual comments in the jsonc file.
    This encoder assumes that data will remain sorted according to insertion order,
    the default behaviour of json package.
    """
    def encode(self, obj):
        json_str = super().encode(obj)
        json_str = '\n'.join(line if not line.lstrip().startswith('"__comment_') 
                             else json.loads(f"{{{line.rsplit(',',1)[0]}}}").popitem()[1]
                             for line in json_str.split('\n'))
        return json_str
        
# write to json file
def update_json(data, file):
    with open(file, 'w') as f:
        json_str = JSONCEncoder(indent=4).encode(data)
        f.write(json_str)


# test reading and writing
def test():
    from pprint import pprint
    info = read_json("info.jsonc")
    pprint(info, sort_dicts=False)
    update_json(info, "info.jsonc")
    
if __name__ == "__main__":
    test()