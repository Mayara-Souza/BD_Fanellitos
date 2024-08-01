import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from tkinter import font as tkfont
import bd

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("FANELLITOS DB")
        self.create_login_screen()

    def set_fullscreen(self):
        self.root.attributes('-fullscreen', True)  # Define a janela como tela cheia
        self.root.bind("<F11>", self.toggle_fullscreen)  # Permite alternar entre tela cheia e janela normal com F11
        self.root.bind("<Escape>", self.quit_fullscreen)  # Permite sair da tela cheia com Esc

    def toggle_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))

    def quit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)
        self.root.geometry("1200x800")  # Define um tamanho padrão para a janela se sair da tela cheia

    def create_login_screen(self):
        self.clear_screen()  # Limpa a tela e configura a cor de fundo
        self.root['bg'] = '#3a86d1'

        # Frame principal para centralizar os widgets
        self.login_frame = tk.Frame(self.root, bg="#3073b7", pady=10, padx=10)
        self.login_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Definindo uma fonte grande e em negrito
        bold_font = tkfont.Font(family="Ubuntu", size=16, weight="bold")
        # Definindo uma fonte para botões e textos
        regular_font = tkfont.Font(family="Ubuntu", size=12, weight="bold")

        # Labels e Entradas
        tk.Label(self.login_frame, text="Nome de Usuário", bg="#3073b7", fg="black", font=bold_font, width=20).grid(row=0, column=0, pady=10, padx=10)
        self.username_entry = tk.Entry(self.login_frame, width=20, font='arial 14 bold', selectbackground='#f37107', selectborderwidth=8, selectforeground='white')
        self.username_entry.grid(row=0, column=1, pady=10, padx=10)
        

        tk.Label(self.login_frame, text="Senha", bg="#3073b7", fg="black", font=bold_font).grid(row=1, column=0, pady=10, padx=10)
        self.password_entry = tk.Entry(self.login_frame, show="*", width=20, font='arial 14 bold', selectbackground='#f37107', selectborderwidth=8, selectforeground='white')
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)

        # Botões
        button_frame = tk.Frame(self.login_frame, bg="#3073b7")
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        self.login_button = tk.Button(button_frame, text="Login", command=self.login, bg="#f37107", fg="white", font=regular_font)
        self.login_button.pack(side=tk.LEFT, padx=10)

        self.signup_button = tk.Button(button_frame, text="Cadastre-se", command=self.create_signup_screen, bg="#f37107", fg="white",  font=regular_font)
        self.signup_button.pack(side=tk.LEFT, padx=10)

        self.forgot_password_button = tk.Button(self.login_frame, text="Esqueceu sua senha?", command=self.create_forgot_password_screen, bg="#f37107", fg="white",  font=regular_font)
        self.forgot_password_button.grid(row=3, column=0, columnspan=2, pady=10)

    def create_signup_screen(self):
        # Placeholder for signup screen
        pass

    def create_forgot_password_screen(self):
        # Placeholder for forgot password screen
        pass

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
        user = bd.autenticar_usuario(username, password)
        if user:
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
            bd.redefinir_senha(email, new_password)
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
            if bd.cadastrar_usuario(username, email, password):
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
