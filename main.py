from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
# DATA_DIR = BASE_DIR / "data"
# DB_PATH = DATA_DIR / "dpm.db"
# RESOURCES_DIR = BASE_DIR / "resources"
# ICONS_DIR = RESOURCES_DIR / "icons"


import sys
import tkinter as tk
from pathlib import Path
from search_form import SearchForm
from tkinter import messagebox


def exibir_sobre():
  messagebox.showinfo(
      "Sobre o FindIn",
      "FindIn — Busca Profunda de Conteúdo\n\n"
      "Desenvolvido por: Devbrax\n"
      "Licença: MIT License\n\n"
      "Contato / Sugestões / Propostas:\n"
      "• E-mail: devbrax.software@gmail.com\n"
      "• GitHub: https://github.com/Fabiorsc",
  )

def obter_caminho_recurso(nome_arquivo):
    """Retorna o caminho do arquivo tanto no Python normal quanto dentro do .exe do PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        # Pasta temporaria onde o PyInstaller extrai os arquivos ao rodar o .exe
        return Path(sys._MEIPASS) / nome_arquivo
    # Pasta raiz onde esta o script .py
    return Path(__file__).resolve().parent / nome_arquivo


def centralizar_janela(root, largura=850, altura=600):
    root.update_idletasks()
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)
    root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")


def main():
    root = tk.Tk()

    # Cria a barra de menus no topo da janela
    menubar = tk.Menu(root)

    # Cria o menu "Ajuda"
    menu_ajuda = tk.Menu(menubar, tearoff=0)
    menu_ajuda.add_command(label="Sobre / Contato", command=exibir_sobre)

    # Adiciona o menu "Ajuda" na barra principal
    menubar.add_cascade(label="Ajuda", menu=menu_ajuda)

    # Associa a barra de menu à janela principal
    root.config(menu=menubar)

    root.title("FindIn — Busca Profunda de Conteúdo")

    # Localiza o app.ico dentro do pacote e aplica na janela
    icon_path = obter_caminho_recurso("app.ico")
    if icon_path.exists():
        try:
            root.iconbitmap(str(icon_path))
        except Exception:
            pass

    centralizar_janela(root, largura=850, altura=600)
    root.minsize(700, 450)

    app = SearchForm(root)
    root.mainloop()


if __name__ == "__main__":
    main()