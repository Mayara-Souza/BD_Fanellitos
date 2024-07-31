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
        self.root.geometry("300x250")

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

        self.forgot_password_button = tk.Button(self.login_frame, text="Esqueceu sua senha?", command=self.forgot_password)
        self.forgot_password_button.grid(row=3, columnspan=2, pady=5)

        self.register_button = tk.Button(self.login_frame, text="Cadastre-se", command=self.register)
        self.register_button.grid(row=4, columnspan=2, pady=5)

    def create_category_selection_screen(self):
        self.clear_screen()
        self.root.geometry("300x200")

        self.category_frame = tk.Frame(self.root)
        self.category_frame.pack(pady=20)

        tk.Label(self.category_frame, text="Selecione uma Categoria").pack(pady=10)

        self.category1_button = tk.Button(self.category_frame, text="CATEGORIA 1", command=lambda: self.create_inventory_screen("CATEGORIA1"))
        self.category1_button.pack(pady=5)

        self.category2_button = tk.Button(self.category_frame, text="CATEGORIA 2", command=lambda: self.create_inventory_screen("CATEGORIA2"))
        self.category2_button.pack(pady=5)

        self.back_button = tk.Button(self.category_frame, text="Voltar", command=self.create_login_screen)
        self.back_button.pack(pady=5)

    def create_inventory_screen(self, categoria):
        self.clear_screen()
        self.root.geometry("600x400")

        self.categoria = categoria

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

        self.tree = ttk.Treeview(self.root, columns=("ID", "Item", "Quantidade", "Última Modificação", "Nome Usuário"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Item", text="Item")
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.heading("Última Modificação", text="Última Modificação")
        self.tree.heading("Nome Usuário", text="Nome Usuário")
        self.tree.pack(pady=20)

        self.tree.bind("<Double-1>", self.on_double_click)

        self.back_button = tk.Button(self.inventory_frame, text="Voltar", command=self.create_category_selection_screen)
        self.back_button.grid(row=3, columnspan=2, pady=10)

        self.update_tree()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_cat1 = bd.autenticar_usuario('CATEGORIA1', username, password)
        user_cat2 = bd.autenticar_usuario('CATEGORIA2', username, password)
        if user_cat1 or user_cat2:
            messagebox.showinfo("Login", "Login bem-sucedido!")
            self.username = username
            self.create_category_selection_screen()
        else:
            messagebox.showerror("Login", "Nome de usuário ou senha incorretos")

    def add_item(self):
        item = self.item_entry.get()
        quantity = int(self.quantity_entry.get())
        bd.inserir_item(self.categoria, item, quantity, self.username)
        self.update_tree()

    def remove_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = int(self.tree.item(selected_item)['values'][0])
            bd.deletar_item(self.categoria, item_id)
            self.update_tree()

    def edit_item(self, item_id, item, quantity):
        new_quantity = simpledialog.askinteger("Quantidade", "Digite a nova quantidade:", initialvalue=quantity)
        if new_quantity is not None:
            bd.atualizar_item(self.categoria, item_id, item, new_quantity, self.username)
            self.update_tree()

    def on_double_click(self, event):
        item_id = int(self.tree.item(self.tree.selection())['values'][0])
        item = self.tree.item(self.tree.selection())['values'][1]
        quantity = self.tree.item(self.tree.selection())['values'][2]
        self.edit_item(item_id, item, quantity)

    def update_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        itens = bd.listar_itens(self.categoria)
        for item in itens:
            self.tree.insert("", "end", values=item)

    def forgot_password(self):
        self.clear_screen()
        self.root.geometry("300x200")

        self.forgot_password_frame = tk.Frame(self.root)
        self.forgot_password_frame.pack(pady=20)

        tk.Label(self.forgot_password_frame, text="E-mail").grid(row=0, column=0, pady=5)
        self.email_entry = tk.Entry(self.forgot_password_frame)
        self.email_entry.grid(row=0, column=1, pady=5)

        self.reset_button = tk.Button(self.forgot_password_frame, text="Redefinir Senha", command=self.reset_password)
        self.reset_button.grid(row=1, columnspan=2, pady=10)

        self.back_button = tk.Button(self.forgot_password_frame, text="Voltar", command=self.create_login_screen)
        self.back_button.grid(row=2, columnspan=2, pady=10)

    def reset_password(self):
        email = self.email_entry.get()
        new_password = simpledialog.askstring("Redefinir Senha", "Digite a nova senha:")
        if new_password:
            bd.redefinir_senha('CATEGORIA1', email, new_password)
            bd.redefinir_senha('CATEGORIA2', email, new_password)
            messagebox.showinfo("Redefinir Senha", "Senha redefinida com sucesso!")
            self.create_login_screen()

    def register(self):
        self.clear_screen()
        self.root.geometry("300x300")

        self.register_frame = tk.Frame(self.root)
        self.register_frame.pack(pady=20)

        tk.Label(self.register_frame, text="Nome de Usuário").grid(row=0, column=0, pady=5)
        self.reg_username_entry = tk.Entry(self.register_frame)
        self.reg_username_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.register_frame, text="E-mail").grid(row=1, column=0, pady=5)
        self.reg_email_entry = tk.Entry(self.register_frame)
        self.reg_email_entry.grid(row=1, column=1, pady=5)

        tk.Label(self.register_frame, text="Senha").grid(row=2, column=0, pady=5)
        self.reg_password_entry = tk.Entry(self.register_frame, show="*")
        self.reg_password_entry.grid(row=2, column=1, pady=5)

        tk.Label(self.register_frame, text="Confirme a Senha").grid(row=3, column=0, pady=5)
        self.reg_confirm_password_entry = tk.Entry(self.register_frame, show="*")
        self.reg_confirm_password_entry.grid(row=3, column=1, pady=5)

        self.register_button = tk.Button(self.register_frame, text="Cadastrar", command=self.register_user)
        self.register_button.grid(row=4, columnspan=2, pady=10)

        self.back_button = tk.Button(self.register_frame, text="Voltar", command=self.create_login_screen)
        self.back_button.grid(row=5, columnspan=2, pady=10)

    def register_user(self):
        username = self.reg_username_entry.get()
        email = self.reg_email_entry.get()
        password = self.reg_password_entry.get()
        confirm_password = self.reg_confirm_password_entry.get()

        if password == confirm_password:
            if bd.cadastrar_usuario('CATEGORIA1', username, email, password) or bd.cadastrar_usuario('CATEGORIA2', username, email, password):
                messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso!")
                self.create_login_screen()
            else:
                messagebox.showerror("Cadastro", "Erro ao cadastrar usuário. Nome de usuário ou e-mail já existe.")
        else:
            messagebox.showerror("Cadastro", "As senhas não coincidem.")

# Executando a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
