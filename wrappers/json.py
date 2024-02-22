import json

# decoder for json files with comments
class JSON5Decoder(json.JSONDecoder):
    # preserves empty lines and comments by wrapping with the key "__comment_LineNum__"
    # encoder assumes data will remain sorted according to insertion order
    def decode(self, json_str: str):
        json_str = '\n'.join(line if line.lstrip() and not line.lstrip().startswith('//')
                             else f'"__comment_{n+1:03d}__": {json.dumps(line)},'
                             for n,line in enumerate(json_str.split('\n')))
        return super().decode(json_str)

# read json file
def read_json(file):
    with open(file) as f:
        data = f.read()
        return JSON5Decoder().decode(data)



# encoder for json files with comments
class JSON5Encoder(json.JSONEncoder):
    # convert value with "__comment_LineNum__" key to actual comment
    # assumes data will remain sorted according to insertion order
    def encode(self, obj):
        json_str = super().encode(obj)
        json_str = '\n'.join(line if not line.lstrip().startswith('"__comment_') 
                             else json.loads(f"{{{line.rsplit(',',1)[0]}}}").popitem()[1]
                             for line in json_str.split('\n'))
        return json_str
        
# write to json file
def update_json(data, file):
    with open(file, 'w') as f:
        json_str = JSON5Encoder(indent=4).encode(data)
        f.write(json_str)


# test reading and writing
def test():
    from pprint import pprint
    info = read_json("info.jsonc")
    pprint(info, sort_dicts=False)
    update_json(info, "info.jsonc")
    
if __name__ == "__main__":
    test()