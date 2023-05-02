import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from tkintertable import TableCanvas, TableModel
import datetime
from datetime import datetime, timedelta, date
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
def fechar_programa():
    # Verifica se houve alteração nos resultados
    if not df_resultados.equals(df_resultados_copy):
        # Exibe caixa de diálogo para confirmar a gravação
        resposta = messagebox.askquestion("Salvar Alterações", "Deseja salvar as alterações dos resultados?")

        if resposta == "yes":
            # Salva as alterações no arquivo Apostas.csv
            df_tabela.update(df_filtrado.loc[:, df_filtrado.columns != 'add'])
            df_tabela.to_csv('Apostas.csv', index=False)

    # Fecha o programa
    janela.destroy()

janela = ThemedTk(theme="marine")
janela.protocol("WM_DELETE_WINDOW", fechar_programa)

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
        colunas = ["id", "add", "time_casa", "time_fora", "dia", "mes", "mes_id", "ano", "hora", "minuto", "bethouse1", "mercado1", "valor1", "odd1", "aposta1", "resultado1", "bethouse2", "mercado2", "valor2", "odd2", "aposta2", "resultado2", "bethouse3", "mercado3", "valor3", "odd3", "aposta3", "resultado3", "lucro_estimado", "lucro_per_estimado", "lucroReal", "lucro_perReal"]
        csv.writer(f).writerow(colunas)

df_tabela = pd.read_csv("Apostas.csv")
df_filtrado = df_tabela.copy()
df_resultados_copy = df_tabela[["resultado1", "resultado2", "resultado3"]].copy()
df_resultados = df_tabela[["resultado1", "resultado2", "resultado3"]] # Configurações iniciais

# Filtros
def toggle_order():
    current_order = order_button["text"]
    if current_order == "Crescente de Datas":
        order_button["text"] = "Decrescente de Datas"
    elif current_order == "Decrescente de Datas":
        order_button["text"] = "Crescente de Adição"
    elif current_order == "Crescente de Adição":
        order_button["text"] = "Decrescente de Adição"
    else:
        order_button["text"] = "Crescente de Datas"
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
    df_filtrado = filter_selection()
    save_bethouse_options()

ordem_label = tk.Label(frameTabela, text="Ordem:")
ordem_label.grid(row=0, column=0)

order_button = tk.Button(frameTabela, text="Crescente de Datas", command=toggle_order)
order_button.grid(row=0, column=1)

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
    situation_frame.place(x=379, y=0)
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


def preencher_treeview():
    # Limpar o conteúdo atual do Treeview
    tabela.delete(*tabela.get_children())

    # Configurar cores de fundo alternadas para as linhas
    tabela.tag_configure("linha_par", background="#F0F0F0")
    tabela.tag_configure("linha_impar", background="white")

    # Preencher o Treeview com os dados do arquivo
    for i, row in df_filtrado.iterrows():
        ID = row['id']
        jogo = f"{row['time_casa']}\n{row['time_fora']}"
        data = "{:02d} / {}\n{:02d}:{:02d}".format(int(row['dia']), (row['mes']), int(row['hora']), int(row['minuto']))
        bethouses = "{}({} × R$ {:.2f})\n{}({} × R$ {:.2f})".format(row['bethouse1'], float(row['odd1']), float(row['aposta1']),row['bethouse2'], float(row['odd2']), float(row['aposta2']))
        if pd.notna(row['bethouse3']) and row['bethouse3'] in bethouse_options.keys():
            bethouses += "\n{}({} × R$ {:.2f})".format(row['bethouse3'], float(row['odd3']), float(row['aposta3']))

        # Add alternating background colors to rows
        if i % 2 == 0:
            tabela.insert("", "end", values=(ID, jogo, data, bethouses), tags=("linha_par",))
        else:
            tabela.insert("", "end", values=(ID, jogo, data, bethouses), tags=("linha_impar",))

def load_options():
    global bethouse_options, mercado_options, arred_var
    try:
        with open('bethouse_options.json', 'r') as f:
            data = json.load(f)
            bethouse_options = data.get("bethouse_options", {})
            mercado_options = data.get("mercado_options", [])
            arred_var = tk.DoubleVar(value=data.get("arredondamento"))
            filtros = data.get("filtros", {})
            order_text = filtros.get("ordem", "Crescente de Datas")
            time_text = filtros.get("time", "Feitas desde")
            timeframe_text = filtros.get("timeframe", "hoje")
            selected_situations = filtros.get("situations", [])
            return order_text, time_text, timeframe_text, selected_situations
    except FileNotFoundError:
        bethouse_options = {}
        mercado_options = []
        arred_var = tk.DoubleVar(value=0.01)
        order_text = "Crescente de Datas"
        time_text = "Feitas desde"
        timeframe_text = "hoje"
        selected_situations = []
        return order_text, time_text, timeframe_text, selected_situations


order_text, time_text, timeframe_text, selected_situations = load_options()
order_button["text"] = order_text
time_button["text"] = time_text
timeframe_combobox.set(timeframe_text)
if len(selected_situations) != len(situation_vars):
    print("Erro: O tamanho das listas selected_situations e situation_vars é diferente")
else:
    for i, var in enumerate(situation_vars):
        var.set(selected_situations[i]) # Configurações de usuário

def filter_selection():
    global df_filtrado
    # Cria uma cópia do dataframe para não modificar o original
    df_filtrado = df_tabela.copy()
    df_filtrado = df_filtrado.rename(columns={'ano': 'year', 'mes_id': 'month', 'dia': 'day', 'hora': 'hour', 'minuto': 'minute'})
    df_filtrado['datetime'] = pd.to_datetime(df_filtrado[['year', 'month', 'day', 'hour', 'minute']])
    # Cria máscaras booleanas para cada situação
    mask_vencidas = ((df_filtrado['resultado1'].isna() | df_filtrado['resultado2'].isna()) & ((df_filtrado['bethouse3'].notna() & (df_filtrado['resultado1'].isna() | df_filtrado['resultado2'].isna() | df_filtrado[ 'resultado3'].isna())) | (df_filtrado['bethouse3'].isna())) & (df_filtrado['datetime'].apply(lambda x: x + timedelta(hours=2)) < datetime.now()))

    mask_abertas = ((df_filtrado['resultado1'].isna() | df_filtrado['resultado2'].isna()) & ((df_filtrado['bethouse3'].notna() & (df_filtrado['resultado1'].isna() | df_filtrado['resultado2'].isna() | df_filtrado[ 'resultado3'].isna())) | (df_filtrado['bethouse3'].isna())))

    mask_fechadas = ((df_filtrado['resultado1'].notna() & df_filtrado['resultado2'].notna()) & ((df_filtrado['bethouse3'].notna() & df_filtrado['resultado3'].notna()) | (df_filtrado['bethouse3'].isna())))

    # Aplica as máscaras de acordo com as opções selecionadas pelo usuário
    if situation_vars[0].get() and situation_vars[1].get() and situation_vars[2].get():
        pass
    elif situation_vars[0].get() and situation_vars[1].get():
        df_filtrado = df_filtrado[mask_vencidas | mask_abertas]
    elif situation_vars[0].get() and situation_vars[2].get():
        df_filtrado = df_filtrado[mask_vencidas | mask_fechadas]
    elif situation_vars[1].get() and situation_vars[2].get():
        df_filtrado = df_filtrado[mask_abertas | mask_fechadas]
    elif situation_vars[0].get():
        df_filtrado = df_filtrado[mask_vencidas]
    elif situation_vars[1].get():
        df_filtrado = df_filtrado[mask_abertas]
    elif situation_vars[2].get():
        df_filtrado = df_filtrado[mask_fechadas]
    df_filtrado = df_filtrado.rename(columns={'year': 'ano', 'month': 'mes_id', 'day': 'dia', 'hour': 'hora', 'minute': 'minuto'})

    # Ordenação
    if order_button["text"] == "Crescente de Datas":
        df_filtrado = df_filtrado.sort_values(by=['ano', 'mes_id', 'dia', 'hora', 'minuto'])
    elif order_button["text"] == "Decrescente de Datas":
        df_filtrado = df_filtrado.sort_values(by=['ano', 'mes_id', 'dia', 'hora', 'minuto'], ascending=False)
    elif order_button["text"] == "Crescente de Adição":
        df_filtrado = df_filtrado.sort_values(by=['id'])
    elif order_button["text"] == "Decrescente de Adição":
        df_filtrado = df_filtrado.sort_values(by=['id'], ascending=False)

    # Filtro de tempo
    df_filtrado['add'] = pd.to_datetime(df_filtrado['add'])
    if time_button["text"] == "Vencem até":
        if timeframe_combobox.get() == "hoje":
            df_filtrado = df_filtrado[
                (df_filtrado['dia'] == datetime.now().day) &
                (df_filtrado['mes_id'] == datetime.now().month) &
                (df_filtrado['ano'] == datetime.now().replace(hour=0, minute=0).year)]
        elif timeframe_combobox.get() == "amanhã":
            end_date = datetime.now().replace(hour=0, minute=0) + timedelta(days=1)
            df_filtrado = df_filtrado[
                (df_filtrado['dia'] <= end_date.day) & (df_filtrado['mes_id'] <= end_date.month) & (
                        df_filtrado['ano'] <= end_date.year)]
        elif timeframe_combobox.get() == "1 semana":
            end_date = datetime.now().replace(hour=0, minute=0) + timedelta(weeks=1)
            df_filtrado = df_filtrado[(df_filtrado['dia'] <= end_date.day) & (df_filtrado['mes_id'] <= end_date.month) & (
                        df_filtrado['ano'] <= end_date.year)]
        elif timeframe_combobox.get() == "1 mês":
            end_date = datetime.now().replace(hour=0, minute=0) + timedelta(days=30)
            df_filtrado = df_filtrado[(df_filtrado['dia'] <= end_date.day) & (df_filtrado['mes_id'] <= end_date.month) & (
                        df_filtrado['ano'] <= end_date.year)]
    else:
        if timeframe_combobox.get() == "hoje":
            df_filtrado = df_filtrado[(df_filtrado['add'] >= datetime.now().replace(hour=0, minute=0))]
        elif timeframe_combobox.get() == "ontem":
            df_filtrado = df_filtrado[(df_filtrado['add'] >= datetime.now().replace(hour=0, minute=0) - pd.DateOffset(days=1))]
        elif timeframe_combobox.get() == "1 semana":
            df_filtrado = df_filtrado[(df_filtrado['add'] >= datetime.now().replace(hour=0, minute=0) - pd.DateOffset(weeks=1))]
        elif timeframe_combobox.get() == "1 mês":
            df_filtrado = df_filtrado[(df_filtrado['add'] >= datetime.now().replace(day=1, hour=0, minute=0))]
        elif timeframe_combobox.get() == "30 dias":
            df_filtrado = df_filtrado[(df_filtrado['add'] >= datetime.now().replace(hour=0, minute=0) - pd.DateOffset(days=30))]
        elif timeframe_combobox.get() == "6 meses":
            df_filtrado = df_filtrado[(df_filtrado['add'] >= datetime.now().replace(hour=0, minute=0) - pd.DateOffset(months=6))]
        elif timeframe_combobox.get() == "esse ano":
            df_filtrado = df_filtrado[(df_filtrado['add'] >= datetime.now().replace(day=1, month=1, hour=0, minute=0))]
        elif timeframe_combobox.get() == "365 dias":
            df_filtrado = df_filtrado[(df_filtrado['add'] <= datetime.now().replace(hour=0, minute=0) - pd.DateOffset(year=1))]

    preencher_treeview()
    # Exibir o resultado
    return df_filtrado

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
    add_bethouse_button.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

    # Cria a lista de BetHouses
    configStyle = ttk.Style()
    configStyle.configure("Normal.Treeview", rowheight=20)
    bethouses_list = sorted(bethouse_options.keys())
    bethouses_tree = ttk.Treeview(bethouses_frame, columns=('Bethouse', 'Taxa'), show='headings', style="Normal.Treeview")
    bethouses_tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
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
    remove_bethouse_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

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
    new_mercado_entry.grid(row=2, column=4, padx=5, pady=5)

    # Cria um botão para adicionar a nova opção de mercado
    add_mercado_button = tk.Button(bethouses_frame, text="Adicionar", command=add_mercado_option)
    add_mercado_button.grid(row=3, column=3, columnspan=2, padx=5, pady=5)

    # Cria a lista de opções de mercado
    mercado_options_list = sorted(list(mercado_options), key=lambda x: x[0])
    # Adiciona as BetHouses à Listbox
    mercado_options_listbox = tk.Listbox(bethouses_frame)
    mercado_options_listbox.grid(row=4, column=3, columnspan=2, padx=5, pady=5)
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
    remove_mercado_button.grid(row=5, column=3, columnspan=2, padx=5, pady=5)

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
            "ordem": order_button["text"],
            "time": time_button["text"],
            "timeframe": timeframe_combobox.get(),
            "situations": [var.get() for var in situation_vars]
        }
    }
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
opcoes_anos = [datetime.now().date().year - 1, datetime.now().date().year, datetime.now().date().year + 1]
ano_var = tk.StringVar(value=datetime.now().year)
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
dia_atual = datetime.now().day
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
mes_atual = datetime.now().strftime('%b')
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
minuto_entry.grid(row=2, column=7, padx=5, pady=5, sticky=tk.W) # Data


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
        bethouse_combobox.current(0)  # Seleciona a primeira opção
        bethouse_combobox.event_generate("<<ComboboxSelected>>")  # Gera o evento ComboboxSelected

def on_select1(value):
    selected_bethouse = bethouse_var.get()
    text_color = bethouse_options[selected_bethouse]['text_color']
    background_color = bethouse_options[selected_bethouse]['background_color']
    valor_entry.configure(fg=text_color, bg=background_color)
    odd_entry.configure(fg=text_color, bg=background_color)
    aposta_entry.configure(fg=text_color, bg=background_color)
    #frameApostas.configure(bg=bethouse_options.get(bethouse_var.get(), {}).get('background_color', None))

bethouse_label = tk.Label(frameApostas, text="BetHouse")
bethouse_label.grid(row=1, column=9)
bethouse_var = tk.StringVar(value=None)
bethouse_combobox = ttk.Combobox(frameApostas, textvariable=bethouse_var, values=list(bethouse_options.keys()), width=7)
bethouse_combobox.bind("<KeyRelease>", update_bethouse_combobox)
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
        bethouse_combobox2.current(0)  # Seleciona a primeira opção
        bethouse_combobox2.event_generate("<<ComboboxSelected>>")  # Gera o evento ComboboxSelected

def on_select2(value):
    selected_bethouse = bethouse_var2.get()
    text_color = bethouse_options[selected_bethouse]['text_color']
    background_color = bethouse_options[selected_bethouse]['background_color']
    valor_entry2.configure(fg=text_color, bg=background_color)
    odd_entry2.configure(fg=text_color, bg=background_color)
    aposta_entry2.configure(fg=text_color, bg=background_color)
bethouse_var2 = tk.StringVar(value=None)
bethouse_combobox2 = ttk.Combobox(frameApostas, textvariable=bethouse_var2, values=list(bethouse_options.keys()), width=7)
bethouse_combobox2.bind("<KeyRelease>", update_bethouse_combobox2)
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
        bethouse_combobox3.current(0)  # Seleciona a primeira opção
        bethouse_combobox3.event_generate("<<ComboboxSelected>>")  # Gera o evento ComboboxSelected


def on_select3(value):
    selected_bethouse = bethouse_var3.get()
    text_color = bethouse_options[selected_bethouse]['text_color']
    background_color = bethouse_options[selected_bethouse]['background_color']
    valor_entry3.configure(fg=text_color, bg=background_color)
    odd_entry3.configure(fg=text_color, bg=background_color)
    aposta_entry3.configure(fg=text_color, bg=background_color)
bethouse_var3 = tk.StringVar(value=None)
bethouse_combobox3 = ttk.Combobox(frameApostas, textvariable=bethouse_var3, values=list(bethouse_options.keys()), width=7)
bethouse_combobox3.bind("<KeyRelease>", update_bethouse_combobox3) # BetHouse 3
bethouse_combobox3.bind("<<ComboboxSelected>>", on_select3) # BetHouses

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
    if P == '-':
        return True
    if P[0] == '-':
        P = P[1:]
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
valor_entry3.bind("<KeyRelease>", lambda event: on_entry_change_valor3(valor_entry3)) # Mercados

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
        entry.icursor(len(current_text)) # Odds

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
    return aposta1, aposta2, aposta3, liability, lucro1, lucro2, lucro3, lucro_percent # Cálculos

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
    global df_tabela, df_filtrado
    odds = [odd_var.get(), odd_var2.get(), odd_var3.get()]
    apostas = [aposta_var.get(), aposta_var2.get(), aposta_var3.get()]

    if (len([odd for odd in odds if odd != 0.0]) >= 2)\
            and (len([aposta for aposta in apostas if aposta != 0.0]) >= 1)\
            and jogo_entry != ""\
            and (bethouse_combobox.get() in bethouse_options.keys())\
            and (bethouse_combobox2.get() in bethouse_options.keys())\
            and ((num_bets != 3) or (num_bets == 3 and bethouse_combobox3.get() in bethouse_options.keys())):
        mes_id_map = {'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4, 'mai': 5, 'jun': 6, 'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11, 'dez': 12}
        dados = {
            'id': len(df_tabela) + 1,
            'add': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'time_casa': jogo_entry.get().split(" - ")[0],
            'time_fora': jogo_entry.get().split(" - ")[1],
            'dia': dia_entry.get(),
            'mes': mes_combobox.get(),
            'mes_id': mes_id_map[mes_combobox.get().lower()],
            'ano': ano_combobox.get(),
            'hora': hora_entry.get(),
            'minuto': minuto_entry.get(),
            'bethouse1': bethouse_combobox.get(),
            'mercado1': mercado_combobox.get(),
            'valor1': valor_entry.get(),
            'odd1': odd_entry.get(),
            'aposta1': palpite1_label.cget("text").replace("R$", "").strip() if aposta_var.get() == 0.0 or aposta_var.get() == "" else aposta_var.get(),
            'resultado1': "",
            'bethouse2': bethouse_combobox2.get(),
            'mercado2': mercado_combobox2.get(),
            'valor2': valor_entry2.get(),
            'odd2': odd_entry2.get(),
            'aposta2': palpite2_label.cget("text").replace("R$", "").strip() if aposta_var2.get() == 0.0 or aposta_var2.get() == "" else aposta_var2.get(),
            'resultado2': "",
            'bethouse3': bethouse_combobox3.get(),
            'mercado3': mercado_combobox3.get(),
            'valor3': valor_entry3.get(),
            'odd3': odd_entry3.get(),
            'aposta3': palpite3_label.cget("text").replace("R$", "").strip() if aposta_var3.get() == 0.0 or aposta_var3.get() == "" else aposta_var3.get(),
            'resultado3': ""
        }

        # Gravação dos dados no arquivo CSV
        with open("Apostas.csv", "a", newline="") as f:
            csv.writer(f).writerow(dados.values())
        df_tabela = pd.read_csv("Apostas.csv")
        resetar_variaveis()
        filter_selection()
        preencher_treeview()
    else:
        messagebox.showwarning("Aviso", "Preencha o jogo, as BetHouses, as odds e uma aposta.")

gravar_button = tk.Button(frameGravar, text="Gravar", command=gravar)
gravar_button.grid(row=0, column=0)
clear_button = tk.Button(frameGravar, text="Limpar", command=resetar_variaveis)
clear_button.grid(row=0, column=1) # Gravar

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

    # Buscar as informações da linha correspondente ao ID no DataFrame df_filtrado
    row = df_filtrado[df_filtrado['id'] == id_selecionado].iloc[0]

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

    def editar_bets():
        # Obter o item selecionado na tabela
        item_id = tabela.focus()
        item_values = tabela.item(item_id)['values']

        # Obter o ID da linha selecionada
        id_selecionado = item_values[0]  # Índice 0 corresponde ao campo 'ID'

        # Atualizar os valores da linha correspondente no DataFrame df_filtrado
        mask = df_filtrado['id'] == id_selecionado
        df_filtrado.loc[mask, 'add'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df_filtrado.loc[mask, 'time_casa'] = jogo_entry.get().split(" - ")[0]
        df_filtrado.loc[mask, 'time_fora'] = jogo_entry.get().split(" - ")[1]
        df_filtrado.loc[mask, 'dia'] = dia_entry.get()
        df_filtrado.loc[mask, 'mes'] = mes_combobox.get()
        df_filtrado.loc[mask, 'ano'] = ano_combobox.get()
        df_filtrado.loc[mask, 'hora'] = hora_entry.get()
        df_filtrado.loc[mask, 'minuto'] = minuto_entry.get()
        df_filtrado.loc[mask, 'bethouse1'] = bethouse_combobox.get()
        df_filtrado.loc[mask, 'bethouse2'] = bethouse_combobox2.get()
        df_filtrado.loc[mask, 'bethouse3'] = bethouse_combobox3.get()
        df_filtrado.loc[mask, 'mercado1'] = mercado_combobox.get()
        df_filtrado.loc[mask, 'mercado2'] = mercado_combobox2.get()
        df_filtrado.loc[mask, 'mercado3'] = mercado_combobox3.get()
        df_filtrado.loc[mask, 'valor1'] = valor_entry.get()
        df_filtrado.loc[mask, 'valor2'] = valor_entry2.get()
        df_filtrado.loc[mask, 'valor3'] = valor_entry3.get()
        df_filtrado.loc[mask, 'odd1'] = odd_entry.get()
        df_filtrado.loc[mask, 'odd2'] = odd_entry2.get()
        df_filtrado.loc[mask, 'odd3'] = odd_entry3.get()
        if float(df_filtrado.loc[mask, 'aposta1']) == 0.0:
            df_filtrado.loc[mask, 'aposta1'] = palpite1_label.cget("text").replace("R$", "").strip()
        else:
            df_filtrado.loc[mask, 'aposta1'] = aposta_var.get()
        if float(df_filtrado.loc[mask, 'aposta2']) == 0.0:
            df_filtrado.loc[mask, 'aposta2'] = palpite2_label.cget("text").replace("R$", "").strip()
        else:
            df_filtrado.loc[mask, 'aposta2'] = aposta_var2.get()
        if float(df_filtrado.loc[mask, 'aposta3']) == 0.0:
            df_filtrado.loc[mask, 'aposta3'] = palpite3_label.cget("text").replace("R$", "").strip()
        else:
            df_filtrado.loc[mask, 'aposta3'] = aposta_var3.get()

        # Salvar o DataFrame atualizado no arquivo Apostas.csv
        df_tabela.update(df_filtrado.loc[:, df_filtrado.columns != 'add'])
        df_tabela.to_csv("Apostas.csv", index=False)

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
        self.bind("<Button-2>", self.on_click)
        self.canvas = Canvas(self, width=200, height=40)
        self.canvas.bind("<Button-1>", self.on_canvas_click)  # Bind the on_canvas_click method to the <Button-1> event of the Canvas widget
        self.icons = ["",
                      PhotoImage(file="win.png").subsample(13, 13),
                      PhotoImage(file="loss.png").subsample(13, 13),
                      PhotoImage(file="return.png").subsample(13, 13),
                      PhotoImage(file="half-win.png").subsample(13, 13),
                      PhotoImage(file="half-loss.png").subsample(13, 13)]
        self.iconSave = PhotoImage(file="save.png").subsample(18, 18)
        self.current_icons = {}
        self.clicked_row = None

    def update_icons(self, df_filtrado):
        for row in self.get_children():
            item = self.item(row)
            id = item['values'][0]
            df_row = df_filtrado.loc[df_filtrado['id'] == id]
            for i in range(1, 4):
                resultado = df_row[f'resultado{i}'].values[0]
                icon = self.get_icon_from_result(resultado)
                self.set(row, f'icon{i}', icon)

    def get_icon_from_result(self, resultado):
        # Aqui você pode definir o mapeamento de resultados para ícones
        if resultado == 'win':
            return self.icons[1]
        elif resultado == 'loss':
            return self.icons[2]
        elif resultado == 'return':
            return self.icons[3]
        elif resultado == 'half-win':
            return self.icons[4]
        elif resultado == 'half-loss':
            return self.icons[5]
        else:
            return self.icons[0]

    def on_click(self, event):
        row = self.identify_row(event.y)
        column = self.identify_column(event.x)
        item = self.item(row)  # Get the item data for the clicked row
        id = item['values'][0]
        df_row = df_filtrado.loc[df_filtrado['id'] == id]
        icons = []
        for i in range(1, 4):
            resultado = df_row[f'resultado{i}'].values[0]
            icon = self.get_icon_from_result(resultado)
            icons.append(icon)

        x, y = event.x, event.y
        self.canvas.place(x=x, y=y)
        self.canvas.delete("all")  # Clear the canvas
        bg_color1 = bethouse_options[df_row['bethouse1'].values[0]]['background_color']
        fg_color1 = bethouse_options[df_row['bethouse1'].values[0]]['text_color']
        bg_color2 = bethouse_options[df_row['bethouse2'].values[0]]['background_color']
        fg_color2 = bethouse_options[df_row['bethouse2'].values[0]]['text_color']
        self.canvas.create_rectangle(30, 0, 200, 20, fill=bg_color1)
        self.canvas.create_rectangle(30, 40, 200, 20, fill=bg_color2)
        self.canvas.create_image(0, 0, image=icons[0], anchor=NW, tags='imagem')
        self.canvas.create_text(30, 10, text=item['values'][3].split("\n")[0], anchor=W, fill=fg_color1)
        self.canvas.create_image(0, 20, image=icons[1], anchor=NW, tags='imagem')
        self.canvas.create_text(30, 30, text=item['values'][3].split("\n")[1], anchor=W, fill=fg_color2)

        if len(item['values'][3].split("\n")) > 2:  # Check the value of bethouse3
            self.canvas.config(height=80)  # Increase the height of the canvas
            bg_color3 = bethouse_options[df_row['bethouse3'].values[0]]['background_color']
            fg_color3 = bethouse_options[df_row['bethouse3'].values[0]]['text_color']
            self.canvas.create_rectangle(30, 60, 200, 40, fill=bg_color3)
            self.canvas.create_image(0, 40, image=icons[2], anchor=NW, tags='imagem')  # Create the third icon
            self.canvas.create_text(30, 50, text=item['values'][3].split("\n")[2], anchor=W, fill=fg_color3)
            self.canvas.create_image(0, 60, image=self.iconSave, anchor=NW, tags='imagem')
            self.canvas.create_text(30, 70, text="Salvar Resultados", anchor=W)
        else:
            self.canvas.config(height=60)  # Set the height of the canvas back to 40
            self.canvas.create_image(0, 40, image=self.iconSave, anchor=NW, tags='imagem')
            self.canvas.create_text(30, 50, text="Salvar Resultados", anchor=W)

        self.clicked_row = row  # Store the clicked row
        self.master.bind_all("<Button-1>", self.on_master_click)

    def on_master_click(self, event):
        if event.widget == self.canvas or self.canvas.winfo_containing(event.x_root, event.y_root) == self.canvas:
            return
        self.canvas.place_forget()
        self.master.unbind_all("<Button-1>")

    def on_canvas_click(self, event):
        global df_resultados
        def save_results():
            id = item['values'][0]
            df_row = df_filtrado.loc[df_filtrado['id'] == id]
            if pd.isna(df_row['resultado1'].values[0]) or pd.isna(df_row['resultado2'].values[0]) or (len(item['values'][3].split("\n")) > 2 and pd.isna(df_row['resultado3'].values[0])):
                messagebox.showinfo("Aviso", "Preencha todos os resultados do jogo!")
            else:
                def calculate_fator_resultado(resultado, odd):
                    if resultado == 'win':
                        return 1
                    elif resultado == 'loss':
                        return 0
                    elif resultado == 'half-win':
                        return (odd + 1) / (2 * odd)
                    elif resultado == 'half-loss':
                        return 1 / (2 * odd)
                    elif resultado == 'return':
                        return 1 / odd
                    else:
                        return 0

                #print(pd.notna(df_row['aposta2'].values[0])) #in bethouse_options.keys()
                somaApostas = df_row['aposta1'].values[0] + df_row['aposta2'].values[0] + (df_row['aposta3'].values[0] if df_row['bethouse3'].values[0] in bethouse_options.keys() else 0)
                retorno1 = round(df_row['aposta1'].values[0] * df_row['odd1'].values[0] * calculate_fator_resultado(df_row['resultado1'].values[0], df_row['odd1'].values[0]), 2)
                retorno2 = round(df_row['aposta2'].values[0] * df_row['odd2'].values[0] * calculate_fator_resultado(df_row['resultado2'].values[0], df_row['odd2'].values[0]), 2)
                retorno3 = round(df_row['aposta3'].values[0] * df_row['odd3'].values[0] * calculate_fator_resultado(df_row['resultado3'].values[0], df_row['odd3'].values[0]) if df_row['bethouse3'].values[0] in bethouse_options.keys() else 0, 2)
                somaRetornos = round(retorno1 + retorno2 + retorno3, 2)
                lucroReal =  round(somaRetornos - somaApostas, 2)
                lucro_perReal = lucroReal / somaApostas
                print(lucroReal, lucro_perReal)
                df_filtrado.loc[df_filtrado['id'] == id, 'lucroReal'] = lucroReal
                df_filtrado.loc[df_filtrado['id'] == id, 'lucro_perReal'] = lucro_perReal
                df_tabela.update(df_filtrado.loc[:, df_filtrado.columns != 'add'])
                df_tabela.to_csv('Apostas.csv', index=False)
                filter_selection()
                preencher_treeview()
                self.canvas.place_forget()
                def show_message(title, message):
                    popup = tk.Toplevel()
                    popup.title(title)
                    tk.Label(popup, text=message).pack()
                    popup.after(2000, popup.destroy)

                show_message("Aviso", "Resultados salvos com sucesso!")

        row = self.clicked_row  # Get the clicked row
        item = self.item(row)  # Get the item data for the clicked row
        id = item['values'][0]
        df_row = df_filtrado.loc[df_filtrado['id'] == id]
        if event.y <= 20:
            # The first icon was clicked
            resultado = df_row['resultado1'].values[0]
            if pd.isna(resultado):
                next_resultado = self.get_next_result('')
            else:
                next_resultado = self.get_next_result(resultado)
            df_filtrado.loc[df_filtrado['id'] == id, 'resultado1'] = next_resultado
            icon1 = self.get_icon_from_result(next_resultado)
            resultado = df_row['resultado2'].values[0]
            icon2 = self.get_icon_from_result(resultado)
            if len(item['values'][3].split("\n")) > 2:
                resultado = df_row['resultado3'].values[0]
                icon3 = self.get_icon_from_result(resultado)
            self.canvas.delete('imagem')  # Clear the canvas
            self.canvas.create_image(0, 0, image=icon1, anchor=NW, tags='imagem')
            self.canvas.create_image(0, 20, image=icon2, anchor=NW, tags='imagem')

            if len(item['values'][3].split("\n")) > 2:  # Check the value of bethouse3
                self.canvas.create_image(0, 40, image=icon3, anchor=NW, tags='imagem')  # Create the third icon
                self.canvas.create_image(0, 60, image=self.iconSave, anchor=NW)
            else:
                self.canvas.create_image(0, 40, image=self.iconSave, anchor=NW)
        elif event.y <= 40:
            # The second icon was clicked
            resultado = df_row['resultado2'].values[0]
            if pd.isna(resultado):
                next_resultado = self.get_next_result('')
            else:
                next_resultado = self.get_next_result(resultado)
            df_filtrado.loc[df_filtrado['id'] == id, 'resultado2'] = next_resultado
            icon1 = self.get_icon_from_result(df_row['resultado1'].values[0])
            icon2 = self.get_icon_from_result(next_resultado)
            if len(item['values'][3].split("\n")) > 2:
                resultado = df_row['resultado3'].values[0]
                icon3 = self.get_icon_from_result(resultado)
            self.canvas.delete("imagem")  # Clear the canvas
            self.canvas.create_image(0, 0, image=icon1, anchor=NW, tags='imagem')
            self.canvas.create_image(0, 20, image=icon2, anchor=NW, tags='imagem')

            if len(item['values'][3].split("\n")) > 2:  # Check the value of bethouse3
                self.canvas.create_image(0, 40, image=icon3, anchor=NW, tags='imagem')  # Create the third icon
                self.canvas.create_image(0, 60, image=self.iconSave, anchor=NW)
            else:
                self.canvas.create_image(0, 40, image=self.iconSave, anchor=NW)
        elif event.y <= 60:
            # The third icon was clicked
            if not pd.isna(df_row['bethouse3'].values[0]):
                resultado = df_row['resultado3'].values[0]
                if pd.isna(resultado):
                    next_resultado = self.get_next_result('')
                else:
                    next_resultado = self.get_next_result(resultado)
                df_filtrado.loc[df_filtrado['id'] == id, 'resultado3'] = next_resultado
                icon3 = self.get_icon_from_result(next_resultado)
            else:
                icon3 = None
            icon1 = self.get_icon_from_result(df_row['resultado1'].values[0])
            icon2 = self.get_icon_from_result(df_row['resultado2'].values[0])
            self.canvas.delete("imagem")  # Clear the canvas
            self.canvas.create_image(0, 0, image=icon1, anchor=NW, tags='imagem')
            self.canvas.create_image(0, 20, image=icon2, anchor=NW, tags='imagem')
            if len(item['values'][3].split("\n")) > 2:  # Check the value of bethouse3
                self.canvas.create_image(0, 40, image=icon3, anchor=NW, tags='imagem')  # Create the third icon
                self.canvas.create_image(0, 60, image=self.iconSave, anchor=NW)
            else:
                self.canvas.create_image(0, 40, image=self.iconSave, anchor=NW)
                save_results()
        else:
            save_results()
        df_resultados = df_filtrado[["resultado1", "resultado2", "resultado3"]]
    def get_next_result(self, resultado):
        # Aqui você pode definir a ordem dos resultados
        resultados = ['', 'win', 'loss', 'return', 'half-win', 'half-loss']
        index = resultados.index(resultado)
        next_index = (index + 1) % len(resultados)
        return resultados[next_index]


# Definir estilo para o Treeview
style = ttk.Style()
style.configure("Treeview", rowheight=60)

# Criar o Treeview com as colunas desejadas
tabela = MyTreeview(frameTabela, columns=("ID", "jogo", "data", "betHouses"), show="headings", style="Treeview")
tabela.heading("ID", text="ID")
tabela.heading("jogo", text="Jogo")
tabela.heading("data", text="Data")
tabela.heading("betHouses", text="BetHouses")
tabela.column("ID", width=30)
tabela.column("jogo", width=130)
tabela.column("data", width=70)
tabela.column("betHouses", width=150)
tabela.grid(row=2, column=0, columnspan=10, rowspan= 10)
tabela.bind('<Double-Button-1>', select_bets) # Tabela
filter_selection()

# Chamar a função para preencher o Treeview
if len(tabela.get_children()) == 0:
    preencher_treeview()

#––––––––––––––––––––––––––––––––––––––# ESTATÍSTICA #––––––––––––––––––––––––––––––––––––––


# inicia o loop da janela
janela.mainloop()