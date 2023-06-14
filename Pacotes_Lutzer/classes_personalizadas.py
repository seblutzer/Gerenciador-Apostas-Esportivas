import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
import datetime
from datetime import datetime, timedelta
import pandas as pd
from Pacotes_Lutzer.convert import convert_mes, convert_dia
from Pacotes_Lutzer.validate import validate_num, on_entry_change
import os
import re
import numpy as np
import sqlite3
from pandastable import Table
import webbrowser

global contador
contador = 0
def import_df_filtrado():
    return df_filtrado
def preencher_treeview(conn, tabela, options, situation_vars, order_button1, order_button2, time_button, timeframe_combobox, search_var, frameTabela, frameSaldos, bethouse_list=None):
    global bethouse_options, df_filtrado
    bethouse_options = options

    # Montar a consulta SQL com base nas variáveis de situação e filtro
    query = filter_selection(conn, situation_vars, order_button1, order_button2, time_button, timeframe_combobox, search_var, frameTabela)
    # Executar a consulta SQL e obter o resultado como DataFrame
    df_filtrado = pd.read_sql_query(query, conn)

    # Limpar o conteúdo atual do Treeview
    tabela.delete(*tabela.get_children())

    # Configurar cores de fundo alternadas para as linhas
    tabela.tag_configure("linha_par", background="#F0F0F0")
    tabela.tag_configure("linha_impar", background="white")
    index = 1

    # Preencher o Treeview com os dados do arquivo
    for i, row in df_filtrado.iterrows():
        id = row['id']
        jogo = f"{row['time_casa']}\n{row['time_fora']}"
        data_jogo = datetime.strptime(row['data_jogo'], '%Y-%m-%d %H:%M:%S')
        data = "  {}\n{:02d}/{}\n {:02d}:{:02d}".format(convert_dia(data_jogo.strftime('%a')), data_jogo.day,
                                                      convert_mes(data_jogo.month), data_jogo.hour, data_jogo.minute)

        def show_results(resultados):
            if resultados == "win":
                return "W"
            elif resultados == "loss":
                return "L"
            elif resultados == "return":
                return "X"
            elif resultados == "half-win":
                return "HW"
            elif resultados == "half-loss":
                return "HL"
            else:
                return ""

        resultados = f"{show_results(row['resultado1'])}\n{show_results(row['resultado2'])}"
        if pd.notna(row['bethouse3']) and row['bethouse3'] in bethouse_options.keys():
            resultados += f"\n{show_results(row['resultado3'])}"
        bethouses = f"{row['bethouse1']}\n{row['bethouse2']}"
        if pd.notna(row['bethouse3']) and row['bethouse3'] in bethouse_options.keys():
            bethouses += f"\n{row['bethouse3']}"
        odds = "{:.3f}".format(float(row['odd1'])).rstrip('0').rstrip('.') + "\n{:.3f}".format(
            float(row['odd2'])).rstrip('0').rstrip('.')
        if pd.notna(row['bethouse3']) and row['bethouse3'] in bethouse_options.keys():
            odds += "\n{:.3f}".format(float(row['odd3'])).rstrip('0').rstrip('.')
        apostas = f"R$ {float(row['aposta1']):.2f}" if isinstance(float(row['aposta1']), (float, int)) else f"\nR$ 0.00"
        apostas += f"\nR$ {float(row['aposta2']):.2f}" if isinstance(float(row['aposta2']),
                                                                     (float, int)) else f"\nR$ 0.00"
        if pd.notna(row['bethouse3']) and row['bethouse3'] in bethouse_options.keys():
            apostas += f"\nR$ {float(row['aposta3']):.2f}" if isinstance(float(row['aposta3']), (float, int)) else ""
        mercados = str(row['mercado1'])
        if pd.notna(row['valor1']):
            valor1 = float(row['valor1'])
            if isinstance(valor1, (int, float)):
                mercados += "({:.2f}".format(valor1).rstrip('0').rstrip('.') + ")"
            else:
                mercados += valor1
        mercados += f"\n{str(row['mercado2'])}"
        if pd.notna(row['valor2']):
            valor2 = float(row['valor2'])
            if isinstance(valor2, (int, float)):
                mercados += "({:.2f}".format(valor2).rstrip('0').rstrip('.') + ")"
            else:
                mercados += valor2
        if pd.notna(row['bethouse3']) and row['bethouse3'] in bethouse_options.keys():
            mercados += f"\n{str(row['mercado3'])}"
            if pd.notna(row['valor3']):
                valor3 = float(row['valor3'])
                if isinstance(valor3, (int, float)):
                    mercados += "({:.2f}".format(valor3).rstrip('0').rstrip('.') + ")"
                else:
                    mercados += valor3
        data_entrada = datetime.strptime(row['data_entrada'], '%Y-%m-%d %H:%M:%S')
        adds = "{:02d}/{}".format(data_entrada.day, convert_mes(data_entrada.month))

        # Add alternating background colors to rows
        if index % 2 == 0:
            tabela.insert("", "end",
                          values=(index, adds, jogo, data, resultados, bethouses, odds, apostas, mercados, id),
                          tags=("linha_par",))
        else:
            tabela.insert("", "end",
                          values=(index, adds, jogo, data, resultados, bethouses, odds, apostas, mercados, id),
                          tags=("linha_impar",))
        index += 1

    if bethouse_list == set():
        pass
    else:
        tabela_bethouses(frameSaldos, conn, bethouse_list=bethouse_list)

def filter_selection(conn, situation_vars, order_button1, order_button2, time_button, timeframe_combobox, search_var, frameTabela):
    global contador, frame_vencidas
    contador += 1 if contador < 2 else 0

    # Aplicar os filtros diretamente na consulta SQL
    query = "SELECT * FROM apostas WHERE "
    data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    aberta = "((bethouse3 IS NULL AND (resultado1 IS NULL OR resultado2 IS NULL)) OR (bethouse3 IS NOT NULL AND (resultado1 IS NULL OR resultado2 IS NULL OR resultado3 IS NULL)))"
    vencida = f"{aberta} AND data_jogo <= datetime('{data}', '-2 hour')" #horário UTC, então precisa de acrescer -3 para o nosso fuso.
    fechada = "((bethouse3 IS NULL AND resultado1 IS NOT NULL AND resultado2 IS NOT NULL) OR (bethouse3 IS NOT NULL AND resultado1 IS NOT NULL AND resultado2 IS NOT NULL AND resultado3 IS NOT NULL))"
    if all(situation_vars[i].get() for i in [1, 2]) or not any(situation_vars[i].get() for i in [0, 1, 2]):
        query += "1 = 1"  # Nenhum filtro aplicado
    elif situation_vars[0].get() and situation_vars[2].get():
        query += f"{vencida} OR {fechada}"
    elif situation_vars[0].get():
        query += vencida
    elif situation_vars[1].get():
        query += aberta
    elif situation_vars[2].get():
        query += fechada

    count_query = f"SELECT COUNT(*) FROM apostas WHERE {vencida}"
    c = conn.cursor()
    c.execute(count_query)
    result = c.fetchone()
    num_vencidas = result[0]

    # Filtro de tempo
    if time_button["text"] == "Vencem até":
        if timeframe_combobox.get() == "hoje":
            query += f" AND (DATE(data_jogo) = DATE('{data}'))"
        elif timeframe_combobox.get() == "amanhã":
            query += f" AND (DATE(data_jogo) <= DATE('{data}', '+1 day'))"
        elif timeframe_combobox.get() == "1 semana":
            query += f" AND (DATE(data_jogo) <= DATE('{data}', 'weekday 0', '+7 days'))"
        elif timeframe_combobox.get() == "1 mês":
            query += f" AND (DATE(data_jogo) <= DATE('{data}', 'start of month', '+31 days'))"
    else:
        if timeframe_combobox.get() == "hoje":
            query += f" AND (DATE(data_entrada) >= DATE('{data}'))"
        elif timeframe_combobox.get() == "ontem":
            query += f" AND (DATE(data_entrada) >= DATE('{data}', '-1 day'))"
        elif timeframe_combobox.get() == "1 semana":
            query += f" AND (DATE(data_entrada) >= DATE('{data}', 'weekday 0', '-7 days'))"
        elif timeframe_combobox.get() == "1 mês":
            query += f" AND (DATE(data_entrada) >= DATE('{data}', 'start of month'))"
        elif timeframe_combobox.get() == "30 dias":
            query += f" AND (DATE(data_entrada) >= DATE('{data}', '-30 day'))"
        elif timeframe_combobox.get() == "6 meses":
            query += f" AND (DATE(data_entrada) >= DATE('{data}', '-6 month'))"
        elif timeframe_combobox.get() == "esse ano":
            query += f" AND (DATE(data_entrada) >= DATE('{data}', 'start of year'))"
        elif timeframe_combobox.get() == "365 dias":
            query += f" AND (DATE(data_entrada) <= DATE('{data}', '-1 year'))"

    if search_var.get() == '':
        pass
    else:
        # Obtém a palavra-chave da variável de controle
        palavra_chave = search_var.get()
        # Adiciona o filtro de pesquisa aos campos desejados
        query += f" AND (id LIKE '%{palavra_chave}%' OR data_entrada LIKE '%{palavra_chave}%' OR data_jogo LIKE '%{palavra_chave}%' OR time_casa LIKE '%{palavra_chave}%' OR time_fora LIKE '%{palavra_chave}%' OR bethouse1 LIKE '%{palavra_chave}%' OR mercado1 LIKE '%{palavra_chave}%' OR valor1 LIKE '%{palavra_chave}%' OR odd1 LIKE '%{palavra_chave}%' OR aposta1 LIKE '%{palavra_chave}%' OR bethouse2 LIKE '%{palavra_chave}%' OR mercado2 LIKE '%{palavra_chave}%' OR valor2 LIKE '%{palavra_chave}%' OR odd2 LIKE '%{palavra_chave}%' OR aposta2 LIKE '%{palavra_chave}%' OR bethouse3 LIKE '%{palavra_chave}%' OR mercado3 LIKE '%{palavra_chave}%' OR valor3 LIKE '%{palavra_chave}%' OR odd3 LIKE '%{palavra_chave}%' OR aposta3 LIKE '%{palavra_chave}%' OR esporte LIKE '%{palavra_chave}%')"

    # Ordenação
    if order_button1["text"] == "Crescente" and order_button2["text"] == "Data":
        query += " ORDER BY data_jogo ASC"
    elif order_button1["text"] == "Decrescente" and order_button2["text"] == "Data":
        query += " ORDER BY data_jogo DESC"
    elif order_button1["text"] == "Crescente" and order_button2["text"] == "Adição":
        query += " ORDER BY id ASC"
    else:  # Decrescente e Adição
        query += " ORDER BY id DESC"

    if contador == 1:
        frame_vencidas = tk.Canvas(frameTabela, width=16, height=16, highlightthickness=0)
        frame_vencidas.create_oval(0, 0, 15, 15, fill="red", tags='frame')
        frame_vencidas.create_text(8, 8, text=num_vencidas, fill="white", font=("Arial", 12, "bold"),tags=('count', 'frame'))
        frame_vencidas.place(x=412, y=0)
    if num_vencidas > 0:
        if not frame_vencidas.winfo_viewable():
            frame_vencidas.place(x=412, y=0)
        frame_vencidas.itemconfigure('count', text=num_vencidas)
    else:
        frame_vencidas.place_forget()


    #if num_vencidas > 0:
    #    frame_vencidas.itemconfigure('count', text=num_vencidas)
    #else:
    #    frame_vencidas.delete('frame')
    #    frame_vencidas.place_forget()

    # Exibir o resultado
    return query

class BetHistTreeview(ttk.Treeview):
    def __init__(self, master=None, situation_vars=None, order_button1=None, order_button2=None, time_button=None, timeframe_combobox=None, search_var=None, frameTabela=None, frameSaldos=None, conn=None, **kw):
        ttk.Treeview.__init__(self, master, **kw)
        self.situation_vars = situation_vars
        self.order_button1 = order_button1
        self.order_button2 = order_button2
        self.time_button = time_button
        self.timeframe_combobox = timeframe_combobox
        self.conn = conn
        self.search_var = search_var
        self.frameTabela = frameTabela
        self.frameSaldos = frameSaldos
        self.bind("<<TreeviewSelect>>", self.on_select)
        self.canvas1 = Canvas(self, width=300, height=40, bg="#b3d7fe", highlightthickness=0) #bg="#b3d7fe"
        image = PhotoImage(file='save.png').subsample(10, 10)
        self.save = Label(self, image=image, bg="#b3d7fe", highlightthickness=0)
        self.save.image = image
        self.save.bind("<Button-1>", self.on_save_click)
        self.canvas1.bind("<Button-1>", self.on_canvas_click)  # Bind the on_canvas_click method to the <Button-1> event of the Canvas widget
        self.icons = ["",
                      PhotoImage(file="win.png").subsample(13, 13),
                      PhotoImage(file="loss.png").subsample(13, 13),
                      PhotoImage(file="return.png").subsample(13, 13),
                      PhotoImage(file="half-win.png").subsample(13, 13),
                      PhotoImage(file="half-loss.png").subsample(13, 13)]
        self.iconSave = PhotoImage(file="save.png").subsample(18, 18)
        self.current_icons = {}
        self.clicked_row = None

    def update_icons(self):
        for row in self.get_children():
            item = self.item(row)
            id = item['values'][9]
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

    def on_select(self, event):
        global bethouse_options
        selected_item = self.focus()
        item = self.item(selected_item)  # Get the item data for the clicked row
        id = item['values'][9]
        df_row = df_filtrado.loc[df_filtrado['id'] == id]
        icons = []
        for i in range(1, 4):
            resultado = df_row[f'resultado{i}'].values[0]
            icon = self.get_icon_from_result(resultado)
            icons.append(icon)

        x = 255 #event.x
        x_save = 20
        y = self.bbox(selected_item)[1]  # Get the y-coordinate of the top of the row
        self.canvas1.place(x=x, y=y)
        self.canvas1.delete("all")
        self.save.place(x=x_save, y=y+3)

        bg_color1 = bethouse_options[df_row['bethouse1'].values[0]]['background_color']
        fg_color1 = bethouse_options[df_row['bethouse1'].values[0]]['text_color']
        bg_color2 = bethouse_options[df_row['bethouse2'].values[0]]['background_color']
        fg_color2 = bethouse_options[df_row['bethouse2'].values[0]]['text_color']
        self.canvas1.create_rectangle(28, 20, 300, 0, fill=bg_color1)
        self.canvas1.create_image(0, 0, image=icons[0], anchor=NW, tags='imagem')
        self.canvas1.create_text(28, 10, text=df_row['bethouse1'].values[0], anchor = W, fill = fg_color1)
        self.canvas1.create_text(100, 10, text=df_row['odd1'].values[0], anchor = W, fill = fg_color1)
        self.canvas1.create_text(150, 10, text=f"R$ {float(df_row['aposta1'].values[0]):.2f}", anchor = W, fill = fg_color1)
        formatted_valor1 = "" if pd.isna(df_row['valor1'].values[0]) or df_row['valor1'].values[0] == '' else "(" + f"{float(df_row['valor1'].values[0]):.2f}".rstrip('0').rstrip('.') + ")"
        self.canvas1.create_text(219, 10, text="{}{}".format(df_row['mercado1'].values[0], formatted_valor1), anchor=W, fill=fg_color1)
        self.canvas1.create_rectangle(28, 40, 300, 20, fill=bg_color2)
        self.canvas1.create_image(0, 20, image=icons[1], anchor=NW, tags='imagem')
        self.canvas1.create_text(28, 30, text=df_row['bethouse2'].values[0], anchor=W, fill=fg_color2)
        self.canvas1.create_text(100, 30, text=df_row['odd2'].values[0], anchor=W, fill=fg_color2)
        self.canvas1.create_text(150, 30, text=f"R$ {float(df_row['aposta2'].values[0]):.2f}", anchor=W, fill=fg_color2)
        formatted_valor2 = "" if pd.isna(df_row['valor2'].values[0]) or df_row['valor1'].values[0] == '' else "(" + f"{float(df_row['valor2'].values[0]):.2f}".rstrip('0').rstrip('.') + ")"
        self.canvas1.create_text(219, 30, text="{}{}".format(df_row['mercado2'].values[0], formatted_valor2), anchor=W, fill=fg_color2)

        if df_row['bethouse3'].values[0] in bethouse_options.keys():  # Check the value of bethouse3
            self.canvas1.config(height=60)  # Increase the height of the canvas
            bg_color3 = bethouse_options[df_row['bethouse3'].values[0]]['background_color']
            fg_color3 = bethouse_options[df_row['bethouse3'].values[0]]['text_color']
            self.canvas1.create_rectangle(28, 60, 300, 40, fill=bg_color3)
            self.canvas1.create_image(0, 40, image=icons[2], anchor=NW, tags='imagem')  # Create the third icon
            self.canvas1.create_text(28, 50, text=df_row['bethouse3'].values[0], anchor=W, fill=fg_color3)
            self.canvas1.create_text(100, 50, text=df_row['odd3'].values[0], anchor=W, fill=fg_color3)
            self.canvas1.create_text(150, 50, text=f"R$ {float(df_row['aposta3'].values[0]):.2f}", anchor=W, fill=fg_color3)
            formatted_valor3 = "" if pd.isna(df_row['valor3'].values[0]) or df_row['valor1'].values[0] == '' else "(" + f"{float(df_row['valor3'].values[0]):.2f}".rstrip('0').rstrip('.') + ")"
            self.canvas1.create_text(219, 50, text="{}{}".format(df_row['mercado3'].values[0], f"{formatted_valor3}" if pd.notna(df_row['valor3'].values[0]) else ""),anchor=W, fill=fg_color3)
        else:
            self.canvas1.config(height=40)
            self.canvas1.place(x=x, y=y+10)
        self.clicked_row = selected_item  # Store the clicked row
        self.master.bind_all("<Button-1>", self.on_master_click)

    def on_master_click(self, event):
        if event.widget == self.canvas1 or self.canvas1.winfo_containing(event.x_root, event.y_root) == self.canvas1:
            return
        self.canvas1.place_forget()
        self.save.place_forget()
        self.master.unbind_all("<Button-1>")

    def on_canvas_click(self, event):
        global df_resultados, bethouse_options
        selected_item = self.focus()
        item = self.item(selected_item)  # Get the item data for the clicked row
        id = item['values'][9]
        df_row = df_filtrado.loc[df_filtrado['id'] == id]
        if event.y <= 20:
            if event.x <= 30:
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
                if df_row['bethouse3'].values[0] in bethouse_options.keys():
                    resultado = df_row['resultado3'].values[0]
                    icon3 = self.get_icon_from_result(resultado)
                self.canvas1.delete('imagem')  # Clear the canvas
                self.canvas1.create_image(0, 0, image=icon1, anchor=NW, tags='imagem')
                self.canvas1.create_image(0, 19, image=icon2, anchor=NW, tags='imagem')

                if df_row['bethouse3'].values[0] in bethouse_options.keys():  # Check the value of bethouse3
                    self.canvas1.create_image(0, 38, image=icon3, anchor=NW, tags='imagem')  # Create the third icon
            else:
                url = bethouse_options[df_row['bethouse1'].values[0]]['html']['link']
                navegador = bethouse_options[df_row['bethouse1'].values[0]]['html']['navegador']
                if navegador == 'sistema':
                    webbrowser.open(url)
                else:
                    browser = webbrowser.get(navegador)
                    browser.open(url)

        elif event.y <= 40:
            if event.x <= 30:
                # The second icon was clicked
                resultado = df_row['resultado2'].values[0]
                if pd.isna(resultado):
                    next_resultado = self.get_next_result('')
                else:
                    next_resultado = self.get_next_result(resultado)
                df_filtrado.loc[df_filtrado['id'] == id, 'resultado2'] = next_resultado
                icon1 = self.get_icon_from_result(df_row['resultado1'].values[0])
                icon2 = self.get_icon_from_result(next_resultado)
                if df_row['bethouse3'].values[0] in bethouse_options.keys():
                    resultado = df_row['resultado3'].values[0]
                    icon3 = self.get_icon_from_result(resultado)
                self.canvas1.delete("imagem")  # Clear the canvas
                self.canvas1.create_image(0, 0, image=icon1, anchor=NW, tags='imagem')
                self.canvas1.create_image(0, 19, image=icon2, anchor=NW, tags='imagem')

                if df_row['bethouse3'].values[0] in bethouse_options.keys():  # Check the value of bethouse3
                    self.canvas1.create_image(0, 38, image=icon3, anchor=NW, tags='imagem')  # Create the third icon
            else:
                url = bethouse_options[df_row['bethouse2'].values[0]]['html']['link']
                navegador = bethouse_options[df_row['bethouse2'].values[0]]['html']['navegador']
                if navegador == 'sistema':
                    webbrowser.open(url)
                else:
                    browser = webbrowser.get(navegador)
                    browser.open(url)

        elif event.y <= 60:
            if event.x <= 30:
                # The third icon was clicked
                if df_row['bethouse3'].values[0] in bethouse_options.keys():
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
                self.canvas1.delete("imagem")
                self.canvas1.create_image(0, 0, image=icon1, anchor=NW, tags='imagem')
                self.canvas1.create_image(0, 19, image=icon2, anchor=NW, tags='imagem')
                if df_row['bethouse3'].values[0] in bethouse_options.keys():  # Check the value of bethouse3
                    self.canvas1.create_image(0, 38, image=icon3, anchor=NW, tags='imagem')  # Create the third icon
            else:
                if df_row['bethouse3'].values[0] in bethouse_options.keys():
                    url = bethouse_options[df_row['bethouse3'].values[0]]['html']['link']
                    navegador = bethouse_options[df_row['bethouse3'].values[0]]['html']['navegador']
                    if navegador == 'sistema':
                        webbrowser.open(url)
                    else:
                        browser = webbrowser.get(navegador)
                        browser.open(url)

    def on_save_click(self, event):
        global df_resultados
        selected_item = self.focus()
        item = self.item(selected_item)
        id = item['values'][9]
        df_row = df_filtrado.loc[df_filtrado['id'] == id]

        def save_results():
            global bethouse_options
            c = self.conn.cursor()
            if pd.isna(df_row['resultado1'].values[0]) or pd.isna(df_row['resultado2'].values[0]) or (
                    len(item['values'][5].split("\n")) > 2 and pd.isna(df_row['resultado3'].values[0])):
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
                odd = {}  # Dicionários para armazenar os valores calculados
                retornos = []
                for i in range(1, 4 if df_row['bethouse3'].values[0] in bethouse_options.keys() else 3):
                    if df_row[f'mercado{i}'].values[0] == "Lay":
                        odd[i] = (float(df_row[f'odd{i}'].values[0]) / (float(df_row[f'odd{i}'].values[0]) - 1) - 1) * (1 - float(bethouse_options[df_row[f'bethouse{i}'].values[0]]['taxa'])) + 1
                    else:
                        odd[i] = (float(df_row[f'odd{i}'].values[0]) - 1) * (1 - float(bethouse_options[df_row[f'bethouse{i}'].values[0]]['taxa'])) + 1
                    if f'aposta{i}' in df_row.columns and f'resultado{i}' in df_row.columns:
                        retorno = round(float(df_row[f'aposta{i}'].values[0]) * odd[i] * calculate_fator_resultado(df_row[f'resultado{i}'].values[0], odd[i]) - float(df_row[f'aposta{i}'].values[0]), 2)
                        retornos.append(retorno)
                somaApostas = float(df_row['aposta1'].values[0]) + float(df_row['aposta2'].values[0]) + (float(df_row['aposta3'].values[0]) if df_row['bethouse3'].values[0] in bethouse_options.keys() else 0)
                lucro_real = round(sum(retornos), 2)
                lucro_per_real = round(lucro_real / somaApostas, 4)
                bethouse_list = {valor for valor in [df_row['bethouse1'].values[0], df_row['bethouse2'].values[0],df_row['bethouse3'].values[0]] if valor}

                # Atualizar a linha correspondente na tabela apostas do dados.db
                query = f'''
                UPDATE apostas
                SET lucro_real = {lucro_real}, 
                    lucro_per_real = {lucro_per_real},
                    resultado1 = '{df_row['resultado1'].values[0]}', 
                    resultado2 = '{df_row['resultado2'].values[0]}',
                    resultado3 = '{df_row['resultado3'].values[0]}'
                WHERE id = {df_row['id'].values[0]}
                '''
                c.execute(query)

                for i in range(1, 4 if df_row['bethouse3'].values[0] in bethouse_options.keys() else 3):
                    bethouse_key = df_row[f'bethouse{i}'].values[0]
                    resultado = df_row[f'resultado{i}'].values[0]
                    # Modificar o nome da tabela substituindo caracteres não permitidos por sublinhado (_)
                    table_name = f"{bethouse_key}_saldos"
                    table_name = re.sub(r'\W+', '_', table_name)
                    if table_name[0].isdigit():
                        table_name = f'_{table_name}'
                    # Atualizar a linha correspondente na tabela {bethouse}_saldos do dados.db
                    query = f'''
                    UPDATE "{table_name}"
                    SET resultado = '{resultado}', 
                        balanco = {retornos[i-1]}, 
                        dif_real = {retornos[i-1]}
                    WHERE id = {df_row['id'].values[0]} AND 
                        odd = {str(df_row[f'odd{i}'].values[0]).rstrip('0').rstrip('.')} AND 
                        aposta = {str(df_row[f'aposta{i}'].values[0]).rstrip('0').rstrip('.')}
                    '''
                    c.execute(query)

                # Commit das alterações
                self.conn.commit()
                preencher_treeview(self.conn, self, bethouse_options, self.situation_vars, self.order_button1, self.order_button2, self.time_button, self.timeframe_combobox, self.search_var, self.frameTabela, self.frameSaldos, bethouse_list=bethouse_list)
                self.canvas1.place_forget()

                def show_message(title, message):
                    popup = tk.Toplevel()
                    popup.title(title)
                    tk.Label(popup, text=message).pack()
                    popup.after(2000, popup.destroy)

                show_message("Aviso", "Resultados salvos com sucesso!")

        save_results()
        df_resultados = df_filtrado[["resultado1", "resultado2", "resultado3"]]
        self.save.place_forget()

    def get_next_result(self, resultado):
        # Aqui você pode definir a ordem dos resultados
        resultados = ['', 'win', 'loss', 'return', 'half-win', 'half-loss']
        index = resultados.index(resultado)
        next_index = (index + 1) % len(resultados)
        return resultados[next_index]

def tabela_bethouses(parent, conn, bethouse_list=None):
    global bethouse_options, cache
    if bethouse_list is None:
        bethouse_list = bethouse_options.keys()
        cache = {}
    c = conn.cursor()
    treeview = ttk.Treeview(parent, style='Normal.Treeview', height=8)
    treeview.grid(row=0, column=0)
    data_atual = datetime.today()

    columns = ['BetHouses', 'A', 'V', 'D', 'Saldo', 'Em Aberto', 'Total', 'Diário', 'Mensal']
    treeview['columns'] = columns
    for column in columns:
        treeview.heading(column, text=column)
        if column == 'A' or column == 'V' or column == 'D':
            treeview.column(column, width=30)
        elif column == 'BetHouses':
            treeview.column(column, width=65)
        elif column == 'Diário':
            treeview.column(column, width=70)
        else:
            treeview.column(column, width=85)
    treeview['show'] = 'headings'

    for bethouse in bethouse_list:
        if bethouse in bethouse_options.keys():
            if bethouse not in bethouse_options.keys():
                cache.pop(bethouse, None)
                break
            table_name = f"{bethouse}_saldos"
            table_name = re.sub(r'\W+', '_', table_name)
            if table_name[0].isdigit():
                table_name = f'_{table_name}'

            # Consulta para obter os valores
            query = f'''
            SELECT resultado
            FROM "{table_name}"
            WHERE data_fim > DATE('{data_atual}', 'start of month')
            '''
            c.execute(query)
            rows = c.fetchall()

            abertas = sum(result[0] is None for result in rows)
            vitorias = sum(result[0] in ['win', 'half-win'] for result in rows) // 2
            derrotas = sum(result[0] in ['loss', 'half-loss'] for result in rows) // 2
            saldo_atual = c.execute(f"SELECT SUM(balanco) FROM {table_name}").fetchone()[0]
            saldo_atual = float(saldo_atual) if saldo_atual is not None else 0
            montante_aberto = c.execute(f"SELECT SUM(balanco) FROM {table_name} WHERE resultado IS NULL").fetchone()
            montante_aberto = -float(montante_aberto[0] if montante_aberto[0] is not None else 0)
            montante_total = float(saldo_atual + montante_aberto)
            dif_diaria = c.execute(f"SELECT SUM(balanco) FROM {table_name} WHERE resultado IS NOT NULL AND resultado IS NOT 'depósito' AND resultado IS NOT 'saque' AND (DATE(data_fim) = DATE('{data_atual}'))").fetchone()[0]
            dif_diaria = float(dif_diaria) if dif_diaria is not None else 0
            dif_mensal = c.execute(f"SELECT SUM(balanco) FROM {table_name} WHERE resultado IS NOT NULL AND resultado IS NOT 'depósito' AND resultado IS NOT 'saque' AND (DATE(data_fim) >= DATE('{data_atual}', 'start of month'))").fetchone()[0]
            dif_mensal = float(dif_mensal) if dif_mensal is not None else 0

            cache[bethouse] = {
                'abertas': abertas,
                'vitorias': vitorias,
                'derrotas': derrotas,
                'saldo_atual': saldo_atual,
                'montante_aberto': montante_aberto,
                'montante_total': montante_total,
                'dif_diaria': dif_diaria,
                'dif_mensal': dif_mensal
            }
        else:
            cache.pop(bethouse, None)

    # Calcular valores totais
    chaves = ['vitorias', 'derrotas', 'saldo_atual', 'montante_aberto', 'montante_total', 'dif_diaria', 'dif_mensal']
    cache.pop('Total', None)  # Remover a chave 'Total' do dicionário cache
    cache['Total'] = {chave: sum(data[chave] for data in cache.values()) for chave in chaves}
    cache['Total']['abertas'] = c.execute(f'SELECT COUNT(*) FROM apostas WHERE resultado1 IS NULL OR resultado2 IS NULL OR (bethouse3 IS NOT NULL AND resultado3 IS NULL)').fetchone()[0]

    for bethouse, data in cache.items():
        abertas = data['abertas']
        vitorias = data['vitorias']
        derrotas = data['derrotas']
        saldo_atual = data['saldo_atual']
        montante_aberto = data['montante_aberto']
        montante_total = data['montante_total']
        dif_diaria = data['dif_diaria']
        dif_mensal = data['dif_mensal']

        values = [bethouse, abertas, vitorias, derrotas, f"R$ {saldo_atual:.2f}", f"R$ {montante_aberto:.2f}", f"R$ {montante_total:.2f}", f"R$ {dif_diaria:.2f}", f"R$ {dif_mensal:.2f}"]
        treeview.insert('', 'end', values=values, tags=(bethouse,))
        if bethouse == 'Total':
            treeview.tag_configure(bethouse, background='white', foreground='black')
        else:
            treeview.tag_configure(bethouse, background=bethouse_options[bethouse]['background_color'], foreground=bethouse_options[bethouse]['text_color'])

    class MyDialog(tk.Toplevel):
        def __init__(self, parent, title, labeltext):
            tk.Toplevel.__init__(self, parent)
            self.title(title)
            self.label = tk.Label(self, text=labeltext)
            self.label.pack()
            vcmd = (self.register(lambda s: validate_num(s, dig=4, dec=2, negative=False)), '%P')
            self.entry = tk.Entry(self, validate='key', validatecommand=vcmd)
            self.entry.bind("<KeyRelease>", lambda event: on_entry_change(self.entry))
            self.entry.pack()
            self.button = tk.Button(self, text="OK", command=self.ok)
            self.button.pack()
            self.result = None

        def ok(self):
            try:
                self.result = float(self.entry.get().replace(',', '.'))
            except ValueError:
                self.result = None
            self.destroy()

    def deposit():
        dialog = MyDialog(parent, "Depósito", f"Valor a depositar em {bethouse_saldo}:")
        parent.wait_window(dialog)
        value = dialog.result
        status = 'deposito'
        table_name = f"{bethouse_saldo}_saldos"
        table_name = re.sub(r'\W+', '_', table_name)
        if table_name[0].isdigit():
            table_name = f'_{table_name}'
        depositos_hoje = c.execute(f"SELECT COUNT(*) FROM {table_name} WHERE DATE(data_entrada) = DATE('{data_atual}') AND resultado = 'depósito'").fetchone()[0] + 1
        id = f"{datetime.now().strftime('%y%m%d')}01{str(depositos_hoje).zfill(2)}"
        if value is not None:
            add_to_database(id, bethouse_saldo, status, value)

    def withdraw():
        dialog = MyDialog(parent, "Saque", f"Valor a sacar de {bethouse_saldo}:")
        parent.wait_window(dialog)
        value = dialog.result
        status = 'saque'
        table_name = f"{bethouse_saldo}_saldos"
        table_name = re.sub(r'\W+', '_', table_name)
        if table_name[0].isdigit():
            table_name = f'_{table_name}'
        saques_hoje = c.execute(f"SELECT COUNT(*) FROM {table_name} WHERE DATE(data_entrada) = DATE('{data_atual}') AND resultado = 'saque'").fetchone()[0] + 1
        id = f"{datetime.now().strftime('%y%m%d')}02{str(saques_hoje).zfill(2)}"
        if value is not None:
            add_to_database(id, bethouse_saldo, status, -value)

    def ajuste_saldo(saldo):
        dialog = MyDialog(parent, "Novo Saldo", f"Novo Saldo atual em {bethouse_saldo}:")
        parent.wait_window(dialog)
        value = dialog.result
        montante = round(-saldo + value, 2)
        status = 'ajuste'
        table_name = f"{bethouse_saldo}_saldos"
        table_name = re.sub(r'\W+', '_', table_name)
        if table_name[0].isdigit():
            table_name = f'_{table_name}'
        ajustes_hoje = c.execute(f"SELECT COUNT(*) FROM {table_name} WHERE DATE(data_entrada) = DATE('{data_atual}') AND resultado = 'saque'").fetchone()[0] + 1
        id = f"{datetime.now().strftime('%y%m%d')}03{str(ajustes_hoje).zfill(2)}"

        if montante is not None:
            add_to_database(id, bethouse_saldo, status, montante)

    def add_to_database(id, bethouse, status, value):
        table_name = f"{bethouse}_saldos"
        table_name = re.sub(r'\W+', '_', table_name)
        if table_name[0].isdigit():
            table_name = f'_{table_name}'
        data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT INTO {} (id, data_entrada, data_fim, odd, aposta, resultado, balanco, dif_real) VALUES (?, ?, ?, NULL, NULL, ?, ?, ?)".format(table_name)
        values = (id, data, data, status, value, value)
        conn.execute(query, values)
        conn.commit()
        bethouse_list = {bethouse}
        tabela_bethouses(parent, conn, bethouse_list = bethouse_list)

    # Criando o menu de contexto
    menu = Menu(parent, tearoff=0)
    menu.add_command(label='Depósito', command=deposit)
    menu.add_command(label='Retirada', command=withdraw)
    menu.add_command(label='Novo Saldo', command=lambda: ajuste_saldo(saldo_atualizado))

    # Função para exibir o menu de contexto
    def show_menu(event):
        global bethouse_saldo, saldo_atualizado
        row_id = treeview.identify_row(event.y)
        bethouse_saldo = treeview.item(row_id)['values'][0]
        saldo_atualizado = float(treeview.item(row_id)['values'][4].replace('R$ ', '').strip())
        menu.post(event.x_root, event.y_root)


    # Adicionando o evento de clique com o botão direito do mouse ao treeview
    treeview.bind('<Button-2>', show_menu)

def calculate_balance(row, num=''):
    if num == '':
        aposta = row['aposta']
        resultado = row['resultado']
        odd_real = row['odd_real']
    else:
        odd = float(row[f'odd{num}'].values[0])
        aposta = float(row[f'aposta{num}'].values[0])
        resultado = row[f'resultado{num}'].values[0]
        taxa = bethouse_options[row[f'bethouse{num}'].values[0]]['taxa']
        odd_real = float(
            (odd - 1) * (1 - taxa) + 1 if row[f'mercado{num}'].values[0] != 'Lay' else (odd / (odd - 1) - 1) * (
                    1 - taxa) + 1)
    if resultado == 'win':
        return odd_real * aposta - aposta
    elif resultado == 'half-win':
        return aposta / 2 + aposta / 2 * odd_real - aposta
    elif resultado == 'return':
        return 0
    elif resultado == 'half-loss':
        return aposta / 2 - aposta
    else:
        return -aposta

def save_apostas(dados, conn, linha_antiga=None, tipo='a'):
    c = conn.cursor()
    if tipo == 'add' or tipo == 'a' or tipo == 'append':
        # Montar a query de inserção
        insert_query = "INSERT INTO apostas ({}) VALUES ({})".format(
            ', '.join(dados.keys()),
            ', '.join(['?' for _ in range(len(dados))])
        )
        # Executar a query de inserção
        c.execute(insert_query, list(dados.values()))

        dados_saldos = {}
        for j in range(1, 4 if dados['bethouse3'] in bethouse_options.keys() else 3):
            bethouse_key = dados[f'bethouse{j}']
            table_name = f"{bethouse_key}_saldos"
            table_name = re.sub(r'\W+', '_', table_name)
            if table_name[0].isdigit():
                table_name = f'_{table_name}'

            odd = dados[f'odd{j}']
            dados_saldos = {
                'id': dados['id'],
                'data_entrada': dados['data_entrada'],
                'data_fim': dados['data_jogo'],
                'odd': float(odd),
                'aposta': dados[f'aposta{j}'],
                'resultado': dados[f'resultado{j}'],
                'balanco': -dados[f'aposta{j}'],
                'dif_real': 0
            }

            # Montar a query de inserção
            insert_query = "INSERT INTO " + f"{table_name} " + "({}) VALUES ({})".format(
                ', '.join(dados_saldos.keys()),
                ', '.join(['?' for _ in range(len(dados_saldos))])
            )
            # Executar a query de inserção
            c.execute(insert_query, list(dados_saldos.values()))


    elif tipo == 'edit' or tipo == 'e':
        query = """
            UPDATE apostas
            SET data_entrada = ?,
                data_jogo = ?,
                time_casa = ?,
                time_fora = ?,
                bethouse1 = ?,
                bethouse2 = ?,
                bethouse3 = ?,
                mercado1 = ?,
                mercado2 = ?,
                mercado3 = ?,
                valor1 = ?,
                valor2 = ?,
                valor3 = ?,
                odd1 = ?,
                odd2 = ?,
                odd3 = ?,
                aposta1 = ?,
                aposta2 = ?,
                aposta3 = ?,
                lucro_estimado = ?,
                lucro_per_estimado = ?,
                esporte = ?
            WHERE id = ?
        """

        params = (
            dados["data_entrada"],
            dados["data_jogo"],
            dados["time_casa"],
            dados["time_fora"],
            dados["bethouse1"],
            dados["bethouse2"],
            dados["bethouse3"],
            dados["mercado1"],
            dados["mercado2"],
            dados["mercado3"],
            dados["valor1"],
            dados["valor2"],
            dados["valor3"],
            dados["odd1"],
            dados["odd2"],
            dados["odd3"],
            dados["aposta1"],
            dados["aposta2"],
            dados["aposta3"],
            dados["lucro_estimado"],
            dados["lucro_per_estimado"],
            dados["esporte"],
            dados["id"]
        )
        # Executar a query de atualização
        c.execute(query, params)

        # Deletar entradas anteriores
        for bethouse in linha_antiga:
            table_name = f"{bethouse}_saldos"
            table_name = re.sub(r'\W+', '_', table_name)
            if table_name[0].isdigit():
                table_name = f'_{table_name}'
            delete_query = f"DELETE FROM {table_name} WHERE id = {dados['id']}"
            c.execute(delete_query)

        # Iterar sobre os dados
        for j in range(1, 4 if dados['bethouse3'] in bethouse_options.keys() else 3):
            bethouse_key = dados[f'bethouse{j}']
            if bethouse_key in bethouse_options.keys():
                odd = float(dados[f'odd{j}'])
                odd_real = round((odd - 1) * (1 - bethouse_options[bethouse_key]['taxa']) + 1, 2) if dados[f'mercado{j}'] != 'Lay' else round((odd / (odd - 1) - 1) * (1 - bethouse_options[bethouse_key]['taxa']) + 1, 3)
                aposta = float(dados[f'aposta{j}'])

                # Modificar o nome da tabela substituindo caracteres não permitidos por sublinhado (_)
                table_name = f"{bethouse_key}_saldos"
                table_name = re.sub(r'\W+', '_', table_name)
                if table_name[0].isdigit():
                    table_name = f'_{table_name}'

                # Inserir os valores na tabela
                insert_query = f'''
                    INSERT INTO "{table_name}" (id, data_entrada, data_fim, odd, aposta, resultado, balanco, dif_real)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                '''
                values = (
                    int(dados['id']),
                    dados['data_entrada'],
                    dados['data_jogo'],
                    odd,
                    aposta,
                    dados[f'resultado{j}'],
                    -aposta,
                    0.0
                )

                c.execute(insert_query, values)

    # Commit das alterações e fechamento da conexão
    conn.commit()

def graph():
    def update_graph():
        range_val = int(range_val_entry.get())
        periodo_tempo = periodo_tempo_var.get()

        filtered_dfs = {}
        for bethouse, df in df_saldos_bethouses.items():
            if periodo_tempo == 'Dia':
                filtered_df = df.tail(range_val)
            elif periodo_tempo == 'Semana':
                filtered_df = df.resample('W').last().tail(range_val)
            elif periodo_tempo == 'Mês':
                filtered_df = df.resample('M').last().tail(range_val)
            elif periodo_tempo == 'Ano':
                filtered_df = df.resample('Y').last().tail(range_val)
            filtered_dfs[bethouse] = filtered_df

        # Criar o gráfico de linhas
        plt.figure(figsize=(8, 2.7))

        for bethouse, df in filtered_dfs.items():
            plt.plot(df.index, df['balanco'], label=bethouse)
        plt.xlabel('data_fim')
        plt.ylabel('Saldo Diário')
        plt.legend()

        # Atualizar o gráfico no frameStatus
        canvas = FigureCanvasTkAgg(plt.gcf(), master=frameStatus)
        canvas.draw()
        canvas.get_tk_widget().grid(row=5, column=0, padx=10, pady=10, rowspan=8, columnspan=6)


    range_val_label = Label(frameStatus, text="range_val:")
    # Criar o entry e o label para range_val
    range_val_label.grid(row=3, column=0)
    range_val_entry = Entry(frameStatus, width=4)
    range_val_entry.grid(row=3, column=1)

    # Criar o menu suspenso para periodo_tempo
    periodo_tempo_var = StringVar(frameStatus)
    periodo_tempo_var.set('Dia')  # Valor padrão
    periodo_tempo_options = ['Dia', 'Semana', 'Mês', 'Ano']
    periodo_tempo_menu = OptionMenu(frameStatus, periodo_tempo_var, *periodo_tempo_options)
    periodo_tempo_menu.grid(row=3, column=2)

    # Criar o botão para atualizar o gráfico
    update_button = Button(frameStatus, text="Atualizar Gráfico", command=update_graph)
    update_button.grid(row=3, column=3)


