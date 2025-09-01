import tkinter as tk
from tkinter import messagebox
import sqlite3

# --- 1. Lógica do Banco de Dados ---

def conectar_banco():
    """Conecta ao banco de dados 'escola.db' e cria a tabela 'alunos' se ela não existir."""
    conn = sqlite3.connect('escola.db')
    cursor = conn.cursor()
    # Cria a tabela 'alunos' com colunas para ID, nome, idade e série
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER,
            serie TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn, cursor

def inserir_aluno(nome, idade, serie):
    """Insere um novo aluno na tabela."""
    conn, cursor = conectar_banco()
    try:
        # A ? funciona como um placeholder para evitar injeção de SQL
        cursor.execute("INSERT INTO alunos (nome, idade, serie) VALUES (?, ?, ?)",
                       (nome, idade, serie))
        conn.commit()
        messagebox.showinfo("Sucesso", f"Aluno {nome} cadastrado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
    finally:
        conn.close()

def visualizar_alunos():
    """Busca e retorna todos os alunos cadastrados."""
    conn, cursor = conectar_banco()
    cursor.execute("SELECT * FROM alunos")
    registros = cursor.fetchall()
    conn.close()
    return registros

# --- 2. Funções da Interface Gráfica ---

def cadastrar_aluno():
    """Função chamada pelo botão 'Cadastrar'."""
    nome = entry_nome.get()
    idade = entry_idade.get()
    serie = entry_serie.get()

    # Validação simples dos campos
    if not nome or not idade or not serie:
        messagebox.showwarning("Atenção", "Todos os campos são obrigatórios.")
        return
    
    try:
        idade = int(idade)
    except ValueError:
        messagebox.showerror("Erro", "A idade deve ser um número inteiro.")
        return

    inserir_aluno(nome, idade, serie)
    limpar_campos()
    atualizar_lista()

def atualizar_lista():
    """Função para atualizar a lista exibida na caixa de texto."""
    # Limpa a caixa de texto antes de adicionar os novos dados
    lista_alunos_text.config(state=tk.NORMAL)
    lista_alunos_text.delete(1.0, tk.END)
    
    alunos = visualizar_alunos()
    if not alunos:
        lista_alunos_text.insert(tk.END, "Nenhum aluno cadastrado.")
    else:
        for aluno in alunos:
            lista_alunos_text.insert(tk.END, f"ID: {aluno[0]} | Nome: {aluno[1]} | Idade: {aluno[2]} | Série: {aluno[3]}\n")
    
    lista_alunos_text.config(state=tk.DISABLED) # Impede a edição

def limpar_campos():
    """Limpa o conteúdo dos campos de entrada."""
    entry_nome.delete(0, tk.END)
    entry_idade.delete(0, tk.END)
    entry_serie.delete(0, tk.END)

# --- 3. Configuração da Janela Principal (Tkinter) ---

# Cria a janela principal
root = tk.Tk()
root.title("Cadastro de Alunos")

# Cria um frame para organizar os widgets de entrada
frame_campos = tk.Frame(root)
frame_campos.pack(padx=20, pady=10)

# Labels e Entrys (campos de texto)
tk.Label(frame_campos, text="Nome do Aluno:").grid(row=0, column=0, sticky="w", pady=5)
entry_nome = tk.Entry(frame_campos, width=40)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_campos, text="Idade:").grid(row=1, column=0, sticky="w", pady=5)
entry_idade = tk.Entry(frame_campos, width=40)
entry_idade.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_campos, text="Série:").grid(row=2, column=0, sticky="w", pady=5)
entry_serie = tk.Entry(frame_campos, width=40)
entry_serie.grid(row=2, column=1, padx=5, pady=5)

# Botão de Cadastro
btn_cadastrar = tk.Button(root, text="Cadastrar Aluno", command=cadastrar_aluno)
btn_cadastrar.pack(pady=10)

# Caixa de texto para exibir a lista de alunos
lista_alunos_text = tk.Text(root, height=15, width=60, bd=2, relief="groove")
lista_alunos_text.pack(padx=20, pady=10)

# --- Início do Programa ---
conectar_banco()  # Garante que o banco e a tabela existam desde o início
atualizar_lista() # Carrega os alunos existentes ao abrir o programa
root.mainloop()   # Inicia o loop principal da interface 