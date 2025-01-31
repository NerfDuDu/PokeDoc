import json

with open('pokedex.json', encoding="utf8") as f:
    contenu = json.load(f)

pokemon = contenu[0]
print(pokemon['type'][0])

#with open('perso.json', 'w', encoding='utf-8') as f:
#    json.dump([{"e":1, "r":[1,2,3]},12], f, ensure_ascii=False, indent=4)

