import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime
from datetime import datetime, timedelta, date
import json
import os
from ttkthemes import ThemedTk
import tkinter.colorchooser as colorchooser
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from PIL import Image, ImageTk
import numpy as np
import fileinput
import io
from Pacotes_Lutzer.convert import convert_to_numeric, convert_mes, convert_ms_to_datetime, converter_esporte
from Pacotes_Lutzer.validate import create_float_entry, create_combobox
from Pacotes_Lutzer.calc_apostas import calc_apostas
from Pacotes_Lutzer.classes_personalizadas import BetHistTreeview, preencher_treeview, import_df_filtrado, save_apostas
from Pacotes_Lutzer.filtros import agregar_datas
import _tkinter
import math
import sqlite3
import re
#from Testes import gerar_saldos

# Cria a janela
janela = tk.Tk()

# Cria o frame
frameOpcoes = tk.Frame(janela, padx=10, pady=10)
frameOpcoes.grid(row=0, column=0)

frameJogo = tk.Frame(janela, padx=10, pady=10)
frameJogo.grid(row=1, column=0)

frameApostas = tk.Frame(janela)
frameApostas.grid(row=5, column=0)

frameGravar = tk.Frame(janela)
frameGravar.grid(row=8, column=0)

frameTabela = tk.Frame(janela)
frameTabela.grid(row=9, column=0)

frameSaldos = tk.Frame(janela, padx=10, pady=10)
frameSaldos.grid(row=10, column=0)

frameStatus = tk.Frame(janela)
frameStatus.grid(row=0, column=1, rowspan=12)

def alternar_tabelas():
    global tabela_visivel
    tabela_visivel = not tabela_visivel
    if tabela_visivel:
        frameTabela.grid(row=9, column=0)
        frameSaldos.grid(row=10, column=0)
        botao_tabelas["text"] = "Ocultar Tabelas"
        botao_stats.grid(row=0, column=2)
    else:
        frameTabela.grid_remove()
        frameSaldos.grid_remove()
        frameStatus.grid_remove()
        botao_stats.grid_remove()
        botao_tabelas["text"] = "Mostrar Tabelas"
def alternar_graficos():
    global stats_visivel
    stats_visivel = not stats_visivel
    if stats_visivel:
        frameStatus.grid(row=0, column=1, rowspan=8)
        botao_stats["text"] = "Ocultar Gráficos"
    else:
        frameStatus.grid_remove()
        botao_stats["text"] = "Mostrar Gráficos"

tabela_visivel = True
stats_visivel = True
botao_tabelas = ttk.Button(frameOpcoes, text="Ocultar Tabelas", command=alternar_tabelas)
botao_stats = ttk.Button(frameOpcoes, text="Mostrar Gráficos", command=alternar_graficos)
botao_tabelas.grid(row=0, column=1)
botao_stats.grid(row=0, column=2)
alternar_graficos()

# Define uma imagem para o botão de configurações
settings_icon = tk.PhotoImage(file="/Users/sergioeblutzer/PycharmProjects/Gerenciamento_Bolsa_Esportiva/engrenagens.png").subsample(20, 20)
settings_button = tk.Button(frameOpcoes, image=settings_icon, bd=0) # Ajustes Iniciais

# Verifica se o arquivo SQLite já existe
if not os.path.isfile("dados.db"):
    conn = sqlite3.connect("dados.db")
    c = conn.cursor()

    # Cria a tabela "apostas"
    c.execute('''CREATE TABLE apostas (
                    id INTEGER,
                    data_entrada TEXT,
                    data_jogo TEXT,
                    time_casa TEXT,
                    time_fora TEXT,
                    bethouse1 TEXT,
                    mercado1 TEXT,
                    valor1 REAL,
                    odd1 REAL,
                    aposta1 REAL,
                    resultado1 TEXT,
                    bethouse2 TEXT,
                    mercado2 TEXT,
                    valor2 REAL,
                    odd2 REAL,
                    aposta2 REAL,
                    resultado2 TEXT,
                    bethouse3 TEXT,
                    mercado3 TEXT,
                    valor3 REAL,
                    odd3 REAL,
                    aposta3 REAL,
                    resultado3 TEXT,
                    lucro_estimado REAL,
                    lucro_per_estimado REAL,
                    lucro_real REAL,
                    lucro_per_real REAL
                )''')

    conn.commit()
else:
    conn = sqlite3.connect("dados.db")
    c = conn.cursor()

# Filtros
def toggle_order_crescente():
    current_order1 = order_button1["text"]
    if current_order1 == "Crescente":
        order_button1["text"] = "Decrescente"
    else:
        order_button1["text"] = "Crescente"
    on_filters_change()
def toggle_order_add():
    current_order2 = order_button2["text"]
    if current_order2 == "Adição":
        order_button2["text"] = "Data"
    else:
        order_button2["text"] = "Adição"
    on_filters_change()
def toggle_time():
    current_time = time_button["text"]
    if current_time == "Vencem até":
        time_button["text"] = "Feitas desde"
        timeframe_combobox["values"] = ["hoje", "ontem", "1 semana", "1 mês", "30 dias", "6 meses", "esse ano", "365 dias", "sempre"]
    else:
        time_button["text"] = "Vencem até"
        timeframe_combobox["values"] = ["hoje", "amanhã", "1 semana", "1 mês"]
        if timeframe_options.index(timeframe_combobox.get()) > 3:
            timeframe_combobox.current(3)
    on_filters_change()

# Ordenação
def on_filters_change():
    bethouse_list = set()
    preencher_treeview(conn, tabela, bethouse_options, situation_vars, order_button1, order_button2, time_button, timeframe_combobox, search_var, frameTabela, frameSaldos, bethouse_list=bethouse_list)
    save_bethouse_options()

order_button1 = tk.Button(frameTabela, text="Crescente", command=toggle_order_crescente, width=8)
order_button1.grid(row=0, column=0)
order_button2 = tk.Button(frameTabela, text="Data", command=toggle_order_add, width=4)
order_button2.grid(row=0, column=1)

# Tempo
time_button = tk.Button(frameTabela, text="Feitas desde", width=5, command=toggle_time)
time_button.grid(row=0, column=2)

timeframe_options = ["hoje", "ontem", "1 semana", "1 mês", "30 dias", "6 meses", "esse ano", "365 dias", "sempre"]
timeframe_combobox = ttk.Combobox(frameTabela, values=timeframe_options, state="readonly", width=5)
timeframe_combobox.current(0)
timeframe_combobox.grid(row=0, column=3)
timeframe_combobox.bind("<<ComboboxSelected>>", lambda event: on_filters_change())

# Situação
def toggle_situation(index):
    if index == 0:
        situation_vars[1].set(0)
    else:
        situation_vars[0].set(0)
    on_filters_change()
def show_frame(event):
    situation_frame = tk.Frame(frameTabela, width=0, height=0)
    situation_frame.place(x=338, y=28)
    for i, (situation, var) in enumerate(zip(situations, situation_vars)):
        if i in [0, 1]:
            tk.Checkbutton(situation_frame, text=situation, variable=var, command=lambda i=i: toggle_situation(i)).grid(row=i+1, column=0)
        else:
            tk.Checkbutton(situation_frame, text=situation, variable=var, command=on_filters_change).grid(row=i+1, column=0)

    def on_window_click(event):
        widget = event.widget
        while widget is not None:
            if widget == situation_frame:
                return
            widget = widget.master
        situation_frame.destroy()

    janela.bind("<Button-1>", on_window_click)

    def toggle_frame(event):
        if situation_frame.winfo_exists():
            situation_frame.destroy()
        else:
            show_frame(event)

    situation_button.bind("<Button-1>", toggle_frame)


situations = ["Vencidas", "Abertas", "Fechadas"]
situation_vars = [tk.IntVar() for _ in situations]
situation_button = tk.Button(frameTabela, text="Situação")
situation_button.grid(row=0, column=4)
situation_button.bind("<Button-1>", show_frame)


#Pesquisa
def search(event=None):
    # Chama a função preencher_treeview passando o valor da pesquisa
    bethouse_list = set()
    preencher_treeview(conn, tabela, bethouse_options, situation_vars, order_button1, order_button2, time_button, timeframe_combobox, search_var, frameTabela, frameSaldos, bethouse_list=bethouse_list)

# Cria uma variável de controle para rastrear as alterações no Entry
search_var = tk.StringVar()
search_entry = tk.Entry(frameTabela, textvariable=search_var, width=10)
search_entry.grid(row=0, column=5)
icon_photo = ImageTk.PhotoImage(Image.open("pesquisa.png").resize((16, 16), Image.LANCZOS))
search_icon_label = tk.Label(frameTabela, image=icon_photo)
search_icon_label.place(x=535, y=4)
# Vincula a função search ao evento de pressionar o botão de pesquisa
search_icon_label.bind("<Button-1>", search)
# Vincula a função search ao evento de pressionar a tecla Enter no campo de pesquisa
search_entry.bind("<Return>", search)

def load_bethouse_options():
    global bethouse_options, mercado_options, arred_var
    try:
        with open('bethouse_options.json', 'r') as f:
            data = json.load(f)
            bethouse_options = data.get("bethouse_options", {})
            mercado_options = data.get("mercado_options", [])
            arred_var = tk.StringVar(value=data.get("arredondamento"))
            filtros = data.get("filtros", {})
            order_text = filtros.get("ordem", "Crescente")
            add_text = filtros.get("data_entrada", "Data")
            time_text = filtros.get("time", "Feitas desde")
            timeframe_text = filtros.get("timeframe", "hoje")
            selected_situations = filtros.get("situations", [])
            return order_text, add_text, time_text, timeframe_text, selected_situations
    except FileNotFoundError:
        bethouse_options = {}
        mercado_options = ["1", "12", "1X", "2", "AH1", "AH2", "ClearSheet1", "ClearSheet2", "DNB1", "DNB2", "EH1", "EH2", "EHX", "Exactly", "Lay", "Not", "Q1", "Q2", "Removal", "ScoreBoth", "TO", "TU", "TO1", "TO2", "TU2", "TU1", "WinNil1", "WinNil2", "WinLeastOneOfPer1", "WinLeastOneOfPer2", "X", "X2"]
        arred_var = tk.StringVar(value='Padrão')
        order_text = "Crescente"
        add_text = "Data"
        time_text = "Feitas desde"
        timeframe_text = "hoje"
        selected_situations = []
        return order_text, add_text, time_text, timeframe_text, selected_situations

order_text, add_text, time_text, timeframe_text, selected_situations = load_bethouse_options()
order_button1["text"] = order_text
order_button2["text"] = add_text
time_button["text"] = time_text
timeframe_combobox.set(timeframe_text)
if len(selected_situations) != len(situation_vars):
    print("Erro: O tamanho das listas selected_situations e situation_vars é diferente")
else:
    for i, var in enumerate(situation_vars):
        var.set(selected_situations[i]) # Configurações de usuário



def open_bethouses():
    # Cria uma janela pop-up
    bethouses_window = tk.Toplevel(frameJogo)
    bethouses_window.title("BetHouses e Mercados")
    bethouses_frame = tk.Frame(bethouses_window)
    bethouses_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

    # Cria a entrada de texto para adicionar novas BetHouses
    bethouse_label = tk.Label(bethouses_frame, text='BetHouse:')
    bethouse_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
    new_bethouse_entry = tk.Entry(bethouses_frame, width=15)
    new_bethouse_entry.grid(row=0, column=2, columnspan=2, padx=5, pady=5)

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
    new_rate_entry = tk.Entry(bethouses_frame, validate='key', validatecommand=vcmd_tax, width=6)
    new_rate_entry.insert(0, '0.0')
    new_rate_entry.grid(row=1, column=1, padx=5, pady=5)

    arred_base_var = tk.DoubleVar(value=0.01)
    arred_base_label = tk.Label(bethouses_frame, text="Arred.:")
    arred_base_label.grid(row=1, column=2)
    arred_base_options = [0.01, 0.05, 0.1, 0.5, 1, 5, 10]
    arred_base_combobox = ttk.Combobox(bethouses_frame, textvariable=arred_base_var, values=arred_base_options, width=3, state="readonly")
    arred_base_combobox.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)


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
            'background_color': background_color,
            'arred': arred_base_var.get()
        }
        new_bethouse_entry.delete(0, tk.END)
        new_rate_entry.delete(0, tk.END)
        text_color_entry.delete(0, tk.END)
        background_color_entry.delete(0, tk.END)
        save_bethouse_options()
        update_bethouses_list()

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
    text_color_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    background_color_button = tk.Button(bethouses_frame, text='Cor de Fundo', command=choose_background_color)
    background_color_button.grid(row=3, column=2, columnspan=2, padx=5, pady=5)

    # Cria botão para adicionar a nova BetHouse
    add_bethouse_button = tk.Button(bethouses_frame, text="Adicionar", command=add_bethouse)
    add_bethouse_button.grid(row=4, column=0, columnspan=4, padx=5, pady=5)

    # Cria a lista de BetHouses
    configStyle = ttk.Style()
    configStyle.configure("Normal.Treeview", rowheight=20)
    bethouses_list = sorted(bethouse_options.keys())
    bethouses_tree = ttk.Treeview(bethouses_frame, columns=('Bethouse', 'Taxa'), show='headings', style="Normal.Treeview")
    bethouses_tree.grid(row=5, column=0, columnspan=4, padx=5, pady=5)
    bethouses_tree.heading('Bethouse', text='BetHouse')
    bethouses_tree.heading('Taxa', text='Taxa')
    bethouses_tree.column('Bethouse', width=70)
    bethouses_tree.column('Taxa', width=70)
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
    remove_bethouse_button.grid(row=6, column=0, columnspan=4, padx=5, pady=5)

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
    mercado_label.grid(row=2, column=4, padx=5, pady=5)
    new_mercado_entry = tk.Entry(bethouses_frame)
    new_mercado_entry.grid(row=3, column=4, padx=5, pady=5)

    # Cria um botão para adicionar a nova opção de mercado
    add_mercado_button = tk.Button(bethouses_frame, text="Adicionar", command=add_mercado_option)
    add_mercado_button.grid(row=4, column=4, columnspan=2, padx=5, pady=5)

    # Cria a lista de opções de mercado
    mercado_options_list = sorted(list(mercado_options), key=lambda x: x[0])
    # Adiciona as BetHouses à Listbox
    mercado_options_listbox = tk.Listbox(bethouses_frame)
    mercado_options_listbox.grid(row=5, column=4, columnspan=2, padx=5, pady=5)
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
    remove_mercado_button.grid(row=6, column=4, columnspan=2, padx=5, pady=5)

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

def save_bethouse_options():
    sorted_bethouse_options = dict(sorted(bethouse_options.items(), key=lambda x: x[0]))
    sorted_mercado_options = sorted(mercado_options, key=lambda x: x[0])
    arredondamento = arred_var.get()
    data = {
        "bethouse_options": sorted_bethouse_options,
        "mercado_options": sorted_mercado_options,
        "arredondamento": arredondamento,
        "filtros": {
            "ordem": order_button1["text"],
            "data_entrada": order_button2["text"],
            "time": time_button["text"],
            "timeframe": timeframe_combobox.get(),
            "situations": [var.get() for var in situation_vars]
        }
    }
    with open('bethouse_options.json', 'w') as f:
        json.dump(data, f, sort_keys=True)

settings_button.grid(row=0, column=0, sticky="w") # Menu de Configurações # Menus

# Botão Arredondamento
def arredondamento_changed(event):
    save_bethouse_options()

arred_label = tk.Label(frameJogo, text="Arred.:")
arred_label.grid(row=2, column=2, columnspan=2)
arred_options = ['Padrão', 0.01, 0.05, 0.1, 0.5, 1, 5, 10]
arred_combobox = ttk.Combobox(frameJogo, textvariable=arred_var, values=arred_options, width=5, state="readonly")
arred_combobox.grid(row=2, column=4, columnspan=2, padx=5, pady=5, sticky=tk.W)
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
opcoes_anos = [datetime.now().date().year - 1, datetime.now().date().year, datetime.now().date().year + 1]
ano_var = tk.StringVar(value=datetime.now().year)
ano_combobox = ttk.Combobox(frameJogo, textvariable=ano_var, values=opcoes_anos, width=4)
ano_combobox.bind('<KeyRelease>', update_year_combobox)
ano_combobox.grid(row=1, column=4, padx=5, pady=5, sticky=tk.W) # Ano
def set_placeholder_text(entry, placeholder):
    entry.insert(0, placeholder)
    entry.bind('<FocusIn>', lambda event: on_entry_click(entry, placeholder))
    entry.bind('<FocusOut>', lambda event: on_focus_out(entry, placeholder))

def on_entry_click(entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, tk.END)  # Limpar o texto existente
        entry.config(foreground='black')  # Alterar a cor do texto para preto

def on_focus_out(entry, placeholder):
    if entry.get() == "":
        entry.insert(0, placeholder)  # Restaurar o texto do placeholder
        entry.config(foreground='gray')

esporte_entry = tk.Entry(frameJogo, foreground='gray')
set_placeholder_text(esporte_entry, "Esporte")
esporte_entry.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

# Adiciona campo Jogo
jogo_label = tk.Label(frameJogo, text="Jogo")
jogo_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
jogo_entry = tk.Entry(frameJogo)
set_placeholder_text(jogo_entry, "Jogo (Equipe 1 - Equipe 2)")
jogo_entry.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W) # Jogo

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
data_label.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W)

# Configurar o box dia
dia_entry = tk.Entry(frameJogo, width=2, validate="key", validatecommand=(frameJogo.register(validate_day), "%P"))
dia_atual = datetime.now().day
dia_entry.insert(0, dia_atual)
dia_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W) # Dia

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
mes_atual = datetime.now().strftime('%b')
mes_atual_pt = {'Jan': 'Jan', 'Feb': 'Fev', 'Mar': 'Mar', 'Apr': 'Abr', 'May': 'Mai', 'Jun': 'Jun', 'Jul': 'Jul', 'Aug': 'Ago', 'Sep': 'Set', 'Oct': 'Out', 'Nov': 'Nov', 'Dec': 'Dez'}[mes_atual]
mes_combobox = ttk.Combobox(frameJogo, values=mes_options, width=3, validate="key", validatecommand=(frameJogo.register(validate_month), "%P"))
if mes_atual_pt in mes_options:
    mes_combobox.current(mes_options.index(mes_atual_pt))
else:
    mes_combobox.set(mes_options[0])
mes_combobox.bind("<KeyRelease>", update_combobox)
mes_combobox.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W) # Mês

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
hora_label.grid(row=0, column=5)
hora_entry = tk.Entry(frameJogo, width=2, validate="key", validatecommand=(frameJogo.register(validate_hour), "%P"))
hora_entry.insert(0, 12)
hora_entry.grid(row=1, column=5, padx=5, pady=5, sticky=tk.W)
doispontos_label = tk.Label(frameJogo, text=":")
doispontos_label.grid(row=1, column=6) # Hora

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
minuto_entry.grid(row=1, column=7, padx=5, pady=5, sticky=tk.W) # Data

# Adiciona campo BetHouse
# BetHouse 1
bethouse_label = tk.Label(frameApostas, text="BetHouses")
bethouse_label.grid(row=0, column=0)
def on_select(value):
    selected_bethouse = bethouse_var.get()
    text_color = bethouse_options[selected_bethouse]['text_color']
    background_color = bethouse_options[selected_bethouse]['background_color']
    valor_entry.configure(fg=text_color, bg=background_color)
    odd_entry.configure(fg=text_color, bg=background_color)
    aposta_entry.configure(fg=text_color, bg=background_color)
bethouse_combobox, bethouse_var = create_combobox(frameApostas, sorted(list(bethouse_options.keys())), row=1, column=0, width=7)
bethouse_combobox.bind("<<ComboboxSelected>>", on_select)
# BetHouse 2
def on_select2(value):
    selected_bethouse = bethouse_var2.get()
    text_color = bethouse_options[selected_bethouse]['text_color']
    background_color = bethouse_options[selected_bethouse]['background_color']
    valor_entry2.configure(fg=text_color, bg=background_color)
    odd_entry2.configure(fg=text_color, bg=background_color)
    aposta_entry2.configure(fg=text_color, bg=background_color)
bethouse_combobox2, bethouse_var2 = create_combobox(frameApostas, sorted(list(bethouse_options.keys())), row=2, column=0, width=7)
bethouse_combobox2.bind("<<ComboboxSelected>>", on_select2)

# cria o botão de alternância
num_bets = 2
def alternar_bets():
    global num_bets
    if num_bets == 2:
        num_bets = 3
        bethouse_combobox3.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        mercado_combobox3.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        valor_entry3.grid(row=3, column=2, padx=5, pady=5, sticky=tk.W)
        odd_entry3.grid(row=3, column=3, padx=5, pady=5, sticky=tk.W)
        real_label3.grid(row=3, column=4)
        aposta_entry3.grid(row=3, column=5, padx=5, pady=5, sticky=tk.W)
        palpite3_label.grid(row=3, column=6)
        lucro3_label.grid(row=3, column=7)
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
alternar_bets_btn.grid(row=2, column=5, columnspan=4) # Add 3ª Aposta

def on_select3(value):
    selected_bethouse = bethouse_var3.get()
    text_color = bethouse_options[selected_bethouse]['text_color']
    background_color = bethouse_options[selected_bethouse]['background_color']
    valor_entry3.configure(fg=text_color, bg=background_color)
    odd_entry3.configure(fg=text_color, bg=background_color)
    aposta_entry3.configure(fg=text_color, bg=background_color)
bethouse_combobox3, bethouse_var3 = create_combobox(frameApostas, sorted(list(bethouse_options.keys())), row=3, column=0, width=7)
bethouse_combobox3.grid_remove()
bethouse_combobox3.bind("<<ComboboxSelected>>", on_select3)
# BetHouses

def on_mercado_combobox_selected(event):
    if mercado_var.get().startswith('T'):
        if mercado_var.get() == 'TO':
            if num_bets == 2 and mercado_var2.get() == '':
                mercado_var2.set('TU')
            elif num_bets == 3 and mercado_var2.get() == '' and mercado_var3.get() == '':
                mercado_var2.set('TU')
                mercado_var3.set('TU')
        elif mercado_var.get() == 'TO1':
            if num_bets == 2 and mercado_var2.get() == '':
                mercado_var2.set('TU1')
            elif num_bets == 3 and mercado_var2.get() == '' and mercado_var3.get() == '':
                mercado_var2.set('TU1')
                mercado_var3.set('TU1')
        elif mercado_var.get() == 'TO2':
            if num_bets == 2 and mercado_var2.get() == '':
                mercado_var2.set('TU2')
            elif num_bets == 3 and mercado_var2.get() == '' and mercado_var3.get() == '':
                mercado_var2.set('TU2')
                mercado_var3.set('TU2')
        elif mercado_var.get() == 'TU':
            if num_bets == 2 and mercado_var2.get() == '':
                mercado_var2.set('TO')
            elif num_bets == 3 and mercado_var2.get() == '' and mercado_var3.get() == '':
                mercado_var2.set('TO')
                mercado_var3.set('TO')
        elif mercado_var.get() == 'TU1':
            if num_bets == 2 and mercado_var2.get() == '':
                mercado_var2.set('TO1')
            elif num_bets == 3 and mercado_var2.get() == '' and mercado_var3.get() == '':
                mercado_var2.set('TO1')
                mercado_var3.set('TO1')
        elif mercado_var.get() == 'TU2':
            if num_bets == 2 and mercado_var2.get() == '':
                mercado_var2.set('TO2')
            elif num_bets == 3 and mercado_var2.get() == '' and mercado_var3.get() == '':
                mercado_var2.set('TO2')
                mercado_var3.set('TO2')
    elif mercado_var.get() == '1':
        if num_bets == 2 and mercado_var2.get() == '':
            mercado_var2.set('2')
        elif num_bets == 3 and mercado_var2.get() == '' and mercado_var3.get() == '':
            mercado_var2.set('X')
            mercado_var3.set('2')
    elif mercado_var.get() == '2':
        if num_bets == 2 and mercado_var2.get() == '':
            mercado_var2.set('1')
        elif num_bets == 3 and mercado_var2.get() == '' and mercado_var3.get() == '':
            mercado_var2.set('X')
            mercado_var3.set('1')
    elif mercado_var.get() == '12':
        if num_bets == 2 and mercado_var2.get() == '':
            mercado_var2.set('X')
    elif mercado_var.get() == 'X':
        if num_bets == 2 and mercado_var2.get() == '':
            mercado_var2.set('12')
    elif mercado_var.get() == '1X':
        if num_bets == 2 and mercado_var2.get() == '':
            mercado_var2.set('2')
    elif mercado_var.get() == 'X2':
        if num_bets == 2 and mercado_var2.get() == '':
            mercado_var2.set('1')
    elif mercado_var.get() == 'DNB1':
        if num_bets == 2 and mercado_var2.get() == '':
            mercado_var2.set('DNB2')
        elif num_bets == 3 and mercado_var2.get() == '' and mercado_var3.get() == '':
            mercado_var2.set('X')
            mercado_var3.set('2')
    elif mercado_var.get() == 'DNB2':
        if num_bets == 2 and mercado_var2.get() == '':
            mercado_var2.set('DNB1')
        elif num_bets == 3 and mercado_var2.get() == '' and mercado_var3.get() == '':
            mercado_var2.set('X')
            mercado_var3.set('1')
    elif mercado_var.get() == 'AH1':
        if num_bets == 2 and mercado_var2.get() == '':
            mercado_var2.set('AH2')
        elif num_bets == 3 and mercado_var2.get() == '' and mercado_var3.get() == '':
            mercado_var2.set('X')
            mercado_var3.set('2')
            valor_var.set(0)
    elif mercado_var.get() == 'AH2':
        if num_bets == 2 and mercado_var2.get() == '':
            mercado_var2.set('AH1')
        elif num_bets == 3 and mercado_var2.get() == '' and mercado_var3.get() == '':
            mercado_var2.set('X')
            mercado_var3.set('1')
            valor_var.set(0)

def on_valor_combobox_selected(event):
    def float_error(valor):
        try:
            valor_float = valor.get()
        except _tkinter.TclError:
            valor_float = ''
        return valor_float
    if float_error(valor_var) == 0 and num_bets == 2:
            valor_var2.set(0)
    elif mercado_var.get().startswith('T'):
        if num_bets == 2 and mercado_var2.get().startswith('T'):
            valor_var2.set(float_error(valor_var))
        elif num_bets == 3 and (float_error(valor_var).is_integer() or (float_error(valor_var)-0.25).is_integer() or (float_error(valor_var)-0.75).is_integer()) and mercado_var2.get().startswith('T') and mercado_var3.get().startswith('T'):
            arred_valor = round(valor_var.get(), 0)
            valor_var2.set(arred_valor - 0.5)
            valor_var3.set(arred_valor + 0.5)
    elif mercado_var.get().startswith('AH') and mercado_var2.get().startswith('AH'):
        if num_bets == 2:
            valor_var2.set(-valor_var.get())
        elif num_bets == 3:
            if mercado_var3.get().startswith('AH') and valor_var.get().is_integer():
                valor_var2.set(-(valor_var.get() - 0.5))
                valor_var3.set(-(valor_var.get() + 0.5))
    elif mercado_var.get().startswith('DNB') and mercado_var2.get().startswith('AH') and num_bets == 2:
        valor_var2.set(0)
    elif mercado_var2.get().startswith('DNB') and mercado_var.get().startswith('AH') and num_bets == 2:
        valor_var.set(0)

# Adiciona campo Mercado
mercado_label = tk.Label(frameApostas, text="Mercado")
mercado_label.grid(row=0, column=1)
mercado_combobox, mercado_var = create_combobox(frameApostas, mercado_options, row=1, column=1, width=7)
mercado_combobox.bind("<<ComboboxSelected>>", lambda event: update_columns())
mercado_combobox.bind("<<ComboboxSelected>>", on_mercado_combobox_selected)
# Adiciona campo Valor
valor_entry, valor_var = create_float_entry(frameApostas, row=1, column=2, width=4, dig=3, dec=2, restrict="quarter")
valor_entry.bind("<FocusOut>", on_valor_combobox_selected)

# Adiciona campo Mercado2
mercado_combobox2, mercado_var2 = create_combobox(frameApostas, mercado_options, row=2, column=1, width=7)
mercado_combobox2.bind("<<ComboboxSelected>>", lambda event: update_columns())

# Adiciona campo Valor2
valor_entry2, valor_var2 = create_float_entry(frameApostas, row=2, column=2, width=4, dig=3, dec=2, restrict="quarter")
valor_entry2.bind("<FocusOut>", on_valor_combobox_selected)

# Adiciona campo Mercado2
mercado_combobox3, mercado_var3 = create_combobox(frameApostas, mercado_options, row=3, column=1, width=7)
mercado_combobox3.grid_remove()
# Adiciona campo Valor2
valor_entry3, valor_var3 = create_float_entry(frameApostas, row=3, column=2, width=4, dig=3, dec=2, restrict="quarter")
valor_entry3.grid_remove()

def fill_empty_entry_with_zero(event):
    entry = event.widget
    if not entry.get():
        entry.delete(0, tk.END)
        entry.insert(0, "0.0")

# Adiciona campo ODD
odd_label = tk.Label(frameApostas, text="ODD")
odd_label.grid(row=0, column=3)
odd_entry, odd_var = create_float_entry(frameApostas, row=1, column=3, width=4, dig=3, dec=3, value=0.0, negative=False)
odd_entry.bind("<FocusOut>", fill_empty_entry_with_zero)
# Adiciona campo ODD2
odd_entry2, odd_var2 = create_float_entry(frameApostas, row=2, column=3, width=4, dig=3, dec=3, value=0.0, negative=False)
odd_entry2.bind("<FocusOut>", fill_empty_entry_with_zero)
# Adiciona campo ODD3
odd_entry3, odd_var3 = create_float_entry(frameApostas, row=3, column=3, width=4, dig=3, dec=3, value=0.0, negative=False)
odd_entry3.bind("<FocusOut>", fill_empty_entry_with_zero)
odd_entry3.grid_remove() # Odds

# Adiciona campo Aposta
real_label = tk.Label(frameApostas, text="R$")
real_label.grid(row=1, column=4)

label_aposta = tk.Label(frameApostas, text="Aposta")
label_aposta.grid(row=0, column=5, padx=5, pady=5, sticky=tk.W)
aposta_entry, aposta_var = create_float_entry(frameApostas, row=1, column=5, width=5, dig=4, dec=2, value=0.0, negative=False)
aposta_entry.bind("<FocusOut>", fill_empty_entry_with_zero)
#Adicionar aposta2
real_label2 = tk.Label(frameApostas, text="R$")
real_label2.grid(row=2, column=4)
aposta_entry2, aposta_var2 = create_float_entry(frameApostas, row=2, column=5, width=5, dig=4, dec=2, value=0.0, negative=False) # Aposta 2
aposta_entry2.bind("<FocusOut>", fill_empty_entry_with_zero)
#Adicionar aposta3
real_label3 = tk.Label(frameApostas, text="R$")
aposta_entry3, aposta_var3 = create_float_entry(frameApostas, row=3, column=5, width=5, dig=4, dec=2, value=0.0, negative=False)
aposta_entry3.grid_remove()
aposta_entry3.bind("<FocusOut>", fill_empty_entry_with_zero)


#Adicionando cálculos
def on_variable_change(*args):
    odds = [odd_var.get(), odd_var2.get(), odd_var3.get()]
    apostas = [aposta_var.get(), aposta_var2.get(), aposta_var3.get()]
    taxas = [bethouse_options.get(bethouse_var.get(), {}).get('taxa', 0.0),
             bethouse_options.get(bethouse_var2.get(), {}).get('taxa', 0.0),
             bethouse_options.get(bethouse_var3.get(), {}).get('taxa', 0.0)]
    def float_error(valor):
        try:
            valor_float = valor.get()
        except _tkinter.TclError:
            valor_float = 0.0
        return valor_float

    if (len([odd for odd in odds if odd != 0.0]) == num_bets) and (len([aposta for aposta in apostas if aposta != 0.0]) >= 1):
        arred = arred_var.get()
        bonus = [bonus1.get(), bonus2.get(), bonus3.get()]
        if arred == 'Padrão':
            arreds = [float(bethouse_options.get(bethouse_var.get(), {}).get('arred', 0.0)),
                      float(bethouse_options.get(bethouse_var2.get(), {}).get('arred', 0.0)),
                      float(bethouse_options.get(bethouse_var3.get(), {}).get('arred', 0.0))]
        else:
            arred = float(arred)
            arreds = [arred, arred, arred]
        resultado = calc_apostas(apostas[0], apostas[1], apostas[2], odds[0], odds[1], odds[2], mercado_var.get(), mercado_var2.get(), mercado_var3.get(), float_error(valor_var), float_error(valor_var2), float_error(valor_var3), taxas[0], taxas[1], taxas[2], arreds, bonus)
        palpite1_label.config(text=f"R$ {format(round(resultado[0],2), '.2f')}" if resultado[0] is not None else "")
        palpite2_label.config(text=f"R$ {format(round(resultado[1],2), '.2f')}" if resultado[1] is not None else "")
        palpite3_label.config(text=f"R$ {format(round(resultado[2],2), '.2f')}" if resultado[2] is not None else "")
        lucro1_label.config(text=f"R$ {format(round(resultado[4],2), '.2f')}" if resultado[4] is not None else "", fg='seagreen' if resultado[4] > 0 else ('red' if resultado[4] < 0 else 'gray'), font=("Arial", 14, "bold"))
        lucro2_label.config(text=f"R$ {format(round(resultado[5],2), '.2f')}" if resultado[5] is not None else "", fg='seagreen' if resultado[5] > 0 else ('red' if resultado[6] < 0 else 'gray'), font=("Arial", 14, "bold"))
        lucro3_label.config(text=f"R$ {format(round(resultado[6],2), '.2f')}" if resultado[6] is not None else "", fg='seagreen' if resultado[6] > 0 else ('red' if resultado[7] < 0 else 'gray'), font=("Arial", 14, "bold"))
        liability_label1.config(text=f"R$ {format(round(resultado[3],2), '.2f')}" if resultado[3] is not None else "")
        liability_label2.config(text=f"R$ {format(round(resultado[8],2), '.2f')}" if resultado[8] is not None else "")
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

def on_label_click(bonus_var, combobox):
    if bonus_var.get():
        response = messagebox.askyesno("Bonus", f"Desativar Bônus para {combobox.get()}?")
        if response:
            bonus_var.set(False)
    else:
        response = messagebox.askyesno("Bonus", f"Ativar Bônus para {combobox.get()}?")
        if response:
            bonus_var.set(True)
bonus1 = tk.BooleanVar(value=False)
bonus2 = tk.BooleanVar(value=False)
bonus3 = tk.BooleanVar(value=False)

#Palpites
palpite_label = tk.Label(frameApostas, text='Palpites')
palpite_label.grid(row=0, column=6, padx=5, pady=5, sticky=tk.W)
palpite1_label = tk.Label(frameApostas, text="")
palpite1_label.grid(row=1, column=6)
palpite1_label.bind("<Button-1>", lambda event: on_label_click(bonus1, bethouse_combobox))
palpite2_label = tk.Label(frameApostas, text="")
palpite2_label.grid(row=2, column=6)
palpite2_label.bind("<Button-1>", lambda event: on_label_click(bonus2, bethouse_combobox2))
palpite3_label = tk.Label(frameApostas, text="")
palpite3_label.bind("<Button-1>", lambda event: on_label_click(bonus3, bethouse_combobox3))
# Palpites

#Lucro
liability_label = tk.Label(frameApostas, text='Liability')
liability_label1 = tk.Label(frameApostas, text='')
liability_label2 = tk.Label(frameApostas, text='')
lucro_label = tk.Label(frameApostas, text='Lucro')
lucro_label.grid(row=0, column=7, padx=5, pady=5, sticky=tk.W)
lucro1_label = tk.Label(frameApostas, text="")
lucro1_label.grid(row=1, column=7)
lucro1_label.bind("<Button-1>", lambda event: on_label_click(bonus1, bethouse_combobox))
lucro2_label = tk.Label(frameApostas, text="")
lucro2_label.grid(row=2, column=7)
lucro2_label.bind("<Button-1>", lambda event: on_label_click(bonus2, bethouse_combobox2))
lucro3_label = tk.Label(frameApostas, text="")
lucro3_label.bind("<Button-1>", lambda event: on_label_click(bonus3, bethouse_combobox3))
lucro_percent_label = tk.Label(frameApostas, text='Lucro %')
lucro_percent_label.grid(row=0, column=8, padx=5, pady=5, sticky=tk.W)
lucro_percent_label1 = tk.Label(frameApostas, text="", font=("Arial", 20, "bold"))
lucro_percent_label1.grid(row=1, column=8, rowspan=2)# Lucro

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
mercado_var3.trace_add('write', on_variable_change)
bonus1.trace_add('write', on_variable_change)
bonus2.trace_add('write', on_variable_change)
bonus3.trace_add('write', on_variable_change)
# on_variable change para variaveis

def update_columns():
    if mercado_var.get() == "Lay" or mercado_var2.get() =="Lay":
        liability_label.grid(row=0, column=7, padx=5, pady=5, sticky=tk.W)
        lucro_label.grid(row=0, column=8, padx=5, pady=5, sticky=tk.W)
        lucro1_label.grid(row=1, column=8)
        lucro2_label.grid(row=2, column=8)
        lucro_percent_label.grid(row=0, column=9, padx=5, pady=5, sticky=tk.W)
        lucro_percent_label1.grid(row=1, column=9, rowspan=2)
        if mercado_var.get() == "Lay" and mercado_var2.get() == "Lay":
            liability_label1.grid(row=1, column=7, padx=5, pady=5, sticky=tk.W)
            liability_label2.grid(row=2, column=7, padx=5, pady=5, sticky=tk.W)
            lucro_percent_label.grid(row=0, column=9, padx=5, pady=5, sticky=tk.W)
            lucro_percent_label1.grid(row=1, column=9, rowspan=2)
        elif mercado_var.get() == "Lay":
            liability_label1.grid(row=1, column=7, padx=5, pady=5, sticky=tk.W)
            liability_label2.grid_remove()
            lucro_percent_label.grid(row=0, column=9, padx=5, pady=5, sticky=tk.W)
            lucro_percent_label1.grid(row=1, column=9, rowspan=2)
        else:
            liability_label2.grid(row=2, column=7, padx=5, pady=5, sticky=tk.W)
            liability_label1.grid_remove()
            lucro_percent_label.grid(row=0, column=9, padx=5, pady=5, sticky=tk.W)
            lucro_percent_label1.grid(row=1, column=9, rowspan=2)
    else:
        liability_label.grid_forget()
        lucro_label.grid(row=0, column=7, padx=5, pady=5, sticky=tk.W)
        lucro1_label.grid(row=1, column=7)
        lucro2_label.grid(row=2, column=7)
        lucro_percent_label.grid(row=0, column=8, padx=5, pady=5, sticky=tk.W)
        lucro_percent_label1.grid(row=1, column=8, rowspan=2) # Cálculos

# cria o botão de gravação
def resetar_variaveis():
    # Redefinir as variáveis para os valores iniciais desejados
    jogo_entry.delete(0, tk.END)
    esporte_entry.delete(0, tk.END)
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
    bonus1.set(False)
    bonus2.set(False)
    bonus3.set(False)
    if num_bets == 3:
        alternar_bets()
    esporte_entry.delete(0, tk.END)
    valor_entry.configure(fg='systemWindowBody', bg='systemWindowBody')
    odd_entry.configure(fg='systemWindowBody', bg='systemWindowBody')
    aposta_entry.configure(fg='systemWindowBody', bg='systemWindowBody')
    valor_entry2.configure(fg='systemWindowBody', bg='systemWindowBody')
    odd_entry2.configure(fg='systemWindowBody', bg='systemWindowBody')
    aposta_entry2.configure(fg='systemWindowBody', bg='systemWindowBody')
    valor_entry3.configure(fg='systemWindowBody', bg='systemWindowBody')
    odd_entry3.configure(fg='systemWindowBody', bg='systemWindowBody')
    aposta_entry3.configure(fg='systemWindowBody', bg='systemWindowBody')
    if 'edit_button' in globals():
        edit_button.grid_remove()

def gravar():
    odds = [odd_var.get(), odd_var2.get(), odd_var3.get()]
    apostas = [aposta_var.get(), aposta_var2.get(), aposta_var3.get()]
    if " - " in jogo_entry.get():
        time_casa, time_fora = jogo_entry.get().split(" - ")
    elif " vs " in jogo_entry.get():
        time_casa, time_fora = jogo_entry.get().split(" vs ")
    elif " x " in jogo_entry.get():
        time_casa, time_fora = jogo_entry.get().split(" x ")
    else:
        time_casa, time_fora = "", ""

    if (len([odd for odd in odds if odd != 0.0]) >= 2)\
            and (len([aposta for aposta in apostas if aposta != 0.0]) >= 1)\
            and time_casa != "" and time_fora != ""\
            and (bethouse_combobox.get() in bethouse_options.keys())\
            and (bethouse_combobox2.get() in bethouse_options.keys())\
            and ((num_bets != 3) or (num_bets == 3 and bethouse_combobox3.get() in bethouse_options.keys())):
        count_query = "SELECT COUNT(*) FROM apostas"
        c.execute(count_query)
        result = c.fetchone()
        num_linhas = result[0]
        dados = {
            'id': num_linhas + 1,
            'data_entrada': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data_jogo': datetime.strptime(f"{ano_combobox.get()}-{convert_mes(mes_combobox.get()):02}-{int(dia_entry.get()):02} {int(hora_entry.get()):02}:{int(minuto_entry.get()):02}:00", '%Y-%m-%d %H:%M:%S'),
            'time_casa': time_casa,
            'time_fora': time_fora,
            'bethouse1': bethouse_combobox.get(),
            'mercado1': mercado_combobox.get(),
            'valor1': valor_entry.get() if valor_entry.get() != '' else None,
            'odd1': odd_entry.get(),
            'aposta1': palpite1_label.cget("text").replace("R$", "").strip(),
            'resultado1': None,
            'bethouse2': bethouse_combobox2.get(),
            'mercado2': mercado_combobox2.get(),
            'valor2': valor_entry2.get() if valor_entry2.get() != '' else None,
            'odd2': odd_entry2.get(),
            'aposta2': palpite2_label.cget("text").replace("R$", "").strip(),
            'resultado2': None,
            'bethouse3': bethouse_combobox3.get() if bethouse_combobox3.get() != '' else None,
            'mercado3': mercado_combobox3.get() if mercado_combobox3.get() != '' else None,
            'valor3': valor_entry3.get() if valor_entry3.get() != '' else None,
            'odd3': odd_entry3.get()  if odd_entry3.get() != '' else None,
            'aposta3': palpite3_label.cget("text").replace("R$", "").strip() if palpite3_label.cget("text").replace("R$", "").strip() != '' else None,
            'resultado3': None,
            'lucro_estimado': lucro1_label.cget("text").replace("R$", "").strip(),
            'lucro_per_estimado': lucro_percent_label1.cget("text").strip("%"),
            'lucro_real': None,
            'lucro_per_real': None,
            'esporte': converter_esporte(esporte_entry.get().split(". ")[0])
        }

        # Gravação dos dados na tabela e atualização da Treeview
        dados = {k: str(v) if isinstance(v, datetime) else convert_to_numeric(v).strip().split('\n')[0] if isinstance(v, str) and '\n' in v else convert_to_numeric(v) for k, v in dados.items()}
        bethouse_list = {valor for valor in [dados['bethouse1'], dados['bethouse2'], dados['bethouse3']] if valor}

        save_apostas(dados, conn)

        preencher_treeview(conn, tabela, bethouse_options, situation_vars, order_button1, order_button2, time_button, timeframe_combobox, search_var, frameTabela, frameSaldos, bethouse_list=bethouse_list)
        resetar_variaveis()

    else:
        messagebox.showwarning("Aviso", "Preencha o jogo, as BetHouses, as odds e uma aposta.")

gravar_button = tk.Button(frameGravar, text="Gravar", command=gravar)
gravar_button.grid(row=0, column=0)
clear_button = tk.Button(frameGravar, text="Limpar", command=resetar_variaveis)
clear_button.grid(row=0, column=1) # Gravar

def select_bets(event):
    global edit_button
    df_filtrado = import_df_filtrado()
    # Obter o item selecionado na tabela
    item_id = tabela.focus()
    item_values = tabela.item(item_id)['values']

    # Obter o ID da linha selecionada
    id_selecionado = item_values[9]  # Índice 9 corresponde ao campo 'ID'

    # Buscar as informações da linha correspondente ao ID no DataFrame df_filtrado
    row = df_filtrado[df_filtrado['id'] == id_selecionado].iloc[0]
    row['data_jogo'] = pd.to_datetime(row['data_jogo'])
    jogo_entry.delete(0, 'end')
    jogo_entry.insert(0, f"{row['time_casa']} - {row['time_fora']}")
    dia_entry.delete(0, 'end')
    dia_entry.insert(0, row['data_jogo'].day)
    mes_combobox.set(convert_mes(row['data_jogo'].month))
    ano_combobox.set(row['data_jogo'].year)
    hora_entry.delete(0, 'end')
    hora_entry.insert(0, row['data_jogo'].hour)
    minuto_entry.delete(0, 'end')
    minuto_entry.insert(0, row['data_jogo'].minute)
    if row['bethouse3'] is not None:
        if num_bets == 2:
            alternar_bets()
        bethouse_combobox3.set(row['bethouse3'])
        mercado_combobox3.set(row['mercado3'])
        valor_entry3.delete(0, 'end')
        valor_entry3.insert(0, row['valor3'] if row['valor3'] is not None else '')
        odd_entry3.delete(0, 'end')
        odd_entry3.insert(0, row['odd3'])
        aposta_var3.set(row['aposta3'])
    bethouse_combobox.set(row['bethouse1'])
    bethouse_combobox2.set(row['bethouse2'])
    mercado_combobox.set(row['mercado1'])
    mercado_combobox2.set(row['mercado2'])
    valor_entry.delete(0, 'end')
    valor_entry.insert(0, row['valor1'] if row['valor1'] is not None else '')
    valor_entry2.delete(0, 'end')
    valor_entry2.insert(0, row['valor2'] if row['valor2'] is not None else '')
    odd_entry.delete(0, 'end')
    odd_entry.insert(0, row['odd1'])
    odd_entry2.delete(0, 'end')
    odd_entry2.insert(0, row['odd2'])
    aposta_var.set(row['aposta1'])
    aposta_var2.set(row['aposta2'])
    esporte_entry.delete(0, 'end')
    esporte_entry.insert(0, row['esporte'])

    def editar_bets():
        # Obter o item selecionado na tabela
        item_id = tabela.focus()
        item_values = tabela.item(item_id)['values']

        # Obter o ID da linha selecionada
        id_selecionado = item_values[9]  # Índice 0 corresponde ao campo 'id'

        # Atualizar os valores da linha correspondente no DataFrame df_filtrado
        mask = df_filtrado['id'] == id_selecionado
        linha_antiga = df_filtrado.loc[mask].iloc[0]
        bethouses_antigas = {valor for valor in [linha_antiga['bethouse1'], linha_antiga['bethouse2'], linha_antiga['bethouse3']] if valor}

        df_filtrado.loc[mask, 'data_entrada'] = df_filtrado.loc[mask, 'data_entrada']
        df_filtrado.loc[mask, 'data_jogo'] = ano_combobox.get() + '-' + f"{convert_mes(mes_combobox.get()):02d}" + '-' + f"{int(dia_entry.get()):02d}" + ' ' + f"{int(hora_entry.get()):02d}" + ':' + f"{int(minuto_entry.get()):02d}" + ":00"
        df_filtrado.loc[mask, 'time_casa'] = jogo_entry.get().split(" - ")[0]
        df_filtrado.loc[mask, 'time_fora'] = jogo_entry.get().split(" - ")[1]
        df_filtrado.loc[mask, 'bethouse1'] = bethouse_combobox.get()
        df_filtrado.loc[mask, 'bethouse2'] = bethouse_combobox2.get()
        df_filtrado.loc[mask, 'bethouse3'] = bethouse_combobox3.get() if bethouse_combobox3.get() != '' else None
        df_filtrado.loc[mask, 'mercado1'] = mercado_combobox.get()
        df_filtrado.loc[mask, 'mercado2'] = mercado_combobox2.get()
        df_filtrado.loc[mask, 'mercado3'] = mercado_combobox3.get() if mercado_combobox3.get() != '' else None
        df_filtrado.loc[mask, 'valor1'] = valor_entry.get() if valor_entry.get().isnumeric() else None
        df_filtrado.loc[mask, 'valor2'] = valor_entry2.get() if valor_entry.get().isnumeric() else None
        df_filtrado.loc[mask, 'valor3'] = valor_entry3.get() if valor_entry.get().isnumeric() else None
        df_filtrado.loc[mask, 'odd1'] = odd_entry.get()
        df_filtrado.loc[mask, 'odd2'] = odd_entry2.get()
        df_filtrado.loc[mask, 'odd3'] = odd_entry3.get() if odd_entry3.get() != '' else None
        df_filtrado.loc[mask, 'aposta1'] = palpite1_label.cget("text").replace("R$", "").strip()
        df_filtrado.loc[mask, 'aposta2'] = palpite2_label.cget("text").replace("R$", "").strip()
        df_filtrado.loc[mask, 'aposta3'] = palpite3_label.cget("text").replace("R$", "").strip() if mercado_combobox3.get() != '' else None
        df_filtrado.loc[mask, 'lucro_estimado'] = round(float(lucro1_label.cget("text").replace("R$", "").strip()), 2)
        df_filtrado.loc[mask, 'lucro_per_estimado'] = round(float(lucro_percent_label1.cget("text").strip("%")), 4)
        df_filtrado.loc[mask, 'esporte'] = esporte_entry.get() if esporte_entry.get() != '' else None

        # Salvar dados na dabela e atualização do Trewwview
        linha = df_filtrado.loc[mask].replace('\n', '', regex=True).to_dict('records')[0]

        bethouse_list = {valor for valor in [linha['bethouse1'], linha['bethouse2'], linha['bethouse3']] if valor}

        save_apostas(linha, conn, tipo='e', linha_antiga=bethouses_antigas)

        # Limpar as variáveis e atualizar a tabela
        preencher_treeview(conn, tabela, bethouse_options, situation_vars, order_button1, order_button2, time_button, timeframe_combobox, search_var, frameTabela, frameSaldos, bethouse_list=bethouse_list)
        resetar_variaveis()

    # Botão Editar
    edit_button = tk.Button(frameGravar, text="Editar", command=editar_bets, foreground="red")
    edit_button.grid(row=0, column=2)

# Definir estilo para o Treeview
style = ttk.Style()
style.configure("Treeview", rowheight=60)

# Criar o Treeview com as colunas desejadas
tabela = BetHistTreeview(frameTabela, situation_vars, order_button1, order_button2, time_button, timeframe_combobox, search_var, frameTabela, frameSaldos, conn, columns=("index", "adds", "jogo", "data", "resultados", "bethouses", "odds", "bets", "mercados", "id"), show="headings", style="Treeview", height=6)
tabela.heading("index", text="")
tabela.heading("adds", text="Adição")
tabela.heading("jogo", text="Jogo")
tabela.heading("data", text="Data")
tabela.heading("resultados", text="W/L")
tabela.heading("bethouses", text="BetHouses")
tabela.heading("odds", text="Odds")
tabela.heading("bets", text="Apostas")
tabela.heading("mercados", text="Mercados")
tabela.heading("id", text="")
tabela.column("id", minwidth=0)
tabela.column("index", width=30)
tabela.column("id", stretch=False)
tabela.column("id", width=0)
tabela.column("jogo", width=130)
tabela.column("data", width=50)
tabela.column("resultados", width=20)
tabela.column("bethouses", width=70)
tabela.column("odds", width=50)
tabela.column("bets", width=70)
tabela.column("mercados", width=70)
tabela.column("adds", width=50)
tabela.grid(row=2, column=0, columnspan=10, rowspan= 10)
tabela.bind('<Double-Button-1>', select_bets) # Tabela

#––––––––––––––––––––––––––––––––––––––# ESTATÍSTICA #––––––––––––––––––––––––––––––––––––––

configStyle = ttk.Style()
configStyle.configure("Normal.Treeview", rowheight=20)

#––––––––––––––––––––––––––––––––––––––# GRÁFICOS #––––––––––––––––––––––––––––––––––––––


#––––––––––––––––––––––––––––––––––––––# RODAR PROGRAMA #––––––––––––––––––––––––––––––––––––––
# Chamar a função para preencher o Treeview
if len(tabela.get_children()) == 0:
    preencher_treeview(conn, tabela, bethouse_options, situation_vars, order_button1, order_button2, time_button, timeframe_combobox, search_var, frameTabela, frameSaldos)

# inicia o loop da janela
janela.mainloop()