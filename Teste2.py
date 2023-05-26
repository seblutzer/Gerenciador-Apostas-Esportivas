from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, Button, Frame
from main import df_saldos_bethouses

# Função para atualizar o gráfico com base nos filtros selecionados
def update_graph():
    range_val = int(range_val_entry.get())
    periodo_tempo = periodo_tempo_var.get()

    filtered_dfs = {}
    for bethouse, df in df_saldos_bethouses.items():
        if periodo_tempo == 'dia':
            filtered_df = df.tail(range_val)
        elif periodo_tempo == 'semana':
            filtered_df = df.resample('W').last().tail(range_val)
        elif periodo_tempo == 'mês':
            filtered_df = df.resample('M').last().tail(range_val)
        elif periodo_tempo == 'ano':
            filtered_df = df.resample('Y').last().tail(range_val)
        filtered_dfs[bethouse] = filtered_df

    # Criar o gráfico de linhas
    plt.figure(figsize=(10, 6))
    for bethouse, df in filtered_dfs.items():
        plt.plot(df.index, df['saldo_diario'], label=bethouse)
    plt.xlabel('Data')
    plt.ylabel('Saldo Diário')
    plt.legend()

    # Atualizar o gráfico no frameStats
    canvas = FigureCanvasTkAgg(plt.gcf(), master=frameStats)
    canvas.draw()
    canvas.get_tk_widget().grid(row=2, column=0, padx=10, pady=10)

# Criar a window
window = Tk()

# Criar o frameStats
frameStats = Frame(window)
frameStats.grid(row=0, column=0)

# Criar o entry e o label para range_val
range_val_label = Label(frameStats, text="range_val:")
range_val_label.grid(row=0, column=0)
range_val_entry = Entry(frameStats)
range_val_entry.grid(row=0, column=1)

# Criar o radio button para periodo_tempo
periodo_tempo_var = StringVar()
dia_radio = Radiobutton(frameStats, text="Dia", variable=periodo_tempo_var, value="dia")
dia_radio.grid(row=1, column=0)
semana_radio = Radiobutton(frameStats, text="Semana", variable=periodo_tempo_var, value="semana")
semana_radio.grid(row=1, column=1)
mes_radio = Radiobutton(frameStats, text="Mês", variable=periodo_tempo_var, value="mês")
mes_radio.grid(row=1, column=2)
ano_radio = Radiobutton(frameStats, text="Ano", variable=periodo_tempo_var, value="ano")
ano_radio.grid(row=1, column=3)

# Criar o botão para atualizar o gráfico
update_button = Button(frameStats, text="Atualizar Gráfico", command=update_graph)
update_button.grid(row=1, column=4)

# Iniciar a window
window.mainloop()

