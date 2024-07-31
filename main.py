import tkinter as tk
from interface import App
import bd

# Garantir que as tabelas existam para ambas as categorias
bd.criar_tabelas('CATEGORIA1')
bd.criar_tabelas('CATEGORIA2')

# Executando a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
