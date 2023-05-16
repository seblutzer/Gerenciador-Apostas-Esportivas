from Pacotes_Lutzer.filtros import agregar_datas
import pandas as pd
import plotly.express as px
import tkinter as tk
from plotly import figure_factory as ff
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import tempfile
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math



# Crie uma janela do tkinter
janela = tk.Tk()

# Defina o dataframe df_tabela (substitua com seu próprio dataframe)
df_tabela = pd.read_csv("Apostas.csv")

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
    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.get_tk_widget().grid(row=1, column=0, columnspan=5)


# Crie uma caixa de entrada para o range_val
range_label = tk.Label(janela, text="Range:")
range_label.grid(row=0, column=0)
range_entry = tk.Entry(janela, width=4)
range_entry.grid(row=0, column=1)
range_entry.insert(0, 5)
range_entry.bind("<FocusOut>", lambda event: atualizar_grafico())

# Crie uma caixa de seleção para o período
periodo_var = tk.StringVar(janela)
periodo_var.set("dia")  # Valor padrão
def atualizar_grafico_periodo(*args):
    atualizar_grafico()

periodo_var.trace("w", atualizar_grafico_periodo)
periodo_dropdown = tk.OptionMenu(janela, periodo_var, "dia", "semana", "mes", "trimestre", "semestre", "ano")
periodo_dropdown.grid(row=0, column=3)
periodo_dropdown.configure(width=4)

# Exiba a janela do tkinter
janela.mainloop()
