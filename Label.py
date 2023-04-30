# Função chamada ao clicar com o botão esquerdo em uma linha do Treeview
def show_menu(event):
    item = tabela.identify_row(event.y)  # Identifica a linha clicada
    if item:  # Verifica se uma linha foi clicada
        menu.post(event.x_root, event.y_root)  # Exibe o menu na posição do clique

# Criação do menu com markbox
menu = tk.Menu(tabela, tearoff=0)
menu.add_checkbutton(label="Correta", variable=tk.BooleanVar())
menu.add_checkbutton(label="Neutra", variable=tk.BooleanVar())
menu.add_checkbutton(label="Incorreta", variable=tk.BooleanVar())
menu.add_checkbutton(label="Parcialmente Positiva", variable=tk.BooleanVar())
menu.add_checkbutton(label="Parcialmente Negativa", variable=tk.BooleanVar())

# Associa o evento de clique com a função do menu
tabela.bind('<Button-1>', show_menu)