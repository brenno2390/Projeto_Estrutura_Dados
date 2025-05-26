import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os

#----- Variáveis globais -------------------------------------------------------------------------------------
COLOR_BACKGROUND = "#FFFFFF"  # Branco para o fundo principal
COLOR_FRAME_BG = "#F0F0F0"    # Cinza claro para frames (opcional, pode usar branco)
COLOR_BUTTON_BG = "#1960CC"   # Azul para fundo do botão
COLOR_BUTTON_FG = "#FFFFFF"   # Branco para texto do botão
COLOR_BUTTON_ACTIVE_BG = "#175DCE" # Azul mais escuro quando pressionado
COLOR_BUTTON_DISABLED_BG = "#A0A0A0" # Cinza para botão desabilitado
COLOR_BUTTON_DISABLED_FG = "#D0D0D0" # Cinza claro para texto desabilitado
COLOR_TEXT = "#000000"       # Preto para texto geral
COLOR_STATUS_BG = "#333333"   # Cinza escuro para fundo da barra de status
COLOR_STATUS_FG = "#FFFFFF"   # Branco para texto da barra de status

FONT_FAMILY = "Arial" # Uma fonte comum e limpa
FONT_SIZE_NORMAL = 10
FONT_SIZE_BUTTON = 11
FONT_WEIGHT_BOLD = "bold"

#----- Funções --------------------------------------------------------------------------------------------------


def enviar_arquivo():
    # Abre janela para selecionar o arquivo
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione um arquivo .ofx",
        filetypes=[("Arquivos OFX", "*.ofx")]
    )

    # Se o usuário cancelar, não faz nada
    if not caminho_arquivo:
        return

    # Verifica a extensão
    if not caminho_arquivo.lower().endswith(".ofx"):
        messagebox.showerror("Erro", "Por favor, selecione um arquivo com extensão .ofx")
        return

    try:
        # Pega o nome do arquivo
        nome_arquivo = os.path.basename(caminho_arquivo)
        
        # Caminho destino (mesmo diretório do script)
        destino = os.path.join(os.getcwd(), nome_arquivo)

        # Copia o arquivo para o destino
        shutil.copy(caminho_arquivo, destino)

        messagebox.showinfo("Sucesso", f"Arquivo '{nome_arquivo}' enviado com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao enviar o arquivo:\n{e}")

#----- Criação da interface gráfica -------------------------------------------------------------------------------------
 
janela = tk.Tk()
janela.title("Enviar Arquivo OFX")
janela.geometry("500x300")
janela_label = tk.Label(text="Data analise", fg=COLOR_BUTTON_BG, bg=COLOR_BACKGROUND, font=("Courier", 35, "bold"))
janela_label.grid(column=1, row=0)

janela.configure(bg=COLOR_BACKGROUND)

#------ Configuração da janela --------------------------------------------------------------------------------    
# Botão de envio
STYLE_BUTTON = {
    "font": (FONT_FAMILY, FONT_SIZE_BUTTON, FONT_WEIGHT_BOLD),
    "bg": COLOR_BUTTON_BG,
    "fg": COLOR_BUTTON_FG,
    "activebackground": COLOR_BUTTON_ACTIVE_BG,
    "activeforeground": COLOR_BUTTON_FG,
    "relief": "raised",
    "borderwidth": 1,
    "width": 25,
    "height": 2,
    "padx": 10,
    "pady": 5
}


botao_enviar = tk.Button(janela, text="Enviar Arquivo .ofx", command=enviar_arquivo)
botao_enviar.config(**STYLE_BUTTON)
botao_enviar.grid(column=1, row=1, padx=10, pady=10)
# Configuração da barra de status
barra_status = tk.Label(janela, text="Pronto", bg=COLOR_STATUS_BG, fg=COLOR_STATUS_FG, anchor="w")
barra_status.grid(column=0, row=2, columnspan=3, sticky="ew")

# Execução da interface
janela.mainloop()
