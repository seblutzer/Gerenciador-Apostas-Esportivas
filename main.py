import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, colorchooser
import datetime
import json
import os
import sys
from datetime import datetime
import pandas as pd
import sqlite3
from PIL import Image, ImageTk
from Pacotes_Lutzer.convert import convert_to_numeric, convert_mes, converter_esporte
from Pacotes_Lutzer.validate import create_float_entry, create_combobox, float_error, gerar_mensagem
from Pacotes_Lutzer.calc_apostas import calc_apostas
from Pacotes_Lutzer.classes_personalizadas import BetHistTreeview, preencher_treeview, import_df_filtrado, save_apostas, tabela_bethouses
from Pacotes_Lutzer.graficos import lucro_tempo, apostas_hora, calc_saldo_bethouse, apostas_bethouses, relacao_bethouses, relacao_esportes, eficiencia_bethouses, odds_x_resultado, participacao_lucros
from language import trans_config, trans_filtros, trans_graficos, trans_jogo
import re
from tkinter import Toplevel, Label

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

# Define the control variable for the language
selected_language = tk.StringVar()

# Dictionary of flags
flags = {
    'Português': '🇧🇷',
    'English': '🇺🇸',
    'Deutsch': '🇩🇪',
    'Italiano': '🇮🇹',
    'Français': '🇫🇷',
    'Ελληνικά': '🇬🇷',
    'Русский': '🇷🇺',
    'Español': '🇪🇸'
}

def save_language(language):
    with open('language.txt', 'w') as f:
        f.write(language)

def load_language():
    if os.path.exists('language.txt'):
        with open('language.txt', 'r') as f:
            language = f.read()
            return language
    return 'English'
def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)
def update_language(language):
    selected_language.set(language)
    language_button.configure(text=flags[language], font=('Arial', 21))
    confirm = messagebox.askyesno(trans_config['Confirmação'][language],
                                  f"{trans_config['Traduzir'][language]} {language}?")
    if confirm:
        save_language(language)
        restart_program()

def open_language_menu():
    global language_frame
    language_frame = tk.Frame(janela)
    language_frame.place(x=language_button.winfo_x() + 60, y=language_button.winfo_y() + language_button.winfo_height())

    language_frame.config(highlightthickness=2, highlightbackground="gray", relief="ridge")
    for i, (language, flag) in enumerate(flags.items()):
        button = tk.Button(language_frame, text=f"{language} {flag}", command=lambda lang=language: update_language(lang))
        button.grid(row=i, column=0)

    def on_window_click(event):
        widget = event.widget
        while widget is not None:
            if widget == language_frame:
                return
            widget = widget.master
        language_frame.destroy()

    janela.bind("<Button-1>", on_window_click)


selected_language.set(load_language())  # Set the default language here
# Define the language button
language_button = tk.Button(frameOpcoes, text=flags[selected_language.get()], command=open_language_menu, width=1, font=('Arial', 21))
language_button.grid(row=0, column=1)
idioma = selected_language.get()
cambio = 'R$'
janela.title(trans_config['programa'][idioma])

def alternar_tabelas():
    global tabela_visivel
    tabela_visivel = not tabela_visivel
    if tabela_visivel:
        frameTabela.grid(row=9, column=0)
        frameSaldos.grid(row=10, column=0)
        botao_tabelas["text"] = trans_config['TabelaOff'][idioma]
    else:
        frameTabela.grid_remove()
        frameSaldos.grid_remove()
        botao_tabelas["text"] = trans_config['TabelaOn'][idioma]

tabela_visivel = True
botao_tabelas = ttk.Button(frameOpcoes, text=trans_config['TabelaOn'][idioma], command=alternar_tabelas)
botao_tabelas.grid(row=0, column=2)
def selecionar_opcao(opcao, popup, row):
    if not popup.winfo_manager():
        popup = tk.Frame(janela)
    popup.place(x=graficos_button.winfo_x() - 65, y=graficos_button.winfo_y() + graficos_button.winfo_height() * (row + 1))
    popup.config(highlightthickness=2, highlightbackground="gray", relief="ridge")

    def on_plot_click(event):
        widget_plot = event.widget
        while widget_plot is not None:
            if widget_plot == popup:
                return
            elif widget_plot == graficos_frame:
                popup.destroy()
                return
            widget_plot = widget_plot.master
        popup.destroy()
        graficos_frame.destroy()

    janela.bind("<Button-1>", on_plot_click)

    if opcao == trans_graficos['lucro tempo'][idioma]:
        labelTitulo = tk.Label(popup, text=opcao, font=('Arial', 14, 'bold'))
        labelTitulo.grid(row=0, column=0, columnspan=2)

        labelTempo = tk.Label(popup, text=trans_graficos['Tempo'][idioma])
        labelTempo.grid(row=1, column=0)

        entryTempo, tempo_var = create_float_entry(popup, row=1, width=8, column=1, dig=2, dec=0)

        labelPeriodo = tk.Label(popup, text=trans_graficos['Período'][idioma])
        labelPeriodo.grid(row=2, column=0)

        comboPeriodo = ttk.Combobox(popup, values=[
            trans_graficos['dia'][idioma],
            trans_graficos['semana'][idioma],
            trans_graficos['mês'][idioma],
            trans_graficos['trimestre'][idioma],
            trans_graficos['semestre'][idioma],
            trans_graficos['ano'][idioma]
        ], state="readonly", width=7)
        comboPeriodo.set(trans_graficos['dia'][idioma])
        comboPeriodo.grid(row=2, column=1)

        labelMedia = tk.Label(popup, text=trans_graficos['Média'][idioma])
        labelMedia.grid(row=3, column=0)

        entryMedia, media_var = create_float_entry(popup, row=3, width=8, column=1, dig=2, dec=0)

        def gerar_grafico():
            tempo = int(entryTempo.get()) if entryTempo.get().isdigit() else 7
            periodo = comboPeriodo.get()
            media = int(entryMedia.get()) if entryMedia.get().isdigit() else 3
            lucro_tempo(tempo, periodo, conn, idioma, cambio, media)

        btnGerarGrafico = tk.Button(popup, text=trans_graficos['Gerar Gráfico'][idioma], command=gerar_grafico)
        btnGerarGrafico.grid(row=4, column=0, columnspan=2)

    elif opcao == trans_graficos['apostas hora'][idioma]:
        labelTitulo = tk.Label(popup, text=opcao, font=('Arial', 14, 'bold'))
        labelTitulo.grid(row=0, column=0, columnspan=2)

        labelTempo = tk.Label(popup, text=trans_graficos['Dias'][idioma])
        labelTempo.grid(row=1, column=0)

        entryTempo, tempo_var = create_float_entry(popup, row=1, width=8, column=1, dig=3, dec=0)

        def gerar_grafico():
            tempo = int(entryTempo.get()) if entryTempo.get().isdigit() else 7
            apostas_hora(conn, tempo, idioma)

        btnGerarGrafico = tk.Button(popup, text=trans_graficos['Gerar Gráfico'][idioma], command=gerar_grafico)
        btnGerarGrafico.grid(row=2, column=0, columnspan=2)

    elif opcao == trans_graficos['historico saldo'][idioma]:
        labelTitulo = tk.Label(popup, text=opcao, font=('Arial', 14, 'bold'))
        labelTitulo.grid(row=0, column=0, columnspan=2)

        labelTempo = tk.Label(popup, text=trans_graficos['Tempo'][idioma])
        labelTempo.grid(row=1, column=0)

        entryTempo, tempo_var = create_float_entry(popup, row=1, width=8, column=1, dig=2, dec=0)

        labelPeriodo = tk.Label(popup, text=trans_graficos['Período'][idioma])
        labelPeriodo.grid(row=2, column=0)

        comboPeriodo = ttk.Combobox(popup, values=[
            trans_graficos['dia'][idioma],
            trans_graficos['semana'][idioma],
            trans_graficos['mês'][idioma],
            trans_graficos['trimestre'][idioma],
            trans_graficos['semestre'][idioma],
            trans_graficos['ano'][idioma]
        ], state="readonly", width=7)
        comboPeriodo.set(trans_graficos['dia'][idioma])
        comboPeriodo.grid(row=2, column=1)

        def gerar_grafico():
            tempo = int(entryTempo.get()) if entryTempo.get().isdigit() else 7
            periodo = comboPeriodo.get()
            calc_saldo_bethouse(conn, tempo, periodo, bethouse_options_total, idioma, cambio)

        btnGerarGrafico = tk.Button(popup, text=trans_graficos['Gerar Gráfico'][idioma], command=gerar_grafico)
        btnGerarGrafico.grid(row=3, column=0, columnspan=2)

    elif opcao == trans_graficos['apostas tempo'][idioma]:
        labelTitulo = tk.Label(popup, text=opcao, font=('Arial', 14, 'bold'))
        labelTitulo.grid(row=0, column=0, columnspan=2)

        labelTempo = tk.Label(popup, text=trans_graficos['Tempo'][idioma])
        labelTempo.grid(row=1, column=0)

        entryTempo, tempo_var = create_float_entry(popup, row=1, width=8, column=1, dig=2, dec=0)

        labelPeriodo = tk.Label(popup, text=trans_graficos['Período'][idioma])
        labelPeriodo.grid(row=2, column=0)

        comboPeriodo = ttk.Combobox(popup, values=[
            trans_graficos['dia'][idioma],
            trans_graficos['semana'][idioma],
            trans_graficos['mês'][idioma],
            trans_graficos['trimestre'][idioma],
            trans_graficos['semestre'][idioma],
            trans_graficos['ano'][idioma]
        ], state="readonly", width=7)
        comboPeriodo.set(trans_graficos['dia'][idioma])
        comboPeriodo.grid(row=2, column=1)

        labelTop = tk.Label(popup, text=trans_graficos['Maiores'][idioma])
        labelTop.grid(row=3, column=0)

        entryTop, top_var = create_float_entry(popup, row=3, width=8, column=1, dig=2, dec=0)

        labelBottom = tk.Label(popup, text=trans_graficos['Menores'][idioma])
        labelBottom.grid(row=4, column=0)

        entryBottom, bottom_var = create_float_entry(popup, row=4, width=8, column=1, dig=2, dec=0)

        def gerar_grafico():
            tempo = int(entryTempo.get()) if entryTempo.get().isdigit() else 7
            periodo = comboPeriodo.get()
            top = int(entryTop.get()) if entryTop.get().isdigit() else 0
            bottom = int(entryBottom.get()) if entryTop.get().isdigit() else 0
            apostas_bethouses(conn, tempo, periodo, bethouse_options_total, idioma, top=top, bottom=bottom)

        btnGerarGrafico = tk.Button(popup, text=trans_graficos['Gerar Gráfico'][idioma], command=gerar_grafico)
        btnGerarGrafico.grid(row=5, column=0, columnspan=2)

    elif opcao == trans_graficos['apostas bethouse'][idioma]:
        labelTitulo = tk.Label(popup, text=opcao, font=('Arial', 14, 'bold'))
        labelTitulo.grid(row=0, column=0, columnspan=2)

        labelTempo = tk.Label(popup, text=trans_graficos['Tempo'][idioma])
        labelTempo.grid(row=1, column=0)

        entryTempo, tempo_var = create_float_entry(popup, row=1, width=8, column=1, dig=3, dec=0)

        def gerar_grafico():
            tempo = int(entryTempo.get()) if entryTempo.get().isdigit() else 7
            relacao_bethouses(conn, tempo, idioma, cambio)

        btnGerarGrafico = tk.Button(popup, text=trans_graficos['Gerar Gráfico'][idioma], command=gerar_grafico)
        btnGerarGrafico.grid(row=2, column=0, columnspan=2)
    elif opcao == trans_graficos['esportes'][idioma]:
        labelTitulo = tk.Label(popup, text=opcao, font=('Arial', 14, 'bold'))
        labelTitulo.grid(row=0, column=0, columnspan=2)

        labelTempo = tk.Label(popup, text=trans_graficos['Tempo'][idioma])
        labelTempo.grid(row=1, column=0)

        entryTempo, tempo_var = create_float_entry(popup, row=1, width=8, column=1, dig=3, dec=0)

        def gerar_grafico():
            tempo = int(entryTempo.get()) if entryTempo.get().isdigit() else 7
            relacao_esportes(conn, tempo, idioma, cambio, valor=True)

        btnGerarGrafico = tk.Button(popup, text=trans_graficos['Gerar Gráfico'][idioma], command=gerar_grafico)
        btnGerarGrafico.grid(row=2, column=0, columnspan=2)

    elif opcao == trans_graficos['resultado bethouse'][idioma]:
        labelTitulo = tk.Label(popup, text=opcao, font=('Arial', 14, 'bold'))
        labelTitulo.grid(row=0, column=0, columnspan=2)

        labelTempo = tk.Label(popup, text=trans_graficos['Tempo'][idioma])
        labelTempo.grid(row=1, column=0)

        entryTempo, tempo_var = create_float_entry(popup, row=1, width=8, column=1, dig=3, dec=0)

        def gerar_grafico():
            tempo = int(entryTempo.get()) if entryTempo.get().isdigit() else 7
            eficiencia_bethouses(conn, idioma, tempo)

        btnGerarGrafico = tk.Button(popup, text=trans_graficos['Gerar Gráfico'][idioma], command=gerar_grafico)
        btnGerarGrafico.grid(row=2, column=0, columnspan=2)

    elif opcao == trans_graficos['odd resultado'][idioma]:
        labelTitulo = tk.Label(popup, text=opcao, font=('Arial', 14, 'bold'))
        labelTitulo.grid(row=0, column=0, columnspan=2)

        labelTempo = tk.Label(popup, text=trans_graficos['Tempo'][idioma])
        labelTempo.grid(row=1, column=0)

        entryTempo, tempo_var = create_float_entry(popup, row=1, width=8, column=1, dig=3, dec=0)

        labelMin = tk.Label(popup, text="Arred.:")
        labelMin.grid(row=2, column=0)
        combobox_var = tk.IntVar()
        combobox_round = ttk.Combobox(popup, textvariable=combobox_var, values=[1, 2], state="readonly", width=7)
        combobox_round.set(2)  # Define o valor inicial selecionado
        combobox_round.grid(row=2, column=1)

        labelMin = tk.Label(popup, text=trans_graficos['Mínimo'][idioma])
        labelMin.grid(row=3, column=0)

        entryMin, min_var = create_float_entry(popup, row=3, width=8, column=1, dig=3, dec=0)

        labelMin_percent = tk.Label(popup, text=trans_graficos['Mínimo'][idioma] + '(%)')
        labelMin_percent.grid(row=4, column=0)

        entryMin_percent, min_percent_var = create_float_entry(popup, row=4, width=8, column=1, dig=2, dec=0)

        def gerar_grafico():
            tempo = int(entryTempo.get()) if entryTempo.get().isdigit() else None
            round = int(combobox_round.get()) if combobox_round.get().isdigit() else 1
            min = int(entryMin.get()) if entryMin.get().isdigit() else 0
            min_percent = int(entryMin_percent.get()) if entryMin_percent.get().isdigit() else 1
            odds_x_resultado(conn, idioma, tempo, round=round, min=min, min_percent=min_percent)

        btnGerarGrafico = tk.Button(popup, text=trans_graficos['Gerar Gráfico'][idioma], command=gerar_grafico)
        btnGerarGrafico.grid(row=5, column=0, columnspan=2)

    elif opcao == trans_graficos['Participação de lucros'][idioma]:
        labelTitulo = tk.Label(popup, text=opcao, font=('Arial', 14, 'bold'))
        labelTitulo.grid(row=0, column=0, columnspan=2)

        labelTempo = tk.Label(popup, text=trans_graficos['Tempo'][idioma])
        labelTempo.grid(row=1, column=0)

        entryTempo, tempo_var = create_float_entry(popup, row=1, width=8, column=1, dig=3, dec=0)

        def gerar_grafico():
            tempo = int(entryTempo.get()) if entryTempo.get().isdigit() else 7
            participacao_lucros(conn, tempo, bethouse_options_total, idioma, cambio, )

        btnGerarGrafico = tk.Button(popup, text=trans_graficos['Gerar Gráfico'][idioma], command=gerar_grafico)
        btnGerarGrafico.grid(row=2, column=0, columnspan=2)

combo_opcoes = ttk.Combobox(frameOpcoes, values=[
    trans_graficos['lucro tempo'][idioma],
    trans_graficos['apostas hora'][idioma],
    trans_graficos['historico saldo'][idioma],
    trans_graficos['apostas tempo'][idioma],
    trans_graficos['apostas bethouse'][idioma],
    trans_graficos['esportes'][idioma],
    trans_graficos['resultado bethouse'][idioma],
    trans_graficos['odd resultado'][idioma],
    trans_graficos['Participação de lucros'][idioma]
], state="readonly", width=14)
def open_graficos_menu():
    global graficos_frame
    graficos_frame = tk.Frame(janela)
    graficos_frame.place(x=graficos_button.winfo_x() + 50, y=graficos_button.winfo_y() + graficos_button.winfo_height())
    graficos_frame.config(highlightthickness=2, highlightbackground="gray", relief="ridge")

    popup = tk.Frame(janela)

    for i, opcao in enumerate(combo_opcoes["values"]):
        button = tk.Button(graficos_frame, text=opcao, command=lambda opt=opcao, row=i: selecionar_opcao(opt, popup, row))
        button.grid(row=i, column=0)

    def on_window_click(event):
        widget = event.widget
        while widget is not None:
            if widget == graficos_frame or widget == popup:
                return
            widget = widget.master
        graficos_frame.destroy()

    janela.bind("<Button-1>", on_window_click)

# Define the graficos button
graficos_button = tk.Button(frameOpcoes, text=trans_graficos['graficos'][idioma], command=open_graficos_menu, width=10)
graficos_button.grid(row=0, column=3)


blank_label = tk.Label(frameOpcoes, text='                                ')
blank_label.grid(row=0, column=4)

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
                    lucro_per_real REAL,
                    esporte TEXT
                )''')

    conn.commit()
else:
    conn = sqlite3.connect("dados.db")
    c = conn.cursor()



def update_lucro_diario():
    hoje = datetime.today().strftime('%Y-%m-%d')
    lucro_diario = c.execute(f"SELECT SUM(lucro_estimado) FROM apostas WHERE DATE(data_entrada) = '{hoje}'").fetchone()[
        0]
    if lucro_diario:
        lucro_diario = format(float(lucro_diario), '.2f')
    else:
        lucro_diario = f'{0.00:.2f}'
    frame_lucro.itemconfigure('lucro_text', text=f'{cambio} {lucro_diario}')

    if float(lucro_diario) <= 0:
        frame_lucro.itemconfigure('bg', fill='red')
    elif float(lucro_diario) > 0 and float(lucro_diario) <= meta / 2:
        green_value = int((float(lucro_diario) / (meta / 2)) * 200)
        red_value = int((255 - green_value * 1.275) * (1 + (green_value * 1.275) / 2550))
        frame_lucro.itemconfigure('bg', fill=f'#{red_value:02x}{green_value:02x}00')
    else:
        blue_value = int(((float(lucro_diario) - (meta / 2)) / (meta / 2)) * 255)
        blue_value = 255 if blue_value > 255 else blue_value
        green_value = int((200 - blue_value / 1.275) * (1 + blue_value / 2550))
        frame_lucro.itemconfigure('bg', fill=f'#00{green_value:02x}{blue_value:02x}')

frame_lucro = tk.Canvas(janela, width=132, height=57, highlightthickness=0)
frame_lucro.create_rectangle(0, 15, 130, 55, tags='bg')
frame_lucro.create_text(65, 5, text=trans_config['Lucro Estimado Hoje'][idioma], fill="black", font=("Arial", 12, "bold"))
frame_lucro.create_text(65, 35, text="", fill="white", font=("Arial", 24, "bold"), tag='lucro_text')
frame_lucro.place(x=450, y=5)

# Filtros
def toggle_order_crescente():
    current_order1 = order_button1["text"]
    if current_order1 == trans_filtros['Crescente'][idioma]:
        order_button1["text"] = trans_filtros['Decrescente'][idioma]
    else:
        order_button1["text"] = trans_filtros['Crescente'][idioma]
    on_filters_change()
def toggle_order_add():
    current_order2 = order_button2["text"]
    if current_order2 == trans_filtros['Adição'][idioma]:
        order_button2["text"] = trans_filtros['Data'][idioma]
    else:
        order_button2["text"] = trans_filtros['Adição'][idioma]
    on_filters_change()
def toggle_time():
    current_time = time_button["text"]
    if current_time == trans_filtros['Vencem até'][idioma]:
        time_button["text"] = trans_filtros['Feitas desde'][idioma]
        timeframe_combobox["values"] = [trans_filtros['hoje'][idioma], trans_filtros['ontem'][idioma], trans_filtros['essa semana'][idioma], trans_filtros['esse mês'][idioma], trans_filtros['30 dias'][idioma], trans_filtros['6 meses'][idioma], trans_filtros['esse ano'][idioma], trans_filtros['365 dias'][idioma], trans_filtros['sempre'][idioma]]
    else:
        time_button["text"] = trans_filtros['Vencem até'][idioma]
        timeframe_combobox["values"] = [trans_filtros['hoje'][idioma], trans_filtros['amanhã'][idioma], trans_filtros['essa semana'][idioma], trans_filtros['esse mês'][idioma]]
        if timeframe_options.index(timeframe_combobox.get()) > 3:
            timeframe_combobox.current(3)
    on_filters_change()

# Ordenação
def on_filters_change():
    bethouse_list = set()
    preencher_treeview(conn, tabela, bethouse_options, situation_vars, order_button1, order_button2, time_button, timeframe_combobox, search_var, frameTabela, frameSaldos, idioma, cambio, linhas_bethouses, bethouse_list=bethouse_list)
    save_bethouse_options()

order_button1 = tk.Button(frameTabela, text=trans_filtros['Crescente'][idioma], command=toggle_order_crescente, width=8)
order_button1.grid(row=0, column=0)
order_button2 = tk.Button(frameTabela, text=trans_filtros['Data'][idioma], command=toggle_order_add, width=4)
order_button2.grid(row=0, column=1)

# Tempo
time_button = tk.Button(frameTabela, text=trans_filtros['Feitas desde'][idioma], width=5, command=toggle_time)
time_button.grid(row=0, column=2)

timeframe_options = [trans_filtros['hoje'][idioma], trans_filtros['ontem'][idioma], trans_filtros['essa semana'][idioma], trans_filtros['esse mês'][idioma], trans_filtros['30 dias'][idioma], trans_filtros['6 meses'][idioma], trans_filtros['esse ano'][idioma], trans_filtros['365 dias'][idioma], trans_filtros['sempre'][idioma]]
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
    situation_frame.place(x=situation_button.winfo_x(), y=situation_button.winfo_y() + situation_button.winfo_height())
    situation_frame.config(highlightthickness=2, highlightbackground="gray", relief="ridge")

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


situations = [trans_filtros['Vencidas'][idioma], trans_filtros['Abertas'][idioma], trans_filtros['Fechadas'][idioma]]
situation_vars = [tk.IntVar() for _ in situations]
situation_button = tk.Button(frameTabela, text=trans_filtros['Situação'][idioma])
situation_button.grid(row=0, column=4)
situation_button.bind("<Button-1>", show_frame)

#Pesquisa
def search(event=None):
    # Chama a função preencher_treeview passando o valor da pesquisa
    bethouse_list = set()
    preencher_treeview(conn, tabela, bethouse_options, situation_vars, order_button1, order_button2, time_button, timeframe_combobox, search_var, frameTabela, frameSaldos, idioma, cambio, linhas_bethouses, bethouse_list=bethouse_list)

# Cria uma variável de controle para rastrear as alterações no Entry
search_var = tk.StringVar()
search_entry = tk.Entry(frameTabela, textvariable=search_var, width=10)
search_entry.grid(row=0, column=5)
icon_photo = ImageTk.PhotoImage(Image.open("pesquisa.png").resize((16, 16), Image.LANCZOS))
search_icon_label = tk.Label(frameTabela, image=icon_photo)
search_icon_label.place(x=510, y=4)
# Vincula a função search ao evento de pressionar o botão de pesquisa
search_icon_label.bind("<Button-1>", search)
# Vincula a função search ao evento de pressionar a tecla Enter no campo de pesquisa
search_entry.bind("<Return>", search)

def load_bethouse_options():
    global bethouse_options, bethouse_options_total, mercado_options, arred_var, cambio, meta, linhas_apostas, linhas_bethouses
    try:
        with open('bethouse_options.json', 'r') as f:
            data = json.load(f)
            bethouse_options_total = data.get("bethouse_options", {})
            bethouse_options = {bethouse: options for bethouse, options in bethouse_options_total.items() if options.get("ativa", "False") == "True"}
            mercado_options = data.get("mercado_options", [])
            arred_var = tk.StringVar(value=data.get("arredondamento"))
            if arred_var.get() in trans_config['Padrão'].values():
                arred_var = tk.StringVar(value=trans_config['Padrão'][idioma])
            custom = data.get('custom', {})
            cambio = custom.get('cambio', 'US$')
            meta = float(custom.get('meta', 100))
            linhas_apostas = custom.get('linhas_apostas', 6)
            linhas_bethouses = custom.get('linhas_bethouses', 8)
            filtros = data.get("filtros", {})
            order_text = filtros.get('ordem', trans_filtros['Crescente'][idioma])
            if order_text in trans_filtros['Crescente'].values():
                order_text = trans_filtros['Crescente'][idioma]
            else:
                order_text = trans_filtros['Decrescente'][idioma]
            add_text = filtros.get('data_entrada', trans_filtros['Adição'][idioma])
            if add_text in trans_filtros['Adição'].values():
                add_text = trans_filtros['Adição'][idioma]
            else:
                add_text = trans_filtros['Data'][idioma]
            time_text = filtros.get('time', trans_filtros['Feitas desde'][idioma])
            if time_text in trans_filtros['Feitas desde'].values():
                time_text = trans_filtros['Feitas desde'][idioma]
            else:
                time_text = trans_filtros['Vencem até'][idioma]
            timeframe_text = filtros.get('timeframe', trans_filtros['hoje'][idioma])
            if timeframe_text in trans_filtros['hoje'].values():
                timeframe_text = trans_filtros['hoje'][idioma]
            elif timeframe_text in trans_filtros['amanhã'].values():
                timeframe_text = trans_filtros['amanhã'][idioma]
            elif timeframe_text in trans_filtros['ontem'].values():
                timeframe_text = trans_filtros['ontem'][idioma]
            elif timeframe_text in trans_filtros['essa semana'].values():
                timeframe_text = trans_filtros['essa semana'][idioma]
            elif timeframe_text in trans_filtros['esse mês'].values():
                timeframe_text = trans_filtros['esse mês'][idioma]
            elif timeframe_text in trans_filtros['30 dias'].values():
                timeframe_text = trans_filtros['30 dias'][idioma]
            elif timeframe_text in trans_filtros['6 meses'].values():
                timeframe_text = trans_filtros['6 meses'][idioma]
            elif timeframe_text in trans_filtros['esse ano'].values():
                timeframe_text = trans_filtros['esse ano'][idioma]
            elif timeframe_text in trans_filtros['365 dias'].values():
                timeframe_text = trans_filtros['365 dias'][idioma]
            else:
                timeframe_text = trans_filtros['sempre'][idioma]
            selected_situations = filtros.get("situations", [])
            return order_text, add_text, time_text, timeframe_text, selected_situations
    except FileNotFoundError:
        bethouse_options_total = {}
        bethouse_options = {}
        mercado_options = ["1", "12", "1X", "2", "AH1", "AH2", "ClearSheet1", "ClearSheet2", "DNB1", "DNB2", "EH1", "EH2", "EHX", "Exactly", "Lay", "Not", "Q1", "Q2", "Removal", "ScoreBoth", "TEv", "TO", "TO (3-way)", "TU", "TU (3-way)", "TO1", "TO1 (3-way)", "TO2", "TO2 (3-way)",  "TOd", "TU2", "TU2 (3-way)", "TU1", "TU1 (3-way)", "WinAllPer1", "WinAllPer2", "WinNil1", "WinNil2", "WinLeastOneOfPer1", "WinLeastOneOfPer2", "X", "X2"]
        cambio = 'US$'
        linhas_apostas = 6
        linhas_apostas = 8
        arred_var = tk.StringVar(value=trans_config['Padrão'][idioma])
        order_text = trans_filtros['Crescente'][idioma]
        add_text = trans_filtros['Data'][idioma]
        time_text = trans_filtros['Feitas desde'][idioma]
        timeframe_text = trans_filtros['hoje'][idioma]
        selected_situations = []
        return order_text, add_text, time_text, timeframe_text, selected_situations

# Carregar Bethouse_options
order_text, add_text, time_text, timeframe_text, selected_situations = load_bethouse_options()
order_button1["text"] = order_text
order_button2["text"] = add_text
time_button["text"] = time_text
timeframe_combobox.set(timeframe_text)
for i, var in enumerate(situation_vars):
        var.set(selected_situations[i]) # Configurações de usuário
update_lucro_diario()

def open_bethouses():
    def on_close_config():
        # Função para lidar com o fechamento da janela
        if bethouse_list:
            tabela_bethouses(frameSaldos, idioma, cambio, linhas_bethouses, conn, bethouse_list=bethouse_list)
        bethouses_window.destroy()

    # Cria uma janela pop-up
    bethouses_window = tk.Toplevel(frameJogo)
    bethouses_window.title(trans_config['Configurações'][idioma])
    bethouses_frame = tk.Frame(bethouses_window)
    bethouses_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
    bethouses_window.protocol("WM_DELETE_WINDOW", on_close_config)
    bethouse_list = set()

    # Cria a entrada de texto para adicionar novas BetHouses
    bethouse_label = tk.Label(bethouses_frame, text=f"{trans_config['BetHouse'][idioma]}:")
    bethouse_label.grid(row=0, column=0, padx=5, pady=5)
    new_bethouse_entry = tk.Entry(bethouses_frame, width=15)
    new_bethouse_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5)

    # Cria um widget Label para o título 'Taxa:'
    def validate_rate_input(new_value):
        new_value = new_value.replace(',', '.')
        if not new_value:
            return True
        try:
            float(new_value)
        except ValueError:
            return False
        if new_value.count('.') > 1:
            return False
        if '.' in new_value:
            decimal_part = new_value.split('.')[1]
            if len(decimal_part) > 3:
                return False
        return True

    def on_focus_out(event):
        # Função para lidar com o evento FocusOut
        if not new_rate_entry.get():
            new_rate_entry.insert(0, 0)

    rate_label = tk.Label(bethouses_frame, text=f"{trans_config['Taxa'][idioma]}(%):")
    rate_label.grid(row=1, column=0, padx=5, pady=5)
    vcmd_tax = (bethouses_frame.register(validate_rate_input), '%P')
    new_rate_entry = tk.Entry(bethouses_frame, validate='key', validatecommand=vcmd_tax, width=3)
    new_rate_entry.insert(0, 0)
    new_rate_entry.grid(row=1, column=1, padx=5, pady=5)
    new_rate_entry.bind("<FocusOut>", on_focus_out)

    arred_base_var = tk.DoubleVar(value=0.01)
    arred_base_label = tk.Label(bethouses_frame, text=f"{trans_graficos['Arred'][idioma]}:")
    arred_base_label.grid(row=1, column=2)
    arred_base_options = [0.01, 0.05, 0.1, 0.5, 1, 5, 10]
    arred_base_combobox = ttk.Combobox(bethouses_frame, textvariable=arred_base_var, values=arred_base_options, width=3, state="readonly")
    arred_base_combobox.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)

    # Cria a entrada de texto para adicionar links
    link_label = tk.Label(bethouses_frame, text=f"{trans_config['Link'][idioma]}:")
    link_label.grid(row=2, column=0, padx=5, pady=5)
    link_entry = tk.Entry(bethouses_frame, width=15)
    link_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
    # Cria a combobox com as opções
    navegador = [trans_config['sistema'][idioma], 'chrome', 'firefox', 'edge', 'safari']
    navegador_combobox = ttk.Combobox(bethouses_frame, values=navegador, width=5)
    navegador_combobox.set(trans_config['sistema'][idioma])
    navegador_combobox.grid(row=2, column=3, padx=5, pady=5)

    # Cria uma função para adicionar uma nova BetHouse à lista
    def add_bethouse():
        new_bethouse = new_bethouse_entry.get()
        if not new_bethouse:
            tk.messagebox.showwarning(trans_config['Aviso'][idioma], trans_config['Dê o nome da BetHouse'][idioma])
            return
        exist = new_bethouse in bethouse_options_total.keys()
        new_bethouse = new_bethouse_entry.get().strip()
        new_rate = float(new_rate_entry.get().replace(',', '.').strip()) if new_rate_entry.get().strip() != "" else 0.0
        text_color = text_color_entry.get().strip()
        background_color = background_color_entry.get().strip()
        bethouse_options_total[new_bethouse] = {
            'taxa': new_rate / 100,
            'text_color': text_color,
            'background_color': background_color,
            'arred': arred_base_var.get(),
            'ativa': 'True',
            'html': {'link': link_entry.get().strip(),
                     'navegador': navegador_combobox.get()}
        }
        bethouse_options[new_bethouse] = {
            'taxa': new_rate / 100,
            'text_color': text_color,
            'background_color': background_color,
            'arred': arred_base_var.get(),
            'ativa': 'True',
            'html': {"link": link_entry.get().strip(),
                     'navegador': navegador_combobox.get()}
        }
        if not exist:
            table_name = f"{new_bethouse}_saldos"
            table_name = re.sub(r'\W+', '_', table_name)
            if table_name[0].isdigit():
                table_name = f'_{table_name}'
            create_table_query = f'''
                    CREATE TABLE "{table_name}" (
                        id INTEGER,
                        data_entrada TEXT,
                        data_fim TEXT,
                        odd REAL,
                        aposta REAL,
                        resultado TEXT,
                        balanco REAL,
                        dif_real REAL
                    )
                    '''
            c.execute(create_table_query)
        new_bethouse_entry.delete(0, tk.END)
        new_rate_entry.delete(0, tk.END)
        arred_combobox.set(0.01)
        text_color_entry.delete(0, tk.END)
        background_color_entry.delete(0, tk.END)
        link_entry.delete(0, tk.END)
        navegador_combobox.set('sistema')
        bethouse_list.add(new_bethouse)
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
    text_color_button = tk.Button(bethouses_frame, text=trans_config['Cor do Texto'][idioma], command=choose_text_color)
    text_color_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    background_color_button = tk.Button(bethouses_frame, text=trans_config['Cor de Fundo'][idioma], command=choose_background_color)
    background_color_button.grid(row=3, column=2, columnspan=2, padx=5, pady=5)

    # Cria botão para adicionar a nova BetHouse
    add_bethouse_button = tk.Button(bethouses_frame, text=trans_config['Adicionar'][idioma], command=add_bethouse)
    add_bethouse_button.grid(row=4, column=0, columnspan=4, padx=5, pady=5)

    def activate_bethouse(bethouse):
        # Função para ativar ou desativar uma bethouse
        if bethouse_options_total[bethouse]['ativa'] == "True":
            bethouse_options_total[bethouse]['ativa'] = "False"
            bethouse_options.pop(bethouse, None)
        else:
            bethouse_options_total[bethouse]['ativa'] = "True"
            bethouse_options[bethouse] = bethouse_options_total[bethouse]
        bethouse_list.add(bethouse)
        save_bethouse_options()
        update_bethouses_list()

    def on_right_click(event):
        # Função para lidar com o evento de clique com o botão direito do mouse
        item = bethouses_tree.identify('item', event.x, event.y)
        if item:
            bethouse = bethouses_tree.item(item, 'values')[0]
            if bethouse_options_total[bethouse]['ativa'] == "True":
                activate_menu.entryconfigure(0, label=trans_config['Desativar'][idioma], command=lambda b=bethouse: activate_bethouse(b))
            else:
                activate_menu.entryconfigure(0, label=trans_config['Ativar'][idioma], command=lambda b=bethouse: activate_bethouse(b))
            activate_menu.tk_popup(event.x_root, event.y_root)

    # Cria a lista de BetHouses
    configStyle = ttk.Style()
    configStyle.configure("Normal.Treeview", rowheight=20)
    bethouses_list = sorted(bethouse_options_total.keys())
    bethouses_tree = ttk.Treeview(bethouses_frame, columns=(trans_config['BetHouse'][idioma], trans_config['Taxa'][idioma], trans_graficos['Arred'][idioma], trans_config['Ativa'][idioma]), show='headings', style="Normal.Treeview")
    bethouses_tree.grid(row=5, column=0, columnspan=4, padx=5, pady=5)
    bethouses_tree.heading(trans_config['BetHouse'][idioma], text=trans_config['BetHouse'][idioma])
    bethouses_tree.heading(trans_config['Taxa'][idioma], text=trans_config['Taxa'][idioma])
    bethouses_tree.heading(trans_graficos['Arred'][idioma], text=trans_graficos['Arred'][idioma])
    bethouses_tree.heading(trans_config['Ativa'][idioma], text=trans_config['Ativa'][idioma])
    bethouses_tree.column(trans_config['BetHouse'][idioma], width=70)
    bethouses_tree.column(trans_config['Taxa'][idioma], width=40)
    bethouses_tree.column(trans_graficos['Arred'][idioma], width=40)
    bethouses_tree.column(trans_config['Ativa'][idioma], width=40)

    for bethouse in bethouses_list:
        taxa = f'{float(bethouse_options_total[bethouse]["taxa"]) * 100:g} %'
        arred = bethouse_options_total[bethouse]["arred"]
        ativa = bethouse_options_total[bethouse]["ativa"]
        if ativa == 'True':
            ativa = trans_config['Sim'][idioma]
        else:
            ativa = trans_config['Não'][idioma]
        bethouses_tree.insert('', 'end', values=(bethouse, taxa, arred,  ativa), tags=(bethouse,))
        bethouses_tree.tag_configure(bethouse, background=bethouse_options_total[bethouse]['background_color'], foreground=bethouse_options_total[bethouse]['text_color'])

    # Cria o menu de contexto para ativar ou desativar
    activate_menu = Menu(bethouses_tree, tearoff=False)
    activate_menu.add_command(label="")

    # Associa o menu de contexto à treeview
    bethouses_tree.bind("<Button-2>", on_right_click)

    def on_double_click(event):
        selected_item = bethouses_tree.selection()[0]
        selected_bethouse = bethouses_tree.item(selected_item)['values'][0]
        taxa = bethouse_options_total[selected_bethouse]["taxa"]
        arred = bethouse_options_total[selected_bethouse]["arred"]
        text_color = bethouse_options_total[selected_bethouse]["text_color"]
        background_color = bethouse_options_total[selected_bethouse]["background_color"]
        link = bethouse_options_total[selected_bethouse]["html"]["link"]
        navegador = bethouse_options_total[selected_bethouse]["html"]["navegador"]
        new_bethouse_entry.delete(0, tk.END)
        new_bethouse_entry.insert(0, selected_bethouse)
        new_rate_entry.delete(0, tk.END)
        new_rate_entry.insert(0, f'{taxa * 100:g}')
        arred_base_combobox.set(arred)
        text_color_entry.delete(0, tk.END)
        text_color_entry.insert(0, text_color)
        background_color_entry.delete(0, tk.END)
        background_color_entry.insert(0, background_color)
        link_entry.delete(0, tk.END)
        link_entry.insert(0, link)
        navegador_combobox.set(navegador)

    bethouses_tree.bind('<Double-1>', on_double_click)

    # Cria uma função para remover a BetHouse selecionada da lista
    def remove_bethouse():
        selected_item = bethouses_tree.selection()[0]
        selected_bethouse = bethouses_tree.item(selected_item)['values'][0]
        table_name = f"{selected_bethouse}_saldos"
        table_name = re.sub(r'\W+', '_', table_name)
        if table_name[0].isdigit():
            table_name = f'_{table_name}'
        # Verifica se a tabela existe
        check_table_query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        c.execute(check_table_query)
        result = c.fetchone()

        if result is not None:
            # Verifica se a tabela está vazia
            check_empty_query = f"SELECT COUNT(*) FROM {table_name}"
            c.execute(check_empty_query)
            count = c.fetchone()[0]
            if count > 0:
                answer = messagebox.askquestion(trans_config['Apagar histórico'][idioma], f"{trans_config['Apagar todo histórico'][idioma]} {table_name}, {trans_config['confirmar apagar histórico'][idioma]}")
                if answer == 'yes':
                    c.execute(f"DROP TABLE {table_name}")
                else:
                    return
        # Apaga a tabela se estiver vazia
        c.execute(f"DROP TABLE {table_name}")
        del bethouse_options_total[selected_bethouse]
        if selected_bethouse in bethouse_options.keys():
            del bethouse_options[selected_bethouse]
        bethouse_list.add(selected_bethouse)

        update_bethouses_list()
        save_bethouse_options()  # Salva os dados em um arquivo JSON

    # Cria um botão para remover a BetHouse selecionada
    remove_bethouse_button = tk.Button(bethouses_frame, text=trans_config['Remover'][idioma], command=remove_bethouse)
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
        bethouses_list = sorted(bethouse_options_total.keys())
        # Adiciona as BetHouses à Treeview
        for bethouse in bethouses_list:
            taxa = f'{float(bethouse_options_total[bethouse]["taxa"]) * 100:g} %'
            arred = bethouse_options_total[bethouse]["arred"]
            ativa = bethouse_options_total[bethouse]["ativa"]
            if ativa == 'True':
                ativa = trans_config['Sim'][idioma]
            else:
                ativa = trans_config['Não'][idioma]
            bethouses_tree.insert('', 'end', values=(bethouse, taxa, arred, ativa), tags=(bethouse,))
            bethouses_tree.tag_configure(bethouse, background=bethouse_options_total[bethouse]['background_color'], foreground=bethouse_options_total[bethouse]['text_color'])

    # Chama a função para atualizar a lista de BetHouses
    update_bethouses_list()

    def add_mercado_option():
        new_option = new_mercado_entry.get()
        if not new_option:
            tk.messagebox.showwarning(trans_config['Aviso'][idioma], trans_config['Dê o nome da opção de mercado'][idioma])
            return
        mercado_options.append(new_option)
        new_mercado_entry.delete(0, tk.END)
        save_bethouse_options()
        update_mercado_options_list()

    # Cria a entrada de texto para adicionar novas opções de mercado
    mercado_label = tk.Label(bethouses_frame, text=f"{trans_config['Mercado'][idioma]}:")
    mercado_label.grid(row=2, column=4, padx=5, pady=5)
    new_mercado_entry = tk.Entry(bethouses_frame)
    new_mercado_entry.grid(row=3, column=4, padx=5, pady=5)

    # Cria um botão para adicionar a nova opção de mercado
    add_mercado_button = tk.Button(bethouses_frame, text=trans_config['Adicionar'][idioma], command=add_mercado_option)
    add_mercado_button.grid(row=4, column=4, columnspan=2, padx=5, pady=5)

    # Cria a lista de opções de mercado
    mercado_options_list = sorted(list(mercado_options), key=lambda x: x[0])

    # Cria o Treeview
    mercado_options_tree = ttk.Treeview(bethouses_frame, columns=[trans_config['Mercado'][idioma]], show='headings',
                                        height=10, style="Normal.Treeview")
    mercado_options_tree.grid(row=5, column=4, columnspan=2, padx=5, pady=5)
    mercado_options_tree.heading(trans_config['Mercado'][idioma], text=trans_config['Mercado'][idioma])

    # Adiciona as opções de mercado ao Treeview
    for i, mercado in enumerate(mercado_options_list):
        mercado_options_tree.insert('', 'end', values=[mercado])
        if i % 2 == 1:
            mercado_options_tree.item(mercado_options_tree.get_children()[-1], tags=['oddrow'])

    # Define o estilo para linhas ímpares
    mercado_options_tree.tag_configure('oddrow', background='gray90')

    # Função para remover a opção de mercado selecionada
    def remove_mercado_option():
        selected_item = mercado_options_tree.focus()
        if selected_item:
            values = mercado_options_tree.item(selected_item)['values']
            if values:
                selected_option = values[0]
                mercado_options_tree.delete(selected_item)
                mercado_options.remove(selected_option)
                save_bethouse_options()
                update_mercado_options_list()

    # Cria um botão para remover a opção de mercado selecionada
    remove_mercado_button = tk.Button(bethouses_frame, text=trans_config['Remover'][idioma], command=remove_mercado_option)
    remove_mercado_button.grid(row=6, column=4, columnspan=2, padx=5, pady=5)

    # Cria uma função para atualizar a lista de BetHouses
    def update_mercado_options_list():
        # Atualiza as opções do combobox
        mercados = sorted(list(mercado_options), key=lambda x: x[0])
        mercado_combobox['values'] = mercados
        mercado_combobox2['values'] = mercados
        mercado_combobox3['values'] = mercados
        # Limpa o Treeview
        mercado_options_tree.delete(*mercado_options_tree.get_children())
        # Adiciona as opções de mercado ao Treeview
        for i, mercado in enumerate(mercados):
            mercado_options_tree.insert('', 'end', values=[mercado])
            if i % 2 == 1:
                mercado_options_tree.item(mercado_options_tree.get_children()[-1], tags=['oddrow'])


def open_customization_window():
    # Função para lidar com o clique no comando "Personalizar"
    def save_customization():
        # Função para salvar as configurações personalizadas
        global linhas_apostas, linhas_bethouses, cambio, tabela, meta
        linhas_apostas = int(spinbox_linhas_apostas.get())
        linhas_bethouses = int(spinbox_linhas_bethouses.get())
        cambio = entry_cambio.get() if entry_cambio.get() != '' else 'US$'
        meta = float(entry_meta.get())
        if tabela:
            tabela.destroy()  # Destruir tabela atual, se existir
        customization_window.destroy()
        save_bethouse_options()
        update_lucro_diario()
        tabela = BetHistTreeview(frameTabela, situation_vars, order_button1, order_button2, time_button, timeframe_combobox, search_var, frameTabela, frameSaldos, idioma, cambio, linhas_bethouses, conn, columns=("index", "adds", "jogo", "data", "resultados", "bethouses", "odds", "bets", "mercados", "id"), show="headings", style="Treeview", height=linhas_apostas)
        tabela.heading("index", text="")
        tabela.heading("adds", text=trans_filtros['Adição'][idioma].capitalize())
        tabela.heading("jogo", text=trans_jogo['Times'][idioma].capitalize())
        tabela.heading("data", text=trans_graficos['dia'][idioma].capitalize())
        tabela.heading("resultados", text=trans_jogo['W/L'][idioma].upper())
        tabela.heading("bethouses", text=trans_config['BetHouses'][idioma].capitalize())
        tabela.heading("odds", text=trans_graficos['Odds'][idioma].capitalize())
        tabela.heading("bets", text=trans_graficos['apostas'][idioma].capitalize())
        tabela.heading("mercados", text=trans_config['Mercados'][idioma].capitalize())
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
        tabela.grid(row=2, column=0, columnspan=10, rowspan=10)
        tabela.bind('<Double-Button-1>', select_bets)  # Tabela
        preencher_treeview(conn, tabela, bethouse_options, situation_vars, order_button1, order_button2, time_button, timeframe_combobox, search_var, frameTabela, frameSaldos, idioma, cambio, linhas_bethouses, bethouse_list=bethouse_options.keys())

    # Criação da janela de customização
    customization_window = tk.Toplevel()
    customization_window.title("Customização")

    def validate_spinbox_input(value):
        # Verifica se o valor inserido contém apenas números
        if (value.isdigit() and int(value) <= 10) or value == '':
            return True
        else:
            return False
    # Labels e campos de entrada
    label_linhas_apostas = tk.Label(customization_window, text="Linhas de apostas:")
    label_linhas_apostas.pack()
    spinbox_var = tk.StringVar()
    spinbox_var.set(linhas_apostas)  # Define o valor inicial do Spinbox
    validate_input = customization_window.register(validate_spinbox_input)  # Registra a função de validação
    spinbox_linhas_apostas = tk.Spinbox(customization_window, from_=0, to=10, increment=1, width=4, textvariable=spinbox_var, validate="key", validatecommand=(validate_input, "%P"))
    spinbox_linhas_apostas.pack()

    label_linhas_bethouses = tk.Label(customization_window, text="Linhas de bethouses:")
    label_linhas_bethouses.pack()
    spinbox_var2 = tk.StringVar()
    spinbox_var2.set(linhas_apostas)
    spinbox_linhas_bethouses = tk.Spinbox(customization_window, from_=0, to=20, increment=1, width=4, textvariable=spinbox_var2, validate="key", validatecommand=(validate_input, "%P"))
    spinbox_linhas_bethouses.pack()

    label_cambio = tk.Label(customization_window, text="Moeda:")
    label_cambio.pack()
    entry_cambio = tk.Entry(customization_window, width=5)
    entry_cambio.insert(tk.END, cambio)
    entry_cambio.pack()

    def validate_meta(value):
        # Verifica se o valor inserido contém apenas números
        if value.isdigit() or value == '':
            return True
        else:
            return False

    label_meta = tk.Label(customization_window, text=f"Meta diária ({cambio}):")
    label_meta.pack()
    validate_input_meta = customization_window.register(validate_meta)  # Registra a função de validação
    entry_meta = tk.Entry(customization_window, width=5)
    entry_meta.insert(tk.END, meta)
    entry_meta.config(validate="key", validatecommand=(validate_input_meta, "%P"))
    entry_meta.pack()

    # Botão de salvar
    button_save = tk.Button(customization_window, text="Salvar", command=save_customization)
    button_save.pack()

# Cria um menu pop-up com as opções desejadas
settings_menu = tk.Menu(frameJogo, tearoff=False)
settings_menu.add_command(label=trans_config['Configurações'][idioma], command=open_bethouses)
settings_menu.add_command(label=trans_config['Personalizar'][idioma], command=open_customization_window)
settings_menu.add_separator()
settings_menu.add_command(label=trans_config['Sair'][idioma], command=frameJogo.quit)

# Define a ação do botão de configurações para mostrar o menu pop-up
def show_settings_menu(event):
    settings_menu.post(event.x_root, event.y_root)

# Define uma imagem para o botão de configurações
settings_icon = tk.PhotoImage(file="/Users/sergioeblutzer/PycharmProjects/Gerenciamento_Bolsa_Esportiva/engrenagens.png").subsample(20, 20)
settings_button = tk.Button(frameOpcoes, image=settings_icon, bd=0) # Ajustes Iniciais

# Associa a ação do botão de configurações ao clique do mouse
settings_button.bind("<Button-1>", show_settings_menu)


# Coloca o botão de configurações no row 0 colunm 0 da janela principal

def save_bethouse_options():
    sorted_bethouse_options = dict(sorted(bethouse_options_total.items(), key=lambda x: x[0]))
    sorted_mercado_options = sorted(mercado_options, key=lambda x: x[0])
    arredondamento = arred_var.get()
    data = {
        "bethouse_options": sorted_bethouse_options,
        "mercado_options": sorted_mercado_options,
        "arredondamento": arredondamento,
        "custom": {
            "cambio": cambio,
            "linhas_apostas": linhas_apostas,
            "linhas_bethouses": linhas_bethouses,
            "meta": meta
        },
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

def show_tooltip_simples(event, onde, oque):
    global tooltip_window
    tooltip_window = Toplevel(frameJogo)
    tooltip_window.wm_overrideredirect(True)
    x = onde.winfo_rootx()
    y = onde.winfo_rooty() - 20
    tooltip_window.wm_geometry(f"+{x}+{y}")
    if oque == 'jogo':
        label = Label(tooltip_window, text=trans_jogo['Adicione times'][idioma])
    elif oque == 'esporte':
        label = Label(tooltip_window, text=trans_jogo['Adicione o esporte'][idioma])
    elif oque == 'dia':
        label = Label(tooltip_window, text=trans_jogo['Insira o dia'][idioma])
    elif oque == 'mês':
        label = Label(tooltip_window, text=trans_jogo['Selecione o mês'][idioma])
    elif oque == 'ano':
        label = Label(tooltip_window, text=trans_jogo['Insira o ano'][idioma])
    elif oque == 'hora':
        label = Label(tooltip_window, text=trans_jogo['Insira a hora'][idioma])
    elif oque == 'minuto':
        label = Label(tooltip_window, text=trans_jogo['Insira o minuto'][idioma])
    elif oque == 'arred':
        label = Label(tooltip_window, text=trans_jogo['Arred padrão'][idioma])
    elif oque == 'duplo':
        label = Label(tooltip_window, text=trans_jogo['Defina 2'][idioma])
    elif oque == 'triplo':
        label = Label(tooltip_window, text=trans_jogo['Defina 3'][idioma])
    elif oque == 'bethouse':
        label = Label(tooltip_window, text=trans_jogo['Selecione as BetHouses'][idioma])
    elif oque == 'mercado':
        label = Label(tooltip_window, text=trans_jogo['Selecione os mercados'][idioma])
    elif oque == 'mercado':
        label = Label(tooltip_window, text=trans_jogo['Insira os valores'][idioma])
    elif oque == 'odd':
        label = Label(tooltip_window, text=trans_jogo['Insira as odds'][idioma])
    elif oque == 'aposta':
        label = Label(tooltip_window, text=trans_jogo['Insira as apostas'][idioma])
    elif oque == 'surebets':
        label = Label(tooltip_window, text=trans_jogo['Melhores apostas'][idioma])
    elif oque == 'lucro':
        label = Label(tooltip_window, text=trans_jogo['Lucro estimado'][idioma])
    elif oque == 'lucro_per':
        label = Label(tooltip_window, text=trans_jogo['Lucro percentual estimado'][idioma])
    elif oque == 'liability':
        label = Label(tooltip_window, text=trans_jogo['liability'][idioma])
    elif oque == 'col_bethouse':
        label = Label(tooltip_window, text=trans_jogo['Lista bethouses'][idioma])
    elif oque == 'col_O':
        label = Label(tooltip_window, text=trans_jogo['Apostas em aberto'][idioma])
    elif oque == 'col_V':
        label = Label(tooltip_window, text=trans_jogo['Vitórias mensal'][idioma])
    elif oque == 'col_D':
        label = Label(tooltip_window, text=trans_jogo['Derrotas mensal'][idioma])
    elif oque == 'col_atual':
        label = Label(tooltip_window, text=trans_jogo['Montante atual'][idioma])
    elif oque == 'col_em_aberto':
        label = Label(tooltip_window, text=trans_jogo['Montante em aberto'][idioma])
    elif oque == 'col_total':
        label = Label(tooltip_window, text=trans_jogo['Montante total'][idioma])
    elif oque == 'col_hoje':
        label = Label(tooltip_window, text=trans_jogo['Lucro diário'][idioma])
    else:
        label = Label(tooltip_window, text=trans_jogo['Lucro mensal'][idioma])
    label.pack()
def hide_tooltip_simples(event):
    global tooltip_window
    if tooltip_window:
        tooltip_window.destroy()

# Botão Arredondamento
def arredondamento_changed(event):
    save_bethouse_options()

arred_label = tk.Label(frameJogo, text="Arred.:")
arred_label.grid(row=2, column=2, columnspan=2)
arred_options = ['Padrão', 0.01, 0.05, 0.1, 0.5, 1, 5, 10]
arred_combobox = ttk.Combobox(frameJogo, textvariable=arred_var, values=arred_options, width=5, state="readonly")
arred_combobox.bind('<Enter>', lambda event: show_tooltip_simples(event, arred_combobox, 'arred'))
arred_combobox.bind('<Leave>', hide_tooltip_simples)
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
ano_combobox.bind('<Enter>', lambda event: show_tooltip_simples(event, ano_combobox, 'ano'))
ano_combobox.bind('<Leave>', hide_tooltip_simples)
ano_combobox.bind('<KeyRelease>', update_year_combobox)
ano_combobox.grid(row=1, column=4, padx=5, pady=5, sticky=tk.W) # Ano

def processar_colar(event):
    dados = janela.clipboard_get()
    linhas = dados.splitlines()
    jogo_entry.delete(0, tk.END)
    jogo_entry.insert(tk.END, linhas[0])
    esporte_entry.delete(0, tk.END)

    partes = linhas[1].split('.')
    esporte_entry.insert(tk.END, partes[0])
    jogo_entry.focus_set()
    dia_entry.focus_set()


esporte_entry = tk.Entry(frameJogo, foreground='gray')
esporte_entry.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
esporte_entry.bind('<Enter>', lambda event: show_tooltip_simples(event, esporte_entry, 'esporte'))
esporte_entry.bind('<Leave>', hide_tooltip_simples)
janela.bind_all('<<Paste>>', processar_colar)

def on_enter_game(event):
    # Obtém o nome completo do jogo inserido na entry
    if " - " in jogo_entry.get():
        time_casa, time_fora = jogo_entry.get().strip().split(" - ")
    elif " vs " in jogo_entry.get():
        time_casa, time_fora = jogo_entry.get().strip().split(" vs ")
    elif " x " in jogo_entry.get():
        time_casa, time_fora = jogo_entry.get().strip().split(" x ")
    else:
        jogo_entry.focus_set()
        return

    # Converte a data e hora atual para string no formato YYYY-MM-DD hh:mm:ss
    data_hora_atual = datetime.now()

    # Executa a consulta na tabela 'apostas' pelo nome da equipe da casa e data do jogo
    c.execute(f"SELECT data_jogo FROM apostas WHERE time_casa = '{time_casa}' AND time_fora = '{time_fora}' AND data_jogo > '{data_hora_atual}'",)
    jogo_encontrado = c.fetchone()

    # Verifica se há um jogo futuro encontrado na consulta
    if jogo_encontrado:
        # Obtém a data do jogo
        data_jogo = jogo_encontrado[0]

        # Converte a data do jogo para objeto datetime
        data_jogo_obj = datetime.strptime(data_jogo, "%Y-%m-%d %H:%M:%S")

        # Verifica se o jogo é no futuro em relação à data e hora atual
        if data_jogo_obj > data_hora_atual:
            # Insere os valores nas entries correspondentes
            dia_entry.delete(0, 'end')
            dia_entry.insert(0, data_jogo_obj.day)
            mes_combobox.set(convert_mes(data_jogo_obj.month))
            hora_entry.delete(0, 'end')
            hora_entry.insert(0, data_jogo_obj.hour)
            minuto_entry.delete(0, 'end')
            minuto_entry.insert(0, data_jogo_obj.minute)
            # Define o foco para o bethouse_combobox
            bethouse_combobox.focus_set()

# Adiciona campo Jogo
jogo_label = tk.Label(frameJogo, text=trans_jogo['Jogo / Esporte'][idioma])
jogo_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
jogo_entry = tk.Entry(frameJogo)
jogo_entry.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
jogo_entry.bind('<FocusOut>', on_enter_game)
jogo_entry.bind('<Enter>', lambda event: show_tooltip_simples(event, jogo_entry, 'jogo'))
jogo_entry.bind('<Leave>', hide_tooltip_simples)


# Jogo

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
data_label = tk.Label(frameJogo, text=trans_filtros['Data'][idioma])
data_label.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W)

# Configurar o box dia
dia_entry = tk.Entry(frameJogo, width=2, validate="key", validatecommand=(frameJogo.register(validate_day), "%P"))
dia_atual = datetime.now().day
dia_entry.bind('<Enter>', lambda event: show_tooltip_simples(event, dia_entry, 'dia'))
dia_entry.bind('<Leave>', hide_tooltip_simples)
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
mes_options = [trans_graficos['Jan'][idioma], trans_graficos['Fev'][idioma], trans_graficos['Mar'][idioma], trans_graficos['Abr'][idioma], trans_graficos['Mai'][idioma], trans_graficos['Jun'][idioma], trans_graficos['Jul'][idioma], trans_graficos['Ago'][idioma], trans_graficos['Set'][idioma], trans_graficos['Out'][idioma], trans_graficos['Nov'][idioma], trans_graficos['Dez'][idioma]]
mes_atual = datetime.now().strftime('%b')
mes_atual_pt = {'Jan': trans_graficos['Jan'][idioma], 'Feb': trans_graficos['Fev'][idioma], 'Mar': trans_graficos['Mar'][idioma], 'Apr': trans_graficos['Abr'][idioma], 'May': trans_graficos['Mai'][idioma], 'Jun': trans_graficos['Jun'][idioma], 'Jul': trans_graficos['Jul'][idioma], 'Aug': trans_graficos['Ago'][idioma], 'Sep': trans_graficos['Set'][idioma], 'Oct': trans_graficos['Out'][idioma], 'Nov': trans_graficos['Nov'][idioma], 'Dec': trans_graficos['Dez'][idioma]}[mes_atual]
mes_combobox = ttk.Combobox(frameJogo, values=mes_options, width=3, validate="key", validatecommand=(frameJogo.register(validate_month), "%P"))
if mes_atual_pt in mes_options:
    mes_combobox.current(mes_options.index(mes_atual_pt))
else:
    mes_combobox.set(mes_options[0])
mes_combobox.bind("<KeyRelease>", update_combobox)
mes_combobox.bind('<Enter>', lambda event: show_tooltip_simples(event, mes_combobox, 'mês'))
mes_combobox.bind('<Leave>', hide_tooltip_simples)
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
hora_label = tk.Label(frameJogo, text=trans_graficos['Hora'][idioma])
hora_label.grid(row=0, column=5)
hora_entry = tk.Entry(frameJogo, width=2, validate="key", validatecommand=(frameJogo.register(validate_hour), "%P"))
hora_entry.insert(0, 12)
hora_entry.bind('<Enter>', lambda event: show_tooltip_simples(event, hora_entry, 'hora'))
hora_entry.bind('<Leave>', hide_tooltip_simples)
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
minuto_entry.bind('<Enter>', lambda event: show_tooltip_simples(event, minuto_entry, 'minuto'))
minuto_entry.bind('<Leave>', hide_tooltip_simples)
minuto_entry.grid(row=1, column=7, padx=5, pady=5, sticky=tk.W) # Data

# Adiciona campo BetHouse
# BetHouse 1
bethouse_label = tk.Label(frameApostas, text=trans_config['BetHouses'][idioma])
bethouse_label.bind('<Enter>', lambda event: show_tooltip_simples(event, bethouse_label, 'bethouse'))
bethouse_label.bind('<Leave>', hide_tooltip_simples)
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
        odd_entry3.grid(row=3, column=3, padx=5, pady=5, sticky=tk.W)
        real_label3.grid(row=3, column=4)
        aposta_entry3.grid(row=3, column=5, padx=5, pady=5, sticky=tk.W)
        palpite3_label.grid(row=3, column=6)
        lucro3_label.grid(row=3, column=7)
        alternar_bets_btn["text"] = trans_jogo['Duplo'][idioma]
        alternar_bets_btn.bind('<Enter>', lambda event: show_tooltip_simples(event, alternar_bets_btn, 'duplo'))
        alternar_bets_btn.bind('<Leave>', hide_tooltip_simples)
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
        liability_label3.grid_remove()
        alternar_bets_btn["text"] = trans_jogo['Triplo'][idioma]
        alternar_bets_btn.bind('<Enter>', lambda event: show_tooltip_simples(event, alternar_bets_btn, 'triplo'))
        alternar_bets_btn.bind('<Leave>', hide_tooltip_simples)

alternar_bets_btn = tk.Button(frameJogo, text=trans_jogo['Triplo'][idioma], command=alternar_bets)
alternar_bets_btn.bind('<Enter>', lambda event: show_tooltip_simples(event, alternar_bets_btn, 'triplo'))
alternar_bets_btn.bind('<Leave>', hide_tooltip_simples)
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
    update_columns()
    mercado = mercado_var.get()
    mercado2 = mercado_var2.get()
    mercado3 = mercado_var3.get()
    if mercado.startswith('T'):
        if len(mercado) == 2:
            igual = ''
            complemento = ''
        elif len(mercado) == 3:
            igual = mercado[2]
            complemento = ''
        else:
            igual = mercado[2]
            complemento = mercado[3:]
        operacao = mercado[1]
        if operacao == 'O':
            inverso = 'U'
        else:
            inverso = 'O'
        if num_bets == 2:
            if mercado.startswith('TEv'):
                mercado_var2.set('TOd')
                return
            elif mercado.startswith('TOd'):
                mercado_var2.set('TEv')
                return
            mercado_var2.set(f'T{inverso}{igual}{complemento}')
        else:
            if mercado.endswith('(3-way)'):
                mercado_var2.set('Exactly')
                mercado_var3.set(f'T{inverso}{igual}')
    elif mercado.startswith('AH'):
        igual = mercado[2]
        if igual == '1':
            oposto = '2'
        else:
            oposto = '1'
        if num_bets == 2:
            mercado_var2.set(f'AH{oposto}')
        else:
            mercado_var2.set('X')
            mercado_var3.set('2')
    elif mercado.startswith('DNB'):
        igual = mercado[3]
        if igual == '1':
            oposto = '2'
        else:
            oposto = '1'
        if num_bets == 2:
            mercado_var2.set(f'DNB{oposto}')
        elif num_bets == 3:
            mercado_var2.set('X')
            mercado_var3.set('1')
    elif mercado == '1':
        if num_bets == 2:
            mercado_var2.set('2')
        else:
            mercado_var2.set('X')
            mercado_var3.set('2')
    elif mercado == '2':
        if num_bets == 2:
            mercado_var2.set('1')
        else:
            mercado_var2.set('X')
            mercado_var3.set('1')
    elif mercado == '12':
        if num_bets == 2:
            mercado_var2.set('X')
    elif mercado == 'X':
        if num_bets == 2:
            mercado_var2.set('12')
    elif mercado == '1X':
        if num_bets == 2:
            mercado_var2.set('2')
    elif mercado == 'X2':
        if num_bets == 2:
            mercado_var2.set('1')
    elif mercado == 'EH1':
        if num_bets == 2:
            mercado_var2.set('AH2')
    elif mercado == 'EH2':
        if num_bets == 2:
            mercado_var2.set('AH1')
    elif mercado == 'Q1':
        mercado_var2.set('Q2')
    elif mercado == 'Q2':
        mercado_var2.set('Q1')
    elif mercado.startswith(('Score', 'Win', 'Remo', 'Clear')):
        mercado_var2.set('Not')

def on_valor_chosen(event):
    mercado = mercado_var.get()
    if mercado == 'lay' or liability_label1.winfo_manager():
        update_columns()
    valor = float_error(valor_var, '')
    if valor != '':
        if mercado.startswith('AH'):
            arred_valor = round(valor, 0)
            igual = mercado[2]
            if igual == '1':
                oposto = '2'
            else:
                oposto = '1'
            if num_bets == 2:
                valor_var2.set(-valor)
            else:
                if valor == 0:
                    return
                elif valor =='':
                    valor_var.set(0)
                    return
                elif valor.is_integer():
                    mercado_var2.set(f'AH{oposto}')
                    mercado_var3.set(f'AH{oposto}')
                    valor_var2.set(-(valor - 0.5))
                    valor_var3.set(-(valor + 0.5))
                elif (valor - 0.25).is_integer() or (valor - 0.75).is_integer():
                    mercado_var2.set(f'AH{oposto}')
                    mercado_var3.set(f'AH{oposto}')
                    valor_var2.set(-arred_valor - 0.5)
                    valor_var3.set(-arred_valor + 0.5)
                elif valor == -0.5:
                    mercado_var2.set('X')
                    mercado_var3.set(f'DNB{oposto}')
                else:
                    mercado_var2.set(f'EH{oposto}')
                    mercado_var3.set(f'EH{oposto}')
                    if valor > 0:
                        valor_var2.set(-arred_valor + 1)
                        valor_var3.set(-arred_valor)
                    else:
                        valor_var2.set(-arred_valor)
                        valor_var3.set(-arred_valor - 1)
        elif mercado.startswith('T'):
            if len(mercado) == 2:
                igual = ''
                complemento = ''
            elif len(mercado) == 3:
                igual = mercado[2]
                complemento = ''
            else:
                igual = mercado[2]
                complemento = mercado[3:]
            operacao = mercado[1]
            if operacao == 'O':
                inverso = 'U'
            else:
                inverso = 'O'
            arred_valor = round(valor, 0)
            if num_bets == 2:
                mercado_var2.set(f'T{inverso}{igual}{complemento}')
                valor_var2.set(valor)
            else:
                if mercado.endswith('(3-way)'):
                    mercado_var2.set('Exactly')
                    mercado_var3.set(f'T{inverso}{igual}')
                    valor_var2.set(valor)
                    valor_var3.set(valor)
                elif (valor.is_integer() or (valor - 0.25).is_integer() or (valor - 0.75).is_integer()):
                    mercado_var2.set(f'T{inverso}{igual}')
                    mercado_var3.set(f'T{inverso}{igual}')
                    valor_var2.set(arred_valor - 0.5)
                    valor_var3.set(arred_valor + 0.5)

def on_mercado_combobox2_selected(event):
    mercado = mercado_var.get()
    mercado2 = mercado_var2.get()
    mercado3 = mercado_var3.get()
    if mercado2 == 'Lay' or liability_label2.winfo_manager():
        update_columns()
    if mercado.startswith('T'):
        valor = float_error(valor_var, '')
        if valor != '':
            arred_valor = round(valor, 0)
            if len(mercado) == 2:
                igual = ''
            elif len(mercado) == 3:
                igual = mercado[2]
            else:
                igual = mercado[2]
            operacao = mercado[1]
            if operacao == 'O':
                inverso = 'U'
            else:
                inverso = 'O'
            if num_bets == 3:
                if mercado2.startswith('Exac'):
                    if valor.is_integer():
                        valor_var2.set(valor)
                    elif mercado.startswith('TO') and not valor.is_integer():
                        valor_var2.set(arred_valor)
                        mercado_var3.set(f'T{inverso}{igual}')
                        valor_var3.set(arred_valor - 0.5)
                    elif mercado.startswith('TU') and not valor.is_integer():
                        valor_var2.set(arred_valor + 1)
                        mercado_var3.set(f'T{inverso}{igual}')
                        valor_var3.set(arred_valor + 0.5)
                    elif mercado.endswith('(3-way)'):
                        valor_var2.set(valor)
                        mercado_var3.set(f'T{inverso}{igual}')
                        valor_var2.set(valor)
    elif mercado.startswith('AH'):
        valor = valor_var.get()
        arred_valor = round(valor, 0)
        igual = mercado[2]
        if igual == '1':
            oposto = '2'
        else:
            oposto = '1'
        if num_bets == 2:
            if mercado2.startswith('EH') and (valor - 0.5).is_integer():
                valor_var2.set(-(valor - 0.5))
        else:
            if mercado2 == 'X2' and valor == -0.5:
                mercado_var3.set('AH1')
                valor_var3.set(-0.25)
            elif mercado2 == '1X' and valor == -0.5:
                mercado_var3.set('AH1')
                valor_var3.set(-0.25)
    elif mercado == '1':
        if mercado2.startswith('AH'):
            valor_var2.set(0.5)
        elif mercado2.startswith('EH'):
            valor_var2.set(1)
    elif mercado == '2' and mercado2.startswith('AH'):
        if mercado2.startswith('AH'):
            valor_var2.set(0.5)
        elif mercado2.startswith('EH'):
            valor_var2.set(1)
    elif mercado == '1X' and mercado2.startswith('AH'):
        if mercado2.startswith('AH'):
            valor_var2.set(-0.5)
        elif mercado2.startswith('EH'):
            valor_var2.set(0)
    elif mercado == 'X2' and mercado2.startswith('AH'):
        if mercado2.startswith('AH'):
            valor_var2.set(-0.5)
        elif mercado2.startswith('EH'):
            valor_var2.set(0)
    elif mercado.startswith('DNB'):
        if num_bets == 2:
            if mercado2.startswith('AH'):
                valor_var2.set(0)

def on_valor2_chosen(event):
    if num_bets == 2:
        return
    else:
        return

def on_mercado_combobox3_selected(event):
    mercado = mercado_var.get()
    mercado2 = mercado_var2.get()
    mercado3 = mercado_var3.get()
    if mercado3 == 'Lay' or liability_label3.winfo_manager():
        update_columns()
    if mercado.startswith('T') and mercado2.startswith('Exac'):
        valor = valor_var.get()
        valor2 = valor_var2.get()
        valor3 = valor_var3.get()
        valor = valor_var.get()
        arred_valor = round(valor, 0)
        if len(mercado) == 2:
            igual = ''
            complemento = ''
        elif len(mercado) == 3:
            igual = mercado[2]
            complemento = ''
        else:
            igual = mercado[2]
            complemento = mercado[3:]
        operacao = mercado[1]
        if operacao == 'O':
            inverso = 'U'
        else:
            inverso = 'O'
        if valor.is_integer():
            valor_var3.set(valor)
        else:
            if mercado3.endswith('(3-way)'):
                valor_var3.set(valor2)
            else:
                if valor > valor2:
                    valor_var3.set(valor2 + 0.5)
                else:
                    valor_var3.set(valor2 - 0.5)


def show_tooltip(event, valor, valor_entry, mercado, esporte, modx=None, mody=None):
    if valor == '' and mercado == '':
        return
    global tooltip_window
    tooltip_window = Toplevel(frameApostas)
    tooltip_window.wm_overrideredirect(True)
    if modx:
        x = valor_entry.winfo_rootx() + modx
    else:
        x = valor_entry.winfo_rootx()
    if mody:
        y = valor_entry.winfo_rooty() + mody
    else:
        y = valor_entry.winfo_rooty()
    tooltip_window.wm_geometry(f"+{x}+{y}")
    mensagem = gerar_mensagem(str(mercado), valor, esporte, idioma)
    label = Label(tooltip_window, text=mensagem)
    label.pack()

def hide_tooltip(event):
    global tooltip_window
    if tooltip_window:
        tooltip_window.destroy()

# Adiciona campo Mercado
mercado_label = tk.Label(frameApostas, text=trans_config['Mercado'][idioma])
mercado_label.bind('<Enter>', lambda event: show_tooltip_simples(event, mercado_label, 'mercado'))
mercado_label.bind('<Leave>', hide_tooltip_simples)
mercado_label.grid(row=0, column=1)
mercado_combobox, mercado_var = create_combobox(frameApostas, mercado_options, row=1, column=1, width=7)
mercado_combobox.bind("<<ComboboxSelected>>", on_mercado_combobox_selected)
mercado_combobox.bind("<Enter>", lambda event: show_tooltip(event, float_error(valor_var, ''), mercado_combobox, mercado_var.get(), converter_esporte(esporte_entry.get()), mody = -45))
mercado_combobox.bind("<Leave>", hide_tooltip)

# Adiciona campo Valor
valor_entry, valor_var = create_float_entry(frameApostas, row=1, column=2, width=4, dig=3, dec=2, restrict="quarter")
valor_entry.grid_remove()
valor_entry.bind("<FocusOut>", on_valor_chosen)
tooltip_window = None
valor_entry.bind("<Enter>", lambda event: show_tooltip(event, float_error(valor_var, ''), valor_entry, mercado_var.get(), converter_esporte(esporte_entry.get()), mody = -45))
valor_entry.bind("<Leave>", hide_tooltip)

def retorna_focus(event, teste1, teste2, destino, teste3='', teste4='', destino2=''):
    if teste1.startswith(('TO', 'TU', 'AH', 'EH', 'Exac')) and float_error(teste2, '') == '':
        if teste1 == 'TOd':
            pass
        else:
            janela.after(100, destino.focus_set())
    if teste3.startswith(('TO', 'TU', 'AH', 'EH', 'Exac')) and float_error(teste4, '') == '':
        if teste3 == 'TOd':
            pass
        else:
            janela.after(100, destino2.focus_set())

# Adiciona campo Mercado2
mercado_combobox2, mercado_var2 = create_combobox(frameApostas, mercado_options, row=2, column=1, width=7)
mercado_combobox2.bind("<FocusIn>", lambda event: retorna_focus(event, mercado_var.get(), valor_var, valor_entry))
mercado_combobox2.bind("<<ComboboxSelected>>", on_mercado_combobox2_selected)
mercado_combobox2.bind("<Enter>", lambda event: show_tooltip(event, float_error(valor_var2, ''), mercado_combobox2, mercado_var2.get(), converter_esporte(esporte_entry.get()), mody = 25))
mercado_combobox2.bind("<Leave>", hide_tooltip)

# Adiciona campo Valor2
valor_entry2, valor_var2 = create_float_entry(frameApostas, row=2, column=2, width=4, dig=3, dec=2, restrict="quarter")
valor_entry2.bind("<FocusOut>", on_valor2_chosen)
valor_entry2.grid_remove()
valor_entry2.bind("<Enter>", lambda event: show_tooltip(event, float_error(valor_var2, ''), valor_entry2, mercado_var2.get(), converter_esporte(esporte_entry.get()), mody = 25))
valor_entry2.bind("<Leave>", hide_tooltip)

# Adiciona campo Mercado2
mercado_combobox3, mercado_var3 = create_combobox(frameApostas, mercado_options, row=3, column=1, width=7)
mercado_combobox3.bind("<FocusIn>", lambda event: retorna_focus(event, mercado_var2.get(), valor_var2, valor_entry2))
mercado_combobox3.grid_remove()
mercado_combobox3.bind("<<ComboboxSelected>>", on_mercado_combobox3_selected)
mercado_combobox3.bind("<Enter>", lambda event: show_tooltip(event, float_error(valor_var3, ''), mercado_combobox3, mercado_var3.get(), converter_esporte(esporte_entry.get()), mody = 25))
mercado_combobox3.bind("<Leave>", hide_tooltip)
# Adiciona campo Valor2
valor_entry3, valor_var3 = create_float_entry(frameApostas, row=3, column=2, width=4, dig=3, dec=2, restrict="quarter")
valor_entry3.grid_remove()
valor_entry3.bind("<Enter>", lambda event: show_tooltip(event, float_error(valor_var3, ''), valor_entry3, mercado_var3.get(), converter_esporte(esporte_entry.get()), mody = 25))
valor_entry3.bind("<Leave>", hide_tooltip)

def fill_empty_entry_with_zero(event):
    entry = event.widget
    if not entry.get():
        entry.delete(0, tk.END)
        entry.insert(0, "0.0")

# Adiciona campo ODD
odd_label = tk.Label(frameApostas, text=trans_graficos['Odds'][idioma].capitalize())
odd_label.bind('<Enter>', lambda event: show_tooltip_simples(event, odd_label, 'odd'))
odd_label.bind('<Leave>', hide_tooltip_simples)
odd_label.grid(row=0, column=3)
odd_entry, odd_var = create_float_entry(frameApostas, row=1, column=3, width=4, dig=3, dec=3, value=0.0, negative=False)
odd_entry.bind("<FocusIn>", lambda event: retorna_focus(event, mercado_var2.get(), valor_var2, valor_entry2, teste3=mercado_var3.get(), teste4=valor_var3, destino2=valor_entry3))
odd_entry.bind("<FocusOut>", fill_empty_entry_with_zero)
# Adiciona campo ODD2
odd_entry2, odd_var2 = create_float_entry(frameApostas, row=2, column=3, width=4, dig=3, dec=3, value=0.0, negative=False)
odd_entry2.bind("<FocusOut>", fill_empty_entry_with_zero)
# Adiciona campo ODD3
odd_entry3, odd_var3 = create_float_entry(frameApostas, row=3, column=3, width=4, dig=3, dec=3, value=0.0, negative=False)
odd_entry3.bind("<FocusOut>", fill_empty_entry_with_zero)
odd_entry3.grid_remove() # Odds

# Adiciona campo Aposta
real_label = tk.Label(frameApostas, text=cambio)
real_label.grid(row=1, column=4)

label_aposta = tk.Label(frameApostas, text=trans_jogo['valor de aposta'][idioma].capitalize())
label_aposta.bind('<Enter>', lambda event: show_tooltip_simples(event, label_aposta, 'aposta'))
label_aposta.bind('<Leave>', hide_tooltip_simples)
label_aposta.grid(row=0, column=5, padx=5, pady=5, sticky=tk.W)
aposta_entry, aposta_var = create_float_entry(frameApostas, row=1, column=5, width=5, dig=4, dec=2, value=0.0, negative=False)
aposta_entry.bind("<FocusOut>", fill_empty_entry_with_zero)
#Adicionar aposta2
real_label2 = tk.Label(frameApostas, text=cambio)
real_label2.grid(row=2, column=4)
aposta_entry2, aposta_var2 = create_float_entry(frameApostas, row=2, column=5, width=5, dig=4, dec=2, value=0.0, negative=False) # Aposta 2
aposta_entry2.bind("<FocusOut>", fill_empty_entry_with_zero)
#Adicionar aposta3
real_label3 = tk.Label(frameApostas, text=cambio)
aposta_entry3, aposta_var3 = create_float_entry(frameApostas, row=3, column=5, width=5, dig=4, dec=2, value=0.0, negative=False)
aposta_entry3.grid_remove()
aposta_entry3.bind("<FocusOut>", fill_empty_entry_with_zero)


#Adicionando cálculos
def on_variable_change(*args):
    if mercado_var.get().startswith(('TO', 'TU', 'AH', 'EH', 'Exac')):
        if mercado_var.get() == 'TOd':
            pass
        else:
            valor_entry.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
    else:
        if valor_entry.winfo_manager():
            valor_var.set('')
            valor_entry.grid_remove()
    if mercado_var2.get().startswith(('TO', 'TU', 'AH', 'EH', 'Exac')):
        if mercado_var.get() == 'TOd':
            pass
        else:
            valor_entry2.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
    else:
        if valor_entry2.winfo_manager():
            valor_var2.set('')
            valor_entry2.grid_remove()
    if mercado_var3.get().startswith(('TO', 'TU', 'AH', 'EH', 'Exac')):
        if mercado_var.get() == 'TOd':
            pass
        else:
            valor_entry3.grid(row=3, column=2, padx=5, pady=5, sticky=tk.W)
    else:
        if valor_entry3.winfo_manager():
            valor_var3.set('')
            valor_entry3.grid_remove()
    odds = [odd_var.get(), odd_var2.get(), odd_var3.get()]
    apostas = [aposta_var.get(), aposta_var2.get(), aposta_var3.get()]
    taxas = [bethouse_options.get(bethouse_var.get(), {}).get('taxa', 0.0),
             bethouse_options.get(bethouse_var2.get(), {}).get('taxa', 0.0),
             bethouse_options.get(bethouse_var3.get(), {}).get('taxa', 0.0)]

    if (len([odd for odd in odds if odd != 0.0]) == num_bets) and (len([aposta for aposta in apostas if aposta != 0.0]) >= 1):
        arred = arred_var.get()
        if arred == trans_config['Padrão'][idioma]:
            arreds = [float(bethouse_options.get(bethouse_var.get(), {}).get('arred', 0.01)),
                      float(bethouse_options.get(bethouse_var2.get(), {}).get('arred', 0.01)),
                      float(bethouse_options.get(bethouse_var3.get(), {}).get('arred', 0.01))]
        else:
            arred = float(arred)
            arreds = [arred, arred, arred]
        bonus = [bonus1.get(), bonus2.get(), bonus3.get()]
        resultado = calc_apostas(apostas[0], apostas[1], apostas[2], odds[0], odds[1], odds[2], mercado_var.get(), mercado_var2.get(), mercado_var3.get(), float_error(valor_var, 0.0), float_error(valor_var2, 0.0), float_error(valor_var3, 0.0), taxas[0], taxas[1], taxas[2], arreds, bonus)
        palpite1_label.config(text=f"{cambio} {format(round(resultado[0] ,2), '.2f')}" if resultado[0] is not None else "")
        palpite2_label.config(text=f"{cambio} {format(round(resultado[1] ,2), '.2f')}" if resultado[1] is not None else "")
        palpite3_label.config(text=f"{cambio} {format(round(resultado[2] ,2), '.2f')}" if resultado[2] is not None else "")
        lucro1_label.config(text=f"{cambio} {format(round(resultado[4] ,2), '.2f')}" if resultado[4] is not None else "", fg='seagreen' if resultado[4] > 0 else ('red' if resultado[4] < 0 else 'gray'), font=("Arial", 14, "bold"))
        lucro2_label.config(text=f"{cambio} {format(round(resultado[5] ,2), '.2f')}" if resultado[5] is not None else "", fg='seagreen' if resultado[5] > 0 else ('red' if resultado[6] < 0 else 'gray'), font=("Arial", 14, "bold"))
        lucro3_label.config(text=f"{cambio} {format(round(resultado[6] ,2), '.2f')}" if resultado[6] is not None else "", fg='seagreen' if resultado[6] > 0 else ('red' if resultado[7] < 0 else 'gray'), font=("Arial", 14, "bold"))
        liability_label1.config(text=f"{cambio} {format(round(resultado[3] ,2), '.2f')}" if resultado[3] is not None else "")
        liability_label2.config(text=f"{cambio} {format(round(resultado[8] ,2), '.2f')}" if resultado[8] is not None else "")
        liability_label3.config(text=f"{cambio} {format(round(resultado[9], 2), '.2f')}" if resultado[9] is not None else "")
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
        liability_label3.config(text="")
        lucro_percent_label1.config(text="")

def on_label_click(bonus_var, combobox):
    if bonus_var.get():
        if combobox.get() in bethouse_options.keys():
            response = messagebox.askyesno(trans_jogo['Bônus'][idioma], f"{trans_jogo['Desativar Bônus'][idioma]} {combobox.get()}?")
            if response:
                bonus_var.set(False)
    else:
        if combobox.get() in bethouse_options.keys():
            response = messagebox.askyesno(trans_jogo['Bônus'][idioma], f"{trans_jogo['Ativar Bônus'][idioma]} {combobox.get()}?")
            if response:
                bonus_var.set(True)
bonus1 = tk.BooleanVar(value=False)
bonus2 = tk.BooleanVar(value=False)
bonus3 = tk.BooleanVar(value=False)

#Palpites
palpite_label = tk.Label(frameApostas, text=trans_jogo['Palpite'][idioma])
palpite_label.bind('<Enter>', lambda event: show_tooltip_simples(event, palpite_label, 'surebets'))
palpite_label.bind('<Leave>', hide_tooltip_simples)
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
liability_label = tk.Label(frameApostas, text=trans_jogo['Liability'][idioma])
liability_label.bind('<Enter>', lambda event: show_tooltip_simples(event, liability_label, 'liability'))
liability_label.bind('<Leave>', hide_tooltip_simples)
liability_label1 = tk.Label(frameApostas, text='')
liability_label2 = tk.Label(frameApostas, text='')
liability_label3 = tk.Label(frameApostas, text='')
lucro_label = tk.Label(frameApostas, text=trans_jogo['Lucro'][idioma])
lucro_label.bind('<Enter>', lambda event: show_tooltip_simples(event, lucro_label, 'lucro'))
lucro_label.bind('<Leave>', hide_tooltip_simples)
lucro_label.grid(row=0, column=7, padx=5, pady=5, sticky=tk.W)
lucro1_label = tk.Label(frameApostas, text="")
lucro1_label.grid(row=1, column=7)
lucro1_label.bind("<Button-1>", lambda event: on_label_click(bonus1, bethouse_combobox))
lucro2_label = tk.Label(frameApostas, text="")
lucro2_label.grid(row=2, column=7)
lucro2_label.bind("<Button-1>", lambda event: on_label_click(bonus2, bethouse_combobox2))
lucro3_label = tk.Label(frameApostas, text="")
lucro3_label.bind("<Button-1>", lambda event: on_label_click(bonus3, bethouse_combobox3))
lucro_percent_label = tk.Label(frameApostas, text=f"{trans_jogo['Lucro'][idioma]} %")
lucro_percent_label.bind('<Enter>', lambda event: show_tooltip_simples(event, lucro_percent_label, 'lucro_per'))
lucro_percent_label.bind('<Leave>', hide_tooltip_simples)
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
    mercados = [mercado_var.get(), mercado_var2.get(), mercado_var3.get()]
    if any(x == 'Lay' for x in mercados):
        liability_label.grid(row=0, column=7, padx=5, pady=5, sticky=tk.W)
        lucro_label.grid(row=0, column=8, padx=5, pady=5, sticky=tk.W)
        lucro1_label.grid(row=1, column=8)
        lucro2_label.grid(row=2, column=8)
        if num_bets == 3:
            lucro3_label.grid(row=3, column=8)
        lucro_percent_label.grid(row=0, column=9, padx=5, pady=5, sticky=tk.W)
        lucro_percent_label1.grid(row=1, column=9, rowspan=2)
        liability_labels = [liability_label1, liability_label2, liability_label3]
        for i, mercado in enumerate(mercados):
            if mercado == "Lay":
                liability_labels[i].grid(row=i + 1, column=7, padx=5, pady=5, sticky=tk.W)
            else:
                liability_labels[i].grid_remove()
    else:
        liability_label.grid_forget()
        lucro_label.grid(row=0, column=7, padx=5, pady=5, sticky=tk.W)
        lucro1_label.grid(row=1, column=7)
        lucro2_label.grid(row=2, column=7)
        if num_bets == 3:
            lucro3_label.grid(row=3, column=7)
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
    update_columns()
    valor_entry.configure(fg='black', bg='systemWindowBody')
    odd_entry.configure(fg='black', bg='systemWindowBody')
    aposta_entry.configure(fg='black', bg='systemWindowBody')
    valor_entry2.configure(fg='black', bg='systemWindowBody')
    odd_entry2.configure(fg='black', bg='systemWindowBody')
    aposta_entry2.configure(fg='black', bg='systemWindowBody')
    valor_entry3.configure(fg='black', bg='systemWindowBody')
    odd_entry3.configure(fg='black', bg='systemWindowBody')
    aposta_entry3.configure(fg='black', bg='systemWindowBody')
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

    def change_not(mercado, outro_mercado, outro_mercado2=None):
        if mercado == 'Not':
            if outro_mercado.startswith(('Clear', 'Remo', 'Score', 'Win', 'Q')):
                return f'Not {outro_mercado}'
            elif outro_mercado.startswith('TO') or outro_mercado == 'Lay':
                return 'Not ScoreBoth'
            if outro_mercado2 is not None:
                if outro_mercado2.startswith(('Clear', 'Remo', 'Score', 'Win', 'Q')):
                    return f'Not {outro_mercado2}'
                elif outro_mercado2.startswith('TO'):
                    return 'Not ScoreBoth'
        else:
            return mercado


    if (len([odd for odd in odds if odd != 0.0]) >= 2)\
            and (len([aposta for aposta in apostas if aposta != 0.0]) >= 1)\
            and time_casa != "" and time_fora != ""\
            and (bethouse_combobox.get() in bethouse_options.keys())\
            and (bethouse_combobox2.get() in bethouse_options.keys())\
            and ((num_bets != 3) or (num_bets == 3 and bethouse_combobox3.get() in bethouse_options.keys())):
        mercados = [mercado_combobox.get(), mercado_combobox2.get(), (mercado_combobox3.get() if mercado_combobox3.get() != '' else None)]
        hoje = datetime.today().strftime('%Y-%m-%d')
        bet_hoje = c.execute(f"SELECT COUNT(*) FROM apostas WHERE DATE(data_entrada) = DATE('{hoje}')").fetchone()[0]
        dados = {
            'id': f"{datetime.now().strftime('%Y%m%d')}{str(bet_hoje).zfill(3)}",
            'data_entrada': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data_jogo': datetime.strptime(f"{ano_combobox.get()}-{convert_mes(mes_combobox.get()):02}-{int(dia_entry.get()):02} {int(hora_entry.get()):02}:{int(minuto_entry.get()):02}:00", '%Y-%m-%d %H:%M:%S'),
            'time_casa': time_casa,
            'time_fora': time_fora,
            'bethouse1': bethouse_combobox.get(),
            'mercado1': change_not(mercados[0], mercados[1], mercados[2]),
            'valor1': float_error(valor_entry, None),
            'odd1': odd_entry.get(),
            'aposta1': palpite1_label.cget("text").replace(cambio, "").strip(),
            'resultado1': None,
            'bethouse2': bethouse_combobox2.get(),
            'mercado2': change_not(mercados[1], mercados[0], mercados[2]),
            'valor2': float_error(valor_entry2, None),
            'odd2': odd_entry2.get(),
            'aposta2': palpite2_label.cget("text").replace(cambio, "").strip(),
            'resultado2': None,
            'bethouse3': bethouse_combobox3.get() if bethouse_combobox3.get() != '' else None,
            'mercado3': change_not(mercados[2], mercados[0], mercados[1]) if mercados[2] != '' else None,
            'valor3': float_error(valor_entry3, None),
            'odd3': odd_entry3.get() if odd_entry3.get() != '' else None,
            'aposta3': palpite3_label.cget("text").replace(f"{cambio} ", "").strip() if palpite3_label.cget("text").replace(f"{cambio} ", "").strip() != '' else None,
            'resultado3': None,
            'lucro_estimado': round((float(lucro1_label.cget("text").replace(f"{cambio} ", "").strip()) + float(lucro2_label.cget("text").replace(f"{cambio} ", "").strip()) + (float(lucro3_label.cget("text").replace(f"{cambio} ", "").strip()) if mercado_combobox3.get() in bethouse_options.keys() else 0)) / (3 if mercado_combobox3.get() in bethouse_options.keys() else 2), 2),
            'lucro_per_estimado': float(lucro_percent_label1.cget("text").strip("%")) / 100,
            'lucro_real': None,
            'lucro_per_real': None,
            'esporte': converter_esporte(esporte_entry.get().split(". ")[0])
        }
        # Gravação dos dados na tabela e atualização da Treeview
        dados = {k: str(v) if isinstance(v, datetime) else v if isinstance(v, float) else v if isinstance(v, int) else convert_to_numeric(v).strip().split('\n')[0] if isinstance(v, str) and '\n' in v else convert_to_numeric(v) for k, v in dados.items()}

        bethouse_list = {valor for valor in [dados['bethouse1'], dados['bethouse2'], dados['bethouse3']] if valor}

        save_apostas(dados, conn)
        update_lucro_diario()
        resetar_variaveis()
        preencher_treeview(conn, tabela, bethouse_options, situation_vars, order_button1, order_button2, time_button, timeframe_combobox, search_var, frameTabela, frameSaldos, idioma, cambio, linhas_bethouses, bethouse_list=bethouse_list)

    else:
        messagebox.showwarning(trans_config['Aviso'][idioma], trans_jogo['Preencha o jogo'][idioma])

gravar_button = tk.Button(frameGravar, text=trans_jogo['Gravar'][idioma], command=gravar)
gravar_button.grid(row=0, column=0)
clear_button = tk.Button(frameGravar, text=trans_jogo['Limpar'][idioma], command=resetar_variaveis)
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
        valor_entry3.insert(0, row['valor3'] if (row['valor3'] is not None and row['valor3'] != '') else '')
        odd_entry3.delete(0, 'end')
        odd_entry3.insert(0, row['odd3'])
        aposta_var3.set(row['aposta3'])
    bethouse_combobox.set(row['bethouse1'])
    bethouse_combobox2.set(row['bethouse2'])
    mercado_combobox.set(row['mercado1'])
    mercado_combobox2.set(row['mercado2'])
    valor_entry.delete(0, 'end')
    valor_entry.insert(0, row['valor1'] if (row['valor1'] is not None and row['valor1'] != '') else '')
    valor_entry2.delete(0, 'end')
    valor_entry2.insert(0, row['valor2'] if (row['valor2'] is not None and row['valor2'] != '') else '')
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
        df_filtrado.loc[mask, 'valor1'] = valor_entry.get() if (valor_entry.get() is not None and valor_entry.get() != '') else None
        df_filtrado.loc[mask, 'valor2'] = valor_entry2.get() if (valor_entry2.get() is not None and valor_entry2.get() != '') else None
        df_filtrado.loc[mask, 'valor3'] = valor_entry3.get() if (valor_entry3.get() is not None and valor_entry3.get() != '') else None
        df_filtrado.loc[mask, 'odd1'] = odd_entry.get()
        df_filtrado.loc[mask, 'odd2'] = odd_entry2.get()
        df_filtrado.loc[mask, 'odd3'] = odd_entry3.get() if odd_entry3.get() != '' else None
        df_filtrado.loc[mask, 'aposta1'] = palpite1_label.cget("text").replace(f"{cambio} ", "").strip()
        df_filtrado.loc[mask, 'aposta2'] = palpite2_label.cget("text").replace(f"{cambio} ", "").strip()
        df_filtrado.loc[mask, 'aposta3'] = palpite3_label.cget("text").replace(f"{cambio} ", "").strip() if mercado_combobox3.get() != '' else None
        df_filtrado.loc[mask, 'lucro_estimado'] = round(float(lucro1_label.cget("text").replace(f"{cambio} ", "").strip()), 2)
        df_filtrado.loc[mask, 'lucro_per_estimado'] = round(float(lucro_percent_label1.cget("text").strip("%")), 4)
        df_filtrado.loc[mask, 'esporte'] = esporte_entry.get() if esporte_entry.get() != '' else None

        # Salvar dados na dabela e atualização do Trewwview
        linha = df_filtrado.loc[mask].replace('\n', '', regex=True).to_dict('records')[0]

        bethouse_list = {valor for valor in [linha['bethouse1'], linha['bethouse2'], linha['bethouse3']] if valor}

        save_apostas(linha, conn, tipo='e', linha_antiga=bethouses_antigas)

        # Limpar as variáveis e atualizar a tabela
        update_lucro_diario()
        preencher_treeview(conn, tabela, bethouse_options, situation_vars, order_button1, order_button2, time_button, timeframe_combobox, search_var, frameTabela, frameSaldos, idioma, cambio, linhas_bethouses, bethouse_list=bethouse_list)
        resetar_variaveis()

    # Botão Editar
    edit_button = tk.Button(frameGravar, text=trans_jogo['Editar'][idioma], command=editar_bets, foreground="red")
    edit_button.grid(row=0, column=2)

# Definir estilo para o Treeview
style = ttk.Style()
style.configure("Treeview", rowheight=60)

# Criar o Treeview com as colunas desejadas
tabela = BetHistTreeview(frameTabela, situation_vars, order_button1, order_button2, time_button, timeframe_combobox, search_var, frameTabela, frameSaldos, idioma, cambio, linhas_bethouses, conn, columns=("index", "adds", "jogo", "data", "resultados", "bethouses", "odds", "bets", "mercados", "id"), show="headings", style="Treeview", height=linhas_apostas)
tabela.heading("index", text="")
tabela.heading("adds", text=trans_filtros['Adição'][idioma].capitalize())
tabela.heading("jogo", text=trans_jogo['Times'][idioma].capitalize())
tabela.heading("data", text=trans_graficos['dia'][idioma].capitalize())
tabela.heading("resultados", text=trans_jogo['W/L'][idioma].upper())
tabela.heading("bethouses", text=trans_config['BetHouses'][idioma].capitalize())
tabela.heading("odds", text=trans_graficos['Odds'][idioma].capitalize())
tabela.heading("bets", text=trans_graficos['apostas'][idioma].capitalize())
tabela.heading("mercados", text=trans_config['Mercados'][idioma].capitalize())
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
    preencher_treeview(conn, tabela, bethouse_options, situation_vars, order_button1, order_button2, time_button, timeframe_combobox, search_var, frameTabela, frameSaldos, idioma, cambio, linhas_bethouses)

# inicia o loop da janela
janela.mainloop()