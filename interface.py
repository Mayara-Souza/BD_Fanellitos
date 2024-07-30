import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import bd

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Controle de Estoque")
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        self.root.geometry("300x200")

        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Nome de Usuário").grid(row=0, column=0, pady=5)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.login_frame, text="Senha").grid(row=1, column=0, pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, columnspan=2, pady=10)

    def create_inventory_screen(self, userid):
        self.clear_screen()
        self.root.geometry("600x400")

        self.userid = userid

        self.inventory_frame = tk.Frame(self.root)
        self.inventory_frame.pack(pady=20)

        tk.Label(self.inventory_frame, text="Item").grid(row=0, column=0, pady=5)
        self.item_entry = tk.Entry(self.inventory_frame)
        self.item_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.inventory_frame, text="Quantidade").grid(row=1, column=0, pady=5)
        self.quantity_entry = tk.Entry(self.inventory_frame)
        self.quantity_entry.grid(row=1, column=1, pady=5)

        self.add_button = tk.Button(self.inventory_frame, text="Adicionar", command=self.add_item)
        self.add_button.grid(row=2, column=0, pady=10)

        self.remove_button = tk.Button(self.inventory_frame, text="Retirar", command=self.remove_item)
        self.remove_button.grid(row=2, column=1, pady=10)

        self.tree = ttk.Treeview(self.root, columns=("ID", "Item", "Quantidade", "Última Modificação", "UserID"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Item", text="Item")
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.heading("Última Modificação", text="Última Modificação")
        self.tree.heading("UserID", text="UserID")
        self.tree.pack(pady=20)

        self.tree.bind("<Double-1>", self.on_double_click)

        self.update_tree()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = bd.autenticar_usuario(username, password)
        if user:
            messagebox.showinfo("Login", "Login bem-sucedido!")
            self.create_inventory_screen(user[0])
        else:
            messagebox.showerror("Login", "Nome de usuário ou senha incorretos")

    def add_item(self):
        item = self.item_entry.get()
        quantity = int(self.quantity_entry.get())
        bd.inserir_item(item, quantity, self.userid)
        self.update_tree()

    def remove_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = int(self.tree.item(selected_item)['values'][0])
            bd.deletar_item(item_id)
            self.update_tree()

    def edit_item(self, item_id, item, quantity):
        new_quantity = simpledialog.askinteger("Quantidade", "Digite a nova quantidade:", initialvalue=quantity)
        if new_quantity is not None:
            bd.atualizar_item(item_id, item, new_quantity, self.userid)
            self.update_tree()

    def on_double_click(self, event):
        item_id = int(self.tree.item(self.tree.selection())['values'][0])
        item = self.tree.item(self.tree.selection())['values'][1]
        quantity = self.tree.item(self.tree.selection())['values'][2]
        self.edit_item(item_id, item, quantity)

    def update_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        itens = bd.listar_itens()
        for item in itens:
            self.tree.insert("", "end", values=item)

# Executando a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
