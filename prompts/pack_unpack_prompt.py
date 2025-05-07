import json

def unpack(lang):
    with open("base_prompts.json") as f:
        texts = json.load(f)[lang]
    
    for key, val in texts.items():
        with open(key+".md", "w") as f:
            f.write(val)

def pack(lang):
    with open("base_prompts.json") as f:
        old_json = json.load(f)
    
    
    for key, val in old_json[lang].items():
        with open(key+".md") as f:
            old_json[lang][key] = f.read()
     
    with open("base_prompts.json", "w") as f:
        json.dump(old_json, f)
    
unpack("en-US")
#pack("pt-BR")
