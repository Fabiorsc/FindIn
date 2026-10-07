import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading

import history_manager
import search_engine
from treeview_widget import Treeview

class SearchForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self.parent = parent
        self.historico = history_manager.carregar_historico()
        self.cancel_event = threading.Event()

        self.pack(fill="both", expand=True)
        self._criar_widgets()

    def _criar_widgets(self):
        # --- Painel Superior: Inputs ---
        frame_inputs = ttk.Frame(self)
        frame_inputs.pack(fill="x", pady=(0, 5))

        # Seleção de Local (Pasta ou Arquivo)
        ttk.Label(frame_inputs, text="Local:").grid(row=0, column=0, sticky="w", pady=3)
        self.combo_pasta = ttk.Combobox(frame_inputs, values=self.historico.get("pastas", []), width=55)
        self.combo_pasta.grid(row=0, column=1, padx=5, pady=3, sticky="we")
        
        self.btn_procurar = ttk.Button(frame_inputs, text="Procurar...", command=self._selecionar_local)
        self.btn_procurar.grid(row=0, column=2, padx=2)

        # Termo de Busca
        ttk.Label(frame_inputs, text="Texto:").grid(row=1, column=0, sticky="w", pady=3)
        self.combo_termo = ttk.Combobox(frame_inputs, values=self.historico.get("termos", []), width=55)
        self.combo_termo.grid(row=1, column=1, padx=5, pady=3, sticky="we")

        # Botão Buscar
        self.btn_buscar = ttk.Button(frame_inputs, text="Buscar", command=self._iniciar_busca)
        self.btn_buscar.grid(row=1, column=2, padx=2)

        frame_inputs.columnconfigure(1, weight=1)

        # --- Painel do Meio: Progresso + Status + Cancelar ---
        frame_progresso = ttk.Frame(self)
        frame_progresso.pack(fill="x", pady=(2, 5))

        # Barra de Progresso
        self.progress_bar = ttk.Progressbar(frame_progresso, orient="horizontal", mode="determinate")
        self.progress_bar.pack(fill="x", side="top", pady=(0, 2))

        # Linha de Status
        frame_status_linha = ttk.Frame(frame_progresso)
        frame_status_linha.pack(fill="x", side="top")

        self.lbl_status = ttk.Label(
            frame_status_linha, 
            text="Pronto | Passe o mouse sobre a linha para ver o caminho completo", 
            foreground="#555555"
        )
        self.lbl_status.pack(side="left", anchor="w")

        # Botão / Link de Cancelar
        self.lbl_cancelar = ttk.Label(
            frame_status_linha, 
            text="Cancelar", 
            foreground="#cc0000", 
            cursor="hand2", 
            font=("TkDefaultFont", 9, "underline")
        )
        self.lbl_cancelar.bind("<Button-1>", self._solicitar_cancelamento)
        self.lbl_cancelar.pack_forget()

        # --- Painel Inferior: Tabela de Resultados ---
        frame_tabela = ttk.Frame(self)
        frame_tabela.pack(fill="both", expand=True)

        colunas = ("arquivo", "linha", "conteudo", "caminho_full")
        self.tabela = Treeview(frame_tabela, columns=colunas, show="headings", selectmode="browse")

        self.tabela.heading("arquivo", text="Arquivo")
        self.tabela.heading("linha", text="Linha")
        self.tabela.heading("conteudo", text="Trecho Encontrado")
        self.tabela.heading("caminho_full", text="")

        self.tabela.column("arquivo", width=180, minwidth=120, anchor="w")
        self.tabela.column("linha", width=70, minwidth=50, anchor="center")
        self.tabela.column("conteudo", width=550, minwidth=200, anchor="w")
        self.tabela.column("caminho_full", width=0, stretch=False)

        scrollbar_y = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tabela.yview)
        scrollbar_x = ttk.Scrollbar(frame_tabela, orient="horizontal", command=self.tabela.xview)
        self.tabela.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.tabela.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        frame_tabela.rowconfigure(0, weight=1)
        frame_tabela.columnconfigure(0, weight=1)

        self.tabela.bind("<Double-1>", self._abrir_arquivo_selecionado)

    def _selecionar_local(self):
        caminho = filedialog.askopenfilename(
            title="Selecione um arquivo ou escolha um arquivo dentro da pasta desejada",
            filetypes=[
                ("Todos os documentos suportados", "*.txt *.docx *.xlsx *.pdf *.log *.py *.json *.csv"),
                ("Documentos PDF", "*.pdf"),
                ("Documentos Word", "*.docx"),
                ("Planilhas Excel", "*.xlsx"),
                ("Arquivos de Texto", "*.txt *.log *.py *.json *.csv"),
                ("Todos os arquivos", "*.*")
            ]
        )
        if caminho:
            self.combo_pasta.set(caminho)

    def _definir_estado_interface(self, bloqueado: bool):
        """Bloqueia ou libera todos os controles da tela."""
        estado = "disabled" if bloqueado else "normal"
        self.btn_buscar.config(state=estado)
        self.btn_procurar.config(state=estado)
        self.combo_pasta.config(state=estado)
        self.combo_termo.config(state=estado)

    def _solicitar_cancelamento(self, event=None):
        """Ativado IMEDIATAMENTE ao clicar no link Cancelar."""
        self.cancel_event.set()
        self.lbl_cancelar.pack_forget()
        self.lbl_status.config(text="Cancelando...", foreground="#cc0000")

    def _iniciar_busca(self):
        local = self.combo_pasta.get().strip()
        termo = self.combo_termo.get().strip()

        if not local or not termo:
            messagebox.showwarning("Aviso", "Preencha o local e o texto de busca.")
            return

        history_manager.salvar_busca(local, termo)
        
        # Limpa tabela
        for row in self.tabela.get_children():
            self.tabela.delete(row)

        self._definir_estado_interface(bloqueado=True)
        self.cancel_event.clear()

        self.progress_bar["value"] = 0
        self.lbl_status.config(text="Iniciando busca...", foreground="#000000")
        self.lbl_cancelar.pack(side="right", anchor="e")

        threading.Thread(target=self._executar_busca, args=(local, termo), daemon=True).start()

    def _atualizar_progresso_gui(self, processados, total, eta):
        if self.cancel_event.is_set():
            return

        porcentagem = (processados / total) * 100 if total > 0 else 0
        self.progress_bar["value"] = porcentagem
        
        if total == 1:
            tempo_str = "analisando arquivo..."
        elif eta > 60:
            minutos = int(eta // 60)
            segundos = int(eta % 60)
            tempo_str = f"~{minutos}m {segundos}s restantes"
        else:
            tempo_str = f"~{int(eta)}s restantes"

        self.lbl_status.config(
            text=f"Analisando: {processados}/{total} ({porcentagem:.1f}%) — {tempo_str}"
        )

    def _executar_busca(self, local, termo):
        def callback(proc, tot, eta):
            self.parent.after(0, self._atualizar_progresso_gui, proc, tot, eta)

        resultados, foi_cancelado = search_engine.buscar_texto_paralelo(
            local, termo, callback_progresso=callback, cancel_event=self.cancel_event
        )
        self.parent.after(0, self._exibir_resultados, resultados, foi_cancelado)

    def _exibir_resultados(self, resultados, foi_cancelado):
        # 1. Trata a interrupção/cancelamento
        if foi_cancelado or self.cancel_event.is_set():
            # Exibe o alerta modal
            messagebox.showinfo("FindIn", "Busca cancelada pelo usuário!")
            
            # Preenche a tabela com o que foi coletado até a interrupção
            if resultados:
                for item in resultados:
                    nome_arquivo = os.path.basename(item["arquivo"])
                    caminho_completo = item["arquivo"]

                    self.tabela.insert(
                        "", 
                        "end", 
                        values=(f"📄 {nome_arquivo}", item["linha"], item["conteudo"], caminho_completo)
                    )

            # Restaura a interface e exibe contagem com texto preto
            self.lbl_cancelar.pack_forget()
            self._definir_estado_interface(bloqueado=False)
            
            total_parcial = len(resultados)
            if total_parcial > 0:
                self.lbl_status.config(
                    text=f"{total_parcial} ocorrência(s) encontrada(s) até a interrupção. Double-click para abrir.", 
                    foreground="#000000"
                )
            else:
                self.lbl_status.config(
                    text="0 ocorrência(s) encontrada(s).", 
                    foreground="#000000"
                )
            return

        # 2. Caso a busca tenha concluído normalmente
        self.lbl_cancelar.pack_forget()
        self._definir_estado_interface(bloqueado=False)

        if not resultados:
            self.progress_bar["value"] = 100
            self.lbl_status.config(text="Busca concluída. Nenhum resultado encontrado.", foreground="#cc0000")
        else:
            self.progress_bar["value"] = 100
            for item in resultados:
                nome_arquivo = os.path.basename(item["arquivo"])
                caminho_completo = item["arquivo"]

                self.tabela.insert(
                    "", 
                    "end", 
                    values=(f"📄 {nome_arquivo}", item["linha"], item["conteudo"], caminho_completo)
                )

            self.lbl_status.config(
                text=f"Busca concluída! {len(resultados)} ocorrência(s) encontrada(s). Double-click para abrir.", 
                foreground="#008800"
            )

    def _abrir_arquivo_selecionado(self, event):
        item_selecionado = self.tabela.selection()
        if not item_selecionado:
            return

        valores = self.tabela.item(item_selecionado[0], "values")
        if len(valores) >= 4:
            caminho_arquivo = valores[3]

            if os.path.exists(caminho_arquivo):
                try:
                    if sys.platform == "win32":
                        os.startfile(caminho_arquivo)
                    elif sys.platform == "darwin":
                        subprocess.call(["open", caminho_arquivo])
                    else:
                        subprocess.call(["xdg-open", caminho_arquivo])
                except Exception as e:
                    messagebox.showerror("Erro", f"Não foi possível abrir o arquivo:\n{e}")