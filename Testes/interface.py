import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os

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

# Criação da interface gráfica
janela = tk.Tk()
janela.title("Enviar Arquivo OFX")
janela.geometry("300x150")

# Botão de envio
botao_enviar = tk.Button(janela, text="Enviar Arquivo .ofx", command=enviar_arquivo)
botao_enviar.pack(expand=True)

# Execução da interface
janela.mainloop()
