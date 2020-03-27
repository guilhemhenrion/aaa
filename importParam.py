import json




def importParam():
    with open("param.json") as f:
        data = json.load(f)
    return data