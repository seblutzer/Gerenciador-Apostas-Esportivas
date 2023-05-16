import pandas as pd
import numpy as np
from Pacotes_Lutzer.filtros import agregar_datas




df_tabela = pd.read_csv("Apostas.csv")
groupby_cols = ['bethouse1', 'bethouse2', 'bethouse3']
combined_values = list(pd.concat([df_tabela[col] for col in df_tabela[groupby_cols]], ignore_index=True).unique())

periodo_tempo = 'dia'  # Período de tempo desejado: 'dia', 'semana', 'mes', 'ano', 'trimestre', 'semestre'
colunas = ['lucro_estimado', 'lucroReal']  # Lista das colunas a serem agregadas
metodos = ['sum', 'sum']  # Lista dos métodos de agregação para cada coluna

resultado = agregar_datas(df_tabela, 'add', periodo_tempo, colunas, metodos, range_val=5, cont_hora=False, groupby_cols=['bethouse1', 'bethouse2', 'bethouse3'], fusion=True)
print(resultado)
