import pandas as pd
import tkinter as tk
from tkinter import ttk

def search_data(*args):
    keyword = search_var.get().lower()  # Obtém o texto digitado e converte para minúsculas

    # Limpa a exibição atual do TreeView
    tree.delete(*tree.get_children())

    # Filtra os dados com base na palavra-chave digitada
    for index, row in df.iterrows():
        if any(keyword in str(value).lower() for value in row):
            tree.insert('', 'end', values=row.tolist())

# Cria a janela principal
root = tk.Tk()
df = pd.read_csv("Apostas.csv")

# Cria uma variável de controle para rastrear as alterações no Entry
search_var = tk.StringVar()

# Cria um Entry para a pesquisa
search_entry = tk.Entry(root, textvariable=search_var)
search_entry.pack()

# Vincula a função de pesquisa ao evento de alteração na variável
search_var.trace('w', search_data)

# Cria um TreeView para exibir os dados filtrados
tree = ttk.Treeview(root, columns=df.columns, show='headings')
tree.pack()

# Define os cabeçalhos das colunas
for col in df.columns:
    if col in tree['columns']:
        tree.heading(col, text=col)


# Insere os dados iniciais no TreeView
for index, row in df.iterrows():
    tree.insert('', 'end', values=row.tolist())

# Inicia o loop principal da janela
root.mainloop()
