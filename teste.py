'''import pandas as pd
# Criando um DataFrame de exemplo
data = []
data.append ({
        'id': "1",
        'tipo_transacao': 'Compra',
        'data_transacao': '2023-10-01',
        'valor': 100.50,
        'descricao_transacao': 'Compra de materiais'
    })

# Criando o DataFrame
df = pd.DataFrame(data)
# Salvar em um arquivo Excel
df.to_csv("out.csv", index=False)

for i in range(1,4):
    wb =   
print(df)'''
import pandas as pd

# Exemplo de dicionário
data = {
    'Nome': ['Alice', 'Bob', 'Charlie'],
    'Idade': [25, 30, 35],
    'Cidade': ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte']
}

# Criar um DataFrame a partir do dicionário
df = pd.DataFrame(data)

# Salvar o DataFrame em um arquivo CSV
df.to_csv('dados.csv', index=False, sep=';')

print("Arquivo CSV criado com sucesso!")
