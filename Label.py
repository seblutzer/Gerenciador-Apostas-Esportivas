import pandas as pd
from Pacotes_Lutzer.convert import convert_mes

df_tabela = pd.read_csv("Apostas.csv")
# converter mês para o formato desejado
df_tabela['month'] = df_tabela['month'].apply(convert_mes)

# criar coluna datetime
df_tabela['datetime'] = pd.to_datetime(df_tabela[['year', 'month', 'day', 'hour', 'minute']])


# selecionar apenas as colunas necessárias
df_tabela = df_tabela[['id', 'add', 'datetime', 'time_casa', 'time_fora', 'bethouse1', 'mercado1', 'valor1', 'odd1', 'aposta1', 'resultado1', 'bethouse2', 'mercado2', 'valor2', 'odd2', 'aposta2', 'resultado2', 'bethouse3', 'mercado3', 'valor3', 'odd3', 'aposta3', 'resultado3', 'lucro_estimado', 'lucro_per_estimado', 'lucroReal', 'lucro_perReal', 'esporte']]


df_tabela.to_csv("Apostas.csv", index=False)
#df_tabela.to_csv("Apostas.csv", index=False)
