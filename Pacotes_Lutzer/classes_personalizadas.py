import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
import datetime
from datetime import datetime, timedelta
import csv
import pandas as pd
from Pacotes_Lutzer.convert import convert_mes
from Pacotes_Lutzer.validate import validate_num, on_entry_change
import os
import numpy as np


def preencher_treeview(tabela, bethouse_options, df_base, situation_vars, order_button1, order_button2, time_button, timeframe_combobox, frameTabela):
    global df_filtrado, df_tabela
    df_tabela = df_base
    df_filtrado = filter_selection(df_tabela, situation_vars, order_button1, order_button2, time_button, timeframe_combobox, frameTabela)
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
        data = "{:02d}/{}\n{:02d}:{:02d}".format(row['datetime'].day, convert_mes(row['datetime'].month), row['datetime'].hour,row['datetime'].minute)
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
        odds = "{:.3f}".format(float(row['odd1'])).rstrip('0').rstrip('.') + "\n{:.3f}".format(float(row['odd2'])).rstrip('0').rstrip('.')
        if pd.notna(row['bethouse3']) and row['bethouse3'] in bethouse_options.keys():
            odds += "\n{:.3f}".format(float(row['odd3'])).rstrip('0').rstrip('.')
        apostas = f"R$ {float(row['aposta1']):.2f}" if isinstance(float(row['aposta1']), (float, int)) else f"\nR$ 0.00"
        apostas += f"\nR$ {float(row['aposta2']):.2f}" if isinstance(float(row['aposta2']), (float, int)) else f"\nR$ 0.00"
        if pd.notna(row['bethouse3']) and row['bethouse3'] in bethouse_options.keys():
            apostas += f"\nR$ {float(row['aposta3']):.2f}" if isinstance(float(row['aposta3']), (float, int)) else ""
        mercados = str(row['mercado1'])
        if pd.notna(row['valor1']):
            valor1 = row['valor1']
            if isinstance(valor1, (int, float)):
                mercados += "({:.2f}".format(valor1).rstrip('0').rstrip('.') + ")"
            else:
                mercados += valor1
        mercados += f"\n{str(row['mercado2'])}"
        if pd.notna(row['valor2']):
            valor2 = row['valor2']
            if isinstance(valor2, (int, float)):
                mercados += "({:.2f}".format(valor2).rstrip('0').rstrip('.') + ")"
            else:
                mercados += valor2
        if pd.notna(row['bethouse3']) and row['bethouse3'] in bethouse_options.keys():
            mercados += f"\n{str(row['mercado3'])}"
            if pd.notna(row['valor3']):
                valor3 = row['valor3']
                if isinstance(valor3, (int, float)):
                    mercados += "({:.2f}".format(valor3).rstrip('0').rstrip('.') + ")"
                else:
                    mercados += valor3
        adds = "{:02d}/{}".format(row['add'].day, convert_mes(row['add'].month))

        # Add alternating background colors to rows
        if index % 2 == 0:
            tabela.insert("", "end", values=(index, adds, jogo, data, resultados, bethouses, odds, apostas, mercados, id), tags=("linha_par",))
        else:
            tabela.insert("", "end", values=(index, adds, jogo, data, resultados, bethouses, odds, apostas, mercados, id), tags=("linha_impar",))
        index += 1


def filter_selection(df_tabela, situation_vars, order_button1, order_button2, time_button, timeframe_combobox, frameTabela):
    global df_filtrado
    # Cria uma cópia do dataframe para não modificar o original

    df_filtrado = df_tabela.copy()

    df_filtrado['add'] = pd.to_datetime(df_filtrado['add'])
    df_filtrado['datetime'] = pd.to_datetime(df_filtrado['datetime'])
    df_tabela['datetime'] = pd.to_datetime(df_tabela['datetime'])

    # Cria máscaras booleanas para cada situação
    mask_abertas = ((df_filtrado['resultado1'].isna() | df_filtrado['resultado2'].isna()) & ((df_filtrado['bethouse3'].notna() & (df_filtrado['resultado1'].isna() | df_filtrado['resultado2'].isna() | df_filtrado[ 'resultado3'].isna())) | (df_filtrado['bethouse3'].isna())))

    mask_vencidas = mask_abertas & (df_filtrado['datetime'].apply(lambda x: x + timedelta(hours=2)) < datetime.now())

    mask_fechadas = ((df_filtrado['resultado1'].notna() & df_filtrado['resultado2'].notna()) & ((df_filtrado['bethouse3'].notna() & df_filtrado['resultado3'].notna()) | (df_filtrado['bethouse3'].isna())))
    # Aplica as máscaras conforme as opções selecionadas pelo usuário
    if situation_vars[1].get() and situation_vars[2].get():
        pass
    elif situation_vars[0].get() and situation_vars[2].get():
        df_filtrado = df_filtrado[mask_vencidas | mask_fechadas]
    elif situation_vars[0].get():
        df_filtrado = df_filtrado[mask_vencidas]
    elif situation_vars[1].get():
        df_filtrado = df_filtrado[mask_abertas]
    elif situation_vars[2].get():
        df_filtrado = df_filtrado[mask_fechadas]

    # Ordenação
    if order_button1["text"] == "Crescente" and order_button2["text"] == "Data":
        df_filtrado = df_filtrado.sort_values(by=['datetime'])
    elif order_button1["text"] == "Decrescente" and order_button2["text"] == "Data":
        df_filtrado = df_filtrado.sort_values(by=['datetime'], ascending=False)
    elif order_button1["text"] == "Crescente" and order_button2["text"] == "Adição":
        df_filtrado = df_filtrado.sort_values(by=['id'])
    else:  # Decrescente e Adição
        df_filtrado = df_filtrado.sort_values(by=['id'], ascending=False)

    # Filtro de tempo
    if time_button["text"] == "Vencem até":
        if timeframe_combobox.get() == "hoje":
            current_datetime = datetime.now()
            df_filtrado = df_filtrado[df_filtrado['datetime'].dt.date == current_datetime.date()]
        elif timeframe_combobox.get() == "amanhã":
            end_datetime = datetime.now().replace(hour=0, minute=0) + timedelta(days=1)
            df_filtrado = df_filtrado[df_filtrado['datetime'] <= end_datetime]
        elif timeframe_combobox.get() == "1 semana":
            end_datetime = datetime.now().replace(hour=0, minute=0) + timedelta(weeks=1)
            df_filtrado = df_filtrado[df_filtrado['datetime'] <= end_datetime]
        elif timeframe_combobox.get() == "1 mês":
            end_datetime = datetime.now().replace(hour=0, minute=0) + timedelta(days=30)
            df_filtrado = df_filtrado[df_filtrado['datetime'] <= end_datetime]
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

    df_vencidas = df_tabela[((df_tabela['resultado1'].isna() | df_tabela['resultado2'].isna()) & ((df_tabela['bethouse3'].notna() & (df_tabela['resultado1'].isna() | df_tabela['resultado2'].isna() | df_tabela[ 'resultado3'].isna())) | (df_tabela['bethouse3'].isna()))) & (df_tabela['datetime'].apply(lambda x: x + timedelta(hours=2)) < datetime.now())]
    if len(df_vencidas) == 0:
        pass
    else:
        frame = tk.Canvas(frameTabela, width=20, height=20, highlightthickness=0)
        frame.create_oval(0, 0, 20, 20, fill="red")
        frame.create_text(10, 10, text=len(df_vencidas), fill="white", font=("Arial", 15, "bold"))
        frame.place(x=405, y=0)
    #linhas_label = tk.Label(frameTabela, text=len(df_filtrado))
    #linhas_label.grid(row=0, column=5)

    # Exibir o resultado
    return df_filtrado
class BetHistTreeview(ttk.Treeview):
    def __init__(self, master=None, situation_vars=None, order_button1=None, order_button2=None, time_button=None, timeframe_combobox=None, frameTabela=None, frameSaldos=None, **kw):
        ttk.Treeview.__init__(self, master, **kw)
        self.situation_vars = situation_vars
        self.order_button1 = order_button1
        self.order_button2 = order_button2
        self.time_button = time_button
        self.timeframe_combobox = timeframe_combobox
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

    def update_icons(self, tabela_filtrada):
        for row in self.get_children():
            item = self.item(row)
            id = item['values'][9]
            df_row = tabela_filtrada.loc[tabela_filtrada['id'] == id]
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
        self.canvas1.create_rectangle(30, 20, 300, 0, fill=bg_color1)
        self.canvas1.create_image(0, 0, image=icons[0], anchor=NW, tags='imagem')
        self.canvas1.create_text(30, 10, text=df_row['bethouse1'].values[0], anchor = W, fill = fg_color1)
        self.canvas1.create_text(105, 10, text=df_row['odd1'].values[0], anchor = W, fill = fg_color1)
        self.canvas1.create_text(155, 10, text=f"R$ {float(df_row['aposta1'].values[0]):.2f}", anchor = W, fill = fg_color1)
        formatted_valor1 = "" if pd.isna(df_row['valor1'].values[0]) or df_row['valor1'].values[0] == '' else "(" + f"{float(df_row['valor1'].values[0]):.2f}".rstrip('0').rstrip('.') + ")"
        self.canvas1.create_text(225, 10, text="{}{}".format(df_row['mercado1'].values[0], formatted_valor1), anchor=W, fill=fg_color1)
        self.canvas1.create_rectangle(30, 40, 300, 20, fill=bg_color2)
        self.canvas1.create_image(0, 20, image=icons[1], anchor=NW, tags='imagem')
        self.canvas1.create_text(30, 30, text=df_row['bethouse2'].values[0], anchor=W, fill=fg_color2)
        self.canvas1.create_text(105, 30, text=df_row['odd2'].values[0], anchor=W, fill=fg_color2)
        self.canvas1.create_text(155, 30, text=f"R$ {float(df_row['aposta2'].values[0]):.2f}", anchor=W, fill=fg_color2)
        formatted_valor2 = "" if pd.isna(df_row['valor2'].values[0]) or df_row['valor1'].values[0] == '' else "(" + f"{float(df_row['valor2'].values[0]):.2f}".rstrip('0').rstrip('.') + ")"
        self.canvas1.create_text(225, 30, text="{}{}".format(df_row['mercado2'].values[0], formatted_valor2), anchor=W, fill=fg_color2)

        if df_row['bethouse3'].values[0] in bethouse_options.keys():  # Check the value of bethouse3
            self.canvas1.config(height=60)  # Increase the height of the canvas
            bg_color3 = bethouse_options[df_row['bethouse3'].values[0]]['background_color']
            fg_color3 = bethouse_options[df_row['bethouse3'].values[0]]['text_color']
            self.canvas1.create_rectangle(30, 60, 300, 40, fill=bg_color3)
            self.canvas1.create_image(0, 40, image=icons[2], anchor=NW, tags='imagem')  # Create the third icon
            self.canvas1.create_text(30, 50, text=df_row['bethouse3'].values[0], anchor=W, fill=fg_color3)
            self.canvas1.create_text(105, 50, text=df_row['odd3'].values[0], anchor=W, fill=fg_color3)
            self.canvas1.create_text(155, 50, text=f"R$ {df_row['aposta3'].values[0]:.2f}", anchor=W, fill=fg_color3)
            formatted_valor3 = "" if pd.isna(df_row['valor3'].values[0]) or df_row['valor1'].values[0] == '' else "(" + f"{float(df_row['valor3'].values[0]):.2f}".rstrip('0').rstrip('.') + ")"
            self.canvas1.create_text(225, 50, text="{}{}".format(df_row['mercado3'].values[0], f"{formatted_valor3}" if pd.notna(df_row['valor3'].values[0]) else ""),anchor=W, fill=fg_color3)
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
        if event.y <= 20 and event.x <= 30:
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

        elif event.y <= 40 and event.x <= 30:
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

        elif event.y <= 60 and event.x <= 30:
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

    def on_save_click(self, event):
        global df_resultados
        selected_item = self.focus()
        item = self.item(selected_item)
        id = item['values'][9]
        df_row = df_filtrado.loc[df_filtrado['id'] == id]

        def save_results():
            global df_saldos_bethouses, bethouse_options
            if pd.isna(df_row['resultado1'].values[0]) or pd.isna(df_row['resultado2'].values[0]) or (
                    len(item['values'][3].split("\n")) > 2 and pd.isna(df_row['resultado3'].values[0])):
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

                somaApostas = float(df_row['aposta1'].values[0]) + float(df_row['aposta2'].values[0]) + (float(df_row['aposta3'].values[0]) if df_row['bethouse3'].values[0] in bethouse_options.keys() else 0)
                odd = {}  # Dicionário para armazenar os valores calculados
                for i in range(1, 4 if df_row['bethouse3'].values[0] in bethouse_options.keys() else 3):
                    if df_row[f'mercado{i}'].values[0] == "Lay":
                        odd[i] = (float(df_row[f'odd{i}'].values[0]) / (float(df_row[f'odd{i}'].values[0]) - 1) - 1) * (1 - float(bethouse_options[df_row[f'bethouse{i}'].values[0]]['taxa'])) + 1
                    else:
                        odd[i] = (float(df_row[f'odd{i}'].values[0]) - 1) * (1 - float(bethouse_options[df_row[f'bethouse{i}'].values[0]]['taxa'])) + 1
                retorno1 = round(float(df_row['aposta1'].values[0]) * odd[1] * calculate_fator_resultado(df_row['resultado1'].values[0], odd[1]), 2)
                retorno2 = round(float(df_row['aposta2'].values[0]) * odd[2] * calculate_fator_resultado(df_row['resultado2'].values[0], odd[2]), 2)
                retorno3 = round(float(df_row['aposta3'].values[0]) * odd[3] * calculate_fator_resultado(df_row['resultado3'].values[0], odd[3]) if df_row['bethouse3'].values[0] in bethouse_options.keys() else 0, 2)

                mask = df_saldos_bethouses[df_row['bethouse1'].values[0]]['id'] == df_row['id'].values[0]
                df_saldos_bethouses[df_row['bethouse1'].values[0]].loc[mask, 'resultado'] = df_row['resultado1'].values[0]

                mask = df_saldos_bethouses[df_row['bethouse2'].values[0]]['id'] == df_row['id'].values[0]
                df_saldos_bethouses[df_row['bethouse2'].values[0]].loc[mask, 'resultado'] = df_row['resultado2'].values[0]

                if df_row['bethouse3'].values[0] in bethouse_options:
                    mask = df_saldos_bethouses[df_row['bethouse3'].values[0]]['id'] == df_row['id'].values[0]
                    df_saldos_bethouses[df_row['bethouse3'].values[0]].loc[mask, 'resultado'] = df_row['resultado3'].values[0]

                tabela_bethouses(self.frameSaldos, df_saldos_bethouses, df_depositos_bethouses)
                somaRetornos = round(retorno1 + retorno2 + retorno3, 2)
                lucroReal = round(somaRetornos - somaApostas, 2)
                lucro_perReal = round(lucroReal / somaApostas, 4)
                df_filtrado.loc[df_filtrado['id'] == id, 'lucroReal'] = lucroReal
                df_filtrado.loc[df_filtrado['id'] == id, 'lucro_perReal'] = lucro_perReal
                df_tabela.update(df_filtrado.loc[df_filtrado.index[df_filtrado['id'] == id], ['resultado1', 'resultado2', 'resultado3', 'lucroReal', 'lucro_perReal']])
                df_tabela.to_csv('Apostas.csv', index=False)
                preencher_treeview(self, bethouse_options, df_tabela, self.situation_vars, self.order_button1, self.order_button2, self.time_button, self.timeframe_combobox, self.frameTabela)
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

def tabela_bethouses(parent, dataframes, dataframes_deposito):
    global df_saldos_bethouses, df_depositos_bethouses, bethouse_options
    df_saldos_bethouses = dataframes
    df_depositos_bethouses = dataframes_deposito
    treeview = ttk.Treeview(parent, style='Normal.Treeview', height=8)
    treeview.grid(row=0, column=0)

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
        else :
            treeview.column(column, width=85)
    treeview['show'] = 'headings'

    total_abertas = 0
    total_vitórias = 0
    total_derrotas = 0
    total_saldo_atual = 0
    total_montante_aberto = 0
    total_montante_total = 0
    total_diferença_diária = 0
    total_diferênça_mensal = 0

    for bethouse, df in dataframes.items():
        abertas = int(df['resultado'].isna().sum())
        vitórias = int((df['resultado'] == 'win').sum() + (df['resultado'] == 'half-win').sum() / 2)
        derrotas = int((df['resultado'] == 'loss').sum() + (df['resultado'] == 'half-loss').sum() / 2)
        saldo_atual = dataframes_deposito[bethouse]['Valor'].sum() + df['balanco'].sum()
        montante_aberto = -df.loc[df['resultado'].isna(), 'balanco'].sum()
        montante_total = saldo_atual + montante_aberto
        diferença_diária = df.loc[(df['data_fim'].dt.date == pd.to_datetime('today').date()) & ~df['resultado'].isna(), 'balanco'].sum()
        diferença_mensal = df.loc[(df['data_fim'].dt.month == pd.to_datetime('today').month) & (df['data_fim'].dt.year == pd.to_datetime('today').year) & ~df['resultado'].isna(), 'balanco'].sum()
        values = [bethouse, abertas, vitórias, derrotas, f"R$ {saldo_atual:.2f}", f"R$ {montante_aberto:.2f}", f"R$ {montante_total:.2f}", f"R$ {diferença_diária:.2f}", f"R$ {diferença_mensal:.2f}"]
        treeview.insert('', 'end', values=values, tags=(bethouse,))
        treeview.tag_configure(bethouse, background=bethouse_options[bethouse]['background_color'], foreground=bethouse_options[bethouse]['text_color'])

        total_abertas += abertas
        total_saldo_atual += saldo_atual
        total_montante_aberto += montante_aberto
        total_montante_total += montante_total
        total_diferença_diária += diferença_diária
        total_diferênça_mensal += diferença_mensal
        total_vitórias += vitórias
        total_derrotas += derrotas

    values = ['Total', total_abertas, total_vitórias, total_derrotas, f"R$ {total_saldo_atual:.2f}", f"R$ {total_montante_aberto:.2f}", f"R$ {total_montante_total:.2f}", f"R$ {total_diferença_diária:.2f}", f"R$ {total_diferênça_mensal:.2f}"]
    treeview.insert('', 'end', values=values)

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
        if value is not None:
            add_to_csv(bethouse_saldo, status, value)

    def withdraw():
        dialog = MyDialog(parent, "Saque", f"Valor a sacar de {bethouse_saldo}:")
        parent.wait_window(dialog)
        value = dialog.result
        status = 'saque'
        if value is not None:
            add_to_csv(bethouse_saldo, status, -value)

    def ajuste_saldo(saldo):
        dialog = MyDialog(parent, "Novo Saldo", f"Novo Saldo atual em {bethouse_saldo}:")
        parent.wait_window(dialog)
        value = dialog.result
        montante = round(-saldo + value, 2)
        status = 'ajuste'
        if montante is not None:
            add_to_csv(bethouse_saldo, status, montante)

    def add_to_csv(bethouse, status, value):
        global df_tabela
        data = [bethouse, status, value, datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        with open('./movimentacao.csv', 'a') as csvfile:
            csv.writer(csvfile).writerow(data)
        gerar_saldos(parent, bethouse_options, df_tabela)

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

def add_aposta(frameSaldos, dados, id=None):
    global df_saldos_bethouses, df_depositos_bethouses, bethouse_options
    # Extrair dados para 'bethouse1'
    try:
        bethouse1 = dados['bethouse1'].iloc[0]
    except AttributeError:
        bethouse1 = dados['bethouse1']

    new_row = {
        'id': dados['id'],
        'data_entrada': pd.to_datetime(dados['add']),
        'data_fim': pd.to_datetime(dados['datetime']),
        'bethouse': bethouse1,
        'odd': float(dados['odd1']),
        'aposta': float(dados['aposta1']),
        'resultado': np.nan,
        'balanco': -float(dados['aposta1'])
    }

    if id:
        mask = df_saldos_bethouses[bethouse1]['id'] == id
        df_saldos_bethouses[bethouse1].loc[mask, 'resultado'] = new_row['resultado']
        df_saldos_bethouses[bethouse1].loc[mask, 'data_fim'] = new_row['data_fim']
        df_saldos_bethouses[bethouse1].loc[mask, 'odd'] = new_row['odd']
        df_saldos_bethouses[bethouse1].loc[mask, 'aposta'] = new_row['aposta']
        df_saldos_bethouses[bethouse1].loc[mask, 'balanco'] = new_row['balanco']
    else:
        if bethouse1 in df_saldos_bethouses:
            max_index = df_saldos_bethouses[bethouse1].index.max()
            new_index = max_index + 1
            new_row_index = [new_index]
            df_saldos_bethouses[bethouse1] = pd.concat(
                [df_saldos_bethouses[bethouse1], pd.DataFrame(new_row, index=new_row_index)], ignore_index=False)
    # Extrair dados para 'bethouse2'
    try:
        bethouse2 = dados['bethouse2'].iloc[0]
    except AttributeError:
        bethouse2 = dados['bethouse2']
    new_row = {
        'id': dados['id'],
        'data_entrada': pd.to_datetime(dados['add']),
        'data_fim': pd.to_datetime(dados['datetime']),
        'bethouse': bethouse2,
        'odd': float(dados['odd2']),
        'aposta': float(dados['aposta2']),
        'resultado': np.nan,
        'balanco': -float(dados['aposta2'])
    }

    if id:
        mask = df_saldos_bethouses[bethouse2]['id'] == id
        df_saldos_bethouses[bethouse2].loc[mask, 'resultado'] = new_row['resultado']
        df_saldos_bethouses[bethouse2].loc[mask, 'data_fim'] = new_row['data_fim']
        df_saldos_bethouses[bethouse2].loc[mask, 'odd'] = new_row['odd']
        df_saldos_bethouses[bethouse2].loc[mask, 'aposta'] = new_row['aposta']
        df_saldos_bethouses[bethouse2].loc[mask, 'balanco'] = new_row['balanco']
    else:
        if bethouse2 in df_saldos_bethouses:
            new_index += 1
            new_row_index = [new_index]
            df_saldos_bethouses[bethouse2] = pd.concat(
                [df_saldos_bethouses[bethouse2], pd.DataFrame(new_row, index=new_row_index)], ignore_index=False)

    # Extrair dados para 'bethouse3' (se existir)
    try:
        bethouse3 = dados['bethouse3'].iloc[0]
    except AttributeError:
        bethouse3 = dados['bethouse3']
    if bethouse3 in df_saldos_bethouses:
        new_row = {
            'id': dados['id'],
            'data_entrada': pd.to_datetime(dados['add']),
            'data_fim': pd.to_datetime(dados['datetime']),
            'bethouse': bethouse3,
            'odd': float(dados['odd3']),
            'aposta': float(dados['aposta3']),
            'resultado': np.nan,
            'balanco': -float(dados['aposta3'])
        }
        if id:
            mask = df_saldos_bethouses[bethouse3]['id'] == id
            df_saldos_bethouses[bethouse3].loc[mask, 'resultado'] = new_row['resultado']
            df_saldos_bethouses[bethouse3].loc[mask, 'data_fim'] = new_row['data_fim']
            df_saldos_bethouses[bethouse3].loc[mask, 'odd'] = new_row['odd']
            df_saldos_bethouses[bethouse3].loc[mask, 'aposta'] = new_row['aposta']
            df_saldos_bethouses[bethouse3].loc[mask, 'balanco'] = new_row['balanco']
        else:
            new_index += 1
            new_row_index = [new_index]
            df_saldos_bethouses[bethouse3] = pd.concat(
                [df_saldos_bethouses[bethouse3], pd.DataFrame(new_row, index=new_row_index)], ignore_index=False)

    tabela_bethouses(frameSaldos, df_saldos_bethouses, df_depositos_bethouses)


def calculate_balance(row):
    if row['resultado'] == 'win':
        return row['odd_real'] * row['aposta'] - row['aposta']
    elif row['resultado'] == 'half-win':
        return row['aposta'] / 2 + row['aposta'] / 2 * row['odd_real'] - row['aposta']
    elif row['resultado'] == 'return':
        return 0
    elif row['resultado'] == 'half-loss':
        return row['aposta'] / 2 - row['aposta']
    else:
        return -row['aposta']

def expand_df(df):
    global bethouse_options
    new_rows = []
    for i in range(1, 4 if df['bethouse3'].values[0] in bethouse_options.keys() else 3):
        mask = df[f'bethouse{i}'].isin(bethouse_options.keys())
        new_rows.extend(df.loc[mask].apply(lambda row: {
            'id': row['id'],
            'data_entrada': pd.to_datetime(row['add']),
            'data_fim': pd.to_datetime(row['datetime']),
            'bethouse': row[f'bethouse{i}'],
            'odd': row[f'odd{i}'],
            'odd_real': (row[f'odd{i}'] - 1) * (1 - bethouse_options[df[f'bethouse{i}'].values[0]]['taxa']) + 1 if row[f'mercado{i}'] != 'Lay' else (row[f'odd{i}'] / (row[f'odd{i}'] - 1) -1) * (1 - bethouse_options[row[f'bethouse{i}']]['taxa']) + 1,
            'aposta': row[f'aposta{i}'],
            'resultado': row[f'resultado{i}']
        }, axis=1).tolist())

    new_df = pd.DataFrame(new_rows)
    new_df['balanco'] = new_df.apply(calculate_balance, axis=1)
    new_df['dif_real'] = new_df['balanco'].where(pd.notna(new_df['resultado']), 0)
    new_df['data_entrada'] = pd.to_datetime(new_df['data_entrada'])
    new_df['data_fim'] = pd.to_datetime(new_df['data_fim'])
    return new_df
def gerar_saldos(frameSaldos, options, df):
    global df_tabela, bethouse_options, df_saldos_bethouses, df_depositos_bethouses
    df_tabela = df
    bethouse_options = options
    df_depositos = pd.read_csv("./movimentacao.csv")
    df_saldo = expand_df(df_tabela)
    df_saldos_bethouses = {}
    df_depositos_bethouses = {}

    for bethouse in bethouse_options.keys():
        df_saldo_bethouse = df_saldo[df_saldo['bethouse'] == bethouse].copy()
        df_deposito_bethouse = df_depositos[df_depositos['BetHouse'] == bethouse].copy()
        df_saldos_bethouses[bethouse] = df_saldo_bethouse
        df_depositos_bethouses[bethouse] = df_deposito_bethouse

    tabela_bethouses(frameSaldos, df_saldos_bethouses, df_depositos_bethouses)

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