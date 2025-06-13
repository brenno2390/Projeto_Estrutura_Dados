import pandas as pd
import json
import requests
import re
from services.ConversaoJsonDados import converter_ofx_para_csv
from datetime import datetime

class DeepSeek:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = 'https://openrouter.ai/api/v1/chat/completions'

    def processar(self, extrato_ofx):
        # 1. Converte o OFX para JSON
        dados_json = json.dumps(converter_ofx_para_csv(extrato_ofx), ensure_ascii=False)

        # 2. Monta o payload para o modelo
        payload = {
            "model": "deepseek/deepseek-chat:free",
            "messages": [{
                "role": "user",
                "content": (
                    "Analise e categorize automaticamente os seguintes registros financeiros:\n\n"
                    "**Objetivos:**\n"
                    "- Separar as transações de débito e crédito.\n"
                    "- Categorizar transações de débito com base nas categorias abaixo.\n"
                    "- Identificar segmento do fornecedor/cliente.\n"
                    "- Calcular totais por categoria e por segmento.\n"
                    "- Marcar como 'Não Classificado' quando necessário.\n\n"
                    "**Categorias disponíveis para débito:**\n"
                    "- Tarifas e Taxas Bancárias\n- Cartão de Crédito\n- Entretenimento\n- Manutenção Predial\n"
                    "- Alimentação\n- Aluguel\n- Telefone e Internet\n- IPTU\n- Água\n- Energia Elétrica\n"
                    "- Materiais para Revenda\n- Materiais para Uso Interno\n- Transporte e Logística\n"
                    "- Folha de Pagamento\n- Gastos Médicos\n- Licenças e Softwares\n- Publicidade e Marketing\n"
                    "- Tributos e Impostos\n- Equipamentos e Investimentos\n- Empréstimos e Juros\n"
                    "- Distribuição de Lucros / Pró-Labore\n- Outros\n- Não Classificado\n\n"
                    "**Formato de resposta esperado (em JSON entre crases):**\n"
                    "- 'transações de debito': lista de objetos com 'fornecedor/cliente', 'categoria', 'valor'\n"
                    "- 'transações de credito': idem\n"
                    "- 'totais por categoria': objeto {categoria: total}\n"
                    "- 'totais por segmento': objeto {segmento: total}\n\n"
                    f"Dados de entrada (em JSON):\n{dados_json}\n\n"
                    "Envie a resposta em JSON dentro de três crases (```), para análise automatizada."
                )
            }]
        }

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        # 3. Faz a requisição
        response = requests.post(self.api_url, json=payload, headers=headers)

        if response.status_code == 200:
            try:
                conteudo_resposta = response.json()['choices'][0]['message']['content']
                with open("resposta_deepseek.txt", "w", encoding="utf-8") as f:
                    f.write(conteudo_resposta)

                resultado = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", conteudo_resposta, re.DOTALL | re.IGNORECASE)

                if resultado:
                    json_str = resultado.group(1)
                    with open("resposta_regex.txt", "w", encoding="utf-8") as f:
                        f.write(json_str)

                    dados = json.loads(json_str)

                    # Pegando as transações (com fallback seguro)
                    transacoes_debito = dados.get('transações de debito', [])
                    transacoes_credito = dados.get('transações de credito', [])

                    df_transacoes = pd.DataFrame(transacoes_debito + transacoes_credito)

                    # Totais por categoria
                    totais_categoria = dados.get('totais por categoria', {})
                    df_totais = pd.DataFrame(
                        list(totais_categoria.items()),
                        columns=['Categoria', 'Total']
                    )

                    # Totais por segmento
                    totais_segmento = dados.get('totais por segmento', {})
                    df_segmento = pd.DataFrame(
                        list(totais_segmento.items()),
                        columns=['Segmento', 'Total']
                    )

                    # Nome do arquivo com timestamp
                    nome_arquivo = "teste.xlsx"
                    with pd.ExcelWriter(nome_arquivo, engine='xlsxwriter') as writer:
                        df_transacoes.to_excel(writer, sheet_name='Transações', index=False)
                        df_totais.to_excel(writer, sheet_name='Totais por Categoria', index=False)
                        df_segmento.to_excel(writer, sheet_name='Totais por Segmento', index=False)

                    print(f" Arquivo Excel criado com sucesso: {nome_arquivo}")
                else:
                    print(" JSON estruturado não encontrado na resposta.")
                    print(" Conteúdo da resposta completa:")
                    print(conteudo_resposta)

            except Exception as e:
                print(f"Erro no processamento da resposta: {e}")
        else:
            print(f"Erro na requisição: {response.status_code}")
            print(response.text)
