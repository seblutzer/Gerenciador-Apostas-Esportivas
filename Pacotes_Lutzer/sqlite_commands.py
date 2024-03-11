import pandas as pd
import json
import os
import sqlite3
import re
import datetime
from datetime import date, datetime, timedelta
from Pacotes_Lutzer.convert import convert_mes

import random

global bethouse_options_total
sql_data = '/Users/Sérgio/PycharmProjects/Gerenciador-Apostas-Esportivas/dados.db'
with open('/Users/Sérgio/PycharmProjects/Gerenciador-Apostas-Esportivas/bethouse_options.json', 'r') as f:
    data = json.load(f)
    bethouse_options_total = data.get("bethouse_options", {})
conn = sqlite3.connect(sql_data)
c = conn.cursor()
def apostas_to_tabelas(sql = True):
    sql = True
    dados = pd.read_csv('/Users/Sérgio/PycharmProjects/Gerenciador-Apostas-Esportivas/apostas_antigas.csv')
    with open('/Users/Sérgio/PycharmProjects/Gerenciador-Apostas-Esportivas/bethouse_options.json', 'r') as f:
        data = json.load(f)
        bethouse_options = data.get("bethouse_options", {})

    def calculate_balance(row, num=''):
        odd = row[f'odd{num}']
        aposta = row[f'aposta{num}']
        resultado = row[f'resultado{num}']
        taxa = bethouse_options[row[f'bethouse{num}']]['taxa']
        odd_real = (odd - 1) * (1 - taxa) + 1 if row[f'mercado{num}'] != 'Lay' else (odd / (odd - 1) - 1) * (
                1 - taxa) + 1
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

    if sql:
        conn = sqlite3.connect(sql_data)  # Conectar ao banco de dados SQLite
        cursor = conn.cursor()  # Criar um cursor para executar comandos SQL
        print(len(dados))
        for i in range(len(dados)):
            for j in range(1, 4 if dados['bethouse3'].iloc[i] in bethouse_options.keys() else 3):
                bethouse_key = dados[f'bethouse{j}'].iloc[i]
                if bethouse_key in bethouse_options.keys():
                    odd = dados[f'odd{j}'].iloc[i]
                    odd = "{:.3f}".format(odd).rstrip('0').rstrip('.')
                    odd_real = round((float(odd) - 1) * (1 - bethouse_options[bethouse_key]['taxa']) + 1, 2) if \
                        dados[f'mercado{j}'].iloc[i] != 'Lay' else round(
                        (float(odd) / (float(odd) - 1) - 1) * (1 - bethouse_options[bethouse_key]['taxa']) + 1, 2)
                    odd_real = "{:.3f}".format(odd_real).rstrip('0').rstrip('.')

                    # Modificar o nome da tabela substituindo caracteres não permitidos por sublinhado (_)
                    table_name = f"{bethouse_key}_saldos"
                    table_name = re.sub(r'\W+', '_', table_name)
                    if table_name[0].isdigit():
                        table_name = f'_{table_name}'

                    # Verificar se a tabela já existe no banco de dados
                    check_table_query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
                    cursor.execute(check_table_query)
                    result = cursor.fetchone()

                    if result is None:
                        # A tabela não existe, criar a tabela
                        create_table_query = f'''
                        CREATE TABLE "{table_name}" (
                            id INTEGER,
                            data_entrada TEXT,
                            data_fim TEXT,
                            odd TEXT,
                            aposta REAL,
                            resultado TEXT,
                            balanco REAL,
                            dif_real REAL
                        )
                        '''
                        cursor.execute(create_table_query)

                    # Inserir os valores na tabela
                    insert_query = f'''
                    INSERT INTO "{table_name}" (id, data_entrada, data_fim, odd, aposta, resultado, balanco, dif_real)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    '''
                    values = (
                        int(dados['id'].iloc[i]),
                        dados['data_entrada'].iloc[i],
                        dados['data_jogo'].iloc[i],
                        odd,
                        round(dados[f'aposta{j}'].iloc[i], 2),
                        dados[f'resultado{j}'].iloc[i],
                        round(calculate_balance(dados.iloc[i], j), 2),
                        round(calculate_balance(dados.iloc[i], j), 2) if pd.notna(dados[f'resultado{j}'].iloc[i]) else 0
                    )
                    cursor.execute(insert_query, values)

        conn.commit()  # Salvar as alterações no banco de dados
        conn.close()  # Fechar a conexão com o banco de dados


    else:
        bethouse_dataframes = {}
        bethouse_keys = list(bethouse_options.keys())

        for i in range(len(dados)):
            for j in range(1, 4 if dados['bethouse3'].iloc[i] in bethouse_options.keys() else 3):
                bethouse_key = dados[f'bethouse{j}'].iloc[i]
                if bethouse_key in bethouse_keys:
                    odd = dados[f'odd{j}'].iloc[i]
                    odd = "{:.3f}".format(odd).rstrip('0').rstrip('.')
                    odd_real = round((float(odd) - 1) * (1 - bethouse_options[bethouse_key]['taxa']) + 1, 2) if dados[f'mercado{j}'].iloc[i] != 'Lay' else round((float(odd) / (float(odd) - 1) - 1) * (1 - bethouse_options[bethouse_key]['taxa']) + 1, 2)
                    odd_real = "{:.3f}".format(odd_real).rstrip('0').rstrip('.')
                    df = pd.DataFrame({
                        'id': [dados['id'].iloc[i]],
                        'data_entrada': [dados['data_entrada'].iloc[i]],
                        'data_fim': [dados['data_jogo'].iloc[i]],
                        'bethouse': [bethouse_key],
                        'odd': odd,
                        'odd_real': odd_real,
                        'aposta': [round(dados[f'aposta{j}'].iloc[i], 2)],
                        'resultado': [dados[f'resultado{j}'].iloc[i]],
                        'balanco': [round(calculate_balance(dados.iloc[i], j), 2)],
                        'dif_real': [round(calculate_balance(dados.iloc[i], j), 2)] if pd.notna(dados[f'resultado{j}'].iloc[i]) else [0]
                    })
                    if bethouse_key in bethouse_dataframes:
                        bethouse_dataframes[bethouse_key] = pd.concat([bethouse_dataframes[bethouse_key], df], ignore_index=True)
                    else:
                        bethouse_dataframes[bethouse_key] = df

        # Caminho para o diretório de destino
        dest_dir = 'dados_bethouses'

        # Verifica se o diretório existe, caso contrário, cria
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        # Escreve cada dataframe em um arquivo CSV
        for bethouse_key, dataframe in bethouse_dataframes.items():
            file_name = f"{bethouse_key}_apostas.csv"
            file_path = os.path.join(dest_dir, file_name)
            dataframe.to_csv(file_path, index=False)

#apostas_to_tabelas()

def to_sql(dados, nome_tabela, arquivo_retorno, data_type='dataframe', index=False, if_exists='replace'):
    if data_type == 'csv':
        # Ler o arquivo CSV
        dados = pd.read_csv(dados)

    # Conectar ao banco de dados
    conn = sqlite3.connect(f'{arquivo_retorno}.db')

    # Nome da tabela
    table_name = nome_tabela

    # Inserir os dados no banco de dados
    cursor = conn.cursor()

    # Criar a tabela no banco de dados com as colunas e tipos desejados
    create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER,
            data_entrada DATETIME,
            data_jogo DATETIME,
            time_casa TEXT
            time_fora TEXT,
            bethouse1 TEXT,
            mercado1 TEXT,
            valor1 REAL,
            odd1 REAL,
            aposta1 REAL,
            resultado1 TEXT,
            bethouse2 TEXT,
            mercado2 TEXT,
            valor2 REAL,
            odd2 REAL,
            aposta2 REAL,
            resultado2 TEXT,
            bethouse3 TEXT,
            mercado3 TEXT,
            valor3 REAL,
            odd3 REAL,
            aposta3 REAL,
            resultado3 TEXT,
            lucro_estimado REAL,
            lucro_per_estimado REAL,
            lucroReal REAL,
            lucro_perReal REAL,
            esporte TEXT
        )
        '''
    cursor.execute(create_table_query)

    # Inserir os dados na tabela
    dados.to_sql(table_name, conn, if_exists=if_exists, index=index)

    # Fechar a conexão com o banco de dados
    conn.close()
#apostascsv = '/Users/sergioeblutzer/PycharmProjects/Gerenciamento_Bolsa_Esportiva/Apostas.csv'
#to_sql(apostascsv, 'apostas', 'dados', data_type='csv', index=False, if_exists='replace')


def filter_column(sql_data, sql_table, table_column=None, operation=None, filter=None):
    con = sqlite3.connect(sql_data)
    if table_column==None or operation==None or filter==None:
        query = f"SELECT esporte FROM {sql_table}"
        #query = f"SELECT valor1 FROM {sql_table} WHERE valor1 = ''"
    else:
        query = f"SELECT * FROM {sql_table} WHERE {table_column} {operation} {filter}"
    df = pd.read_sql_query(query, con)
    df = df['esporte'].unique()

    print(df)

    con.close()

#filter_column(sql_data, 'apostas')#, table_column='resultado1', operation='!=', filter="'win'")
def view_tables(sql_data):
    # Conectar ao banco de dados
    conn = sqlite3.connect(sql_data)
    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()

    # Executar a consulta SQL para obter todas as tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

    # Obter os resultados da consulta
    tables = cursor.fetchall()

    # Imprimir o nome de cada tabela
    for table in tables:
        print(table[0])

    # Fechar a conexão com o banco de dados
    conn.close()

#view_tables(dados)

def view_column(sql_data, table):
    # Conectar ao banco de dados
    conn = sqlite3.connect(sql_data)

    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()

    # Obter as informações das colunas da tabela
    cursor.execute(f"PRAGMA table_info({table})")

    # Recuperar os resultados
    results = cursor.fetchall()

    # Exibir as informações das colunas
    for row in results:
        print(row[1])

    # Fechar a conexão com o banco de dados
    conn.close()

#view_column(dados, 'apostas')

def del_column(sql_data, table, column_name):
    # Conectar ao banco de dados
    conn = sqlite3.connect(sql_data)

    cursor = conn.cursor()

    # Executar a instrução SQL para remover a coluna
    alter_query = f"ALTER TABLE {table} DROP COLUMN {column_name}"
    cursor.execute(alter_query)

    # Commit das alterações e fechamento da conexão
    conn.commit()
    conn.close()

#del_column(dados, 'apostas', 'data_entrada_datetime')

def edit_column(sql_data, table, column, edition, editable):
    # Conectar ao banco de dados
    conn = sqlite3.connect(sql_data)

    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()

    # Executar a consulta SQL para atualizar os valores das colunas

    cursor.execute(f"UPDATE {table} SET {column} = {edition} WHERE {column} = '{editable}'")
    #cursor.execute(f"UPDATE apostas SET mercado1 = 'Not ScoreBoth' WHERE ID = 20230626039")
    # Confirmar as alterações no banco de dados

    conn.commit()

    # Fechar a conexão com o banco de dados
    conn.close()
#edit_column(sql_data, 'apostas', 'valor3', 'NULL', '')


def del_line(sql_data, table, limit=1, id='last'):
    # Conectar ao banco de dados
    conn = sqlite3.connect(sql_data)
    cursor = conn.cursor()
    if id == 'last':
        # Executar a instrução SQL para excluir a última linha
        delete_query = f"DELETE FROM {table} WHERE id = (SELECT id FROM apostas ORDER BY id DESC LIMIT {limit})"
        cursor.execute(delete_query)
    else:
        # Executar a instrução SQL para excluir a última linha
        delete_query = f"DELETE FROM {table} WHERE id = {id}"
        cursor.execute(delete_query)

    # Commit das alterações e fechamento da conexão
    conn.commit()
    conn.close()
#del_line(dados, 'apostas', 1)

def view_last_lines(sql_data, table, limit):
    # Conectar ao banco de dados
    conn = sqlite3.connect(sql_data)
    cursor = conn.cursor()

    # Executar a instrução SQL para selecionar as três últimas linhas
    select_query = f"SELECT * FROM {table} ORDER BY data_entrada DESC LIMIT {limit}"
    cursor.execute(select_query)

    # Recuperar os resultados da consulta
    rows = cursor.fetchall()

    # Exibir as três últimas linhas
    print(f'\nUltimas {limit} linhas de {table} são:')
    for row in rows:
        print(row)
    # Fechamento da conexão
    conn.close()

def add_aposta_individual(sql_data, table, dados):
    import sqlite3

    # Conectar ao banco de dados
    conn = sqlite3.connect(sql_data)
    cursor = conn.cursor()

    # Verificar se a tabela já existe no banco de dados
    check_table_query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'"
    cursor.execute(check_table_query)
    result = cursor.fetchone()

    if result is None:
        # A tabela não existe, criar a tabela
        create_table_query = '''
        CREATE TABLE "{table}" (
            id INTEGER,
            data_entrada DATETIME,
            data_fim DATETIME,
            bethouse TEXT,
            odd TEXT,
            odd_real TEXT,
            aposta REAL,
            resultado TEXT,
            balanco REAL,
            dif_real REAL
        )
        '''
        cursor.execute(create_table_query)

    # Inserir os valores na tabela
    insert_query = '''
    INSERT INTO "Pinnacle_apostas" (id, data_entrada, data_fim, bethouse, odd, odd_real, aposta, resultado, balanco, dif_real)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    values = (
        dados['id'],
        dados['data_entrada'],
        dados['data_fim'],
        dados['bethouse'],
        dados['odd'],
        dados['odd_real'],
        dados['aposta'],
        dados['resultado'],
        dados['balanco'],
        dados['dif_real']
    )
    cursor.execute(insert_query, values)

    # Commit das alterações e fechamento da conexão
    conn.commit()
    conn.close()

def filter(sql_data, sql_table, table_column=None, operation=None, filter=None):
    conn = sqlite3.connect(sql_data)
    c = conn.cursor()
    table_name = f"{sql_table}_saldos"
    table_name = re.sub(r'\W+', '_', table_name)
    if table_name[0].isdigit():
        table_name = f'_{table_name}'
    if table_column==None or operation==None or filter==None:
        query = "SELECT data_entrada, balanco, resultado FROM PinUp_saldos WHERE data_entrada >= DATE('2023-07-08', '-30 days')"

        # Recuperar os resultados da consulta
        #resultados = c.fetchall()

        # Imprimir os valores
        #for resultado in resultados:
        #    print(resultado[0])

        #query = f"SELECT * FROM apostas"# WHERE resultado IS NULL"# WHERE DATE(data_entrada) >= '2021-01-01' AND DATE(data_entrada) < '2022-01-01' ORDER BY data_entrada ASC"
    else:
        query = f"SELECT * FROM {sql_table} WHERE {table_column} {operation} {filter}"
    df = pd.read_sql_query(query, conn)
    soma = df['balanco'].sum()

    print(df, soma)
    # Salvando as alterações no banco de dados
    conn.commit()
    conn.close()
    return df
#df = filter(sql_data, 'BetFair')
def add_linhas_from_csv():
    # Conectando ao banco de dados SQLite
    conn = sqlite3.connect(sql_data)
    cursor = conn.cursor()

    # Lendo o arquivo "movimentacao.csv" usando o pandas
    df = pd.read_csv('/Users/sergioeblutzer/PycharmProjects/Gerenciamento_Bolsa_Esportiva/depositos.csv')

    # Obtendo a lista de tabelas existentes no banco de dados
    existing_tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    existing_tables = [table[0] for table in existing_tables]

    # Iterando sobre as linhas do DataFrame
    for index, row in df.iterrows():
        id = row['id']
        bethouse = row['BetHouse']
        status = row['Status']
        valor = row['Valor']
        data = row['Data']

        # Verificando se a tabela correspondente à BetHouse existe
        table_name = f"{bethouse}_saldos"
        table_name = re.sub(r'\W+', '_', table_name)
        if table_name[0].isdigit():
            table_name = f'_{table_name}'
        if table_name in existing_tables:
            # Inserindo os valores nas colunas correspondentes da tabela
            query = f"INSERT INTO {table_name} (id, data_entrada, data_fim, odd, aposta, resultado, balanco, dif_real) VALUES ({id}, '{data}', '{data}', NULL, NULL, '{status}', {valor}, {valor})"
            cursor.execute(query)
        else:
            print(f"Tabela {table_name} não existe.")

    # Salvando as alterações no banco de dados
    conn.commit()
    # Fechando a conexão com o banco de dados
    conn.close()

def sum_lucro_estimado(sql_data, sql_table):
    # Conectar ao banco de dados
    conexao = sqlite3.connect(sql_data)
    cursor = conexao.cursor()

    # Consulta SQL
    consulta = f"SELECT SUM(lucro_estimado) FROM {sql_table} WHERE DATE(data_entrada) = '{date.today()}'"

    # Executar a consulta
    cursor.execute(consulta)

    # Obter o resultado
    resultado = cursor.fetchone()[0]

    # Imprimir o resultado
    print(f"A soma do lucro estimado para hoje é: R$ {round(resultado, 2)}")

    # Fechar a conexão
    conexao.close()

def view_column_type(sql_data, sql_table):
    import sqlite3

    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(sql_data)

    # Consulta SQL para obter as informações de esquema da tabela
    query = f"PRAGMA table_info({sql_table})"

    # Executar a consulta
    cursor = conn.execute(query)

    # Recuperar as informações de esquema da tabela
    esquema_tabela = cursor.fetchall()

    # Exibir o tipo de dado de cada coluna
    for coluna in esquema_tabela:
        nome_coluna = coluna[1]
        tipo_dado = coluna[2]
        print(f"Coluna: {nome_coluna}, Tipo de Dado: {tipo_dado}")

    # Fechar a conexão com o banco de dados
    conn.close()

def change_columns_type(sql_data, sql_table):
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(sql_data)

    # Nome da tabela original e nova tabela
    nome_tabela_original = sql_table
    nome_tabela_nova = f'nova_{sql_table}'

    # Colunas a serem copiadas e seus respectivos tipos de dados atualizados
    colunas_tipos = [
        ('id', 'INTEGER'),
        ('data_entrada', 'TEXT'),
        ('data_fim', 'TEXT'),
        ('odd', 'REAL'),
        ('aposta', 'REAL'),
        ('resultado', 'TEXT'),
        ('balanco', 'REAL'),
        ('dif_real', 'REAL')
    ]

    # Criar a nova tabela com as colunas atualizadas
    query_criar_tabela = f"CREATE TABLE {nome_tabela_nova} ({', '.join(f'{coluna} {tipo}' for coluna, tipo in colunas_tipos)})"
    conn.execute(query_criar_tabela)

    # Montar a lista de colunas a serem selecionadas na ordem desejada
    colunas_selecionadas = ', '.join(coluna for coluna, _ in colunas_tipos)

    # Montar a lista de colunas com os tipos de dados atualizados usando a função CAST
    colunas_tipos_cast = ', '.join(f"CAST({coluna} AS {tipo}) AS {coluna}" for coluna, tipo in colunas_tipos)

    # Copiar os dados da tabela original para a nova tabela, convertendo os tipos de dados
    query_inserir_dados = f"INSERT INTO {nome_tabela_nova} ({colunas_selecionadas}) SELECT {colunas_tipos_cast} FROM {nome_tabela_original}"
    conn.execute(query_inserir_dados)

    # Confirmar as alterações e fechar a conexão com o banco de dados
    conn.commit()
    conn.close()

def del_table(sql_data, sql_table):
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(sql_data)

    # Consulta SQL para deletar a tabela
    query = f"DROP TABLE IF EXISTS {sql_table}"

    # Executar a consulta
    conn.execute(query)

    # Confirmar as alterações e fechar a conexão com o banco de dados
    conn.commit()
    conn.close()

def rename_table(sql_data, sql_table_old, sql_table_new):
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(sql_data)

    # Nome da tabela atual e novo nome da tabela
    nome_tabela_atual = 'nome_tabela_atual'
    novo_nome_tabela = 'novo_nome_tabela'

    # Consulta SQL para renomear a tabela
    query = f"ALTER TABLE {sql_table_old} RENAME TO {sql_table_new}"

    # Executar a consulta
    conn.execute(query)

    # Confirmar as alterações e fechar a conexão com o banco de dados
    conn.commit()
    conn.close()
#sum_lucro_estimado(sql_data, 'apostas')
#filter(sql_data, 'BetFair_apostas')

#valores = {'id': 626, 'data_entrada': '2023-06-01 04:23:11', 'data_fim': '2023-06-04 16:00:00', 'bethouse': 'Pinnacle', 'odd': 1.684, 'odd_real': 1.684, 'aposta': 12.79, 'resultado': None, 'balanco': -12.79, 'dif_real': 0}
#add_aposta_individual(sql_data, 'Pinnacle_apostas', valores)


def arrumar_colunas(sql_data):
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(sql_data)

    # Nome da tabela e colunas que serão atualizadas
    nome_tabela = 'apostas'
    colunas = ['valor1', 'valor2', 'valor3', 'bethouse3', 'odd3', 'aposta3', 'mercado3', 'resultado1', 'resultado2', 'resultado3']  # Substitua pelos nomes das suas colunas

    # Consulta SQL para atualizar as ocorrências
    for coluna in colunas:
        query = f"UPDATE {nome_tabela} SET {coluna} = NULL WHERE {coluna} = 'None'"
        conn.execute(query)

    # Confirmar as alterações e fechar a conexão com o banco de dados
    conn.commit()
    conn.close()

def edit_line(sql_data, sql_table, id, set1, set2='', set3='', set4='', set5='', cond1='', cond2='', cond3='', cond4=''):
    conn = sqlite3.connect(sql_data)
    c = conn.cursor()
    if id is None:
        id = 'id IS NULL'
    else:
        id = f'id = {id}'
    sets = [set2, set3, set4, set5]
    valid_sets = [s for s in sets if s != '']
    concatenated_sets = ', '.join(valid_sets)
    conds = [cond1, cond2, cond3, cond4]
    valid_conds = [s for s in conds if s != '']
    concatenated_conds = ' AND '.join(valid_conds)
    edit_query = f"UPDATE {sql_table} SET {set1}, balanco = 0, dif_real = 0 WHERE {id}"
    #params = [0]  # Lista de parâmetros para substituir o espaço reservado '?'
    c.execute(edit_query)
    # Salvando as alterações no banco de dados
    conn.commit()
    conn.close()

def reconstruir_tabela(conn, sql_table):
    c = conn.cursor()
    rename_query = f"ALTER TABLE {sql_table} RENAME TO {sql_table}_antigas"
    c.execute(rename_query)

    create_query = f"""
            CREATE TABLE {sql_table} (
            id INTEGER,
            data_entrada TEXT,
            data_jogo TEXT,
            time_casa TEXT,
            time_fora TEXT,
            bethouse1 TEXT,
            mercado1 TEXT,
            valor1 REAL,
            odd1 REAL,
            aposta1 REAL,
            resultado1 TEXT,
            bethouse2 TEXT,
            mercado2 TEXT,
            valor2 REAL,
            odd2 REAL,
            aposta2 REAL,
            resultado2 TEXT,
            bethouse3 TEXT,
            mercado3 TEXT,
            valor3 REAL,
            odd3 REAL,
            aposta3 REAL,
            resultado3 TEXT,
            lucro_estimado REAL,
            lucro_per_estimado REAL,
            lucro_real REAL,
            lucro_per_real REAL,
            esporte TEXT
        )
        """
    c.execute(create_query)

    copy_query = f"""
        INSERT INTO apostas (
            id,
            data_entrada,
            data_jogo,
            time_casa,
            time_fora,
            bethouse1,
            mercado1,
            valor1,
            odd1,
            aposta1,
            resultado1,
            bethouse2,
            mercado2,
            valor2,
            odd2,
            aposta2,
            resultado2,
            bethouse3,
            mercado3,
            valor3,
            odd3,
            aposta3,
            resultado3,
            lucro_estimado,
            lucro_per_estimado,
            lucro_real,
            lucro_per_real,
            esporte
        )
        SELECT
            id,
            data_entrada,
            data_jogo,
            time_casa,
            time_fora,
            bethouse1,
            mercado1,
            CAST(valor1 AS REAL),
            CAST(odd1 AS REAL),
            CAST(aposta1 AS REAL),
            resultado1,
            bethouse2,
            mercado2,
            CAST(valor2 AS REAL),
            CAST(odd2 AS REAL),
            CAST(aposta2 AS REAL),
            resultado2,
            bethouse3,
            mercado3,
            CAST(valor3 AS REAL),
            CAST(odd3 AS REAL),
            CAST(aposta3 AS REAL),
            resultado3,
            CAST(lucro_estimado AS REAL),
            CAST(lucro_per_estimado AS REAL),
            CAST(lucro_real AS REAL),
            CAST(lucro_per_real AS REAL),
            esporte
        FROM apostas_antigas
        """
    c.execute(copy_query)
    conn.commit()

################################################
################### GRÁFICOS ###################
################################################


def lucro_esporte(conn, tempo):
    data_3_meses_atras = (datetime.today() - timedelta(days=tempo)).strftime('%Y-%m-%d')

    # Consulta SQL para agrupar o lucro real por esporte nos últimos 3 meses
    query = f"""
        SELECT esporte, SUM(lucro_real) AS lucro_total
        FROM apostas
        WHERE data_entrada >= date('{data_3_meses_atras}')
        GROUP BY esporte
    """

    # Executando a consulta
    resultado = pd.read_sql_query(query, conn)

    # Exibindo o DataFrame com os resultados
    return resultado

#df = contar_bethouses(conn, 7)
#lucro_esporte(conn, 90)
#esportes_tempo(conn, 90)
#edit_column(sql_data, 'apostas', 'esporte', 'Rugby', 'Rugby un')
#edit_query = "UPDATE apostas SET bethouse3 = NULL, mercado3 = NULL WHERE id = 20230604002"
#c.execute(edit_query)
#conn.commit()
#query = "SELECT * FROM apostas WHERE id = 20230604002"
#print(c.execute(query).fetchall())
#reconstruir_tabela(conn, 'apostas')
#df = count_hora(conn, 0)
#df = lucros_por_tempo(7, 'trimestre', conn)
#df, total_apostas = saldo_bethouses(conn, 5, 'semana')
#df = odds_resultados(conn, tempo = 90)
#print(df)

#edit_line(sql_data, 'BWin_saldos', 20230522015, "resultado = 'return'")
#add_linhas_from_csv()
#view_ n(sql_data, '_1xBet_saldos')
#del_column(sql_data, 'apostas', 'id_novo')
#del_table(sql_data, 'apostas')
#del_line(sql_data, 'apostas', id=20230703006)
#del_line(sql_data, 'BWin_saldos', id=20230703006)
#del_line(sql_data, 'Ex_BetFair_saldos', id=20230615049)
#del_line(sql_data, 'FavBet_saldos', id=2306250301)
#del_line(sql_data, 'apostas', id=20230630015)
#del_line(sql_data, 'SportyBet_saldos', id=696)
#del_line(sql_data, 'Pinnacle_saldos', id=2303040101)
#view_tables(sql_data)
view_column(sql_data, 'apostas')
view_last_lines(sql_data, 'apostas', 70)
#view_last_lines(sql_data, 'apostas_antigas', 3)
#view_last_lines(sql_data, 'FavBet_saldos', 30)
#view_last_lines(sql_data, 'FavBet_saldos', 3)
#view_last_lines(sql_data, 'Ex_BetFair_saldos', 3)
#sum_lucro_estimado(sql_data, 'apostas')

#df['saldo'] = round(df['balanco'].cumsum(), 2)

#print(df)
#print(df[['aposta', 'odd', 'resultado', 'balanco', 'dif_real', 'saldo']])

#df = pd.read_csv('/Users/sergioeblutzer/PycharmProjects/Gerenciamento_Bolsa_Esportiva/apostas_antigas.csv')
#print(df)
