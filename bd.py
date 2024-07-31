import sqlite3
import random
import string
import hashlib
import datetime

def conectar(categoria):
    conn = sqlite3.connect(f'{categoria}.db')
    return conn

def criar_tabelas(categoria):
    conn = conectar(categoria)
    cursor = conn.cursor()

    # Criação da tabela de estoque
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS estoque (
        id INTEGER PRIMARY KEY,
        item TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        data_modificacao TEXT NOT NULL,
        nome_usuario TEXT NOT NULL
    )
    ''')

    # Criação da tabela de usuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

def gerar_id_unico():
    return ''.join(random.choices(string.digits, k=6))

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def inserir_item(categoria, item, quantidade, username):
    conn = conectar(categoria)
    cursor = conn.cursor()
    data_modificacao = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item_id = gerar_id_unico()
    cursor.execute('INSERT INTO estoque (id, item, quantidade, data_modificacao, nome_usuario) VALUES (?, ?, ?, ?, ?)', (item_id, item, quantidade, data_modificacao, username))
    conn.commit()
    conn.close()

def deletar_item(categoria, item_id):
    conn = conectar(categoria)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM estoque WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

def atualizar_item(categoria, item_id, item, quantidade, username):
    conn = conectar(categoria)
    cursor = conn.cursor()
    data_modificacao = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('UPDATE estoque SET item = ?, quantidade = ?, data_modificacao = ?, nome_usuario = ? WHERE id = ?', (item, quantidade, data_modificacao, username, item_id))
    conn.commit()
    conn.close()

def listar_itens(categoria):
    conn = conectar(categoria)
    cursor = conn.cursor()
    cursor.execute('SELECT id, item, quantidade, data_modificacao, nome_usuario FROM estoque')
    itens = cursor.fetchall()
    conn.close()
    return itens

def autenticar_usuario(categoria, username, senha):
    conn = conectar(categoria)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE username = ? AND senha = ?', (username, hash_senha(senha)))
    user = cursor.fetchone()
    conn.close()
    return user

def cadastrar_usuario(categoria, username, email, senha):
    conn = conectar(categoria)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO usuarios (username, email, senha) VALUES (?, ?, ?)', (username, email, hash_senha(senha)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def redefinir_senha(categoria, email, nova_senha):
    conn = conectar(categoria)
    cursor = conn.cursor()
    cursor.execute('UPDATE usuarios SET senha = ? WHERE email = ?', (hash_senha(nova_senha), email))
    conn.commit()
    conn.close()
