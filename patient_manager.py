import json 

def get_info():
    with open("patients.json", "r") as f:
        data = json.load(f)

    return data