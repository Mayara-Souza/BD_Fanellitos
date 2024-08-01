import tkinter as tk
from interface import App
import bd

# Garantir que as tabelas existam para ambas as categorias
bd.criar_tabelas('CATEGORIA1')
bd.criar_tabelas('CATEGORIA2')

# Login para teste
bd.cadastrar_usuario(username='admin', email='teste@teste.com', senha='123123')


# Executando a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
