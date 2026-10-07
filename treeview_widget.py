import tkinter as tk
from tkinter import ttk

class Treeview(ttk.Treeview):
    """Treeview personalizado com suporte automático a Tooltip flutuante ao passar o mouse."""
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.tooltip_window = None
        self.current_item = None

        # Registra eventos de movimento e saída do mouse
        self.bind("<Motion>", self._on_mouse_move)
        self.bind("<Leave>", self._hide_tooltip)

    def _on_mouse_move(self, event):
        item_id = self.identify_row(event.y)
        
        if not item_id:
            self._hide_tooltip()
            return

        if item_id != self.current_item:
            self.current_item = item_id
            valores = self.item(item_id, "values")
            if valores and len(valores) >= 4:
                caminho_completo = valores[3]  # Pega a coluna do caminho oculto
                self._show_tooltip(event.x_root + 15, event.y_root + 10, caminho_completo)

    def _show_tooltip(self, x, y, texto):
        self._hide_tooltip()

        self.tooltip_window = tk.Toplevel(self)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            self.tooltip_window,
            text=f" 📍 {texto} ",
            justify="left",
            background="#ffffe0",
            foreground="#000000",
            relief="solid",
            borderwidth=1,
            font=("Segoe UI", 9)
        )
        label.pack()

    def _hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
        self.current_item = None