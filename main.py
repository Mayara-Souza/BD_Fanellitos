import bd
import interface
import tkinter as tk

if __name__ == "__main__":
    # Criar tabelas
    bd.criar_tabelas()

    # Inserir um usuário admin para teste
    bd.inserir_usuario('admin', 'admin123')

    # Iniciar a interface gráfica
    root = tk.Tk()
    app = interface.App(root)
    root.mainloop()
