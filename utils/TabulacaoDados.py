import pandas as pd
import re

# Lendo o arquivo OFX
with open('Extrato.ofx', 'r', encoding='utf-8') as file:
    ofx_data = file.read()

# Extraindo blocos de transações
transactions = re.findall(r'<STMTTRN>(.*?)</STMTTRN>', ofx_data, re.DOTALL)

# Preparando a lista de dados
data = []
for i, transaction in enumerate(transactions, start=1):
    def extract(tag, text):
        match = re.search(fr'<{tag}>(.*?)($|<)', text, re.DOTALL)
        return match.group(1).strip() if match else None

    tipo_transacao = extract('TRNTYPE', transaction)
    data_transacao = extract('DTPOSTED', transaction)
    trnamt = extract('TRNAMT', transaction)
    descricao_transacao = extract('MEMO', transaction)

    # Corrige e converte valor para float
    valor = None
    if trnamt:
        trnamt_clean = re.sub(r'</.*?>', '', trnamt)
        try:
            valor = float(trnamt_clean)
        except ValueError:
            valor = None

    data.append({
        'id': i,
        'tipo_transacao': tipo_transacao,
        'data_transacao': data_transacao,
        'valor': valor,
        'descricao_transacao': descricao_transacao
    })

# Criando o DataFrame
df = pd.DataFrame(data)

# Salvar em um arquivo CSV
df.to_csv("TabulaçãoDados.csv", index=False, sep=';')