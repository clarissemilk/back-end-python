import requests
resp = requestes.get("https://viacep.com.br/ws/45078300/json/")
dados = resp.json()

print(dados)
