#api = sk-4ab57004c4ae4158bf2eb19502d5d5f1
#api2= sk-f124f4d39aa74fe9b4891a42059ebae0
#api_openRuther = "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"
'''import requests
import pandas as pd
import re
import json
import ConversaoJsonDados


# Substitua pela sua chave de API do OpenRouter
API_KEY = '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'
API_URL = 'https://openrouter.ai/api/v1/chat/completions'

# Defina os cabeçalhos para a requisição da API
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}
dados_json = json.dumps(ConversaoJsonDados.converter_ofx_para_csv('Extrato.ofx'), ensure_ascii=False)
# Defina o payload da requisição (dados)
data = {
    "model": "deepseek/deepseek-chat:free",
    "messages": [{"role": "user", "content": f"Gostaria de solicitar a análise e categorização automática dos seguintes registros financeiros, conforme as diretrizes : Objetivo: Classificar cada transação em categorias específicas e identificar o segmento de atuação de cada fornecedor.; Categorias solicitadas: Alimentação (compras de alimentos), Materiais para revenda, Materiais para uso interno, Transporte e logística, Folha de pagamento, Gastos, médicos, Outros (itens não classificáveis nas anteriores); Processamento requerido: Classificar cada transação na categoria mais adequada, Pesquisar e identificar o segmento principal de cada fornecedor, Calcular totais por categoria, Identificar transações não classificáveis; Categoria atribuída: Segmento do fornecedor, Valor original, Total gasto por categoria, Número de transações por segmento; Enviar a resposta em formato de texto, com os totais por categoria descriminando cada uma com todos os fornecedores.Os Dados são os seguintes(em Json): {dados_json}"}]  # Mensagem inicial para a API,
}

# Envie a requisição POST para a API DeepSeek
response = requests.post(API_URL, json=data, headers=headers)

# 2. Verifique se a requisição foi bem-sucedida
if response.status_code == 200:
    # 3. Extraia o conteúdo da resposta
    resposta_completa = response.json()  # Isso contém toda a resposta da API
    
    # 4. Acesse especificamente o conteúdo da mensagem
    conteudo_resposta = resposta_completa['choices'][0]['message']['content']
    
    # Agora você tem o conteúdo em uma variável
    print("Conteúdo da resposta:")
    print(conteudo_resposta)
    
    # 5. (Opcional) Salve em um arquivo
    with open("resposta_deepseek.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo_resposta)
        
    print("Resposta salva em 'resposta_deepseek.txt'")
else:
    print(f"Erro na requisição: {response.status_code}")
    print(response.text)'''
import json
import requests
from ConversaoJsonDados import converter_ofx_para_csv

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
                "Gostaria de solicitar a análise e categorização automática dos seguintes registros financeiros, conforme as diretrizes:\n"
                "- Objetivo: Classificar cada transação em categorias específicas e identificar o segmento de atuação de cada fornecedor.\n"
                "- Categorias: Alimentação, Materiais para revenda, Materiais para uso interno, Transporte e logística, Folha de pagamento, Gastos médicos, Outros.\n"
                "- Processamento requerido: Classificar, pesquisar segmento, calcular totais, identificar não classificáveis.\n"
                "- Resposta esperada: Categoria, Segmento do fornecedor, Valor original, Total por categoria, Número de transações por segmento.\n\n"
                f"Os dados são os seguintes (em JSON): {dados_json}"
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
    print("Conteúdo da resposta:")
    print(conteudo_resposta)

    with open("resposta_deepseek.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo_resposta)
    print("Resposta salva em 'resposta_deepseek.txt'")
else:
    print(f"Erro na requisição: {response.status_code}")
    print(response.text)
