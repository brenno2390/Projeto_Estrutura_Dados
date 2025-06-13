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
        self.centralizar_janela(500, 300)
        self.configurar_estilo()
        self.criar_componentes()

    def centralizar_janela(self, largura, altura):
        largura_tela = self.janela.winfo_screenwidth()
        altura_tela = self.janela.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura // 2)
        pos_y = (altura_tela // 2) - (altura // 2)
        self.janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
        self.janela.minsize(500, 300)

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
        self.janela.configure(bg=self.COLOR_BACKGROUND)
        self.janela.grid_columnconfigure(0, weight=1)
        self.janela.grid_columnconfigure(1, weight=1)
        self.janela.grid_columnconfigure(2, weight=1)
        self.janela.grid_rowconfigure(0, weight=1)
        self.janela.grid_rowconfigure(1, weight=1)
        self.janela.grid_rowconfigure(2, weight=1)
        self.janela.grid_rowconfigure(3, weight=1)

        label = tk.Label(
            self.janela, 
            text="Data análise", 
            fg=self.COLOR_BUTTON_BG, 
            bg=self.COLOR_BACKGROUND, 
            font=("Courier", 28, "bold")
        )
        label.grid(column=1, row=0, pady=(10, 0))

        style_button = {
            "font": (self.FONT_FAMILY, self.FONT_SIZE_BUTTON, self.FONT_WEIGHT_BOLD),
            "bg": self.COLOR_BUTTON_BG,
            "fg": self.COLOR_BUTTON_FG,
            "activebackground": self.COLOR_BUTTON_ACTIVE_BG,
            "activeforeground": self.COLOR_BUTTON_FG,
            "relief": "raised",
            "borderwidth": 1,
            "width": 25,
            "height": 2
        }

        botao = tk.Button(self.janela, text="Enviar Arquivo .ofx", command=self.enviar_arquivo)
        botao.config(**style_button)
        botao.grid(column=1, row=1, pady=20)

        self.barra_status = tk.Label(
            self.janela,
            text="Selecione o arquivo",
            bg=self.COLOR_STATUS_BG,
            fg=self.COLOR_STATUS_FG,
            anchor="center",
            width=40  # Largura controlada em caracteres
        )

        self.barra_status.grid(column=1, row=3, pady=10)

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

            # Processamento
            self.barra_status.config(text="Processando dados...")
            self.callback(nome)  # aqui você processa o arquivo

            # Finaliza a interface
            self.barra_status.config(text="Processamento concluído!")
            self.janela.destroy()

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao enviar o arquivo:\n{e}")


    def iniciar(self):
        self.janela.mainloop()


