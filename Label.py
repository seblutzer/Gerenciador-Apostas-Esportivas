import tkinter as tk
from tkinter import ttk

def toggle_order():
    current_order = order_button["text"]
    if current_order == "Ordem Crescente de Datas":
        order_button["text"] = "Ordem Decrescente de Datas"
    elif current_order == "Ordem Decrescente de Datas":
        order_button["text"] = "Ordem Crescente de Adição"
    elif current_order == "Ordem Crescente de Adição":
        order_button["text"] = "Ordem Decrescente de Adição"
    else:
        order_button["text"] = "Ordem Crescente de Datas"

def toggle_time():
    current_time = time_button["text"]
    if current_time == "Próximos":
        time_button["text"] = "Últimos"
    else:
        time_button["text"] = "Próximos"

def filter_selection():
    selected_time = time_button["text"]
    selected_timeframe = timeframe_combobox.get()
    selected_situations = [var.get() for var in situation_checkbuttons]

    print("Ordem:", order_button["text"])
    print("Tempo:", selected_time, selected_timeframe)
    print("Situação:", selected_situations)

janela = tk.Tk()
janela.title("Filtros")

# Frame para a tabela
frameTabela = tk.Frame(janela)
frameTabela.grid(row=0, column=0, columnspan=2)

# Ordenação
order_button = tk.Button(frameTabela, text="Ordem Crescente de Datas", command=toggle_order)
order_button.grid(row=0, column=0)

# Tempo
time_label = tk.Label(frameTabela, text="Tempo:")
time_label.grid(row=0, column=1)

time_button = tk.Button(frameTabela, text="Último", width=10, command=toggle_time)
time_button.grid(row=0, column=2)

timeframe_options = ["dia", "2 dias", "semana", "mês", "30 dias", "esse ano", "1 ano", "todos os tempos"]
timeframe_combobox = ttk.Combobox(frameTabela, values=timeframe_options, state="readonly")
timeframe_combobox.current(0)
timeframe_combobox.grid(row=0, column=3)

# Situação
situation_label = tk.Label(frameTabela, text="Situação:")
situation_label.grid(row=0, column=4)

situations = ["Vencidas", "Abertas", "Fechadas"]
situation_checkbuttons = []

for idx, situation in enumerate(situations):
    var = tk.IntVar()
    checkbutton = tk.Checkbutton(frameTabela, text=situation, variable=var)
    checkbutton.grid(row=0, column=5+idx, padx=5)
    situation_checkbuttons.append(var)

# Botão de Filtrar
filter_button = tk.Button(frameTabela, text="Filtrar", command=filter_selection)
filter_button.grid(row=0, column=8, padx=10)

janela.mainloop()
