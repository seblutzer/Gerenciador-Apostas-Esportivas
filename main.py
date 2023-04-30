import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from tkintertable import TableCanvas, TableModel
import datetime
import json
import csv
import os.path
import os
from ttkthemes import ThemedTk
import tkinter.colorchooser as colorchooser
import pandas as pd
from IPython.display import display
import ipywidgets as widgets


# cria uma janela
#janela = tk.Tk()
#style = ttk.Style()
#style.theme_use('clam')

janela = ThemedTk(theme="marine")

# Cria o frame
frameJogo = tk.Frame(janela, padx=10, pady=10)
frameJogo.grid(row=0, column=0)

frameApostas = tk.Frame(janela)
frameApostas.grid(row=4, column=0)

frameGravar = tk.Frame(janela)
frameGravar.grid(row=7, column=0)

frameTabela = tk.Frame(janela)
frameTabela.grid(row=8, column=0)

# Define uma imagem para o botão de configurações
settings_icon = tk.PhotoImage(file="/Users/sergioeblutzer/PycharmProjects/Gerenciamento_Bolsa_Esportiva/engrenagens.png").subsample(20, 20)
settings_button = tk.Button(frameJogo, image=settings_icon, bd=0) # Ajustes Iniciais

# Verifica se o arquivo CSV existe
if not os.path.isfile("Apostas.csv"):
    with open("Apostas.csv", "w", newline="") as f:
        colunas = ["id", "time_casa", "time_fora", "dia", "mes", "ano", "hora", "minuto", "bethouse1", "mercado1", "valor1", "odd1", "aposta1", "resultado1", "bethouse2", "mercado2", "valor2", "odd2", "aposta2", "resultado2", "bethouse3", "mercado3", "valor3", "odd3", "aposta3", "resultado3", "lucro_estimado", "lucro_per_estimado", "lucroReal", "lucro_perReal"]
        csv.writer(f).writerow(colunas)

df_tabela = pd.read_csv("Apostas.csv")
print(df_tabela)

def load_options():
    global bethouse_options, mercado_options, arred_var
    try:
        with open('bethouse_options.json', 'r') as f:
            data = json.load(f)
            bethouse_options = data.get("bethouse_options", {})
            mercado_options = data.get("mercado_options", [])
            arred_var = tk.DoubleVar(value=data.get("arredondamento"))
    except FileNotFoundError:
        bethouse_options = {}
        mercado_options = []
        arred_var = tk.DoubleVar(value=0.01)
        pass
load_options()

def open_bethouses():
    # Cria uma janela pop-up
    bethouses_window = tk.Toplevel(frameJogo)
    bethouses_window.title("BetHouses e Mercados")
    bethouses_frame = tk.Frame(bethouses_window)
    bethouses_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

    # Cria a entrada de texto para adicionar novas BetHouses
    bethouse_label = tk.Label(bethouses_frame, text='BetHouse:')
    bethouse_label.grid(row=0, column=0, padx=5, pady=5)
    new_bethouse_entry = tk.Entry(bethouses_frame)
    new_bethouse_entry.grid(row=0, column=1, padx=5, pady=5)

    # Cria um widget Label para o título 'Taxa:'
    def validate_rate_input(new_value):
        if not new_value.startswith('0.0'):
            return False
        if not new_value[2:]:
            return True
        try:
            float(new_value[2:])
        except ValueError:
            return False
        if new_value.count('.') > 1:
            return False
        if '.' in new_value:
            decimal_part = new_value.split('.')[1]
            if len(decimal_part) > 3:
                return False
        return True

    rate_label = tk.Label(bethouses_frame, text='Taxa:')
    rate_label.grid(row=1, column=0, padx=5, pady=5)
    vcmd_tax = (bethouses_frame.register(validate_rate_input), '%P')
    new_rate_entry = tk.Entry(bethouses_frame, validate='key', validatecommand=vcmd_tax)
    new_rate_entry.insert(0, '0.0')
    new_rate_entry.grid(row=1, column=1, padx=5, pady=5)

    # Cria uma função para adicionar uma nova BetHouse à lista
    def add_bethouse():
        new_bethouse = new_bethouse_entry.get()
        if not new_bethouse:
            tk.messagebox.showwarning("Aviso", "Dê o nome da BetHouse")
            return
        new_bethouse = new_bethouse_entry.get().strip()
        new_rate = float(new_rate_entry.get().strip()) if new_rate_entry.get().strip() != "" else 0.0
        text_color = text_color_entry.get().strip()
        background_color = background_color_entry.get().strip()
        bethouse_options[new_bethouse] = {
            'taxa': new_rate,
            'text_color': text_color,
            'background_color': background_color
        }
        new_bethouse_entry.delete(0, tk.END)
        new_rate_entry.delete(0, tk.END)
        text_color_entry.delete(0, tk.END)
        background_color_entry.delete(0, tk.END)
        save_bethouse_options()
        update_bethouses_list()
          # Salva os dados em um arquivo JSON

    #Criar funções para escolher cor de texto e fundo
    def choose_text_color():
        color = colorchooser.askcolor()[1]
        if color:
            text_color_button.configure(bg=color)
            text_color_entry.delete(0, tk.END)
            text_color_entry.insert(0, color)

    def choose_background_color():
        color = colorchooser.askcolor()[1]
        if color:
            background_color_button.configure(bg=color)
            background_color_entry.delete(0, tk.END)
            background_color_entry.insert(0, color)

    # Cria campos de entrada para a cor do texto e cor de fundo
    text_color_entry = tk.Entry(bethouses_frame)
    background_color_entry = tk.Entry(bethouses_frame)

    # Cria botões para seleção de cor de texto e cor de fundo
    text_color_button = tk.Button(bethouses_frame, text='Cor do Texto', command=choose_text_color)
    text_color_button.grid(row=2, column=0, padx=5, pady=5)

    background_color_button = tk.Button(bethouses_frame, text='Cor de Fundo', command=choose_background_color)
    background_color_button.grid(row=2, column=1, padx=5, pady=5)

    # Cria botão para adicionar a nova BetHouse
    add_bethouse_button = tk.Button(bethouses_frame, text="Adicionar", command=add_bethouse)
    add_bethouse_button.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

    # Cria a lista de BetHouses
    configStyle = ttk.Style()
    configStyle.configure("Normal.Treeview", rowheight=20)
    bethouses_list = sorted(bethouse_options.keys())
    bethouses_tree = ttk.Treeview(bethouses_frame, columns=('Bethouse', 'Taxa'), show='headings', style="Normal.Treeview")
    bethouses_tree.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    bethouses_tree.heading('Bethouse', text='Bethouse')
    bethouses_tree.heading('Taxa', text='Taxa')
    for bethouse in bethouses_list:
        taxa = float(bethouse_options[bethouse]["taxa"])
        bethouses_tree.insert('', 'end', values=(bethouse, f"{taxa:.3f}"), tags=(bethouse,))
        bethouses_tree.tag_configure(bethouse, background=bethouse_options[bethouse]['background_color'], foreground=bethouse_options[bethouse]['text_color'])

    def on_double_click(event):
        selected_item = bethouses_tree.selection()[0]
        selected_bethouse = bethouses_tree.item(selected_item)['values'][0]
        taxa = bethouse_options[selected_bethouse]["taxa"]
        text_color = bethouse_options[selected_bethouse]["text_color"]
        background_color = bethouse_options[selected_bethouse]["background_color"]
        new_bethouse_entry.delete(0, tk.END)
        new_bethouse_entry.insert(0, selected_bethouse)
        new_rate_entry.delete(0, tk.END)
        new_rate_entry.insert(0, f"{taxa:.3f}"[3:])
        text_color_entry.delete(0, tk.END)
        text_color_entry.insert(0, text_color)
        background_color_entry.delete(0, tk.END)
        background_color_entry.insert(0, background_color)

    bethouses_tree.bind('<Double-1>', on_double_click)

    # Cria uma função para remover a BetHouse selecionada da lista
    def remove_bethouse():
        selected_item = bethouses_tree.selection()[0]
        selected_bethouse = bethouses_tree.item(selected_item)['values'][0]
        del bethouse_options[selected_bethouse]
        update_bethouses_list()
        save_bethouse_options()  # Salva os dados em um arquivo JSON

    # Cria um botão para remover a BetHouse selecionada
    remove_bethouse_button = tk.Button(bethouses_frame, text="Remover", command=remove_bethouse)
    remove_bethouse_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    # Cria uma função para atualizar a lista de BetHouses
    def update_bethouses_list():
        # Atualiza as opções do combobox
        bethouse_combobox['values'] = sorted(list(bethouse_options.keys()), key=lambda x: x[0])
        bethouse_combobox2['values'] = sorted(list(bethouse_options.keys()), key=lambda x: x[0])
        bethouse_combobox3['values'] = sorted(list(bethouse_options.keys()), key=lambda x: x[0])
        # Limpa a Treeview
        bethouses_tree.delete(*bethouses_tree.get_children())
        # Cria uma nova lista com as BetHouses e suas taxas
        bethouses_list = sorted(bethouse_options.keys())
        # Adiciona as BetHouses à Treeview
        for bethouse in bethouses_list:
            taxa = float(bethouse_options[bethouse]["taxa"])
            bethouses_tree.insert('', 'end', values=(bethouse, f"{taxa:.3f}"), tags=(bethouse,))
            bethouses_tree.tag_configure(bethouse, background=bethouse_options[bethouse]['background_color'], foreground=bethouse_options[bethouse]['text_color'])

    # Chama a função para atualizar a lista de BetHouses
    update_bethouses_list()

    def add_mercado_option():
        new_option = new_mercado_entry.get()
        if not new_option:
            tk.messagebox.showwarning("Aviso", "Dê o nome da opção de mercado")
            return
        mercado_options.append(new_option)
        new_mercado_entry.delete(0, tk.END)
        save_bethouse_options()
        update_mercado_options_list()

    # Cria a entrada de texto para adicionar novas opções de mercado
    mercado_label = tk.Label(bethouses_frame, text='Mercado:')
    mercado_label.grid(row=1, column=3, padx=5, pady=5)
    new_mercado_entry = tk.Entry(bethouses_frame)
    new_mercado_entry.grid(row=1, column=4, padx=5, pady=5)

    # Cria um botão para adicionar a nova opção de mercado
    add_mercado_button = tk.Button(bethouses_frame, text="Adicionar", command=add_mercado_option)
    add_mercado_button.grid(row=2, column=3, columnspan=2, padx=5, pady=5)

    # Cria a lista de opções de mercado
    mercado_options_list = sorted(list(mercado_options), key=lambda x: x[0])
    # Adiciona as BetHouses à Listbox
    mercado_options_listbox = tk.Listbox(bethouses_frame)
    mercado_options_listbox.grid(row=3, column=3, columnspan=2, padx=5, pady=5)
    for mercado in mercado_options_list:
        mercado_options_listbox.insert(tk.END, f"{mercado}")

    # Função para remover a opção de mercado selecionada
    def remove_mercado_option():
        selected_option = mercado_options_listbox.get(tk.ACTIVE)
        mercado_options.remove(selected_option)
        save_bethouse_options()
        update_mercado_options_list()

    # Cria um botão para remover a opção de mercado selecionada
    remove_mercado_button = tk.Button(bethouses_frame, text="Remover", command=remove_mercado_option)
    remove_mercado_button.grid(row=4, column=3, columnspan=2, padx=5, pady=5)

    # Cria uma função para atualizar a lista de BetHouses
    def update_mercado_options_list():
        # Atualiza as opções do combobox
        mercado_combobox['values'] = sorted(list(mercado_options), key=lambda x: x[0])
        mercado_combobox2['values'] = sorted(list(mercado_options), key=lambda x: x[0])
        mercado_combobox3['values'] = sorted(list(mercado_options), key=lambda x: x[0])
        # Limpa a Listbox
        mercado_options_listbox.delete(0, tk.END)
        # Cria uma nova lista com os mercados
        mercado_options_list = sorted(list(mercado_options), key=lambda x: x[0])
        # Adiciona as BetHouses à Listbox
        for mercado in mercado_options_list:
            mercado_options_listbox.insert(tk.END, f"{mercado}")
    # Chama a função para atualizar a lista de BetHouses
    update_bethouses_list()

# Cria um menu pop-up com as opções desejadas
settings_menu = tk.Menu(frameJogo, tearoff=False)
settings_menu.add_command(label="Personalizar", command=open_bethouses)
settings_menu.add_command(label="Finanças")
settings_menu.add_separator()
settings_menu.add_command(label="Sair", command=frameJogo.quit)

# Define a ação do botão de configurações para mostrar o menu pop-up
def show_settings_menu(event):
    settings_menu.tk_popup(event.x, event.y)

# Associa a ação do botão de configurações ao clique do mouse
settings_button.bind("<Button-1>", show_settings_menu)

# Coloca o botão de configurações no row 0 colunm 0 da janela principal
settings_button.grid(row=0, column=0, sticky="w") # Menu de Configurações

# Botão Arredondamento
def save_bethouse_options():
    sorted_bethouse_options = dict(sorted(bethouse_options.items(), key=lambda x: x[0]))
    sorted_mercado_options = sorted(mercado_options, key=lambda x: x[0])
    arredondamento = arred_var.get()
    data = {"bethouse_options": sorted_bethouse_options, "mercado_options": sorted_mercado_options, "arredondamento": arredondamento}
    with open('bethouse_options.json', 'w') as f:
        json.dump(data, f, sort_keys=True)

def arredondamento_changed(event):
    save_bethouse_options()

arred_label = tk.Label(frameJogo, text="Arredondamento")
arred_label.grid(row=3, column=0)
arred_options = [0.01, 0.05, 0.1, 0.5, 1]
arred_combobox = ttk.Combobox(frameJogo, textvariable=arred_var, values=arred_options, width=3, state="readonly")
arred_combobox.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W)
arred_combobox.bind("<<ComboboxSelected>>", arredondamento_changed) # Arredondar

#Adicionar Ano
def validate_year(text):
    if len(text) < 2:
        return False
    if text.isdigit() or text == "":
        if len(text) != 4:
            return False
        if text == "":
            return True
        current_year = datetime.date.today().year
        if int(text) < 1900 or int(text) > current_year:
            return False
    else:
        return False
    return True
def update_year_combobox(event):
    current_input = ano_var.get()
    matching_options = [str(opt) for opt in opcoes_anos]
    if len(current_input) < 2:
        ano_var.set(str(datetime.date.today().year)[:len(current_input)])
        return
    for i, char in enumerate(current_input):
        if not any(len(opt) > i for opt in matching_options):
            ano_var.set(current_input[:-1])
            return
        allowed_chars = [opt[i] for opt in matching_options if len(opt) > i]
        if char not in allowed_chars:
            ano_var.set(current_input[:-1])
            return
        matching_options = [opt for opt in matching_options if opt.startswith(current_input[:i+1])]
    ano_combobox['values'] = matching_options
    if len(matching_options) == 1:
        ano_var.set(matching_options[0])
        ano_combobox.icursor(tk.END)
opcoes_anos = [datetime.date.today().year - 1, datetime.date.today().year, datetime.date.today().year + 1]
ano_var = tk.StringVar(value=datetime.date.today().year)
ano_combobox = ttk.Combobox(frameJogo, textvariable=ano_var, values=opcoes_anos, width=4)
ano_combobox.bind('<KeyRelease>', update_year_combobox)
ano_combobox.grid(row=2, column=4, padx=5, pady=5, sticky=tk.W) # Ano

# Adiciona campo Jogo
jogo_label = tk.Label(frameJogo, text="Jogo")
jogo_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
jogo_entry = tk.Entry(frameJogo)
jogo_entry.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W) # Jogo

# Adiciona campo Data
def validate_day(text):
    if text.isdigit() or text == "":
        if len(text) > 2:
            return False
        if text == "":
            return True
        if int(text) < 1 or int(text) > 31:
            return False
    else:
        return False
    return True
data_label = tk.Label(frameJogo, text="Data")
data_label.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W)

# Configurar o box dia
dia_entry = tk.Entry(frameJogo, width=2, validate="key", validatecommand=(frameJogo.register(validate_day), "%P"))
dia_atual = datetime.date.today().day
dia_entry.insert(0, dia_atual)
dia_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W) # Dia

# Configurar o box mês
def validate_month(text):
    if text in mes_options:
        return True
    else:
        return False
def update_combobox(event):
    current_input = mes_combobox.get()
    matching_options = [opt for opt in mes_options if opt.startswith(current_input)]
    if len(matching_options) > 0:
        new_option = matching_options[0]
        mes_combobox.set(new_option)
        mes_combobox.icursor(len(current_input))
    else:
        mes_combobox.set("")
        mes_combobox.icursor(0)
mes_options = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
mes_atual = datetime.datetime.now().strftime('%b')
mes_atual_pt = {'Jan': 'Jan', 'Feb': 'Fev', 'Mar': 'Mar', 'Apr': 'Abr', 'May': 'Mai', 'Jun': 'Jun', 'Jul': 'Jul', 'Aug': 'Ago', 'Sep': 'Set', 'Oct': 'Out', 'Nov': 'Nov', 'Dec': 'Dez'}[mes_atual]
mes_combobox = ttk.Combobox(frameJogo, values=mes_options, width=3, validate="key", validatecommand=(frameJogo.register(validate_month), "%P"))
if mes_atual_pt in mes_options:
    mes_combobox.current(mes_options.index(mes_atual_pt))
else:
    mes_combobox.set(mes_options[0])
mes_combobox.bind("<KeyRelease>", update_combobox)
mes_combobox.grid(row=2, column=3, padx=5, pady=5, sticky=tk.W) # Mês

def validate_hour(text):
    if text.isdigit() or text == "":
        if len(text) > 2:
            return False
        if text == "":
            return True
        if int(text) < 0 or int(text) > 23:
            return False
    else:
        return False
    return True
# Configurar o box Hora
hora_label = tk.Label(frameJogo, text="Hora")
hora_label.grid(row=1, column=5)
hora_entry = tk.Entry(frameJogo, width=2, validate="key", validatecommand=(frameJogo.register(validate_hour), "%P"))
hora_entry.insert(0, 12)
hora_entry.grid(row=2, column=5, padx=5, pady=5, sticky=tk.W)
doispontos_label = tk.Label(frameJogo, text=":")
doispontos_label.grid(row=2, column=6) # Hora

def validate_minute(text):
    if text.isdigit() or text == "":
        if len(text) > 2:
            return False
        if text == "":
            return True
        if int(text) < 0 or int(text) > 59:
            return False
    else:
        return False
    return True
# Configurar o box minuto
minuto_entry = tk.Entry(frameJogo, width=2, validate="key", validatecommand=(frameJogo.register(validate_minute), "%P"), justify="right")
minuto_entry.insert(0, "00")
minuto_entry.grid(row=2, column=7, padx=5, pady=5, sticky=tk.W) # Minuto

# Adiciona campo BetHouse
def validate_bethouse(text):
    return text in bethouse_options.keys() or not text
def update_bethouse_combobox(event):
    current_input = bethouse_var.get()
    matching_options = list(bethouse_options.keys())
    for i, char in enumerate(current_input):
        if not any(len(opt) > i for opt in matching_options):
            bethouse_var.set(current_input[:-1])
            return
        allowed_chars = [opt[i].upper() for opt in matching_options if len(opt) > i]
        if char.upper() not in allowed_chars:
            bethouse_var.set(current_input[:-1])
            return
        matching_options = [opt for opt in matching_options if opt.lower().startswith(current_input[:i+1].lower())]
    bethouse_combobox['values'] = matching_options
    if len(matching_options) == 1:
        bethouse_var.set(matching_options[0])
        bethouse_combobox.icursor(tk.END)
def on_select1(value):
    selected_bethouse = bethouse_var.get()
    text_color = bethouse_options[selected_bethouse]['text_color']
    background_color = bethouse_options[selected_bethouse]['background_color']
    bethouse_combobox.configure(foreground=text_color, background=background_color)
    valor_entry.configure(fg=text_color, bg=background_color)
    odd_entry.configure(fg=text_color, bg=background_color)
    aposta_entry.configure(fg=text_color, bg=background_color)
    #frameApostas.configure(bg=bethouse_options.get(bethouse_var.get(), {}).get('background_color', None))

bethouse_label = tk.Label(frameApostas, text="BetHouse")
bethouse_label.grid(row=1, column=9)
bethouse_var = tk.StringVar(value=None)
bethouse_combobox = ttk.Combobox(frameApostas, textvariable=bethouse_var, values=list(bethouse_options.keys()), width=7)
bethouse_combobox.bind("<KeyRelease>", update_bethouse_combobox)
bethouse_combobox.bind("<FocusOut>", on_select1)
bethouse_combobox.bind("<<ComboboxSelected>>", on_select1)
bethouse_combobox.grid(row=2, column=9, padx=5, pady=5, sticky=tk.W) # BetHouse 1

def update_bethouse_combobox2(event):
    current_input = bethouse_var2.get()
    matching_options = list(bethouse_options.keys())
    for i, char in enumerate(current_input):
        if not any(len(opt) > i for opt in matching_options):
            bethouse_var2.set(current_input[:-1])
            return
        allowed_chars = [opt[i].upper() for opt in matching_options if len(opt) > i]
        if char.upper() not in allowed_chars:
            bethouse_var2.set(current_input[:-1])
            return
        matching_options = [opt for opt in matching_options if opt.lower().startswith(current_input[:i + 1].lower())]
    bethouse_combobox2['values'] = matching_options
    if len(matching_options) == 1:
        bethouse_var2.set(matching_options[0])
        bethouse_combobox2.icursor(tk.END)
def on_select2(value):
    selected_bethouse = bethouse_var2.get()
    text_color = bethouse_options[selected_bethouse]['text_color']
    background_color = bethouse_options[selected_bethouse]['background_color']
    bethouse_combobox2.configure(foreground=text_color, background=background_color)
    valor_entry2.configure(fg=text_color, bg=background_color)
    odd_entry2.configure(fg=text_color, bg=background_color)
    aposta_entry2.configure(fg=text_color, bg=background_color)
bethouse_var2 = tk.StringVar(value=None)
bethouse_combobox2 = ttk.Combobox(frameApostas, textvariable=bethouse_var2, values=list(bethouse_options.keys()), width=7)
bethouse_combobox2.bind("<KeyRelease>", update_bethouse_combobox2)
bethouse_combobox2.bind("<<FocusOut>>", on_select2)
bethouse_combobox2.bind("<<ComboboxSelected>>", on_select2)
bethouse_combobox2.grid(row=3, column=9, padx=5, pady=5, sticky=tk.W) # BetHouse 2

# cria o botão de alternância
num_bets = 2
def alternar_bets():
    global num_bets
    if num_bets == 2:
        num_bets = 3
        bethouse_combobox3.grid(row=4, column=9, padx=5, pady=5, sticky=tk.W)
        mercado_combobox3.grid(row=4, column=10, padx=5, pady=5, sticky=tk.W)
        valor_entry3.grid(row=4, column=11, padx=5, pady=5, sticky=tk.W)
        odd_entry3.grid(row=4, column=12, padx=5, pady=5, sticky=tk.W)
        real_label3.grid(row=4, column=13)
        aposta_entry3.grid(row=4, column=14, padx=5, pady=5, sticky=tk.W)
        palpite3_label.grid(row=4, column=15)
        lucro3_label.grid(row=4, column=16)
    else:
        num_bets = 2
        bethouse_var3.set("")  # Reverte para o valor inicial
        mercado_var3.set("")
        valor_var3.set("")
        odd_var3.set(0.0)
        aposta_var3.set(0.0)
        bethouse_combobox3.grid_remove()
        mercado_combobox3.grid_remove()
        valor_entry3.grid_remove()
        odd_entry3.grid_remove()
        real_label3.grid_remove()
        aposta_entry3.grid_remove()
        palpite3_label.grid_remove()
        lucro3_label.grid_remove()

alternar_bets_btn = tk.Button(frameJogo, text="Triplo", command=alternar_bets)
alternar_bets_btn.grid(row=3, column=5, columnspan=4) # Add 3ª Aposta

def update_bethouse_combobox3(event):
    current_input = bethouse_var3.get()
    matching_options = list(bethouse_options.keys())
    for i, char in enumerate(current_input):
        if not any(len(opt) > i for opt in matching_options):
            bethouse_var3.set(current_input[:-1])
            return
        allowed_chars = [opt[i].upper() for opt in matching_options if len(opt) > i]
        if char.upper() not in allowed_chars:
            bethouse_var3.set(current_input[:-1])
            return
        matching_options = [opt for opt in matching_options if opt.lower().startswith(current_input[:i + 1].lower())]
    bethouse_combobox3['values'] = matching_options
    if len(matching_options) == 1:
        bethouse_var3.set(matching_options[0])
        bethouse_combobox3.icursor(tk.END)
def on_select3(value):
    selected_bethouse = bethouse_var3.get()
    text_color = bethouse_options[selected_bethouse]['text_color']
    background_color = bethouse_options[selected_bethouse]['background_color']
    bethouse_combobox3.configure(foreground=text_color, background=background_color)
    valor_entry3.configure(fg=text_color, bg=background_color)
    odd_entry3.configure(fg=text_color, bg=background_color)
    aposta_entry3.configure(fg=text_color, bg=background_color)
bethouse_var3 = tk.StringVar(value=None)
bethouse_combobox3 = ttk.Combobox(frameApostas, textvariable=bethouse_var3, values=list(bethouse_options.keys()), width=7)
bethouse_combobox3.bind("<KeyRelease>", update_bethouse_combobox3) # BetHouse 3
bethouse_combobox3.bind("<<FocusOut>>", on_select3)
bethouse_combobox3.bind("<<ComboboxSelected>>", on_select3) # BetHouse 3

# Adiciona campo Mercado
def validate_mercado(text):
    return text in mercado_options or not text

def update_mercado_combobox(event):
    current_input = mercado_var.get()
    matching_options = list(mercado_options)
    for i, char in enumerate(current_input):
        if not any(len(opt) > i for opt in matching_options):
            mercado_var.set(current_input[:-1])
            return
        allowed_chars = [opt[i].upper() for opt in matching_options if len(opt) > i]
        if char.upper() not in allowed_chars:
            mercado_var.set(current_input[:-1])
            return
        matching_options = [opt for opt in matching_options if opt.lower().startswith(current_input[:i+1].lower())]
    mercado_combobox['values'] = matching_options
    if len(matching_options) == 1:
        mercado_var.set(matching_options[0])
        mercado_combobox.icursor(tk.END)

mercado_label = tk.Label(frameApostas, text="Mercado")
mercado_label.grid(row=1, column=10)

mercado_var = tk.StringVar(value=None)
mercado_combobox = ttk.Combobox(frameApostas, textvariable=mercado_var, values=mercado_options, width=7)
mercado_combobox.bind("<KeyRelease>", lambda event: (update_mercado_combobox(event), update_columns()))
mercado_combobox.grid(row=2, column=10, padx=5, pady=5, sticky=tk.W) # Mercado 1

# Adiciona campo Valor
def on_validate_valor(P):
    if not P:
        return True
    P = P.replace(',', '.')
    if not P.replace('.', '', 1).isdigit():
        return False
    if len(P.split('.')[0]) > 3:
        return False
    if '.' in P and len(P.split('.')[1]) > 2:
        return False
    return True
def on_entry_change_valor(entry):
    current_text = entry.get()
    if ',' in current_text:
        current_text = current_text.replace(',', '.')
        entry.delete(0, tk.END)
        entry.insert(0, current_text)
        entry.icursor(len(current_text))
valor_var = tk.DoubleVar(value="")
vcmd_valor = (frameApostas.register(on_validate_valor), '%P')
valor_entry = tk.Entry(frameApostas, textvariable=valor_var, validate="key", validatecommand=vcmd_valor, width=4, justify="right")
valor_entry.bind("<KeyRelease>", lambda event: on_entry_change_valor(valor_entry))
valor_entry.grid(row=2, column=11, padx=5, pady=5, sticky=tk.W) # Valor de Mercado 1

def update_mercado_combobox2(event):
    current_input = mercado_var2.get()
    matching_options = list(mercado_options)
    for i, char in enumerate(current_input):
        if not any(len(opt) > i for opt in matching_options):
            mercado_var2.set(current_input[:-1])
            return
        allowed_chars = [opt[i].upper() for opt in matching_options if len(opt) > i]
        if char.upper() not in allowed_chars:
            mercado_var2.set(current_input[:-1])
            return
        matching_options = [opt for opt in matching_options if opt.lower().startswith(current_input[:i+1].lower())]
    mercado_combobox2['values'] = matching_options
    if len(matching_options) == 1:
        mercado_var2.set(matching_options[0])
        mercado_combobox2.icursor(tk.END)
mercado_var2 = tk.StringVar(value=None)
mercado_combobox2 = ttk.Combobox(frameApostas, textvariable=mercado_var2, values=mercado_options, width=7)
mercado_combobox2.bind("<KeyRelease>", lambda event: (update_mercado_combobox2(event), update_columns()))
mercado_combobox2.grid(row=3, column=10, padx=5, pady=5, sticky=tk.W) # Mercado 2

# Adiciona campo Valor2
def on_entry_change_valor2(entry):
    current_text = entry.get()
    if ',' in current_text:
        current_text = current_text.replace(',', '.')
        entry.delete(0, tk.END)
        entry.insert(0, current_text)
        entry.icursor(len(current_text))
valor_var2 = tk.DoubleVar(value="")
valor_entry2 = tk.Entry(frameApostas, textvariable=valor_var2, validate="key", validatecommand=vcmd_valor, width=4, justify="right")
valor_entry2.bind("<KeyRelease>", lambda event: on_entry_change_valor2(valor_entry2))
valor_entry2.grid(row=3, column=11, padx=5, pady=5, sticky=tk.W) # Valor de Mercado 2

def update_mercado_combobox3(event):
    current_input = mercado_var3.get()
    matching_options = list(mercado_options)
    for i, char in enumerate(current_input):
        if not any(len(opt) > i for opt in matching_options):
            mercado_var3.set(current_input[:-1])
            return
        allowed_chars = [opt[i].upper() for opt in matching_options if len(opt) > i]
        if char.upper() not in allowed_chars:
            mercado_var3.set(current_input[:-1])
            return
        matching_options = [opt for opt in matching_options if opt.lower().startswith(current_input[:i+1].lower())]
    mercado_combobox3['values'] = matching_options
    if len(matching_options) == 1:
        mercado_var3.set(matching_options[0])
        mercado_combobox3.icursor(tk.END)
mercado_var3 = tk.StringVar(value=None)
mercado_combobox3 = ttk.Combobox(frameApostas, textvariable=mercado_var3, values=mercado_options, width=7)
mercado_combobox3.bind("<KeyRelease>", update_mercado_combobox3) # Mercado 3

# Adiciona campo Valor3
def on_entry_change_valor3(entry):
    current_text = entry.get()
    if ',' in current_text:
        current_text = current_text.replace(',', '.')
        entry.delete(0, tk.END)
        entry.insert(0, current_text)
        entry.icursor(len(current_text))
valor_var3 = tk.DoubleVar(value="")
valor_entry3 = tk.Entry(frameApostas, textvariable=valor_var3, validate="key", validatecommand=vcmd_valor, width=4, justify="right")
valor_entry3.bind("<KeyRelease>", lambda event: on_entry_change_valor3(valor_entry3)) # Valor de Mercado 3

# Adiciona campo ODD
odd_label = tk.Label(frameApostas, text="ODD")
odd_label.grid(row=1, column=12)
def on_validate_odd(P):
    if not P:
        return True
    P = P.replace(',', '.')
    if not P.replace('.', '', 1).isdigit():
        return False
    if len(P.split('.')[0]) > 3:
        return False
    if '.' in P and len(P.split('.')[1]) > 3:
        return False
    return True
def on_entry_change_odd(entry):
    current_text = entry.get()
    if ',' in current_text:
        current_text = current_text.replace(',', '.')
        entry.delete(0, tk.END)
        entry.insert(0, current_text)
        entry.icursor(len(current_text))
odd_var = tk.DoubleVar(value=None)
vcmd_odd = (frameApostas.register(on_validate_odd), '%P')
odd_entry = tk.Entry(frameApostas, textvariable=odd_var, validate="key", validatecommand=vcmd_odd, width=4, justify="right")
odd_entry.bind("<KeyRelease>", lambda event: on_entry_change_odd(odd_entry))
odd_entry.grid(row=2, column=12, padx=5, pady=5, sticky=tk.W) # Odd 1

# Adiciona campo ODD2
def on_entry_change_odd2(entry):
    current_text = entry.get()
    if ',' in current_text:
        current_text = current_text.replace(',', '.')
        entry.delete(0, tk.END)
        entry.insert(0, current_text)
        entry.icursor(len(current_text))
odd_var2 = tk.DoubleVar(value=None)
odd_entry2 = tk.Entry(frameApostas, textvariable=odd_var2, validate="key", validatecommand=vcmd_odd, width=4, justify="right")
odd_entry2.bind("<KeyRelease>", lambda event: on_entry_change_odd2(odd_entry2))
odd_entry2.grid(row=3, column=12, padx=5, pady=5, sticky=tk.W) # Odd 2

# Adiciona campo ODD3
odd_var3 = tk.DoubleVar(value=None)
odd_entry3 = tk.Entry(frameApostas, textvariable=odd_var3, validate="key", validatecommand=vcmd_odd, width=4, justify="right")
odd_entry3.bind("<KeyRelease>", lambda event: on_entry_change_odd3(odd_entry3))
def on_entry_change_odd3(entry):
    current_text = entry.get()
    if ',' in current_text:
        current_text = current_text.replace(',', '.')
        entry.delete(0, tk.END)
        entry.insert(0, current_text)
        entry.icursor(len(current_text)) # Odd 3

# Adiciona campo Aposta
real_label = tk.Label(frameApostas, text="R$")
real_label.grid(row=2, column=13)
label_aposta = tk.Label(frameApostas, text="Aposta")
label_aposta.grid(row=1, column=14, padx=5, pady=5, sticky=tk.W)
def on_validate_aposta(P):
    if not P:
        return True
    P = P.replace(',', '.')
    if not P.replace('.', '', 1).isdigit():
        return False
    if len(P.split('.')[0]) > 4:
        return False
    if '.' in P and len(P.split('.')[1]) > 2:
        return False
    return True
def on_entry_change_aposta(entry):
    current_text = entry.get()
    if ',' in current_text:
        current_text = current_text.replace(',', '.')
        entry.delete(0, tk.END)
        entry.insert(0, current_text)
        entry.icursor(len(current_text))
aposta_var = tk.DoubleVar(value=None)
vcmd_aposta = (frameApostas.register(on_validate_aposta), '%P')
aposta_entry = tk.Entry(frameApostas, validate="key", validatecommand=vcmd_aposta, textvariable=aposta_var, width=5, justify="right")
aposta_entry.bind("<KeyRelease>", lambda event: on_entry_change_aposta(aposta_entry))
aposta_entry.grid(row=2, column=14, padx=5, pady=5, sticky=tk.W) # Aposta 1

#Adicionar aposta2
real_label2 = tk.Label(frameApostas, text="R$")
real_label2.grid(row=3, column=13)
def on_entry_change_aposta2(entry):
    current_text = entry.get()
    if ',' in current_text:
        current_text = current_text.replace(',', '.')
        entry.delete(0, tk.END)
        entry.insert(0, current_text)
        entry.icursor(len(current_text))
aposta_var2 = tk.DoubleVar(value=None)
aposta_entry2 = tk.Entry(frameApostas, validate="key", validatecommand=vcmd_aposta, textvariable=aposta_var2, width=5, justify="right")
aposta_entry2.bind("<KeyRelease>", lambda event: on_entry_change_aposta2(aposta_entry2))
aposta_entry2.grid(row=3, column=14, padx=5, pady=5, sticky=tk.W) # Aposta 2

#Adicionar aposta3
real_label3 = tk.Label(frameApostas, text="R$")
def on_entry_change_aposta3(entry):
    current_text = entry.get()
    if ',' in current_text:
        current_text = current_text.replace(',', '.')
        entry.delete(0, tk.END)
        entry.insert(0, current_text)
        entry.icursor(len(current_text))
aposta_var3 = tk.DoubleVar(value=None)
aposta_entry3 = tk.Entry(frameApostas, validate="key", validatecommand=vcmd_aposta, textvariable=aposta_var3, width=5, justify="right")
aposta_entry3.bind("<KeyRelease>", lambda event: on_entry_change_aposta3(aposta_entry3)) # Aposta 3

#Adicionando cálculos
def on_variable_change(*args):
    odds = [odd_var.get(), odd_var2.get(), odd_var3.get()]
    apostas = [aposta_var.get(), aposta_var2.get(), aposta_var3.get()]
    bethouses = [bethouse_options.get(bethouse_var.get(), {}).get('taxa', 0.0), bethouse_options.get(bethouse_var2.get(), {}).get('taxa', 0.0), bethouse_options.get(bethouse_var3.get(), {}).get('taxa', 0.0)]
    if (len([odd for odd in odds if odd != 0.0]) >= 2) and (len([aposta for aposta in apostas if aposta != 0.0]) >= 1):
        calc_apostas(apostas[0], apostas[1], apostas[2], odds[0], odds[1], odds[2], mercado_var.get(), mercado_var2.get(), bethouses[0], bethouses[1], bethouses[2], arred_var.get())
        resultado = calc_apostas(apostas[0], apostas[1], apostas[2], odds[0], odds[1], odds[2], mercado_var.get(),mercado_var2.get(), bethouses[0], bethouses[1], bethouses[2], arred_var.get())
        palpite1_label.config(text=f"R$ {format(round(resultado[0],2), '.2f')}" if resultado[0] is not None else "")
        palpite2_label.config(text=f"R$ {format(round(resultado[1],2), '.2f')}" if resultado[1] is not None else "")
        palpite3_label.config(text=f"R$ {format(round(resultado[2],2), '.2f')}" if resultado[2] is not None else "")
        lucro1_label.config(text=f"R$ {format(round(resultado[4],2), '.2f')}" if resultado[4] is not None else "", fg='seagreen' if resultado[4] > 0 else ('red' if resultado[4] < 0 else 'gray'), font=("Arial", 14, "bold"))
        lucro2_label.config(text=f"R$ {format(round(resultado[5],2), '.2f')}" if resultado[5] is not None else "", fg='seagreen' if resultado[5] > 0 else ('red' if resultado[6] < 0 else 'gray'), font=("Arial", 14, "bold"))
        lucro3_label.config(text=f"R$ {format(round(resultado[6],2), '.2f')}" if resultado[6] is not None else "", fg='seagreen' if resultado[6] > 0 else ('red' if resultado[7] < 0 else 'gray'), font=("Arial", 14, "bold"))
        liability_label1.config(text=f"R$ {format(round(resultado[3],2), '.2f')}" if resultado[3] is not None else "")
        liability_label2.config(text=f"R$ {format(round(resultado[3],2), '.2f')}" if resultado[3] is not None else "")
        lucro_percent_label1.config(text=f"{round(resultado[7],2)}%" if resultado[4] is not None else "", fg='seagreen' if resultado[4] > 0 else ('red' if resultado[4] < 0 else 'gray'), font=("Arial", 20, "bold"))
    else:
        palpite1_label.config(text="")
        palpite2_label.config(text="")
        palpite3_label.config(text="")
        lucro1_label.config(text="")
        lucro2_label.config(text="")
        lucro3_label.config(text="")
        liability_label1.config(text="")
        liability_label2.config(text="")
        lucro_percent_label1.config(text="")

# associando a função on_variable_change para as variáveis
odd_var.trace_add('write', on_variable_change)
odd_var2.trace_add('write', on_variable_change)
odd_var3.trace_add('write', on_variable_change)
aposta_var.trace_add('write', on_variable_change)
aposta_var2.trace_add('write', on_variable_change)
aposta_var3.trace_add('write', on_variable_change)
bethouse_var.trace_add('write', on_variable_change)
bethouse_var2.trace_add('write', on_variable_change)
bethouse_var3.trace_add('write', on_variable_change)
arred_var.trace_add('write', on_variable_change)
mercado_var.trace_add('write', on_variable_change)
mercado_var2.trace_add('write', on_variable_change)
mercado_var3.trace_add('write', on_variable_change) # on_variable change para variaveis

#Palpites
palpite_label = tk.Label(frameApostas, text='Palpites')
palpite_label.grid(row=1, column=15, padx=5, pady=5, sticky=tk.W)
palpite1_label = tk.Label(frameApostas, text="")
palpite1_label.grid(row=2, column=15)
palpite2_label = tk.Label(frameApostas, text="")
palpite2_label.grid(row=3, column=15)
palpite3_label = tk.Label(frameApostas, text="") # Palpites

#Lucro
liability_label = tk.Label(frameApostas, text='Liability')
liability_label1 = tk.Label(frameApostas, text='')
liability_label2 = tk.Label(frameApostas, text='')
lucro_label = tk.Label(frameApostas, text='Lucro')
lucro_label.grid(row=1, column=16, padx=5, pady=5, sticky=tk.W)
lucro1_label = tk.Label(frameApostas, text="")
lucro1_label.grid(row=2, column=16)
lucro2_label = tk.Label(frameApostas, text="")
lucro2_label.grid(row=3, column=16)
lucro3_label = tk.Label(frameApostas, text="")
lucro_percent_label = tk.Label(frameApostas, text='Lucro %')
lucro_percent_label.grid(row=1, column=17, padx=5, pady=5, sticky=tk.W)
lucro_percent_label1 = tk.Label(frameApostas, text="", font=("Arial", 20, "bold"))
lucro_percent_label1.grid(row=2, column=17, rowspan=2) # Lucro

def update_columns():
    if mercado_var.get() == "Lay" or mercado_var2.get() =="Lay":
        liability_label.grid(row=1, column=16, padx=5, pady=5, sticky=tk.W)
        lucro_label.grid(row=1, column=17, padx=5, pady=5, sticky=tk.W)
        lucro1_label.grid(row=2, column=17)
        lucro2_label.grid(row=3, column=17)
        lucro_percent_label.grid(row=1, column=18, padx=5, pady=5, sticky=tk.W)
        lucro_percent_label1.grid(row=2, column=18, rowspan=2)
        if mercado_var.get() == "Lay":
            liability_label1.grid(row=2, column=16, padx=5, pady=5, sticky=tk.W)
            liability_label2.grid_remove()
            lucro_percent_label.grid(row=1, column=18, padx=5, pady=5, sticky=tk.W)
            lucro_percent_label1.grid(row=2, column=18, rowspan=2)
        else:
            liability_label2.grid(row=3, column=16, padx=5, pady=5, sticky=tk.W)
            liability_label1.grid_remove()
            lucro_percent_label.grid(row=1, column=18, padx=5, pady=5, sticky=tk.W)
            lucro_percent_label1.grid(row=2, column=18, rowspan=2)
    else:
        liability_label.grid_forget()
        lucro_label.grid(row=1, column=16, padx=5, pady=5, sticky=tk.W)
        lucro1_label.grid(row=2, column=16)
        lucro2_label.grid(row=3, column=16)
        lucro_percent_label.grid(row=1, column=17, padx=5, pady=5, sticky=tk.W)
        lucro_percent_label1.grid(row=2, column=17, rowspan=2)

#Para Calcular apostas
def calc_apostas(aposta1, aposta2, aposta3, odd1, odd2, odd3, mercado1, mercado2, bethouse_options1, bethouse_options2, bethouse_options3, arred_var):
    if aposta1 + aposta2 + aposta3 == 0.0 or (odd2 == 0.0 and odd3 == 0.0):
        return
    if odd3 > 0.0:
        if mercado1 == "TO" or mercado1 == "TU" or mercado1 == "AH1" or mercado1 == "AH2":
            odd_1 = ((odd1 - 1) * (1 - bethouse_options1)+1)
            odd_2 = ((odd2 - 1) * (1 - bethouse_options2)+1)
            odd_3 = ((odd3 - 1) * (1 - bethouse_options3)+1)
            if aposta1 > 0.0:
                aposta3 = round(aposta1 / odd3, 2)
                aposta2 = round((odd_1 * aposta1 - odd_3 * aposta3) / odd_2, 2)
            elif aposta2 > 0.0:
                aposta3 = 0.0
                while True:
                    if aposta3 * odd_3 + aposta2 * odd_2 <= aposta3 * odd_3 * odd_1:
                        aposta3 = round(aposta3, 2)
                        break
                    aposta3 += 0.01
                aposta1 = round(aposta3 * odd_3, 2)
            elif aposta3 > 0.0:
                aposta1 = round(aposta3 * odd_3, 2)
                aposta2 = round((odd_1 * aposta1 - odd_3 * aposta3) / odd_2, 2)
            percent1 = aposta1 / (aposta1 + aposta2 + aposta3)
            percent2 = aposta2 / (aposta1 + aposta2 + aposta3)
            percent3 = aposta3 / (aposta1 + aposta2 + aposta3)
            lucro1 = round(((aposta1 * odd1 - aposta1) * (1 - bethouse_options1) + aposta1) - aposta1 - aposta2 - aposta3, 2)
            lucro2 = round(((aposta2 * odd2 - aposta2) * (1 - bethouse_options2) + aposta2) - aposta2 - aposta3, 2)
            lucro3 = round(((aposta3 * odd3 - aposta3) * (1 - bethouse_options3) + aposta3) + ((aposta2 * odd2 - aposta2) * (1 - bethouse_options2) + aposta2) - aposta1 - aposta2 - aposta3, 2)
            lucro_percent = round((((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            return aposta1, aposta2, aposta3, None, lucro1, lucro2, lucro3, lucro_percent
        else:
            percent1 = (((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd3 - 1) * (1 - bethouse_options3) + 1)) / ((odd1 - 1) * (1 - bethouse_options1) + 1) / ((((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd3 - 1) * (1 - bethouse_options3) + 1)) / ((odd1 - 1) * (1 - bethouse_options1) + 1) + (((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd3 - 1) * (1 - bethouse_options3) + 1)) / ((odd2 - 1) * (1 - bethouse_options2) + 1) + (((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd3 - 1) * (1 - bethouse_options3) + 1)) / ((odd3 - 1) * (1 - bethouse_options3) + 1))
            percent2 = (((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd3 - 1) * (1 - bethouse_options3) + 1)) / ((odd2 - 1) * (1 - bethouse_options2) + 1) / ((((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd3 - 1) * (1 - bethouse_options3) + 1)) / ((odd1 - 1) * (1 - bethouse_options1) + 1) + (((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd3 - 1) * (1 - bethouse_options3) + 1)) / ((odd2 - 1) * (1 - bethouse_options2) + 1) + (((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd3 - 1) * (1 - bethouse_options3) + 1)) / ((odd3 - 1) * (1 - bethouse_options3) + 1))
            percent3 = (((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd3 - 1) * (1 - bethouse_options3) + 1)) / ((odd3 - 1) * (1 - bethouse_options3) + 1) / ((((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd3 - 1) * (1 - bethouse_options3) + 1)) / ((odd1 - 1) * (1 - bethouse_options1) + 1) + (((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd3 - 1) * (1 - bethouse_options3) + 1)) / ((odd2 - 1) * (1 - bethouse_options2) + 1) + (((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd3 - 1) * (1 - bethouse_options3) + 1)) / ((odd3 - 1) * (1 - bethouse_options3) + 1))
    else:
        percent3 = 0.0
        if mercado2 == "Lay":
            if mercado1 == "Lay":
                percent1 = ((odd2 / (odd2 - 1) - 1) * (1 - bethouse_options2) + 1) / (((odd2 / (odd2 - 1) - 1) * (1 - bethouse_options2) + 1) + ((odd1 / (odd1 - 1) - 1) * (1 - bethouse_options1)+1))
                percent2 = ((odd1 / (odd1 - 1) - 1) * (1 - bethouse_options1) + 1) / (((odd1 / (odd1 - 1) - 1) * (1 - bethouse_options1) + 1) + ((odd2 / (odd2 - 1) - 1) * (1 - bethouse_options2)+1))
            else:
                percent1 = ((odd2 / (odd2 - 1) - 1) * (1 - bethouse_options2) + 1) / (((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 / (odd2 - 1) - 1) * (1 - bethouse_options2) + 1))
                percent2 = ((odd1 - 1) * (1 - bethouse_options1) + 1) / (((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 / (odd2 - 1) - 1) * (1 - bethouse_options2) + 1))
        elif mercado1 == "Lay":
            percent1 = ((odd2 - 1) * (1 - bethouse_options2) + 1) / (((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd1 / (odd1 - 1) - 1) * (1 - bethouse_options1) + 1))
            percent2 = ((odd1 / (odd1 - 1) - 1) * (1 - bethouse_options1) + 1) / (((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd1 / (odd1 - 1) - 1) * (1 - bethouse_options1) + 1))
        else:
            percent1 = ((odd2 - 1)*(1 - bethouse_options2) + 1) / (((odd2 - 1)*(1-bethouse_options2) + 1) + ((odd1 - 1) * (1 - bethouse_options1) + 1))
            percent2 = ((odd1 - 1)*(1 - bethouse_options1) + 1) / (((odd1 - 1)*(1-bethouse_options1) + 1) + ((odd2 - 1) * (1 - bethouse_options2) + 1))
    if aposta2 > 0.0:
        aposta1 = round(((aposta2 * percent1) / percent2) / arred_var) * arred_var
        aposta3 = round(((aposta2 * percent3) / percent2) / arred_var) * arred_var
    elif aposta1 > 0.0:
        aposta2 = round(((aposta1 * percent2) / percent1) / arred_var) * arred_var
        aposta3 = round(((aposta2 * percent3) / percent2) / arred_var) * arred_var
    elif aposta3 > 0.0:
        aposta1 = round(((aposta3 * percent1) / percent3) / arred_var) * arred_var
        aposta2 = round(((aposta1 * percent2) / percent1) / arred_var) * arred_var
    if mercado2 == "Lay":
        liability = round((aposta2 * (odd2 / (odd2 - 1)) - aposta2), 2)
        lucro1 = round(((aposta1 * odd1 - aposta1) * (1 - bethouse_options1) + aposta1) - aposta1 - aposta2 - aposta3, 2)
        lucro2 = round(((aposta2 * (odd2 / (odd2 - 1)) - aposta2) * (1 - bethouse_options2) + aposta2) - aposta1 - aposta2 - aposta3, 2)
    elif mercado1 == "Lay":
        liability = round((aposta1 * (odd1 / (odd1 - 1)) - aposta1), 2)
        lucro1 = round(((aposta1 * (odd1 / (odd1 - 1)) - aposta1) * (1 - bethouse_options1) + aposta1) - aposta1 - aposta2 - aposta3, 2)
        lucro2 = round(((aposta2 * odd2 - aposta2) * (1 - bethouse_options2) + aposta2) - aposta1 - aposta2 - aposta3,2)
    else:
        liability = None
        lucro1 = round(((aposta1 * odd1 - aposta1) * (1 - bethouse_options1) + aposta1) - aposta1 - aposta2 - aposta3,2)
        lucro2 = round(((aposta2 * odd2 - aposta2) * (1 - bethouse_options2) + aposta2) - aposta1 - aposta2 - aposta3,2)
    if odd3 > 0.0:
        lucro3 = round(((aposta3 * odd3 - aposta3) * (1 - bethouse_options3) + aposta3) - aposta1 - aposta2 - aposta3, 2)
        lucro_percent = round((((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3)) * 100, 2)
    else:
        lucro3 = 0
        lucro_percent = round(((lucro1 + lucro2) / 2) / (aposta1 + aposta2) * 100, 2)
    return aposta1, aposta2, aposta3, liability, lucro1, lucro2, lucro3, lucro_percent

# cria o botão de gravação
def resetar_variaveis():
    # Redefinir as variáveis para os valores iniciais desejados
    jogo_entry.delete(0, tk.END)
    dia_entry.delete(0, tk.END)
    dia_entry.insert(0, dia_atual)
    hora_entry.delete(0, tk.END)
    hora_entry.insert(0, 12)
    minuto_entry.delete(0, tk.END)
    minuto_entry.insert(0, "00")
    bethouse_var.set("")
    bethouse_var2.set("")
    bethouse_var3.set("")
    mercado_var.set("")
    mercado_var2.set("")
    mercado_var3.set("")
    valor_var.set("")
    valor_var2.set("")
    valor_var3.set("")
    odd_var.set(0.0)
    odd_var2.set(0.0)
    odd_var3.set(0.0)
    aposta_var.set(0.0)
    aposta_var2.set(0.0)
    aposta_var3.set(0.0)
    if num_bets == 3:
        alternar_bets()
    preencher_treeview()

def gravar():
    odds = [odd_var.get(), odd_var2.get(), odd_var3.get()]
    apostas = [aposta_var.get(), aposta_var2.get(), aposta_var3.get()]
    def gerar_id(arquivo_csv):
        with open(arquivo_csv, "r") as f:
            reader = csv.reader(f)
            count = sum(1 for _ in reader)  # Subtrai 1 para excluir o cabeçalho
        return f"#{str(count).zfill(6)}"  # Formata o número do ID com zeros à esquerda
    if (len([odd for odd in odds if odd != 0.0]) >= 2) and (len([aposta for aposta in apostas if aposta != 0.0]) >= 1) and jogo_entry != "":
        id = gerar_id("Apostas.csv")
        time_casa = jogo_entry.get().split(" - ")[0]
        time_fora = jogo_entry.get().split(" - ")[1]
        dia = dia_entry.get()
        mes = mes_combobox.get()
        ano = ano_combobox.get()
        hora = hora_entry.get()
        minuto = minuto_entry.get()
        bethouse1 = bethouse_combobox.get()
        mercado1 = mercado_combobox.get()
        merc_valor1 = valor_entry.get()
        odd1 = odd_entry.get()
        if aposta_var.get() == 0.0:
            aposta1 = (palpite1_label.cget("text").replace("R$", "").strip())
        else:
            aposta1 = aposta_var.get()
        resultado1 = ""
        bethouse2 = bethouse_combobox2.get()
        mercado2 = mercado_combobox2.get()
        merc_valor2 = valor_entry2.get()
        odd2 = odd_entry2.get()
        if aposta_var2.get() == 0.0:
            aposta2 = (palpite2_label.cget("text").replace("R$", "").strip())
        else:
            aposta2 = aposta_var2.get()
        resultado2 = ""
        bethouse3 = bethouse_combobox3.get()
        mercado3 = mercado_combobox3.get()
        merc_valor3 = valor_entry3.get()
        odd3 = odd_entry3.get()
        if aposta_var3.get() == 0.0 and float(odd3) > 0:
            aposta3 = palpite3_label.cget("text").replace("R$", "").strip()
        else:
            aposta3 = aposta_var3.get()
        resultado3 = ""
        lucro_estimado = round((float(lucro1_label.cget("text").replace("R$", "").strip()) + float(lucro2_label.cget("text").replace("R$", "").strip()) + float(lucro3_label.cget("text").replace("R$", "").strip())) / 3, 2)
        lucro_per_estimado = float(lucro_percent_label1.cget("text").replace("%", "").strip()) / 100
        lucroReal = ""
        lucro_perReal = ""

        # Dados a serem gravados
        dados = [id, time_casa, time_fora, dia, mes, ano, hora, minuto, bethouse1, mercado1, merc_valor1, odd1, aposta1, resultado1, bethouse2, mercado2, merc_valor2, odd2, aposta2, resultado2, bethouse3, mercado3, merc_valor3, odd3, aposta3, resultado3, lucro_estimado, lucro_per_estimado, lucroReal, lucro_perReal]

        # Gravação dos dados no arquivo CSV
        with open("Apostas.csv", "a", newline="") as f:
            csv.writer(f).writerow(dados)

        resetar_variaveis()
    else:
        messagebox.showwarning("Aviso", "Preencha o jogo, as odds e uma aposta.")

gravar_button = tk.Button(frameGravar, text="Gravar", command=gravar)
gravar_button.grid(row=0, column=0)
clear_button = tk.Button(frameGravar, text="Limpar", command=resetar_variaveis)
clear_button.grid(row=0, column=1)

def preencher_treeview():
    # Limpar o conteúdo atual do Treeview
    for row in tabela.get_children():
        tabela.delete(row)

    # Abrir o arquivo CSV
    with open("Apostas.csv", "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        # Configurar cores de fundo alternadas para as linhas
        tabela.tag_configure("linha_par", background="#F0F0F0")
        tabela.tag_configure("linha_impar", background="white")

        # Preencher o Treeview com os dados do arquivo
        for i, row in enumerate(reader):
            ID = row['id']
            jogo = f"{row['time_casa']}\n{row['time_fora']}"
            data = "{:02d} / {} / {}\n{:02d}:{:02d}".format(int(row['dia']), (row['mes']), row['ano'], int(row['hora']), int(row['minuto']))
            bethouses = "{}({} × R$ {:.2f})\n{}({} × R$ {:.2f})".format(row['bethouse1'], float(row['odd1']), float(row['aposta1']),row['bethouse2'], float(row['odd2']), float(row['aposta2']))
            if row['bethouse3']:
                bethouses += "\n{}({} × R$ {:.2f})".format(row['bethouse3'], float(row['odd3']), float(row['aposta3']))

            # Add alternating background colors to rows
            if i % 2 == 0:
                tabela.insert("", "end", values=(ID, jogo, data, bethouses), tags=("linha_par",))
            else:
                tabela.insert("", "end", values=(ID, jogo, data, bethouses), tags=("linha_impar",))
def select_bets(event):
    # Obter o item selecionado na tabela
    item_id = tabela.focus()
    item_values = tabela.item(item_id)['values']

    # Obter o ID da linha selecionada
    id_selecionado = item_values[0]  # Índice 0 corresponde ao campo 'ID'

    def reset_all():
        # Redefinir as variáveis para os valores iniciais desejados
        jogo_entry.delete(0, tk.END)
        dia_entry.delete(0, tk.END)
        dia_entry.insert(0, dia_atual)
        hora_entry.delete(0, tk.END)
        hora_entry.insert(0, 12)
        minuto_entry.delete(0, tk.END)
        minuto_entry.insert(0, "00")
        bethouse_var.set("")
        bethouse_var2.set("")
        bethouse_var3.set("")
        mercado_var.set("")
        mercado_var2.set("")
        mercado_var3.set("")
        valor_var.set("")
        valor_var2.set("")
        valor_var3.set("")
        odd_var.set(0.0)
        odd_var2.set(0.0)
        odd_var3.set(0.0)
        aposta_var.set(0.0)
        aposta_var2.set(0.0)
        aposta_var3.set(0.0)
        if num_bets == 3:
            alternar_bets()
        edit_button.grid_remove()
        clear_button.grid(row=0, column=1)

    # Trocar botão Limpar
    clear_button.grid_remove()
    full_clear_button = tk.Button(frameGravar, text="Limpar", command=reset_all)
    full_clear_button.grid(row=0, column=1)

    # Abrir o arquivo Apostas.csv e buscar as informações da linha correspondente ao ID
    with open("Apostas.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['id'] == id_selecionado:
                jogo_entry.delete(0, 'end')
                jogo_entry.insert(0, f"{row['time_casa']} - {row['time_fora']}")
                dia_entry.delete(0, 'end')
                dia_entry.insert(0, row['dia'])
                mes_combobox.set(row['mes'])
                ano_combobox.set(row['ano'])
                hora_entry.delete(0, 'end')
                hora_entry.insert(0, row['hora'])
                minuto_entry.delete(0, 'end')
                minuto_entry.insert(0, row['minuto'])
                if row['mercado3'] != "" and num_bets == 2:
                    alternar_bets()
                bethouse_combobox.set(row['bethouse1'])
                bethouse_combobox2.set(row['bethouse2'])
                bethouse_combobox3.set(row['bethouse3'])
                mercado_combobox.set(row['mercado1'])
                mercado_combobox2.set(row['mercado2'])
                mercado_combobox3.set(row['mercado3'])
                valor_entry.delete(0, 'end')
                valor_entry.insert(0, row['valor1'])
                valor_entry2.delete(0, 'end')
                valor_entry2.insert(0, row['valor2'])
                valor_entry3.delete(0, 'end')
                valor_entry3.insert(0, row['valor3'])
                odd_entry.delete(0, 'end')
                odd_entry.insert(0, row['odd1'])
                odd_entry2.delete(0, 'end')
                odd_entry2.insert(0, row['odd2'])
                odd_entry3.delete(0, 'end')
                odd_entry3.insert(0, row['odd3'])
                aposta_var.set(row['aposta1'])
                aposta_var2.set(row['aposta2'])
                aposta_var3.set(row['aposta3'])
                break

    def editar_bets():
        # Obter o item selecionado na tabela
        item_id = tabela.focus()
        item_values = tabela.item(item_id)['values']

        # Obter o ID da linha selecionada
        id_selecionado = item_values[0]  # Índice 0 corresponde ao campo 'ID'

        # Ler todas as linhas do arquivo Apostas.csv e armazená-las em uma lista
        with open("Apostas.csv", "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Atualizar os valores da linha correspondente no arquivo Apostas.csv
        for row in rows:
            if row['id'] == id_selecionado:
                row['time_casa'] = jogo_entry.get().split(" - ")[0]
                row['time_fora'] = jogo_entry.get().split(" - ")[1]
                row['dia'] = dia_entry.get()
                row['mes'] = mes_combobox.get()
                row['ano'] = ano_combobox.get()
                row['hora'] = hora_entry.get()
                row['minuto'] = minuto_entry.get()
                row['bethouse1'] = bethouse_combobox.get()
                row['bethouse2'] = bethouse_combobox2.get()
                row['bethouse3'] = bethouse_combobox3.get()
                row['mercado1'] = mercado_combobox.get()
                row['mercado2'] = mercado_combobox2.get()
                row['mercado3'] = mercado_combobox3.get()
                row['valor1'] = valor_entry.get()
                row['valor2'] = valor_entry2.get()
                row['valor3'] = valor_entry3.get()
                row['odd1'] = odd_entry.get()
                row['odd2'] = odd_entry2.get()
                row['odd3'] = odd_entry3.get()
                if float(row['aposta1']) == 0.0:
                    row['aposta1'] = (palpite1_label.cget("text").replace("R$", "").strip())
                else:
                    row['aposta1'] = aposta_var.get()
                if float(row['aposta2']) == 0.0:
                    row['aposta2'] = (palpite2_label.cget("text").replace("R$", "").strip())
                else:
                    row['aposta2'] = aposta_var2.get()
                if float(row['aposta3']) == 0.0:
                    row['aposta3'] = (palpite3_label.cget("text").replace("R$", "").strip())
                else:
                    row['aposta3'] = aposta_var3.get()
                break

        # Escrever as linhas atualizadas no arquivo Apostas.csv
        with open("Apostas.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        # Limpar as variáveis e atualizar a tabela
        resetar_variaveis()
        preencher_treeview()
        edit_button.grid_remove()

    # Botão Editar

    edit_button = tk.Button(frameGravar, text="Editar", command=editar_bets, foreground="red")
    edit_button.grid(row=0, column=2)

class MyTreeview(ttk.Treeview):
    def __init__(self, master=None, **kw):
        ttk.Treeview.__init__(self, master, **kw)
        self.bind("<Button-1>", self.on_click)
        self.canvas = Canvas(self, width=200, height=40)
        self.canvas.bind("<Button-1>",
                         self.on_canvas_click)  # Bind the on_canvas_click method to the <Button-1> event of the Canvas widget
        self.icons = ["",
                      PhotoImage(file="win.png").subsample(13, 13),
                      PhotoImage(file="loss.png").subsample(13, 13),
                      PhotoImage(file="return.png").subsample(13, 13),
                      PhotoImage(file="half-win.png").subsample(13, 13),
                      PhotoImage(file="half-loss.png").subsample(13, 13)]
        self.iconSave = PhotoImage(file="save.png").subsample(18, 18)
        self.current_icons = {}
        self.clicked_row = None

    def on_click(self, event):
        row = self.identify_row(event.y)
        column = self.identify_column(event.x)
        if row not in self.current_icons:
            self.current_icons[row] = (0, 0, 0)  # Add a third icon index
        item = self.item(row)  # Get the item data for the clicked row
        x, y = event.x, event.y
        self.canvas.place(x=x, y=y)
        self.canvas.delete("all")  # Clear the canvas
        self.canvas.create_image(0, 0, image=self.icons[self.current_icons[row][0]], anchor=NW)
        self.canvas.create_rectangle(30, 0, 200, 20, fill="yellow")  # Retângulo com cor de fundo
        self.canvas.create_text(30, 10, text=item['values'][3].split("\n")[0], anchor=W, fill="red")
        self.canvas.create_image(0, 20, image=self.icons[self.current_icons[row][1]], anchor=NW)
        self.canvas.create_text(30, 30, text=item['values'][3].split("\n")[1], anchor=W)

        if len(item['values'][3].split("\n")) > 2:  # Check the value of bethouse3
            self.canvas.config(height=80)  # Increase the height of the canvas
            self.canvas.create_image(0, 40, image=self.icons[self.current_icons[row][2]], anchor=NW)  # Create the third icon
            self.canvas.create_text(30, 50, text=item['values'][3].split("\n")[2], anchor=W)
            self.canvas.create_image(0, 60, image=self.iconSave, anchor=NW)
            self.canvas.create_text(30, 70, text="Salvar Resultados", anchor=W)
        else:
            self.canvas.config(height=60)  # Set the height of the canvas back to 40
            self.canvas.create_image(0, 40, image=self.iconSave, anchor=NW)
            self.canvas.create_text(30, 50, text="Salvar Resultados", anchor=W)

        self.clicked_row = row  # Store the clicked row

    def on_canvas_click(self, event):
        def save_results():
            if self.clicked_row is not None:
                selected_row = tabela.clicked_row
                selected_item = tabela.item(selected_row)

                icon1 = tabela.current_icons[selected_row][0]
                icon2 = tabela.current_icons[selected_row][1]
                icon3 = tabela.current_icons[selected_row][2] if len(selected_item['values'][3].split("\n")) > 2 else ""

                result1 = get_result_from_icon(icon1)
                result2 = get_result_from_icon(icon2)
                result3 = get_result_from_icon(icon3) if icon3 is not None else ""

                # Verifica se result1, result2 e result3 (caso não seja vazio) são maiores que 0
                if result1 != "" and result2 != "" and (len(selected_item['values'][3].split("\n")) <= 2 or result3 != ""):
                    with open('Apostas.csv', 'r', newline='') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=',')
                        rows = list(reader)

                    for row in rows:
                        if row['id'] == selected_item['values'][0]:
                            row['resultado1'] = result1
                            row['resultado2'] = result2
                            row['resultado3'] = result3

                    with open('Apostas.csv', 'w', newline='') as csvfile:
                        fieldnames = rows[0].keys()
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(rows)
                else:
                    print("Preencha todos os resultados!")

        def get_result_from_icon(icon):
            if icon == 1:
                return 'win'
            elif icon == 2:
                return 'loss'
            elif icon == 3:
                return 'return'
            elif icon == 4:
                return 'half-win'
            elif icon == 5:
                return 'half-loss'
            else:
                return ''
        row = self.clicked_row  # Get the clicked row
        item = self.item(row)  # Get the item data for the clicked row
        if event.y <= 20:
            # The first icon was clicked
            current_icon1 = (self.current_icons[row][0] + 1) % len(self.icons)
            self.current_icons[row] = (current_icon1, self.current_icons[row][1], self.current_icons[row][2])
            self.canvas.delete("all")  # Clear the canvas
            self.canvas.create_image(0, 0, image=self.icons[self.current_icons[row][0]], anchor=NW)
            self.canvas.create_text(30, 10, text=item['values'][3].split("\n")[0], anchor=W)
            self.canvas.create_image(0, 20, image=self.icons[self.current_icons[row][1]], anchor=NW)
            self.canvas.create_text(30, 30, text=item['values'][3].split("\n")[1], anchor=W)

            if len(item['values'][3].split("\n")) > 2:  # Check the value of bethouse3
                self.canvas.create_image(0, 40, image=self.icons[self.current_icons[row][2]], anchor=NW)  # Create the third icon
                self.canvas.create_text(30, 50, text=item['values'][3].split("\n")[2], anchor=W)
                self.canvas.create_image(0, 60, image=self.iconSave, anchor=NW)
                self.canvas.create_text(30, 70, text="Salvar Resultados", anchor=W)
            else:
                self.canvas.create_image(0, 40, image=self.iconSave, anchor=NW)
                self.canvas.create_text(30, 50, text="Salvar Resultados", anchor=W)

        elif event.y <= 40:
            # The second icon was clicked
            current_icon2 = (self.current_icons[row][1] + 1) % len(self.icons)
            self.current_icons[row] = (self.current_icons[row][0], current_icon2, self.current_icons[row][2])
            self.canvas.delete("all")  # Clear the canvas
            self.canvas.create_image(0, 0, image=self.icons[self.current_icons[row][0]], anchor=NW)
            self.canvas.create_text(30, 10, text=item['values'][3].split("\n")[0], anchor=W)
            self.canvas.create_image(0, 20, image=self.icons[self.current_icons[row][1]], anchor=NW)
            self.canvas.create_text(30, 30, text=item['values'][3].split("\n")[1], anchor=W)

            if len(item['values'][3].split("\n")) > 2:  # Check the value of bethouse3
                self.canvas.create_image(0, 40, image=self.icons[self.current_icons[row][2]], anchor=NW)  # Create the third icon
                self.canvas.create_text(30, 50, text=item['values'][3].split("\n")[2], anchor=W)
                self.canvas.create_image(0, 60, image=self.iconSave, anchor=NW)
                self.canvas.create_text(30, 70, text="Salvar Resultados", anchor=W)
            else:
                self.canvas.create_image(0, 40, image=self.iconSave, anchor=NW)
                self.canvas.create_text(30, 50, text="Salvar Resultados", anchor=W)

        elif event.y <= 60:
            # The third icon was clicked
            current_icon3 = (self.current_icons[row][2] + 1) % len(self.icons)
            self.current_icons[row] = (self.current_icons[row][0], self.current_icons[row][1], current_icon3)
            self.canvas.delete("all")  # Clear the canvas
            self.canvas.create_image(0, 0, image=self.icons[self.current_icons[row][0]], anchor=NW)
            self.canvas.create_text(30, 10, text=item['values'][3].split("\n")[0], anchor=W)
            self.canvas.create_image(0, 20, image=self.icons[self.current_icons[row][1]], anchor=NW)
            self.canvas.create_text(30, 30, text=item['values'][3].split("\n")[1], anchor=W)

            if len(item['values'][3].split("\n")) > 2:  # Check the value of bethouse3
                self.canvas.create_image(0, 40, image=self.icons[self.current_icons[row][2]], anchor=NW)  # Create the third icon
                self.canvas.create_text(30, 50, text=item['values'][3].split("\n")[2], anchor=W)
                self.canvas.create_image(0, 60, image=self.iconSave, anchor=NW)
                self.canvas.create_text(30, 70, text="Salvar Resultados", anchor=W)
            else:
                self.canvas.create_image(0, 40, image=self.iconSave, anchor=NW)
                self.canvas.create_text(30, 50, text="Salvar Resultados", anchor=W)
                save_results()
        else:
            save_results()


# Definir estilo para o Treeview
style = ttk.Style()
style.configure("Treeview", rowheight=60)

# Criar o Treeview com as colunas desejadas
tabela = MyTreeview(frameTabela, columns=("ID", "jogo", "data", "betHouses"), show="headings", style="Treeview")
tabela.heading("ID", text="ID")
tabela.heading("jogo", text="Jogo")
tabela.heading("data", text="Data")
tabela.heading("betHouses", text="BetHouses")
tabela.column("ID", width=70)
tabela.column("jogo", width=150)
tabela.column("data", width=100)
tabela.column("betHouses", width=150)
tabela.grid(row=0, column=0, columnspan=10, rowspan= 10)
tabela.bind('<Double-Button-1>', select_bets)


# Chamar a função para preencher o Treeview
if len(tabela.get_children()) == 0:
    preencher_treeview()

# inicia o loop da janela
janela.mainloop()