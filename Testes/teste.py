import json

string_json = '{"nome": "João", "idade": 30, "cidade": "Porto"}'
dicionario_python = json.loads(string_json)

print(type(dicionario_python))
print(dicionario_python["nome"])