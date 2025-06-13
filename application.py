from view.interface import InterfaceGrafica
from controller.deepseek import DeepSeek

class Application:
    def __init__(self):
        self.interface = InterfaceGrafica(self.ao_receber_arquivo)
        self.deepseek = DeepSeek(api_key="CHAVE APIIII") #CHAVE APIIIIIIII

    def ao_receber_arquivo(self, nome_arquivo):
        print(f"[INFO] Arquivo recebido: {nome_arquivo}")
        self.interface.barra_status.config(text="Processando dados...")
        self.interface.janela.update_idletasks()

        self.deepseek.processar(nome_arquivo)

        self.interface.barra_status.config(text="Processamento concluído!")
        self.interface.janela.update_idletasks()  # força atualização imediata
        self.interface.janela.after(500, self.interface.janela.destroy)

    def iniciar(self):
        self.interface.iniciar()

if __name__ == "__main__":
    app = Application()
    app.iniciar()