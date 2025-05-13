import re
import pandas as pd

def converter_ofx_para_csv(caminho_ofx, caminho_csv='saida_ofx.csv'):
    try:
        with open(caminho_ofx, 'r', encoding='utf-8') as file:
            ofx_data = file.read()
    except Exception as e:
        return f"Erro ao ler o arquivo: {e}"

    transactions = re.findall(r'<STMTTRN>(.*?)</STMTTRN>', ofx_data, re.DOTALL)
    data = []

    for i, transaction in enumerate(transactions, start=1):
        def extract(tag, text):
            match = re.search(fr'<{tag}>(.*?)($|<)', text, re.DOTALL)
            return match.group(1).strip() if match else None

        tipo_transacao = extract('TRNTYPE', transaction)
        data_transacao = extract('DTPOSTED', transaction)
        trnamt = extract('TRNAMT', transaction)
        descricao_transacao = extract('MEMO', transaction)

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

    if data:
        df = pd.DataFrame(data)
        df.to_csv(caminho_csv, index=False, sep=';')
        return df.to_dict(orient='records')

    return []
