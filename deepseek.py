#api = sk-4ab57004c4ae4158bf2eb19502d5d5f1
#api2= sk-f124f4d39aa74fe9b4891a42059ebae0
#api_openRuther = "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"

import json
import re
import requests
import pandas as pd
from ConversaoJsonDados import converter_ofx_para_csv

#Nova chave API: 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
# Substitua pela sua chave da OpenRouter
API_KEY = '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'
API_URL = 'https://openrouter.ai/api/v1/chat/completions'

# Converte OFX e obtém os dados
dados_json = json.dumps(converter_ofx_para_csv('Extrato.ofx'), ensure_ascii=False)

# Payload para o modelo
data = {
    "model": "deepseek/deepseek-chat:free",
    "messages": [
        {
            "role": "user",
            "content": (
                    "Analise e categorize automaticamente os seguintes registros financeiros, com base nas diretrizes a seguir:\n\n"
                    "**Objetivos:**\n"
                    "- Classificar cada transação em uma das categorias fornecidas.\n"
                    "- Identificar o segmento de atuação de cada fornecedor.\n"
                    "- Calcular totais por categoria e por segmento.\n"
                    "- Identificar transações que não possam ser classificadas.\n\n"
                    "**Categorias disponíveis:**\n"
                    "- Alimentação\n"
                    "- Materiais para revenda\n"
                    "- Materiais para uso interno\n"
                    "- Transporte e logística\n"
                    "- Folha de pagamento\n"
                    "- Gastos médicos\n"
                    "- Outros\n\n"
                    "**Formato de resposta esperado (em JSON):**\n"
                    "Para cada transação:\n"
                    "- Categoria atribuída\n"
                    "- Segmento do fornecedor (ex: alimentação, logística, saúde, etc.)\n"
                    "- Valor original\n\n"
                    "Totais:\n"
                    "- Total por categoria\n\n"

                    f"Dados de entrada (em formato JSON):{dados_json}"
                    "Por favor, envie toda a resposta em JSON estruturado, pronto para análise automatizada."
            )
        }
    ]
}


# Enviando para a API
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

response = requests.post(API_URL, json=data, headers=headers)

# Tratando resposta
if response.status_code == 200:
    conteudo_resposta = response.json()['choices'][0]['message']['content']
    padrao = r'json(.*)'
    resultado = re.search(padrao, conteudo_resposta, re.DOTALL)
    #dicionario_python = json.loads(resultado.group(1))
    print("Conteúdo da resposta:")
    print(conteudo_resposta)

    # Salvando resposta em arquivo

    with open("resposta_deepseek.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo_resposta)
    with open("resposta_regex.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write(resultado.group(1))
            
    print("Resposta salva em 'resposta_deepseek.txt'")
else:
    print(f"Erro na requisição: {response.status_code}")
    print(response.text)
