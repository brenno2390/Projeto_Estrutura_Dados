import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os

class InterfaceGrafica:
    def __init__(self, callback):
        self.arquivo_recebido = None
        self.callback = callback
        self.janela = tk.Tk()
        self.janela.title("Enviar Arquivo OFX")
        self.janela.geometry("500x300")
        self.configurar_estilo()
        self.criar_componentes()

    def configurar_estilo(self):
        self.COLOR_BACKGROUND = "#FFFFFF"
        self.COLOR_BUTTON_BG = "#1960CC"
        self.COLOR_BUTTON_FG = "#FFFFFF"
        self.COLOR_BUTTON_ACTIVE_BG = "#175DCE"
        self.COLOR_STATUS_BG = "#333333"
        self.COLOR_STATUS_FG = "#FFFFFF"
        self.FONT_FAMILY = "Arial"
        self.FONT_SIZE_BUTTON = 11
        self.FONT_WEIGHT_BOLD = "bold"

    def criar_componentes(self):
        #------ Configuração da janela --------------------------------------------------------------------------------    
        label = tk.Label(self.janela, text="Data análise", fg=self.COLOR_BUTTON_BG, bg=self.COLOR_BACKGROUND, font=("Courier", 35, "bold"))
        label.grid(column=1, row=0)
        self.janela.configure(bg=self.COLOR_BACKGROUND)

        # Botão de envio

        style_button = {
            "font": (self.FONT_FAMILY, self.FONT_SIZE_BUTTON, self.FONT_WEIGHT_BOLD),
            "bg": self.COLOR_BUTTON_BG,
            "fg": self.COLOR_BUTTON_FG,
            "activebackground": self.COLOR_BUTTON_ACTIVE_BG,
            "activeforeground": self.COLOR_BUTTON_FG,
            "relief": "raised",
            "borderwidth": 1,
            "width": 25,
            "height": 2,
            "padx": 10,
            "pady": 5
        }

        botao = tk.Button(self.janela, text="Enviar Arquivo .ofx", command=self.enviar_arquivo)
        botao.config(**style_button)
        botao.grid(column=1, row=1, padx=10, pady=10)

        self.barra_status = tk.Label(self.janela, text="Pronto", bg=self.COLOR_STATUS_BG, fg=self.COLOR_STATUS_FG, anchor="w")
        self.barra_status.grid(column=0, row=2, columnspan=3, sticky="ew")

    def enviar_arquivo(self):
        caminho = filedialog.askopenfilename(title="Selecione um arquivo .ofx", filetypes=[("Arquivos OFX", "*.ofx")])
        if not caminho:
            return

        if not caminho.lower().endswith(".ofx"):
            messagebox.showerror("Erro", "Por favor, selecione um arquivo com extensão .ofx")
            return

        try:
            nome = os.path.basename(caminho)
            destino = os.path.join(os.getcwd(), nome)
            shutil.copy(caminho, destino)
            self.barra_status.config(text="Arquivo enviado com sucesso!")
            messagebox.showinfo("Sucesso", f"Arquivo '{nome}' enviado com sucesso!")
            self.arquivo_recebido = nome
            self.callback(nome) 
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao enviar o arquivo:\n{e}")

    def iniciar(self):
        self.janela.mainloop()
