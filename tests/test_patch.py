import requests

BASE = 'http://127.0.0.1:5000/'

response = requests.patch(BASE + 'tarefa/0', {'descricao': 'alteracao da descricao teste'})
print(response)
print(response.json())