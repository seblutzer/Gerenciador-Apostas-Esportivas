import pandas as pd
import datetime
from datetime import datetime as dt
import random
from Pacotes_Lutzer.convert import convert_mes
import sqlite3

def excel_to_csv():
    results = [('Baseball', 8), ('Basquetebol', 13), ('Dardos', 2), ('E-Sports', 41), ('Futebol', 516), ('Futsal', 1),
               ('Handball', 8), ('Hockey', 2), ('Rugby', 4), ('Tênis', 63), ('Tênis de Mesa', 1), ('Voleibol', 10)]
    my_list = [esporte for esporte, count in results for _ in range(count)]

    meses = {}
    meses['abril23'] = pd.read_excel('Bolsa Esportiva Abril 2023.xlsx')
    meses['março23'] = pd.read_excel('Bolsa Esportiva Março 2023.xlsx')
    meses['fevereiro23'] = pd.read_excel('Bolsa Esportiva Fevereiro 2023.xlsx')
    meses['janeiro23'] = pd.read_excel('Bolsa Esportiva Janeiro 2023.xlsx')
    meses['outubro22'] = pd.read_excel('Bolsa Esportiva ano 2022.xlsx', sheet_name='Outubro 2022')
    meses['setembro22'] = pd.read_excel('Bolsa Esportiva ano 2022.xlsx', sheet_name='Setembro 2022')
    meses['agosto22'] = pd.read_excel('Bolsa Esportiva ano 2022.xlsx', sheet_name='Agosto 2022')
    meses['julho22'] = pd.read_excel('Bolsa Esportiva ano 2022.xlsx', sheet_name='Julho 2022')
    meses['junho22'] = pd.read_excel('Bolsa Esportiva ano 2022.xlsx', sheet_name='Junho 2022')
    meses['maio22'] = pd.read_excel('Bolsa Esportiva ano 2022.xlsx', sheet_name='Maio 2022')
    meses['abril22'] = pd.read_excel('Bolsa Esportiva ano 2022.xlsx', sheet_name='Abril 2022')
    meses['agosto21'] = pd.read_excel('Bolsa Esportiva ano 2022.xlsx', sheet_name='Agosto 2021')
    meses['julho21'] = pd.read_excel('Bolsa Esportiva ano 2022.xlsx', sheet_name='Julho 2021')

    dfs = {}
    dic_mov = {}
    padroes = ['acerto de contas', 'acerto de contas diário', 'acerto de contas diario', 'acerto de contas semanal', 'acerto de contas mensal']
    #excels = {'julho21': 2021, 'agosto21': 2021, 'abril22': 2022, 'maio22': 2022, 'junho22': 2022, 'julho22': 2022, 'agosto22': 2022, 'setembro22': 2022, 'outubro22': 2022, 'janeiro23': 2023, 'fevereiro23': 2023, 'março23': 2023, 'abril23': 2023}
    excels = {'julho21': 2021, 'agosto21': 2021, 'abril22': 2022, 'maio22': 2022, 'junho22': 2022, 'julho22': 2022, 'agosto22': 2022, 'setembro22': 2022, 'outubro22': 2022, 'janeiro23': 2023, 'fevereiro23': 2023, 'março23': 2023, 'abril23': 2023}



    for mes in excels.keys():
        meses[mes] = meses[mes].iloc[:, :21]

        # Cabeçalho desejado
        cabecalho = ['numero_aposta', 'status', 'resultado', 'dia', 'num_dia', 'vencimento', 'data_jogo', 'times', 'mercado', 'valor', 'bethouse', 'odd', 'stake', 'arred', 'aposta', 'retorno', 'apo_hoje', 'aberta', 'lucro_estimado', 'lucrp_per_estimado', 'lucro_real']

        # Substituir as duas primeiras linhas pelo cabeçalho
        meses[mes] = meses[mes].iloc[2:].reset_index(drop=True)
        meses[mes].columns = cabecalho

        # Excluir todas as outras colunas
        meses[mes] = meses[mes][cabecalho]

        colunas_para_excluir = ['numero_aposta', 'status', 'num_dia', 'stake', 'vencimento', 'arred', 'retorno', 'apo_hoje', 'aberta']
        meses[mes] = meses[mes].drop(colunas_para_excluir, axis=1)
        columns_to_fill = ['dia', 'data_jogo', 'times', 'lucro_estimado', 'lucrp_per_estimado', 'lucro_real']
        meses[mes][columns_to_fill] = meses[mes][columns_to_fill].fillna(method='ffill')

        # Filtrar as linhas com os padrões e adicionar ao dic_mov[mes]
        dic_mov[mes] = meses[mes][meses[mes]['times'].str.lower().isin(padroes)]

        # Excluir as linhas do meses[mes]
        meses[mes] = meses[mes][~meses[mes]['times'].str.lower().isin(padroes)].reset_index(drop=True)

        ano = excels[mes]
        nome_mes = mes[:3]
        month = convert_mes(nome_mes)
        hora_inicial = datetime.time(4, 0, 0)
        incremento_tempo = datetime.timedelta(minutes=20)
        linhas_por_registro = 3

        dfs[f'df_{mes}'] = pd.DataFrame(columns=['id', 'data_entrada', 'data_jogo', 'time_casa', 'time_fora', 'bethouse1', 'mercado1',
                                         'valor1', 'odd1', 'aposta1', 'resultado1', 'bethouse2', 'mercado2', 'valor2', 'odd2',
                                         'aposta2', 'resultado2', 'bethouse3', 'mercado3', 'valor3', 'odd3', 'aposta3',
                                         'resultado3', 'lucro_estimado', 'lucro_per_estimado', 'lucro_real', 'lucro_per_real',
                                         'esporte'])

        for i in range(0, len(meses[mes]), linhas_por_registro):
            if i == 0 or meses[mes]['dia'][i] != meses[mes]['dia'][i - 1]:
                contador_dia = 1
            else:
                contador_dia += 1

            id = f"{ano}{month:02}{int(meses[mes]['dia'][i]):02}{contador_dia:03}"
            data_entrada = datetime.datetime(int(ano), int(month), int(meses[mes]['dia'][i]), hora_inicial.hour, hora_inicial.minute,
                                             hora_inicial.second) + datetime.timedelta(minutes=(i // linhas_por_registro) * 20)
            data_jogo = meses[mes]['data_jogo'][i]

            #data_jogo = dt.strptime(data_jogo, "%d %b %Y %H:%M").strftime("%Y-%m-%d %H:%M:%S")
            meses_portugues = {
                'jan': 'Jan',
                'fev': 'Feb',
                'mar': 'Mar',
                'abr': 'Apr',
                'mai': 'May',
                'jun': 'Jun',
                'jul': 'Jul',
                'ago': 'Aug',
                'set': 'Sep',
                'out': 'Oct',
                'nov': 'Nov',
                'dez': 'Dec'
            }

            data_extraida = "20 abr 2022 21:00"
            data_jogo_parts = data_extraida.split()

            mes_portugues = data_jogo_parts[1]
            mes_ingles = meses_portugues.get(mes_portugues.lower())

            if mes_ingles:
                data_jogo_parts[1] = mes_ingles

            data_jogo = dt.strptime(' '.join(data_jogo_parts), "%d %b %Y %H:%M").strftime(
                "%Y-%m-%d %H:%M:%S")

            times = meses[mes]['times'][i].split(' - ')
            time_casa = times[0]
            time_fora = times[-1]
            bethouse1 = meses[mes]['bethouse'][i]
            mercado1 = meses[mes]['mercado'][i]
            valor1 = meses[mes]['valor'][i]
            odd1 = meses[mes]['odd'][i]
            aposta1 = round(meses[mes]['aposta'][i], 2)
            resultado1 = meses[mes]['resultado'][i]
            bethouse2 = meses[mes]['bethouse'][i + 1]
            mercado2 = meses[mes]['mercado'][i + 1]
            valor2 = meses[mes]['valor'][i + 1]
            odd2 = meses[mes]['odd'][i + 1]
            aposta2 = round(meses[mes]['aposta'][i + 1], 2)
            resultado2 = meses[mes]['resultado'][i + 1]
            bethouse3 = meses[mes]['bethouse'][i + 2]
            mercado3 = meses[mes]['mercado'][i + 2]
            valor3 = meses[mes]['valor'][i + 2]
            odd3 = meses[mes]['odd'][i + 2]
            aposta3 = round(meses[mes]['aposta'][i + 2], 2)
            resultado3 = meses[mes]['resultado'][i + 2]
            lucro_estimado = round(meses[mes]['lucro_estimado'][i], 2)
            lucro_per_estimado = round(meses[mes]['lucrp_per_estimado'][i], 4)
            lucro_real = round(lucro_estimado, 2)
            lucro_per_real = 0
            esporte = None

            # Atribuir os valores corretos para resultado1, resultado2 e resultado3
            if resultado1 == 'W':
                resultado1 = 'win'
            elif resultado1 == 'L':
                resultado1 = 'loss'
            elif resultado1 == 'X':
                resultado1 = 'return'
            elif resultado1 == '1/2L':
                resultado1 = 'half-loss'
            elif resultado1 == '1/2W':
                resultado1 = 'half-win'

            if resultado2 == 'W':
                resultado2 = 'win'
            elif resultado2 == 'L':
                resultado2 = 'loss'
            elif resultado2 == 'X':
                resultado2 = 'return'
            elif resultado2 == '1/2L':
                resultado2 = 'half-loss'
            elif resultado2 == '1/2W':
                resultado2 = 'half-win'

            if resultado3 == 'W':
                resultado3 = 'win'
            elif resultado3 == 'L':
                resultado3 = 'loss'
            elif resultado3 == 'X':
                resultado3 = 'return'
            elif resultado3 == '1/2L':
                resultado3 = 'half-loss'
            elif resultado3 == '1/2W':
                resultado3 = 'half-win'

            dfs[f'df_{mes}'].loc[len(dfs[f'df_{mes}'])] = {'id': id, 'data_entrada': data_entrada, 'data_jogo': data_jogo,
                                           'time_casa': time_casa, 'time_fora': time_fora, 'bethouse1': bethouse1,
                                           'mercado1': mercado1, 'valor1': valor1, 'odd1': odd1, 'aposta1': aposta1,
                                           'resultado1': resultado1, 'bethouse2': bethouse2, 'mercado2': mercado2,
                                           'valor2': valor2, 'odd2': odd2, 'aposta2': aposta2, 'resultado2': resultado2,
                                           'bethouse3': bethouse3, 'mercado3': mercado3, 'valor3': valor3, 'odd3': odd3,
                                           'aposta3': aposta3, 'resultado3': resultado3, 'lucro_estimado': lucro_estimado,
                                           'lucro_per_estimado': lucro_per_estimado, 'lucro_real': lucro_real,
                                           'lucro_per_real': lucro_per_real, 'esporte': esporte}

        dfs[f'df_{mes}']['lucro_per_real'] = round(dfs[f'df_{mes}']['lucro_real'] / (dfs[f'df_{mes}']['aposta1'] + dfs[f'df_{mes}']['aposta2'] + (dfs[f'df_{mes}']['aposta3'] if pd.notna(dfs[f'df_{mes}']['aposta3'].values[0]) else 0)), 4)

        dfs[f'df_{mes}']['esporte'] = dfs[f'df_{mes}']['esporte'].apply(lambda x: random.choice(my_list))

    # Crie uma lista para armazenar todos os DataFrames
    dfs_list = []

    # Itere sobre os DataFrames do dicionário e adicione-os à lista
    for df_key in dfs:
        dfs_list.append(dfs[df_key])

    # Concatene os DataFrames da lista em um único DataFrame
    merged_df = pd.concat(dfs_list)

    # Escreva o DataFrame resultante em um arquivo CSV
    merged_df.to_csv('apostas_antigas2.csv', index=False, sep=';')

    #print(dfs)
    #print(dfs['df_maio22'][['aposta1', 'aposta2', 'aposta3', 'lucro_estimado', 'lucro_per_estimado', 'lucro_real']])
    #print(dic_mov)

#excel_to_csv()

# Lê o arquivo CSV
df_apostas_antigas = pd.read_csv('apostas_antigas2.csv')

# Conecta-se ao banco de dados
conn = sqlite3.connect('dados.db')

# Escreve os dados no banco de dados
df_apostas_antigas.to_sql('apostas', conn, if_exists='append', index=False)

# Ordena a tabela por data_entrada
df_apostas_ordenadas = pd.read_sql_query('SELECT * FROM apostas ORDER BY data_entrada', conn)

# Reescreve a tabela em ordem de data_entrada
df_apostas_ordenadas.to_sql('apostas', conn, if_exists='replace', index=False)

# Fecha a conexão com o banco de dados
conn.close()

# Contar células em branco em cada coluna
celulas_em_branco = df_apostas_antigas.isna().sum()

# Imprimir o resultado
print(celulas_em_branco)

# Encontrar a linha em que 'bethouse1' está em branco
linha_branco = df_apostas_antigas[df_apostas_antigas['resultado3'] == ' ']
linha_branco
# Imprimir o resultado
print(linha_branco)

#print(df_apostas_antigas['resultado3'].tail(50))