from view.interface import InterfaceGrafica
from controller.deepseek import DeepSeek

class Application:
    def __init__(self):
        self.interface = InterfaceGrafica(self.ao_receber_arquivo)
        self.deepseek = DeepSeek(api_key="CHAVE APIIIIIIIIIIIIIIIIIIIIII") # CHAVE APIIIIIIIIIIIIIIIIIIIIII

    def ao_receber_arquivo(self, nome_arquivo):
        print(f"[INFO] Arquivo recebido: {nome_arquivo}")
        self.deepseek.processar(nome_arquivo)

    def iniciar(self):
        self.interface.iniciar()

if __name__ == "__main__":
    app = Application()
    app.iniciar()
