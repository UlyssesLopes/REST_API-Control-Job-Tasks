import requests

BASE = 'http://127.0.0.1:5000/'

"""data = [{'descricao': 'teste de descricao', 'solicitante': 'Ulysses Lopes'},
        {'descricao': 'segundo teste de descricao', 'solicitante': 'Candice Marten'},
        {'descricao': 'terceiro teste de descricao', 'solicitante': 'Ulysses Lopes'}]

for i in range(len(data)):
    response = requests.put(BASE + 'tarefa/' + str(i), data[i])
    print(response.json())"""

response_two = requests.put(BASE + 'tarefa/4', {'descricao': 'teste put de descricao tres', 'solicitante': 'Ulysses Lopes'})
print(response_two)
print(response_two.json())

