import sqlite3
from datetime import datetime
import hashlib

def conectar(banco):
    return sqlite3.connect(f'{estoque}.db')

def criar_tabelas(banco):
    conn = conectar(banco)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS estoque (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        data_ultima_modificacao TEXT NOT NULL,
        userid INTEGER NOT NULL,
        FOREIGN KEY (userid) REFERENCES usuarios (id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_usuario TEXT NOT NULL,
        senha TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def inserir_usuario(banco, nome_usuario, senha):
    conn = conectar(banco)
    cursor = conn.cursor()
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    cursor.execute('''
    INSERT INTO usuarios (nome_usuario, senha)
    VALUES (?, ?)
    ''', (nome_usuario, senha_hash))
    conn.commit()
    conn.close()

def autenticar_usuario(banco, nome_usuario, senha):
    conn = conectar(banco)
    cursor = conn.cursor()
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    cursor.execute('''
    SELECT * FROM usuarios WHERE nome_usuario = ? AND senha = ?
    ''', (nome_usuario, senha_hash))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

def inserir_item(banco, item, quantidade, userid):
    conn = conectar(banco)
    cursor = conn.cursor()
    data_ultima_modificacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
    INSERT INTO estoque (item, quantidade, data_ultima_modificacao, userid)
    VALUES (?, ?, ?, ?)
    ''', (item, quantidade, data_ultima_modificacao, userid))
    conn.commit()
    conn.close()

def listar_itens(banco):
    conn = conectar(banco)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM estoque')
    itens = cursor.fetchall()
    conn.close()
    return itens

def atualizar_item(banco, id, item, quantidade, userid):
    conn = conectar(banco)
    cursor = conn.cursor()
    data_ultima_modificacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
    UPDATE estoque
    SET item = ?, quantidade = ?, data_ultima_modificacao = ?, userid = ?
    WHERE id = ?
    ''', (item, quantidade, data_ultima_modificacao, userid, id))
    conn.commit()
    conn.close()

def deletar_item(banco, id):
    conn = conectar(banco)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM estoque WHERE id = ?', (id,))
    conn.commit()
    conn.close()