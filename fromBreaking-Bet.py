columns = ['id', 'data_entrada', 'data_jogo', 'time_casa', 'time_fora', 'bethouse1', 'mercado1', 'valor1', 'odd1',
           'aposta1', 'resultado1', 'bethouse2', 'mercado2', 'valor2', 'odd2', 'aposta2', 'resultado2', 'bethouse3',
           'mercado3', 'valor3', 'odd3', 'aposta3', 'resultado3', 'lucro_estimado', 'lucro_per_estimado', 'lucro_real',
           'lucro_per_real', 'esporte']

import pandas as pd
import numpy as np

# Caminho para o arquivo CSV
caminho_arquivo = "./bb_history.csv"


bb_history = pd.read_csv(caminho_arquivo, sep=';')

# Excluindo todas as linhas onde todas as colunas estão vazias
bb_history.dropna(how='all', inplace=True)

# Preenchendo os valores vazios na primeira coluna com os valores das linhas anteriores
#bb_history['#'] = bb_history['#'].astype(int)
bb_history['date'] = bb_history['date'].ffill()

# Convertendo os valores da coluna 'date' para o formato desejado
bb_history['date'] = pd.to_datetime(bb_history['date'], format='%d/%m/%Y %H:%M')
bb_history = bb_history.rename(columns={'date': 'data_entrada'})

# Extrair informações das colunas existentes para criar novas colunas
bb_history['time_casa'] = bb_history['event'].str.split(' - ').str[0]
bb_history['time_fora_sport'] = bb_history['event'].str.split(' - ').str[1].str.split('.').str[0]
bb_history['time_fora'] = bb_history['time_fora_sport'].str.rsplit(' ', n=1).str[0]
bb_history['esporte'] = bb_history['time_fora_sport'].str.split().str[-1]
bb_history['data_jogo'] = bb_history['event'].str.extract('(2024.*)')
#bb_history['data_jogo'].fillna(method='ffill', inplace=True)
bb_history['data_jogo'] = bb_history['data_jogo'].str.replace('2024 ', '', regex=False)
bb_history['data_jogo'] = pd.to_datetime(bb_history['data_jogo'], format='%Y-%m-%d %H:%M')
bb_history['market'] = bb_history['odd'].str.split(' = ').str[0]
bb_history['odd'] = bb_history['odd'].str.split(' = ').str[1]

# Separar mercado de valor
# Filtrar as linhas que terminam com "(XX)"
filtered_rows = bb_history['market'].str.contains(r'\(-?\d+(\.\d+)?\)$')
# Aplicar a regra apenas nessas linhas
bb_history.loc[filtered_rows, 'market_value'] = bb_history.loc[filtered_rows, 'market'].str.split('(').str[-1].str.split(')').str[0]
bb_history.loc[filtered_rows, 'market'] = bb_history.loc[filtered_rows, 'market'].str.split('(').str[0]


bb_history = bb_history[['#', 'data_entrada', 'market', 'market_value', 'odd', 'bookie', 'bet',
    'time_casa', 'time_fora', 'esporte', 'data_jogo']]
bb_history = bb_history.rename(columns={'#': 'id', 'bookie': 'bethouse1', 'market': 'mercado1', 'market_value': 'valor1', 'odd': 'odd1', 'bet': 'aposta1'})

# Adiciona as novas colunas
novas_colunas = ['resultado1', 'bethouse2', 'mercado2', 'valor2', 'odd2', 'aposta2', 'resultado2', 'bethouse3', 'mercado3', 'valor3', 'odd3', 'aposta3', 'resultado3', 'lucro_estimado', 'lucro_per_estimado', 'lucro_real', 'lucro_per_real']
for coluna in novas_colunas:
    bb_history[coluna] = np.nan

# Dicionário de substituição
substitution_dict = {
    'LAY ': 'Lay',
    'Draw No Bet: 1st team': 'DNB1',
    'Draw No Bet: 2nd team': 'DNB2',
    '2-way: Handicap/Spread 1st team': 'AH1',
    '2-way: Handicap/Spread 2nd team': 'AH2',
    'Total Over 1st team': 'TO1',
    'Total Over 2nd team': 'TO2',
    'Total Over': 'TO',
    'Total Under 1st team': 'TU1',
    'Total Under 2nd team': 'TU2',
    'Total Under': 'TU',
    '3-way: 1st team win': '1',
    '3-way: 2nd team win': '2',
    '3-way: draw': 'X',
    'To qualify 1st team': 'Q1',
    'To qualify 2nd team': 'Q2',
    'Not score both': 'Not',
    'Score both teams': 'ScoreBoth',
    'Double chance: draw or 2nd': 'X2',
    'Double chance: 1st team win or draw': '1X',
    'Double chance: 1st team win or 2nd': '12',
    'Clean sheet 1st': 'CleanSheet1',
    'Clean sheet 2nd': 'CleanSheet2',
    'Score 2nd team': 'TO2',
    '3-way: European Handicap/Spread 1st team': 'EH1',
    '3-way: European Handicap/Spread 2nd team': 'EH2',
    '3-way: European Handicap/Spread Draw': 'EHX'
}

# Função para fazer a substituição total
def replace_with_rule(s):
    for pattern, replacement in substitution_dict.items():
        if pattern in s:
            return replacement
    return s

# Aplicar substituição
bb_history['mercado1'] = bb_history['mercado1'].apply(replace_with_rule)

bb_history.reset_index(drop=True, inplace=True)

# Iterar sobre as linhas do DataFrame
for index, row in bb_history.iterrows():
    # Verifica se o 'id' é NaN
    if pd.isna(row['id']):
        # Verifica se o índice - 1 está presente no índice do DataFrame
        if (index - 1) in bb_history.index:
            if pd.isna(bb_history.loc[index - 1, 'bethouse2']):
                # Copiar valores da linha atual para a linha anterior
                #bb_history.loc[index - 1, ['bethouse2', 'mercado2', 'valor2', 'odd2', 'aposta2']] = row[['bethouse1', 'mercado1', 'valor1', 'odd1', 'aposta1']]
                bb_history.loc[index - 1, 'bethouse2'] = row['bethouse1']
                bb_history.loc[index - 1, 'mercado2'] = row['mercado1']
                bb_history.loc[index - 1, 'valor2'] = row['valor1']
                bb_history.loc[index - 1, 'odd2'] = row['odd1']
                bb_history.loc[index - 1, 'aposta2'] = row['aposta1']
            else:
                # Copiar valores da linha atual para a linha anterior
                #bb_history.loc[index - 1, ['bethouse3', 'mercado3', 'valor3', 'odd3', 'aposta3']] = row[['bethouse1', 'mercado1', 'valor1', 'odd1', 'aposta1']]
                bb_history.loc[index - 1, 'bethouse3'] = row['bethouse1']
                bb_history.loc[index - 1, 'mercado3'] = row['mercado1']
                bb_history.loc[index - 1, 'valor3'] = row['valor1']
                bb_history.loc[index - 1, 'odd3'] = row['odd1']
                bb_history.loc[index - 1, 'aposta3'] = row['aposta1']

        else:
            if pd.isna(bb_history.loc[index - 2, 'bethouse2']):
                # Copiar valores da linha atual para a segunda linha anterior
                #bb_history.loc[index - 2, ['bethouse2', 'mercado2', 'valor2', 'odd2', 'aposta2']] = row[['bethouse1', 'mercado1', 'valor1', 'odd1', 'aposta1']]
                bb_history.loc[index - 2, 'bethouse2'] = row['bethouse1']
                bb_history.loc[index - 2, 'mercado2'] = row['mercado1']
                bb_history.loc[index - 2, 'valor2'] = row['valor1']
                bb_history.loc[index - 2, 'odd2'] = row['odd1']
                bb_history.loc[index - 2, 'aposta2'] = row['aposta1']

            else:
                # Copiar valores da linha atual para bethouse3, mercado3, valor3, odd3 e aposta3
                #bb_history.loc[index - 2, ['bethouse3', 'mercado3', 'valor3', 'odd3', 'aposta3']] = row[['bethouse1', 'mercado1', 'valor1', 'odd1', 'aposta1']]
                bb_history.loc[index - 2, 'bethouse3'] = row['bethouse1']
                bb_history.loc[index - 2, 'mercado3'] = row['mercado1']
                bb_history.loc[index - 2, 'valor3'] = row['valor1']
                bb_history.loc[index - 2, 'odd3'] = row['odd1']
                bb_history.loc[index - 2, 'aposta3'] = row['aposta1']

        # Excluir a linha atual
        bb_history.drop(index, inplace=True)

# Reindexar o DataFrame após excluir linhas
bb_history.reset_index(drop=True, inplace=True)

# Organizar as colunas por ordem crescente de data_entrada
bb_history = bb_history.sort_values(by='data_entrada')
#print(bb_history['data_entrada'].value_counts()[bb_history['data_entrada'].value_counts() > 3])
# Substituir os valores de '#' por um ID único
current_date = None
counter = 0

for index, row in bb_history.iterrows():
    if not pd.isnull(row['id']):  # Ignorar linhas vazias
        date_bet = row['data_entrada'].date()  # Pegar apenas a parte da data
        if date_bet != current_date:
            current_date = date_bet
            counter = 1
        else:
            counter += 1
        new_id = date_bet.strftime('%Y%m%d') + str(counter).zfill(3)
        bb_history.at[index, 'id'] = new_id

bb_history = bb_history.sort_values(by='data_entrada', ascending=False)
bb_history['id'].fillna(method='ffill', inplace=True)
bb_history = bb_history.sort_values(by='data_entrada')

bb_history = bb_history[['id', 'data_entrada', 'data_jogo', 'time_casa', 'time_fora', 'bethouse1', 'mercado1', 'valor1', 'odd1',
           'aposta1', 'resultado1', 'bethouse2', 'mercado2', 'valor2', 'odd2', 'aposta2', 'resultado2', 'bethouse3',
           'mercado3', 'valor3', 'odd3', 'aposta3', 'resultado3', 'lucro_estimado', 'lucro_per_estimado', 'lucro_real',
           'lucro_per_real', 'esporte']]

def convert_to_float(value):
    # Verifica se o valor é uma string
    if isinstance(value, str):
        # Divide a string pelo ponto decimal
        parts = value.split('.')
        # Se houver mais de um ponto decimal
        if len(parts) > 2:
            # Reúne a primeira parte (antes do primeiro ponto) e a segunda parte (as duas primeiras casas decimais após o primeiro ponto)
            return float('.'.join(parts[:2]))
    # Retorna o valor original se não for possível converter
    return float(value)

# Aplica a função convert_to_float às colunas relevantes
bb_history['aposta1'] = bb_history['aposta1'].apply(convert_to_float)
bb_history['aposta2'] = bb_history['aposta2'].apply(convert_to_float)
bb_history['aposta3'] = bb_history['aposta3'].apply(convert_to_float)
bb_history['odd1'] = bb_history['odd1'].apply(convert_to_float)
bb_history['odd2'] = bb_history['odd2'].apply(convert_to_float)
bb_history['odd3'] = bb_history['odd3'].apply(convert_to_float)

# Aplicar a fórmula onde bethouse3 é NaN
bb_history.loc[pd.isna(bb_history['bethouse3']), 'lucro_estimado'] = ((bb_history['aposta1'] * bb_history['odd1'] - bb_history['aposta1'] - bb_history['aposta2']) + (bb_history['aposta2'] * bb_history['odd2'] - bb_history['aposta1'] - bb_history['aposta2'])) / 2

# Aplicar a fórmula onde bethouse3 não é NaN
bb_history.loc[~pd.isna(bb_history['bethouse3']), 'lucro_estimado'] = bb_history['aposta1'] * bb_history['odd1'] - bb_history['aposta1'] - bb_history['aposta2'] - bb_history['aposta3']

# Calcular lucro_per_estimado onde bethouse3 é NaN
bb_history.loc[pd.isna(bb_history['bethouse3']), 'lucro_per_estimado'] = bb_history['lucro_estimado'] - bb_history['aposta1'] - bb_history['aposta2']

# Calcular lucro_per_estimado onde bethouse3 não é NaN
bb_history.loc[~pd.isna(bb_history['bethouse3']), 'lucro_per_estimado'] = bb_history['lucro_estimado'] - bb_history['aposta1'] - bb_history['aposta2'] - bb_history['aposta3']

#print(bb_history.columns)
#print(bb_history['market_value'].unique())

bb_history.to_csv('apostas_BB.csv', index=False, sep=';')

