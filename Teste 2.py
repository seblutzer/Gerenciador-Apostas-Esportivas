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

janela = tk.Tk()

frameTabela = tk.Frame(janela)
frameTabela.grid(row=8, column=0)
df_filtrado = pd.read_csv("Apostas.csv")

bethouse_options = {"Bet365": {"background_color": "#12760a", "taxa": 0.0, "text_color": "#f3f3ff"}, "BetFair": {"background_color": "#ffb80c", "taxa": 0.0, "text_color": "#000000"}, "BetWay": {"background_color": "#000000", "taxa": 0.0, "text_color": "#ffffff"}, "Ex BetFair": {"background_color": "#ffb80c", "taxa": 0.065, "text_color": "#000000"}, "FavBet": {"background_color": "#000055", "taxa": 0.0, "text_color": "#f22578"}, "Pinnacle": {"background_color": "#042c54", "taxa": 0.0, "text_color": "#ff5500"}, "VBet": {"background_color": "#160e20", "taxa": 0.0, "text_color": "#ff03fe"}}

def preencher_treeview():
    # Limpar o conteúdo atual do Treeview
    tabela.delete(*tabela.get_children())

    # Configurar cores de fundo alternadas para as linhas
    tabela.tag_configure("linha_par", background="#F0F0F0")
    tabela.tag_configure("linha_impar", background="white")

    # Preencher o Treeview com os dados do arquivo
    for i, row in df_filtrado.iterrows():
        id = row['id']
        jogo = f"{row['time_casa']}\n{row['time_fora']}"
        data = "{:02d}/{}\n{:02d}:{:02d}".format(int(row['dia']), (row['mes']), int(row['hora']), int(row['minuto']))
        bethouses = f"{row['bethouse1']}\n{row['bethouse2']}"
        if pd.notna(row['bethouse3']) and row['bethouse3'] in bethouse_options.keys():
            bethouses += f"\n{row['bethouse3']}"
        odds = "{:.3f}".format(row['odd1']).rstrip('0').rstrip('.') + "\n{:.3f}".format(row['odd2']).rstrip('0').rstrip('.')
        if pd.notna(row['bethouse3']) and row['bethouse3'] in bethouse_options.keys():
            odds += "\n{:.3f}".format(row['odd3']).rstrip('0').rstrip('.')
        apostas = f"R$ {row['aposta1']:.2f}\nR$ {row['aposta2']:.2f}"
        if pd.notna(row['bethouse3']) and row['bethouse3'] in bethouse_options.keys():
            apostas += f"\nR$ {row['aposta3']:.2f}"
        mercados = row['mercado1']
        if pd.notna(row['valor1']):
            mercados += "({:.2f}".format(row['valor1']).rstrip('0').rstrip('.') + ")"
        mercados += f"\n{row['mercado2']}"
        if pd.notna(row['valor2']):
            mercados += "({:.2f}".format(row['valor2']).rstrip('0').rstrip('.') + ")"
        if pd.notna(row['bethouse3']) and row['bethouse3'] in bethouse_options.keys():
            mercados += f"\n{row['mercado3']}"
            if pd.notna(row['valor3']):
                mercados += "({:.2f}".format(row['valor3']).rstrip('0').rstrip('.') + ")"
        adds = datetime.strptime(row['add'], "%Y-%m-%d %H:%M:%S").strftime("%d/%m")

        # Add alternating background colors to rows
        if i % 2 == 0:
            tabela.insert("", "end", values=(adds, jogo, data, bethouses, odds, apostas, mercados, id), tags=("linha_par",))
        else:
            tabela.insert("", "end", values=(adds, jogo, data, bethouses, odds, apostas, mercados, id), tags=("linha_impar",))

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
        id = item['values'][7]
        df_row = df_filtrado.loc[df_filtrado['id'] == id]
        icons = []
        print(df_row['bethouse3'].values[0])
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
        self.canvas.create_text(30, 10, text="{} {}×{}".format(item['values'][3].split('\n')[0], item['values'][4].split('\n')[0], item['values'][5].split('\n')[0]), anchor=W, fill=fg_color1)
        self.canvas.create_image(0, 20, image=icons[1], anchor=NW, tags='imagem')
        self.canvas.create_text(30, 30, text="{} {}×{}".format(item['values'][3].split('\n')[1], item['values'][4].split('\n')[1], item['values'][5].split('\n')[1]), anchor=W, fill=fg_color2)

        if df_row['bethouse3'].values[0] in bethouse_options.keys():  # Check the value of bethouse3
            self.canvas.config(height=80)  # Increase the height of the canvas
            bg_color3 = bethouse_options[df_row['bethouse3'].values[0]]['background_color']
            fg_color3 = bethouse_options[df_row['bethouse3'].values[0]]['text_color']
            self.canvas.create_rectangle(30, 60, 200, 40, fill=bg_color3)
            self.canvas.create_image(0, 40, image=icons[2], anchor=NW, tags='imagem')  # Create the third icon
            self.canvas.create_text(30, 50, text="{} {}×{}".format(item['values'][3].split('\n')[2], item['values'][4].split('\n')[2], item['values'][5].split('\n')[2]), anchor=W, fill=fg_color3)
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
        row = self.clicked_row  # Get the clicked row
        item = self.item(row)  # Get the item data for the clicked row
        id = item['values'][7]
        df_row = df_filtrado.loc[df_filtrado['id'] == id]
        def save_results():
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
                #filter_selection()
                preencher_treeview()
                self.canvas.place_forget()
                def show_message(title, message):
                    popup = tk.Toplevel()
                    popup.title(title)
                    tk.Label(popup, text=message).pack()
                    popup.after(2000, popup.destroy)

                show_message("Aviso", "Resultados salvos com sucesso!")
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
            if df_row['bethouse3'].values[0] in bethouse_options.keys():
                resultado = df_row['resultado3'].values[0]
                icon3 = self.get_icon_from_result(resultado)
            self.canvas.delete('imagem')  # Clear the canvas
            self.canvas.create_image(0, 0, image=icon1, anchor=NW, tags='imagem')
            self.canvas.create_image(0, 20, image=icon2, anchor=NW, tags='imagem')

            if df_row['bethouse3'].values[0] in bethouse_options.keys():  # Check the value of bethouse3
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
            if df_row['bethouse3'].values[0] in bethouse_options.keys():
                resultado = df_row['resultado3'].values[0]
                icon3 = self.get_icon_from_result(resultado)
            self.canvas.delete("imagem")  # Clear the canvas
            self.canvas.create_image(0, 0, image=icon1, anchor=NW, tags='imagem')
            self.canvas.create_image(0, 20, image=icon2, anchor=NW, tags='imagem')

            if df_row['bethouse3'].values[0] in bethouse_options.keys():  # Check the value of bethouse3
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
            if df_row['bethouse3'].values[0] in bethouse_options.keys():  # Check the value of bethouse3
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
tabela = MyTreeview(frameTabela, columns=("adds", "jogo", "data", "bethouses", "odds", "bets", "mercados", "id"), show="headings", style="Treeview")
tabela.heading("adds", text="Adição")
tabela.heading("jogo", text="Jogo")
tabela.heading("data", text="Data")
tabela.heading("bethouses", text="BetHouses")
tabela.heading("odds", text="Odds")
tabela.heading("bets", text="Apostas")
tabela.heading("mercados", text="Mercados")
tabela.heading("id", text="ID")
tabela.column("id", width=30)
tabela.column("jogo", width=130)
tabela.column("data", width=50)
tabela.column("bethouses", width=70)
tabela.column("odds", width=50)
tabela.column("bets", width=70)
tabela.column("mercados", width=70)
tabela.column("adds", width=50)
tabela.grid(row=2, column=0, columnspan=10, rowspan= 10)
tabela.bind('<Double-Button-1>', select_bets) # Tabela
#filter_selection()

preencher_treeview()
# inicia o loop da janela
janela.mainloop()