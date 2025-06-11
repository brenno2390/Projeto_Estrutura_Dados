import pandas as pd
import json
import requests
import re
from services.ConversaoJsonDados import converter_ofx_para_csv

class DeepSeek:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = 'https://openrouter.ai/api/v1/chat/completions'

    def processar(self, extrato_ofx):
        dados_json = json.dumps(converter_ofx_para_csv(extrato_ofx), ensure_ascii=False)

        payload = {
            "model": "deepseek/deepseek-chat:free",
            "messages": [{
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
                    "Por favor, envie toda a resposta em JSON estruturado entre ``` , pronto para análise automatizada."
            )
            }]
        }

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        response = requests.post(self.api_url, json=payload, headers=headers)

        if response.status_code == 200:

            conteudo_resposta = response.json()['choices'][0]['message']['content']
            resultado = re.search(r"```(?:json)?\s*(\{.*?\}|\[.*?\])\s*```", conteudo_resposta, re.DOTALL | re.IGNORECASE)

            with open("resposta_deepseek.txt", "w", encoding="utf-8") as arquivo:
                arquivo.write(conteudo_resposta)
            with open("resposta_regex.txt", "w", encoding="utf-8") as arquivo:
                arquivo.write(resultado.group(1))

            if resultado:
                json_str = resultado.group(1)
                try:
                    # 3. Converter para dicionário Python
                    dados = json.loads(json_str)
                    df_transacoes = pd.DataFrame(dados['transacoes'])

                    df_totais = pd.DataFrame(
                        list(dados['totais_por_categoria'].items()),
                        columns=['Categoria', 'Total']
                    )

                    with pd.ExcelWriter("teste.xlsx", engine='xlsxwriter') as writer:
                        df_transacoes.to_excel(writer, sheet_name='Transações', index=False)
                        df_totais.to_excel(writer, sheet_name='Totais por Categoria', index=False)

                    print(f"Arquivo Excel criado em: 'teste.xlsx'")

                except json.JSONDecodeError as e:
                    print("Erro ao decodificar JSON:", e)
                    dados = None

            print("Resposta salva.")
        else:
            print(f"Erro na requisição: {response.status_code}")
            print(response.text)
