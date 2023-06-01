import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
import datetime
from datetime import datetime, timedelta, date
import json
import csv
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
from Pacotes_Lutzer.convert import convert_to_numeric, convert_mes, convert_ms_to_datetime
from Pacotes_Lutzer.validate import create_float_entry, create_combobox
from Pacotes_Lutzer.calc_apostas import calc_apostas
from Pacotes_Lutzer.classes_personalizadas import BetHistTreeview, preencher_treeview, add_aposta, filter_selection, gerar_saldos
from Pacotes_Lutzer.filtros import agregar_datas
import _tkinter
import math


def fechar_programa():
    # Verifica se houve alteração nos resultados
    if not df_resultados.equals(df_resultados_copy):
        # Exibe caixa de diálogo para confirmar a gravação
        resposta = messagebox.askquestion("Salvar Alterações", "Deseja salvar as alterações dos resultados?")

        if resposta == "yes":
            # Salva as alterações no arquivo Apostas.csv
            df_tabela.update(df_filtrado.loc[:, df_filtrado.columns != 'add'])
            convert_ms_to_datetime("Apostas.csv", "Datetime")
            df_tabela.to_csv('Apostas.csv', index=False)

    # Fecha o programa
    janela.destroy()

janela = ThemedTk(theme="marine")
janela.protocol("WM_DELETE_WINDOW", fechar_programa)
janela.wm_title('Controle de Apostas Esportivas (Sure Bets)')

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
botao_tabelas = Button(frameOpcoes, text="Ocultar Tabelas", command=alternar_tabelas)
botao_stats = Button(frameOpcoes, text="Mostrar Gráficos", command=alternar_graficos)
botao_tabelas.grid(row=0, column=1)
botao_stats.grid(row=0, column=2)
alternar_graficos()

# Define uma imagem para o botão de configurações
settings_icon = tk.PhotoImage(file="/Users/sergioeblutzer/PycharmProjects/Gerenciamento_Bolsa_Esportiva/engrenagens.png").subsample(20, 20)
settings_button = tk.Button(frameOpcoes, image=settings_icon, bd=0) # Ajustes Iniciais

# Verifica se o arquivo CSV existe
if not os.path.isfile("Apostas.csv"):
    with open("Apostas.csv", "w", newline="") as f:
        colunas = ["id", "add", "datetime", "time_casa", "time_fora", "bethouse1", "mercado1", "valor1", "odd1", "aposta1", "resultado1", "bethouse2", "mercado2", "valor2", "odd2", "aposta2", "resultado2", "bethouse3", "mercado3", "valor3", "odd3", "aposta3", "resultado3", "lucro_estimado", "lucro_per_estimado", "lucroReal", "lucro_perReal"]
        csv.writer(f).writerow(colunas)

df_tabela = pd.read_csv("Apostas.csv", delimiter=",")
df_filtrado = df_tabela.copy()
df_resultados_copy = df_tabela[["resultado1", "resultado2", "resultado3"]].copy()
df_resultados = df_tabela[["resultado1", "resultado2", "resultado3"]] # Configurações iniciais

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
    preencher_treeview(tabela, bethouse_options, df_tabela, situation_vars, order_button1, order_button2, time_button, timeframe_combobox, frameTabela)
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
    situation_frame = tk.Frame(frameTabela, width=200, height=150)
    situation_frame.place(x=335, y=0)
    for i, (situation, var) in enumerate(zip(situations, situation_vars)):
        if i in [0, 1]:
            tk.Checkbutton(situation_frame, text=situation, variable=var, command=lambda i=i: toggle_situation(i)).grid(row=i+1, column=0)
        else:
            tk.Checkbutton(situation_frame, text=situation, variable=var, command=on_filters_change).grid(row=i+1, column=0)
    close_button = tk.Button(situation_frame, text="Situação", command=situation_frame.destroy)
    close_button.grid(row=0, column=0)
    situation_frame.bind("<FocusOut>", lambda event: situation_frame.destroy())
    situation_frame.focus_set()

situations = ["Vencidas", "Abertas", "Fechadas"]
situation_vars = [tk.IntVar() for _ in situations]

situation_button = tk.Button(frameTabela, text="Situação")
situation_button.grid(row=0, column=4)
situation_button.bind("<Button-1>", show_frame)

#Pesquisa
def search_data(*args):
    keyword = search_var.get().lower()  # Obtém o texto digitado e converte para minúsculas

    # Limpa a exibição atual do TreeView
    tabela.delete(*tabela.get_children())

    # Filtra os dados com base na palavra-chave digitada
    for values in original_values:
        if any(keyword in str(value).lower() for value in values):
            tabela.insert('', 'end', values=values)

# Cria uma variável de controle para rastrear as alterações no Entry
search_var = tk.StringVar()

# Cria um Entry para a pesquisa
search_entry = tk.Entry(frameTabela, textvariable=search_var, width=10)
search_entry.grid(row=0, column=5)
icon_photo = ImageTk.PhotoImage(Image.open("pesquisa.png").resize((16, 16), Image.LANCZOS))
search_icon_label = tk.Label(frameTabela, image=icon_photo)
search_icon_label.place(x=535, y=4)

# Vincula a função de pesquisa ao evento de alteração na variável
search_var.trace('w', search_data)


def load_options():
    global bethouse_options, mercado_options, arred_var
    try:
        with open('bethouse_options.json', 'r') as f:
            data = json.load(f)
            bethouse_options = data.get("bethouse_options", {})
            mercado_options = data.get("mercado_options", [])
            arred_var = tk.DoubleVar(value=data.get("arredondamento"))
            filtros = data.get("filtros", {})
            order_text = filtros.get("ordem", "Crescente")
            add_text = filtros.get("add", "Data")
            time_text = filtros.get("time", "Feitas desde")
            timeframe_text = filtros.get("timeframe", "hoje")
            selected_situations = filtros.get("situations", [])
            return order_text, add_text, time_text, timeframe_text, selected_situations
    except FileNotFoundError:
        bethouse_options = {}
        mercado_options = []
        arred_var = tk.DoubleVar(value=0.01)
        order_text = "Crescente"
        add_text = "Data"
        time_text = "Feitas desde"
        timeframe_text = "hoje"
        selected_situations = []
        return order_text, add_text, time_text, timeframe_text, selected_situations

order_text, add_text, time_text, timeframe_text, selected_situations = load_options()
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
            'background_color': background_color,
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
    text_color_button.grid(row=3, column=0, padx=5, pady=5)

    background_color_button = tk.Button(bethouses_frame, text='Cor de Fundo', command=choose_background_color)
    background_color_button.grid(row=3, column=1, padx=5, pady=5)

    # Cria botão para adicionar a nova BetHouse
    add_bethouse_button = tk.Button(bethouses_frame, text="Adicionar", command=add_bethouse)
    add_bethouse_button.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

    # Cria a lista de BetHouses
    configStyle = ttk.Style()
    configStyle.configure("Normal.Treeview", rowheight=2)
    bethouses_list = sorted(bethouse_options.keys())
    bethouses_tree = ttk.Treeview(bethouses_frame, columns=('Bethouse', 'Taxa'), show='headings', style="Normal.Treeview")
    bethouses_tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
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
    remove_bethouse_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

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
    mercado_label.grid(row=2, column=3, padx=5, pady=5)
    new_mercado_entry = tk.Entry(bethouses_frame)
    new_mercado_entry.grid(row=3, column=3, padx=5, pady=5)

    # Cria um botão para adicionar a nova opção de mercado
    add_mercado_button = tk.Button(bethouses_frame, text="Adicionar", command=add_mercado_option)
    add_mercado_button.grid(row=4, column=3, columnspan=2, padx=5, pady=5)

    # Cria a lista de opções de mercado
    mercado_options_list = sorted(list(mercado_options), key=lambda x: x[0])
    # Adiciona as BetHouses à Listbox
    mercado_options_listbox = tk.Listbox(bethouses_frame)
    mercado_options_listbox.grid(row=5, column=3, columnspan=2, padx=5, pady=5)
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
    remove_mercado_button.grid(row=6, column=3, columnspan=2, padx=5, pady=5)

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
settings_button.grid(row=0, column=0, sticky="w") # Menu de Configurações # Menus

# Botão Arredondamento
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
            "add": order_button2["text"],
            "time": time_button["text"],
            "timeframe": timeframe_combobox.get(),
            "situations": [var.get() for var in situation_vars]
        }
    }
    with open('bethouse_options.json', 'w') as f:
        json.dump(data, f, sort_keys=True)

def arredondamento_changed(event):
    save_bethouse_options()

arred_label = tk.Label(frameJogo, text="Arred.:")
arred_label.grid(row=2, column=2, columnspan=2)
arred_options = [0.01, 0.05, 0.1, 0.5, 1]
arred_combobox = ttk.Combobox(frameJogo, textvariable=arred_var, values=arred_options, width=3, state="readonly")
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

# Adiciona campo ODD
odd_label = tk.Label(frameApostas, text="ODD")
odd_label.grid(row=0, column=3)
odd_entry, odd_var = create_float_entry(frameApostas, row=1, column=3, width=4, dig=3, dec=3, value=0.0, negative=False)
# Adiciona campo ODD2
odd_entry2, odd_var2 = create_float_entry(frameApostas, row=2, column=3, width=4, dig=3, dec=3, value=0.0, negative=False)
# Adiciona campo ODD3
odd_entry3, odd_var3 = create_float_entry(frameApostas, row=3, column=3, width=4, dig=3, dec=3, value=0.0, negative=False)
odd_entry3.grid_remove() # Odds

# Adiciona campo Aposta
real_label = tk.Label(frameApostas, text="R$")
real_label.grid(row=1, column=4)
label_aposta = tk.Label(frameApostas, text="Aposta")
label_aposta.grid(row=0, column=5, padx=5, pady=5, sticky=tk.W)
aposta_entry, aposta_var = create_float_entry(frameApostas, row=1, column=5, width=5, dig=4, dec=2, value=0.0, negative=False)
#Adicionar aposta2
real_label2 = tk.Label(frameApostas, text="R$")
real_label2.grid(row=2, column=4)
aposta_entry2, aposta_var2 = create_float_entry(frameApostas, row=2, column=5, width=5, dig=4, dec=2, value=0.0, negative=False) # Aposta 2
#Adicionar aposta3
real_label3 = tk.Label(frameApostas, text="R$")
aposta_entry3, aposta_var3 = create_float_entry(frameApostas, row=3, column=5, width=5, dig=4, dec=2, value=0.0, negative=False)
aposta_entry3.grid_remove()

#Adicionando cálculos
def on_variable_change(*args):
    odds = [odd_var.get(), odd_var2.get(), odd_var3.get()]
    apostas = [aposta_var.get(), aposta_var2.get(), aposta_var3.get()]
    bethouses = [bethouse_options.get(bethouse_var.get(), {}).get('taxa', 0.0), bethouse_options.get(bethouse_var2.get(), {}).get('taxa', 0.0), bethouse_options.get(bethouse_var3.get(), {}).get('taxa', 0.0)]
    def float_error(valor):
        try:
            valor_float = valor.get()
        except _tkinter.TclError:
            valor_float = 0.0
        return valor_float
    if (len([odd for odd in odds if odd != 0.0]) >= 2) and (len([aposta for aposta in apostas if aposta != 0.0]) >= 1):
        resultado = calc_apostas(apostas[0], apostas[1], apostas[2], odds[0], odds[1], odds[2], mercado_var.get(), mercado_var2.get(), mercado_var3.get(), float_error(valor_var), float_error(valor_var2), float_error(valor_var3), bethouses[0], bethouses[1], bethouses[2], arred_var.get())
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
palpite_label.grid(row=0, column=6, padx=5, pady=5, sticky=tk.W)
palpite1_label = tk.Label(frameApostas, text="")
palpite1_label.grid(row=1, column=6)
palpite2_label = tk.Label(frameApostas, text="")
palpite2_label.grid(row=2, column=6)
palpite3_label = tk.Label(frameApostas, text="") # Palpites

#Lucro
liability_label = tk.Label(frameApostas, text='Liability')
liability_label1 = tk.Label(frameApostas, text='')
liability_label2 = tk.Label(frameApostas, text='')
lucro_label = tk.Label(frameApostas, text='Lucro')
lucro_label.grid(row=0, column=7, padx=5, pady=5, sticky=tk.W)
lucro1_label = tk.Label(frameApostas, text="")
lucro1_label.grid(row=1, column=7)
lucro2_label = tk.Label(frameApostas, text="")
lucro2_label.grid(row=2, column=7)
lucro3_label = tk.Label(frameApostas, text="")
lucro_percent_label = tk.Label(frameApostas, text='Lucro %')
lucro_percent_label.grid(row=0, column=8, padx=5, pady=5, sticky=tk.W)
lucro_percent_label1 = tk.Label(frameApostas, text="", font=("Arial", 20, "bold"))
lucro_percent_label1.grid(row=1, column=8, rowspan=2) # Lucro

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

def gravar():
    global df_tabela
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

    def converter_esporte(sport):
        sport = sport.lower().strip().split('\n')[0]
        if sport in {'soccer', 'football', 'футбол'}:
            return 'Futebol'
        elif sport in {'basketball', 'basket', 'баскетбол'}:
            return 'Basquetebol'
        elif sport == 'volleyball':
            return 'Voleibol'
        elif sport == 'бейсбол':
            return 'Baseball'
        elif sport in {'handball', 'гандбол'}:
            return 'Handebol'
        elif sport in {'dota2', 'esports', 'esport', 'e-sports', 'cybersports'}:
            return 'E-Sports'
        elif sport in {'ice hockey', 'хоккей'}:
            return 'Hockey'
        elif sport in {'tennis', 'теннис'}:
            return 'Tênis'
        elif sport in {'darts', 'dart', 'дартс'}:
            return 'Dardos'
        elif sport in {'table tennis', 'tabletennis'}:
            return 'Tênis de Mesa'
        elif sport == 'boxing':
            return 'Boxe'
        elif sport == 'футзал':
            return 'Futsal'
        else:
            return sport.capitalize()

    if (len([odd for odd in odds if odd != 0.0]) >= 2)\
            and (len([aposta for aposta in apostas if aposta != 0.0]) >= 1)\
            and time_casa != "" and time_fora != ""\
            and (bethouse_combobox.get() in bethouse_options.keys())\
            and (bethouse_combobox2.get() in bethouse_options.keys())\
            and ((num_bets != 3) or (num_bets == 3 and bethouse_combobox3.get() in bethouse_options.keys())):
        dados = {
            'id': len(df_tabela) + 1,
            'add': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'datetime': datetime.strptime(f"{ano_combobox.get()}-{convert_mes(mes_combobox.get()):02}-{int(dia_entry.get()):02} {int(hora_entry.get()):02}:{int(minuto_entry.get()):02}:00", '%Y-%m-%d %H:%M:%S'),
            'time_casa': time_casa,
            'time_fora': time_fora,
            'bethouse1': bethouse_combobox.get(),
            'mercado1': mercado_combobox.get(),
            'valor1': valor_entry.get(),
            'odd1': odd_entry.get(),
            'aposta1': palpite1_label.cget("text").replace("R$", "").strip(),# if aposta_var.get() == 0.0 or aposta_var.get() == "" else float(aposta_var.get()),
            'resultado1': "",
            'bethouse2': bethouse_combobox2.get(),
            'mercado2': mercado_combobox2.get(),
            'valor2': valor_entry2.get(),
            'odd2': odd_entry2.get(),
            'aposta2': palpite2_label.cget("text").replace("R$", "").strip(),# if aposta_var2.get() == 0.0 or aposta_var2.get() == "" else float(aposta_var2.get()),
            'resultado2': "",
            'bethouse3': bethouse_combobox3.get(),
            'mercado3': mercado_combobox3.get(),
            'valor3': valor_entry3.get(),
            'odd3': odd_entry3.get(),
            'aposta3': palpite3_label.cget("text").replace("R$", "").strip(),# if aposta_var3.get() == 0.0 or aposta_var3.get() == "" else float(aposta_var3.get()),
            'resultado3': "",
            'lucro_estimado': lucro1_label.cget("text").replace("R$", "").strip(),
            'lucro_per_estimado': lucro_percent_label1.cget("text").strip("%"),
            'lucroReal': "",
            'lucro_perReal': "",
            'esporte': converter_esporte(esporte_entry.get().split(". ")[0])
        }

        # Gravação dos dados no arquivo CSV e atualização da tabela
        dados = {k: str(v) if isinstance(v, datetime) else convert_to_numeric(v).strip().split('\n')[0] if isinstance(v, str) and '\n' in v else convert_to_numeric(v) for k, v in dados.items()}
        linha = pd.DataFrame.from_dict(dados, orient='index').T
        with open("Apostas.csv", "a", newline="") as file:
            csv.writer(file).writerow(list(dados.values()))
        df_tabela = pd.concat([df_tabela, pd.DataFrame([dados.values()], columns=df_tabela.columns).replace('', np.nan)], ignore_index=True)

        # atualização dos dados
        add_aposta(linha)
        preencher_treeview(tabela, bethouse_options, df_tabela, situation_vars, order_button1, order_button2, time_button, timeframe_combobox, frameTabela)
        resetar_variaveis()
    else:
        messagebox.showwarning("Aviso", "Preencha o jogo, as BetHouses, as odds e uma aposta.")

gravar_button = tk.Button(frameGravar, text="Gravar", command=gravar)
gravar_button.grid(row=0, column=0)
clear_button = tk.Button(frameGravar, text="Limpar", command=resetar_variaveis)
clear_button.grid(row=0, column=1) # Gravar

def select_bets(event):
    df_filtrado = filter_selection(df_tabela, situation_vars, order_button1, order_button2, time_button, timeframe_combobox, frameTabela)
    # Obter o item selecionado na tabela
    item_id = tabela.focus()
    item_values = tabela.item(item_id)['values']

    # Obter o ID da linha selecionada
    id_selecionado = item_values[9]  # Índice 9 corresponde ao campo 'ID'


    def reset_all():
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
        if num_bets == 3:
            alternar_bets()
        valor_entry.configure(fg='systemWindowBody', bg='systemWindowBody')
        odd_entry.configure(fg='systemWindowBody', bg='systemWindowBody')
        aposta_entry.configure(fg='systemWindowBody', bg='systemWindowBody')
        valor_entry2.configure(fg='systemWindowBody', bg='systemWindowBody')
        odd_entry2.configure(fg='systemWindowBody', bg='systemWindowBody')
        aposta_entry2.configure(fg='systemWindowBody', bg='systemWindowBody')
        valor_entry3.configure(fg='systemWindowBody', bg='systemWindowBody')
        odd_entry3.configure(fg='systemWindowBody', bg='systemWindowBody')
        aposta_entry3.configure(fg='systemWindowBody', bg='systemWindowBody')
        edit_button.grid_remove()
        clear_button.grid(row=0, column=1)

    # Trocar botão Limpar
    clear_button.grid_remove()
    full_clear_button = tk.Button(frameGravar, text="Limpar", command=reset_all)
    full_clear_button.grid(row=0, column=1)

    # Buscar as informações da linha correspondente ao ID no DataFrame df_filtrado
    row = df_filtrado[df_filtrado['id'] == id_selecionado].iloc[0]
    row['datetime'] = pd.to_datetime(row['datetime'])
    jogo_entry.delete(0, 'end')
    jogo_entry.insert(0, f"{row['time_casa']} - {row['time_fora']}")
    dia_entry.delete(0, 'end')
    dia_entry.insert(0, row['datetime'].day)
    mes_combobox.set(convert_mes(row['datetime'].month))
    ano_combobox.set(row['datetime'].year)
    hora_entry.delete(0, 'end')
    hora_entry.insert(0, row['datetime'].hour)
    minuto_entry.delete(0, 'end')
    minuto_entry.insert(0, row['datetime'].minute)
    if pd.notna(row['bethouse3']) and num_bets == 2:
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
        df_filtrado.loc[mask, 'add'] = df_filtrado.loc[mask, 'add']
        df_filtrado.loc[mask, 'datetime'] = ano_combobox.get() + '-' + f"{convert_mes(mes_combobox.get()):02d}" + '-' + f"{int(dia_entry.get()):02d}" + ' ' + f"{int(hora_entry.get()):02d}" + ':' + f"{int(minuto_entry.get()):02d}" + ":00"
        df_filtrado.loc[mask, 'time_casa'] = jogo_entry.get().split(" - ")[0]
        df_filtrado.loc[mask, 'time_fora'] = jogo_entry.get().split(" - ")[1]
        df_filtrado.loc[mask, 'bethouse1'] = bethouse_combobox.get()
        df_filtrado.loc[mask, 'bethouse2'] = bethouse_combobox2.get()
        df_filtrado.loc[mask, 'bethouse3'] = bethouse_combobox3.get() if bethouse_combobox3.get() != '' and bethouse_combobox3.get().lower() != 'nan' else ''
        df_filtrado.loc[mask, 'mercado1'] = mercado_combobox.get()
        df_filtrado.loc[mask, 'mercado2'] = mercado_combobox2.get()
        df_filtrado.loc[mask, 'mercado3'] = mercado_combobox3.get() if mercado_combobox3.get() != '' and mercado_combobox3.get().lower() != 'nan' else ''
        df_filtrado.loc[mask, 'valor1'] = valor_entry.get() if valor_entry.get().isnumeric() else ''
        df_filtrado.loc[mask, 'valor2'] = valor_entry2.get() if valor_entry.get().isnumeric() else ''
        df_filtrado.loc[mask, 'valor3'] = valor_entry3.get() if valor_entry.get().isnumeric() else ''
        df_filtrado.loc[mask, 'odd1'] = odd_entry.get()
        df_filtrado.loc[mask, 'odd2'] = odd_entry2.get()
        df_filtrado.loc[mask, 'odd3'] = odd_entry3.get()
        df_filtrado.loc[mask, 'aposta1'] = palpite1_label.cget("text").replace("R$", "").strip()
        df_filtrado.loc[mask, 'aposta2'] = palpite2_label.cget("text").replace("R$", "").strip()
        df_filtrado.loc[mask, 'aposta3'] = palpite3_label.cget("text").replace("R$", "").strip() if palpite3_label.cget("text").replace("R$", "").strip().isnumeric() else ''
        df_filtrado.loc[mask, 'lucro_estimado'] = round(float(lucro1_label.cget("text").replace("R$", "").strip()), 4)
        df_filtrado.loc[mask, 'lucro_per_estimado'] = round(float(lucro_percent_label1.cget("text").strip("%")), 4)
        df_filtrado.loc[mask, 'esporte'] = esporte_entry.get() if esporte_entry.get() != '' and esporte_entry.get().lower() != 'nan' else ''

        # Salvar o DataFrame atualizado no arquivo Apostas.csv
        linha = df_filtrado.loc[mask].replace('\n', '', regex=True)
        add_aposta(linha, id=id_selecionado)
        df_tabela.update(linha)
        mask_tabela = df_tabela['id'] == id_selecionado
        df_tabela.loc[mask_tabela, 'add'] = df_tabela.loc[mask_tabela, 'add'].apply(lambda x: pd.Timestamp(x).to_pydatetime())
        df_tabela.loc[mask_tabela, 'datetime'] = df_tabela.loc[mask_tabela, 'datetime'].apply(lambda x: pd.Timestamp(x).to_pydatetime())
        csv_string = io.StringIO()
        linha.to_csv(csv_string, header=False, index=False, sep=',')
        novo_conteudo = csv_string.getvalue()
        with fileinput.FileInput('Apostas.csv', inplace=True) as file:
            for i, linha in enumerate(file):
                colunas = linha.split(',')
                if str(id_selecionado) == colunas[0].strip():
                    print(novo_conteudo, end='')
                else:
                    print(linha, end='')

        # Limpar as variáveis e atualizar a tabela
        preencher_treeview(tabela, bethouse_options, df_tabela, situation_vars, order_button1, order_button2, time_button, timeframe_combobox, frameTabela)
        resetar_variaveis()
        edit_button.grid_remove()

    # Botão Editar

    edit_button = tk.Button(frameGravar, text="Editar", command=editar_bets, foreground="red")
    edit_button.grid(row=0, column=2)

# Definir estilo para o Treeview
style = ttk.Style()
style.configure("Treeview", rowheight=60)

# Criar o Treeview com as colunas desejadas
tabela = BetHistTreeview(frameTabela, situation_vars, order_button1, order_button2, time_button, timeframe_combobox, frameTabela, frameSaldos, columns=("index", "adds", "jogo", "data", "resultados", "bethouses", "odds", "bets", "mercados", "id"), show="headings", style="Treeview", height=6)
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


#Pesquisa
# Armazena os valores originais da tabela
original_values = []
for item_id in tabela.get_children():
    item = tabela.item(item_id)
    values = item['values']
    original_values.append(values)


#––––––––––––––––––––––––––––––––––––––# ESTATÍSTICA #––––––––––––––––––––––––––––––––––––––

#hoje = date.today()
#df_vence_hoje = df_tabela[(df_tabela['datetime'].dt.day == hoje.day) & (df_tabela['datetime'].dt.month == hoje.month) & (df_tabela['datetime'].dt.year == hoje.year)].copy()
#df_hoje = df_tabela[pd.to_datetime(df_tabela['add']).dt.date == hoje].copy()
#bets_hoje = len(df_hoje)
#bets_pra_hoje = len(df_vence_hoje)

if not os.path.isfile('movimentacao.csv'):
    with open('movimentacao.csv', 'w') as csvfile:
        csv.writer(csvfile).writerow(['BetHouse', 'Status', 'Valor', 'Data'])

configStyle = ttk.Style()
configStyle.configure("Normal.Treeview", rowheight=20)

gerar_saldos(frameSaldos, bethouse_options, df_tabela)




#––––––––––––––––––––––––––––––––––––––# GRÁFICOS #––––––––––––––––––––––––––––––––––––––
# Defina as colunas_agg, colun_data e metodos
colunas_agg = ['lucro_estimado', 'lucroReal']
colun_data = 'add'
metodos = ['sum', 'sum']

# Função para atualizar o gráfico interativamente
def atualizar_grafico():
    # Obtenha os valores selecionados dos widgets de entrada
    range_val = int(range_entry.get())
    periodo_tempo = periodo_var.get()

    # Chame a função agregação de datas para obter os dados agregados
    estim_x_real = agregar_datas(df_tabela, colun_data, periodo_tempo, colunas_agg, metodos, range_val=range_val)

    # Crie um DataFrame apenas com as colunas necessárias
    dados = pd.DataFrame({'periodo': estim_x_real.index,
                          'lucro_estimado': estim_x_real['lucro_estimado'],
                          'lucroReal': estim_x_real['lucroReal']})

    # Crie um gráfico de linha usando o Seaborn
    fig = plt.Figure(figsize=(4, 2.7))
    ax = fig.add_subplot(1, 1, 1)
    sns.lineplot(data=dados, x=dados['periodo'], y='lucro_estimado', errorbar=None, ax=ax, label='Lucro Estimado')
    sns.lineplot(data=dados, x=dados['periodo'], y='lucroReal', errorbar=None, ax=ax, label='Lucro Real')

    # Adicione os valores acima de cada ponto
    for i, valor in enumerate(dados['lucroReal']):
        ax.annotate(f"R$ {valor:.2f}", (dados['periodo'][i], valor), textcoords="offset points", xytext=(0, 10),
                    ha='center', color='black')

    # Determine o número máximo de ticks no eixo x
    max_ticks = 6

    # Verifique o número total de dados no eixo x
    total_data = len(dados['periodo'])

    # Calcule o passo necessário para pular labels, se houver mais de 6 dados
    if total_data > max_ticks:
        step = math.ceil(total_data / max_ticks)
    else:
        step = 1

    # Defina os ticks do eixo x usando o passo calculado
    ax.set_xticks(range(0, total_data, step))
    for i in range(0, total_data, step):
        if i > 0:
            ax.axvline(i, color='#E5E5E5', linestyle='-')
    ax.grid(True)

    # Crie um widget de canvas para exibir o gráfico
    canvas = FigureCanvasTkAgg(fig, master=frameStatus)
    canvas.get_tk_widget().grid(row=1, column=0, columnspan=4)


# Crie uma caixa de entrada para o range_val
range_label = tk.Label(frameStatus, text="Range:")
range_label.grid(row=0, column=0)
range_entry = tk.Entry(frameStatus, width=4)
range_entry.grid(row=0, column=1)
range_entry.insert(0, 5)
range_entry.bind("<FocusOut>", lambda event: atualizar_grafico())

# Crie uma caixa de seleção para o período
periodo_var = tk.StringVar(frameStatus)
periodo_var.set("dia")  # Valor padrão
def atualizar_grafico_periodo(*args):
    atualizar_grafico()

periodo_var.trace("w", atualizar_grafico_periodo)
periodo_dropdown = tk.OptionMenu(frameStatus, periodo_var, "dia", "semana", "mes", "trimestre", "semestre", "ano")
periodo_dropdown.grid(row=0, column=3)
periodo_dropdown.configure(width=4)
atualizar_grafico()

####### GRÁFICO DE HORA ########

# Defina as colunas_agg, colun_data e metodos
colunas_agg_hora = 'lucro_estimado'
colun_data_hora = 'add'

# Função para atualizar o gráfico interativamente
def atualizar_grafico_hora():
    # Obtenha os valores selecionados dos widgets de entrada
    range_val = int(range_entry.get())
    periodo_tempo = periodo_var.get()
    metodo = metodo_var.get()

    # Define os métodos de acordo com a opção selecionada
    if metodo == 'total':
        metodos = 'sum'
    elif metodo == 'média':
        metodos = 'mean'

    # Chame a função agregação de datas para obter os dados agregados
    apostas_hora = agregar_datas(df_tabela, colun_data_hora, periodo_tempo, colunas_agg_hora, metodos=metodos, range_val=range_val, cont_hora=True)

    # Crie um gráfico de barras usando o Matplotlib
    fig = plt.Figure(figsize=(7, 2.7))
    ax = fig.add_subplot(1, 1, 1)
    apostas_hora = apostas_hora.reset_index()
    sns.barplot(data=apostas_hora, x='hora', y='count', palette='viridis', ax=ax, label='Apostas por Hora')

    # Adicione o gráfico ao frameStatus
    canvas = FigureCanvasTkAgg(fig, master=frameStatus)
    canvas.get_tk_widget().grid(row=1, column=4, columnspan=5)

# Crie uma caixa de entrada para o range_val
range_label = tk.Label(frameStatus, text="Range:")
range_label.grid(row=0, column=4)
range_entry = tk.Entry(frameStatus, width=4)
range_entry.grid(row=0, column=5)
range_entry.insert(0, 5)
range_entry.bind("<FocusOut>", lambda event: atualizar_grafico_hora())

# Crie uma caixa de seleção para o período
periodo_var = tk.StringVar(frameStatus)
periodo_var.set("dia")  # Valor padrão
def atualizar_grafico_periodo_hora(*args):
    atualizar_grafico_hora()

periodo_var.trace("w", atualizar_grafico_periodo_hora)
periodo_dropdown = tk.OptionMenu(frameStatus, periodo_var, "dia", "semana", "mes", "trimestre", "semestre", "ano")
periodo_dropdown.grid(row=0, column=6)
periodo_dropdown.configure(width=7)

# Crie uma caixa de seleção para o método
metodo_var = tk.StringVar(frameStatus)
metodo_var.set("total")  # Valor padrão
def atualizar_grafico_metodo_hora(*args):
    atualizar_grafico_hora()

metodo_var.trace("w", atualizar_grafico_metodo_hora)
metodo_dropdown = tk.OptionMenu(frameStatus, metodo_var, "total", "média")
metodo_dropdown.grid(row=0, column=8)
metodo_dropdown.configure(width=6)
atualizar_grafico_hora()


######## Balanços BetHouses ##########

# Função para atualizar o gráfico com base nos filtros selecionados




#––––––––––––––––––––––––––––––––––––––# RODAR PROGRAMA #––––––––––––––––––––––––––––––––––––––
# Chamar a função para preencher o Treeview
if len(tabela.get_children()) == 0:
    preencher_treeview(tabela, bethouse_options, df_tabela, situation_vars, order_button1, order_button2, time_button, timeframe_combobox, frameTabela)

# inicia o loop da janela
janela.mainloop()