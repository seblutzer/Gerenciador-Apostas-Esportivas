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
sql_data = '/Users/sergioeblutzer/PycharmProjects/Gerenciamento_Bolsa_Esportiva/dados.db'
with open('/Users/sergioeblutzer/PycharmProjects/Gerenciamento_Bolsa_Esportiva/bethouse_options.json', 'r') as f:
    data = json.load(f)
    bethouse_options_total = data.get("bethouse_options", {})
conn = sqlite3.connect(sql_data)
c = conn.cursor()
def apostas_to_tabelas(sql = True):
    sql = True
    dados = pd.read_csv('/Users/sergioeblutzer/PycharmProjects/Gerenciamento_Bolsa_Esportiva/apostas_antigas.csv')
    with open('/Users/sergioeblutzer/PycharmProjects/Gerenciamento_Bolsa_Esportiva/bethouse_options.json', 'r') as f:
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
        query = f"SELECT valor1 FROM {sql_table} WHERE valor1 = ''"
    else:
        query = f"SELECT * FROM {sql_table} WHERE {table_column} {operation} {filter}"
    df = pd.read_sql_query(query, con)

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
#edit_column(sql_data, 'apostas', 'valor1', 'NULL', '')


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
        c.execute("SELECT valor3 FROM apostas WHERE CAST(valor1 AS REAL) IS NULL and valor3 IS NOT NULL")

        # Recuperar os resultados da consulta
        resultados = c.fetchall()

        # Imprimir os valores
        #for resultado in resultados:
        #    print(resultado[0])

        #query = f"SELECT * FROM apostas"# WHERE resultado IS NULL"# WHERE DATE(data_entrada) >= '2021-01-01' AND DATE(data_entrada) < '2022-01-01' ORDER BY data_entrada ASC"
    else:
        query = f"SELECT * FROM {sql_table} WHERE {table_column} {operation} {filter}"
    #df = pd.read_sql_query(query, conn)

    #print(df)
    # Salvando as alterações no banco de dados
    conn.commit()
    conn.close()
    #return df
df = filter(sql_data, 'BetFair')
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

def count_hora(conn, dias):
    # Conectando ao banco de dados
    c = conn.cursor()
    data = datetime.today().strftime('%Y-%m-%d')

    # Consulta SQL para contar as apostas por hora nos últimos 7 dias
    query = f"""
        SELECT strftime('%H', data_entrada) AS hora, COUNT(*) AS total_apostas, SUM(lucro_real) as lucro
        FROM apostas
        WHERE data_entrada >= date('{data}', '-{dias} days')
        GROUP BY hora
        ORDER BY hora
    """
    query = f"""
        WITH subquery AS (
            SELECT strftime('%H', data_entrada) AS hora, COUNT(*) AS total_apostas
            FROM apostas
            WHERE data_entrada >= date('{data}', '-{dias} days')
            GROUP BY hora
        ),
        stats AS (
            SELECT AVG(total_apostas) AS media, COUNT(*) AS count
            FROM subquery
        )
        SELECT s.hora, s.total_apostas, a.lucro, 
               POWER((SUM((s.total_apostas - stats.media)*(s.total_apostas - stats.media))/stats.count), 0.5) AS desvio_padrao
        FROM subquery s
        CROSS JOIN stats
        LEFT JOIN (
            SELECT strftime('%H', data_entrada) AS hora, SUM(lucro_real) AS lucro
            FROM apostas
            WHERE data_entrada >= date('{data}', '-{dias} days')
            GROUP BY hora
        ) a ON s.hora = a.hora
        GROUP BY s.hora, a.lucro
        ORDER BY s.hora
    """

    # Executando a consulta
    c.execute(query)

    # Obtendo os resultados
    resultados = c.fetchall()

    # Consulta SQL para contar os dias diferentes em data_entrada nos últimos 7 dias
    query_days = f"""
        SELECT COUNT(DISTINCT date(data_entrada)) AS total_dias
        FROM apostas
        WHERE data_entrada >= date('{data}', '-{dias} days')
    """
    total_dias = c.execute(query_days).fetchone()[0]

    # Criando o DataFrame com os resultados
    df = pd.DataFrame(resultados, columns=['hora', 'total_apostas', 'lucro', 'desvio_padrao'])
    df['hora'] = df['hora'].apply(lambda x: f'{str(x).zfill(2)}h')
    df['media_apostas'] = df['total_apostas'] / total_dias
    df['media_lucro'] = ((df['lucro'] if dias > 0 else 0) / (df['total_apostas'] if dias > 0 else 1))
    df['lucro_total'] = (df['lucro'] if dias > 0 else 0)

    return df

def lucros_por_tempo(range_val, periodo, conn):
    if periodo == 'dia':
        query = f"""
        SELECT STRFTIME('%d', data_entrada) || '/' ||
        (CASE STRFTIME('%m', data_entrada)
            WHEN '01' THEN 'Jan'
            WHEN '02' THEN 'Fev'
            WHEN '03' THEN 'Mar'
            WHEN '04' THEN 'Abr'
            WHEN '05' THEN 'Mai'
            WHEN '06' THEN 'Jun'
            WHEN '07' THEN 'Jul'
            WHEN '08' THEN 'Ago'
            WHEN '09' THEN 'Set'
            WHEN '10' THEN 'Out'
            WHEN '11' THEN 'Nov'
            WHEN '12' THEN 'Dez'
        END) AS {periodo},
        SUM(lucro_estimado) AS lucro_estimado, SUM(lucro_real) AS lucro_real, SUM(CASE WHEN lucro_real IS NULL THEN lucro_estimado ELSE 0 END) AS aberto FROM apostas WHERE DATE(data_entrada) >= DATE('now', '-{range_val + 1} day') GROUP BY dia ORDER BY DATE(data_entrada) ASC"""
    elif periodo == 'semana':
        range_val = (range_val - 1) * 7 + datetime.today().isoweekday()
        query = f"""
            SELECT STRFTIME('%d', MIN(data_entrada)) || '-' || STRFTIME('%d', MAX(data_entrada)) || '/' || 
            (CASE STRFTIME('%m', data_entrada)
            WHEN '01' THEN 'Jan'
            WHEN '02' THEN 'Fev'
            WHEN '03' THEN 'Mar'
            WHEN '04' THEN 'Abr'
            WHEN '05' THEN 'Mai'
            WHEN '06' THEN 'Jun'
            WHEN '07' THEN 'Jul'
            WHEN '08' THEN 'Ago'
            WHEN '09' THEN 'Set'
            WHEN '10' THEN 'Out'
            WHEN '11' THEN 'Nov'
            WHEN '12' THEN 'Dez'
        END) AS {periodo}, SUM(lucro_estimado) AS lucro_estimado, SUM(lucro_real) AS lucro_real, SUM(CASE WHEN lucro_real IS NULL THEN lucro_estimado ELSE 0 END) AS aberto FROM apostas WHERE DATE(data_entrada) >= DATE('now', '-{range_val} day') GROUP BY STRFTIME('%Y-%W', data_entrada, 'weekday 6') ORDER BY DATE(data_entrada) ASC
        """
    elif periodo == 'mês':
        query = f"""
        SELECT (CASE STRFTIME('%m', data_entrada)
            WHEN '01' THEN 'Jan'
            WHEN '02' THEN 'Fev'
            WHEN '03' THEN 'Mar'
            WHEN '04' THEN 'Abr'
            WHEN '05' THEN 'Mai'
            WHEN '06' THEN 'Jun'
            WHEN '07' THEN 'Jul'
            WHEN '08' THEN 'Ago'
            WHEN '09' THEN 'Set'
            WHEN '10' THEN 'Out'
            WHEN '11' THEN 'Nov'
            WHEN '12' THEN 'Dez'
        END) || '/' || STRFTIME('%Y', data_entrada) AS {periodo}, SUM(lucro_estimado) AS lucro_estimado, SUM(lucro_real) AS lucro_real, SUM(CASE WHEN lucro_real IS NULL THEN lucro_estimado ELSE 0 END) AS aberto FROM apostas WHERE DATE(data_entrada) >= DATE('now', '-{range_val - 1} month', 'start of month') GROUP BY {periodo} ORDER BY DATE(data_entrada) ASC
        """
    elif periodo == 'trimestre':
        query = f"""
        SELECT (CASE 
            WHEN STRFTIME('%m', data_entrada) BETWEEN '01' AND '03' THEN '1ºTrim/' || STRFTIME('%Y', data_entrada) 
            WHEN STRFTIME('%m', data_entrada) BETWEEN '04' AND '06' THEN '2ºTrim/' || STRFTIME('%Y', data_entrada) 
            WHEN STRFTIME('%m', data_entrada) BETWEEN '07' AND '09' THEN '3ºTrim/' || STRFTIME('%Y', data_entrada) 
            ELSE '4ºTrim/' || STRFTIME('%Y', data_entrada) 
        END) AS trimestre, SUM(lucro_estimado) AS lucro_estimado, SUM(lucro_real) AS lucro_real, SUM(CASE WHEN lucro_real IS NULL THEN lucro_estimado ELSE 0 END) AS aberto FROM apostas WHERE DATE(data_entrada) >= DATE('now', '-{range_val * 3 + 1} month') GROUP BY trimestre ORDER BY DATE(data_entrada) ASC
        """
    elif periodo == 'semestre':
        query = f"""
        SELECT (CASE 
            WHEN STRFTIME('%m', data_entrada) >= '07' THEN '2ºSem/' || STRFTIME('%Y', data_entrada) 
            ELSE '1ºSem/' || STRFTIME('%Y', data_entrada) 
        END) AS semestre, SUM(lucro_estimado) AS lucro_estimado, SUM(lucro_real) AS lucro_real, SUM(CASE WHEN lucro_real IS NULL THEN lucro_estimado ELSE 0 END) AS aberto FROM apostas WHERE DATE(data_entrada) >= DATE('now', '-{range_val * 6 + 1} month') GROUP BY semestre ORDER BY DATE(data_entrada) ASC
        """
    else:
        query = f"SELECT STRFTIME('%Y', data_entrada) AS ano, SUM(lucro_estimado) AS lucro_estimado, SUM(lucro_real) AS lucro_real, SUM(CASE WHEN lucro_real IS NULL THEN lucro_estimado ELSE 0 END) AS aberto FROM apostas WHERE DATE(data_entrada) >= DATE('now', '-{range_val - 1} year', 'start of year') GROUP BY ano ORDER BY DATE(data_entrada) ASC"

    df = pd.read_sql_query(query, conn)
    return df

def saldo_bethouses(conn, range_val, periodo):
    c = conn.cursor()

    # Dataframe para armazenar os resultados
    df_saldos = pd.DataFrame()
    current_date = date.today()
    current_month = current_date.month
    condition = ''
    if periodo == 'dia':
        intervalo = f'{range_val - 1} days'
    elif periodo == 'semana':
            intervalo = f'{(range_val - 1) * 7 + (current_date.weekday() + 1)} days'
    elif periodo == 'mês':
        intervalo = f'{range_val - 1} month'
        condition = "'start of month',"
    elif periodo == 'trimestre':
        if current_month <= 3:
            start_of_quarter = date(current_date.year, 1, 1)
        elif current_month <= 6:
            start_of_quarter = date(current_date.year, 4, 1)
        elif current_month <= 9:
            start_of_quarter = date(current_date.year, 7, 1)
        else:
            start_of_quarter = date(current_date.year, 10, 1)
        current_date = start_of_quarter
        intervalo = f'{(range_val - 1) * 3} month'
        condition = "'start of month',"
    elif periodo == 'semestre':
        if current_month <= 6:
            start_of_semester = date(current_date.year, 1, 1)
        elif current_month <= 7:
            start_of_semester = date(current_date.year, 7, 1)
        current_date = start_of_semester
        intervalo = f'{(range_val - 1) * 6} month'
        condition = "'start of month',"
    else:
        intervalo = f'{range_val - 1} years'
        condition = "'start of year',"

    # Loop através das chaves do dicionário bethouse_options
    for bethouse in bethouse_options_total.keys():
        tabela_aposta = f"{bethouse}_saldos"
        tabela_aposta = re.sub(r'\W+', '_', tabela_aposta)
        if tabela_aposta[0].isdigit():
            tabela_aposta = f'_{tabela_aposta}'

        query_saldo = f"""
        SELECT SUM(balanco)
        FROM {tabela_aposta}
        WHERE data_entrada <= DATE('{current_date}', {condition}'-{intervalo}')
        """
        saldo_anterior = c.execute(query_saldo).fetchone()[0]
        saldo_anterior = round(saldo_anterior, 2) if saldo_anterior is not None else 0

        # Consulta para obter a soma de balanco e Valor agrupados por dia
        if periodo == 'dia':
            query = f"""
            WITH all_dates AS (
                SELECT DATE('{current_date}') AS date
                UNION ALL
                SELECT date(date, '-1 day') AS date
                FROM all_dates
                WHERE date > DATE('{current_date}', '-{intervalo}')
            )
            SELECT STRFTIME('%d', all_dates.date) || '/' || 
                (CASE STRFTIME('%m', all_dates.date)
                    WHEN '01' THEN 'Jan'
                    WHEN '02' THEN 'Fev'
                    WHEN '03' THEN 'Mar'
                    WHEN '04' THEN 'Abr'
                    WHEN '05' THEN 'Mai'
                    WHEN '06' THEN 'Jun'
                    WHEN '07' THEN 'Jul'
                    WHEN '08' THEN 'Ago'
                    WHEN '09' THEN 'Set'
                    WHEN '10' THEN 'Out'
                    WHEN '11' THEN 'Nov'
                    WHEN '12' THEN 'Dez'
                END) AS {periodo},
                '{bethouse}' AS bethouse, ROUND(COALESCE(SUM({tabela_aposta}.balanco), 0), 2) AS saldo_periodo, CASE WHEN SUM(aposta) IS NULL THEN COUNT(*) - 1 ELSE COUNT(*) END AS apostas, SUM(aposta) AS investimento, GROUP_CONCAT({tabela_aposta}.id) AS ids, GROUP_CONCAT({tabela_aposta}.id) AS ids
            FROM all_dates
            LEFT JOIN {tabela_aposta} ON all_dates.date = DATE({tabela_aposta}.data_entrada)
            GROUP BY all_dates.date
            """
        elif periodo == 'semana':
            query = f"""
                WITH all_weeks AS (
                SELECT DATE('{current_date}', 'weekday 6') AS start_of_week,
                       STRFTIME('%d', DATE('{current_date}', 'weekday 6')) AS sunday,
                       STRFTIME('%d', DATE('{current_date}', 'weekday 5')) AS saturday
                UNION ALL
                SELECT DATE(start_of_week, '-7 day') AS start_of_week,
                       STRFTIME('%d', DATE(start_of_week, '-6 days')) AS sunday,
                       STRFTIME('%d', DATE(start_of_week)) AS saturday
                FROM all_weeks
                WHERE start_of_week >= DATE('{current_date}', 'weekday 6', '-{intervalo}'))
                SELECT all_weeks.sunday || '-' || all_weeks.saturday || '/' || 
                    (CASE STRFTIME('%m', all_weeks.start_of_week, '+7 days')
                        WHEN '01' THEN 'Jan'
                        WHEN '02' THEN 'Fev'
                        WHEN '03' THEN 'Mar'
                        WHEN '04' THEN 'Abr'
                        WHEN '05' THEN 'Mai'
                        WHEN '06' THEN 'Jun'
                        WHEN '07' THEN 'Jul'
                        WHEN '08' THEN 'Ago'
                        WHEN '09' THEN 'Set'
                        WHEN '10' THEN 'Out'
                        WHEN '11' THEN 'Nov'
                        WHEN '12' THEN 'Dez'
                    END) AS {periodo},
                    '{bethouse}' AS bethouse,
                    ROUND(COALESCE(SUM({tabela_aposta}.balanco), 0), 2) AS saldo_periodo, CASE WHEN SUM(aposta) IS NULL THEN COUNT(*) - 1 ELSE COUNT(*) END AS apostas, SUM(aposta) AS investimento, GROUP_CONCAT({tabela_aposta}.id) AS ids
                FROM all_weeks
                LEFT JOIN {tabela_aposta} ON {tabela_aposta}.data_entrada > all_weeks.start_of_week AND {tabela_aposta}.data_entrada <= DATE(all_weeks.start_of_week, '+7 days')
                GROUP BY STRFTIME('%Y-%W', all_weeks.start_of_week)
                HAVING semana IS NOT NULL
                """
        elif periodo == 'mês':
            query = f"""
                    WITH all_dates AS (
                        SELECT DATE('{current_date}') AS date
                        UNION ALL
                        SELECT date(date, 'start of month', '-1 month') AS date
                        FROM all_dates
                        WHERE date > DATE('{current_date}', 'start of month', '-{intervalo}')
                    )
                    SELECT (CASE STRFTIME('%m', all_dates.date)
                                WHEN '01' THEN 'Jan'
                                WHEN '02' THEN 'Fev'
                                WHEN '03' THEN 'Mar'
                                WHEN '04' THEN 'Abr'
                                WHEN '05' THEN 'Mai'
                                WHEN '06' THEN 'Jun'
                                WHEN '07' THEN 'Jul'
                                WHEN '08' THEN 'Ago'
                                WHEN '09' THEN 'Set'
                                WHEN '10' THEN 'Out'
                                WHEN '11' THEN 'Nov'
                                WHEN '12' THEN 'Dez'
                            END) || '/' || SUBSTR(STRFTIME('%Y', all_dates.date), 3) AS {periodo},
                           '{bethouse}' AS bethouse,
                           ROUND(COALESCE(SUM({tabela_aposta}.balanco), 0), 2) AS saldo_periodo, CASE WHEN SUM(aposta) IS NULL THEN COUNT(*) - 1 ELSE COUNT(*) END AS apostas, SUM(aposta) AS investimento, GROUP_CONCAT({tabela_aposta}.id) AS ids
                    FROM all_dates
                    LEFT JOIN {tabela_aposta} ON STRFTIME('%m/%Y', all_dates.date) = STRFTIME('%m/%Y', {tabela_aposta}.data_entrada)
                    GROUP BY STRFTIME('%Y-%m', all_dates.date)
                """
        elif periodo == 'trimestre':
            query = f"""
                WITH all_quarters AS (
                    SELECT DATE('{current_date}', 'start of month') AS start_of_quarter,
                           (CASE STRFTIME('%m', DATE('{current_date}', 'start of month'))
                                WHEN '01' THEN 'Jan'
                                WHEN '02' THEN 'Fev'
                                WHEN '03' THEN 'Mar'
                                WHEN '04' THEN 'Abr'
                                WHEN '05' THEN 'Mai'
                                WHEN '06' THEN 'Jun'
                                WHEN '07' THEN 'Jul'
                                WHEN '08' THEN 'Ago'
                                WHEN '09' THEN 'Set'
                                WHEN '10' THEN 'Out'
                                WHEN '11' THEN 'Nov'
                                WHEN '12' THEN 'Dez'
                            END) AS start_month,
                           (CASE STRFTIME('%m', DATE('{current_date}', 'start of month', '+2 months'))
                                WHEN '01' THEN 'Jan'
                                WHEN '02' THEN 'Fev'
                                WHEN '03' THEN 'Mar'
                                WHEN '04' THEN 'Abr'
                                WHEN '05' THEN 'Mai'
                                WHEN '06' THEN 'Jun'
                                WHEN '07' THEN 'Jul'
                                WHEN '08' THEN 'Ago'
                                WHEN '09' THEN 'Set'
                                WHEN '10' THEN 'Out'
                                WHEN '11' THEN 'Nov'
                                WHEN '12' THEN 'Dez'
                            END) AS end_month
                    UNION ALL
                    SELECT DATE(start_of_quarter, '-3 months') AS start_of_quarter,
                           (CASE STRFTIME('%m', DATE(start_of_quarter, '-3 months'))
                            WHEN '01' THEN 'Jan'
                            WHEN '02' THEN 'Fev'
                            WHEN '03' THEN 'Mar'
                            WHEN '04' THEN 'Abr'
                            WHEN '05' THEN 'Mai'
                            WHEN '06' THEN 'Jun'
                            WHEN '07' THEN 'Jul'
                            WHEN '08' THEN 'Ago'
                            WHEN '09' THEN 'Set'
                            WHEN '10' THEN 'Out'
                            WHEN '11' THEN 'Nov'
                            WHEN '12' THEN 'Dez'
                        END) AS start_month,
                        (CASE STRFTIME('%m', DATE(start_of_quarter, '-1 month'))
                            WHEN '01' THEN 'Jan'
                            WHEN '02' THEN 'Fev'
                            WHEN '03' THEN 'Mar'
                            WHEN '04' THEN 'Abr'
                            WHEN '05' THEN 'Mai'
                            WHEN '06' THEN 'Jun'
                            WHEN '07' THEN 'Jul'
                            WHEN '08' THEN 'Ago'
                            WHEN '09' THEN 'Set'
                            WHEN '10' THEN 'Out'
                            WHEN '11' THEN 'Nov'
                            WHEN '12' THEN 'Dez'
                        END) AS end_month
                    FROM all_quarters
                    WHERE start_of_quarter > DATE('{current_date}', 'start of month', '-{intervalo}')
                )
                SELECT CASE
                   WHEN {tabela_aposta}.data_entrada IS NULL THEN all_quarters.start_month || '-' || all_quarters.end_month || '/' || SUBSTR(STRFTIME('%Y', all_quarters.start_of_quarter), 3)
                   ELSE all_quarters.start_month || '-' || all_quarters.end_month || '/' || SUBSTR(STRFTIME('%Y', {tabela_aposta}.data_entrada), 3) END AS {periodo}, '{bethouse}' AS bethouse,
                   ROUND(COALESCE(SUM({tabela_aposta}.balanco), 0), 2) AS saldo_periodo, CASE WHEN SUM(aposta) IS NULL THEN COUNT(*) - 1 ELSE COUNT(*) END AS apostas, SUM(aposta) AS investimento, GROUP_CONCAT({tabela_aposta}.id) AS ids
                FROM all_quarters
                LEFT JOIN {tabela_aposta} ON {tabela_aposta}.data_entrada >= all_quarters.start_of_quarter AND {tabela_aposta}.data_entrada < DATE(all_quarters.start_of_quarter, '+3 months')
                GROUP BY STRFTIME('%Y-%m', all_quarters.start_of_quarter)
                """
        elif periodo == 'semestre':
            query = f"""
                WITH all_semesters AS (
                    SELECT DATE('{current_date}', 'start of month') AS start_of_semester,
                           (CASE STRFTIME('%m', DATE('{current_date}', 'start of month'))
                                WHEN '01' THEN 'Jan'
                                WHEN '02' THEN 'Fev'
                                WHEN '03' THEN 'Mar'
                                WHEN '04' THEN 'Abr'
                                WHEN '05' THEN 'Mai'
                                WHEN '06' THEN 'Jun'
                                WHEN '07' THEN 'Jul'
                                WHEN '08' THEN 'Ago'
                                WHEN '09' THEN 'Set'
                                WHEN '10' THEN 'Out'
                                WHEN '11' THEN 'Nov'
                                WHEN '12' THEN 'Dez'
                            END) AS start_month,
                           (CASE STRFTIME('%m', DATE('{current_date}', 'start of month', '+5 months'))
                                WHEN '01' THEN 'Jan'
                                WHEN '02' THEN 'Fev'
                                WHEN '03' THEN 'Mar'
                                WHEN '04' THEN 'Abr'
                                WHEN '05' THEN 'Mai'
                                WHEN '06' THEN 'Jun'
                                WHEN '07' THEN 'Jul'
                                WHEN '08' THEN 'Ago'
                                WHEN '09' THEN 'Set'
                                WHEN '10' THEN 'Out'
                                WHEN '11' THEN 'Nov'
                                WHEN '12' THEN 'Dez'
                            END) AS end_month
                    UNION ALL
                    SELECT DATE(start_of_semester, '-6 months') AS start_of_semester,
                        (CASE STRFTIME('%m', DATE(start_of_semester, '-6 months'))
                            WHEN '01' THEN 'Jan'
                            WHEN '02' THEN 'Fev'
                            WHEN '03' THEN 'Mar'
                            WHEN '04' THEN 'Abr'
                            WHEN '05' THEN 'Mai'
                            WHEN '06' THEN 'Jun'
                            WHEN '07' THEN 'Jul'
                            WHEN '08' THEN 'Ago'
                            WHEN '09' THEN 'Set'
                            WHEN '10' THEN 'Out'
                            WHEN '11' THEN 'Nov'
                            WHEN '12' THEN 'Dez'
                        END) AS start_month,
                        (CASE STRFTIME('%m', DATE(start_of_semester, '-1 month'))
                            WHEN '01' THEN 'Jan'
                            WHEN '02' THEN 'Fev'
                            WHEN '03' THEN 'Mar'
                            WHEN '04' THEN 'Abr'
                            WHEN '05' THEN 'Mai'
                            WHEN '06' THEN 'Jun'
                            WHEN '07' THEN 'Jul'
                            WHEN '08' THEN 'Ago'
                            WHEN '09' THEN 'Set'
                            WHEN '10' THEN 'Out'
                            WHEN '11' THEN 'Nov'
                            WHEN '12' THEN 'Dez'
                        END) AS end_month
                    FROM all_semesters
                    WHERE start_of_semester > DATE('{current_date}', 'start of month', '-{intervalo}')
                )
                SELECT CASE
                   WHEN {tabela_aposta}.data_entrada IS NULL THEN all_semesters.start_month || '-' || all_semesters.end_month || '/' || SUBSTR(STRFTIME('%Y', all_semesters.start_of_semester), 3)
                   ELSE all_semesters.start_month || '-' || all_semesters.end_month || '/' || SUBSTR(STRFTIME('%Y', {tabela_aposta}.data_entrada), 3) END AS {periodo}, '{bethouse}' AS bethouse,
                   ROUND(COALESCE(SUM({tabela_aposta}.balanco), 0), 2) AS saldo_periodo, CASE WHEN SUM(aposta) IS NULL THEN COUNT(*) - 1 ELSE COUNT(*) END AS apostas, SUM(aposta) AS investimento, GROUP_CONCAT({tabela_aposta}.id) AS ids
                FROM all_semesters
                LEFT JOIN {tabela_aposta} ON {tabela_aposta}.data_entrada >= all_semesters.start_of_semester AND {tabela_aposta}.data_entrada < DATE(all_semesters.start_of_semester, '+6 months')
                GROUP BY STRFTIME('%Y-%m', all_semesters.start_of_semester)
                """
        else:
            query = f"""
                WITH all_dates AS (
                    SELECT DATE('{current_date}') AS date
                    UNION ALL
                    SELECT date(date, 'start of year', '-1 year') AS date
                    FROM all_dates
                    WHERE date > DATE('{current_date}', 'start of year', '-{intervalo}')
                )
                SELECT STRFTIME('%Y', all_dates.date) AS {periodo}, '{bethouse}' AS bethouse, ROUND(COALESCE(SUM({tabela_aposta}.balanco), 0), 2) AS saldo_periodo, CASE WHEN SUM(aposta) IS NULL THEN COUNT(*) - 1 ELSE COUNT(*) END AS apostas, SUM(aposta) AS investimento, GROUP_CONCAT({tabela_aposta}.id) AS ids
                FROM all_dates
                LEFT JOIN {tabela_aposta} ON STRFTIME('%Y', all_dates.date) = STRFTIME('%Y', {tabela_aposta}.data_entrada)
                GROUP BY STRFTIME('%Y', all_dates.date)
                HAVING STRFTIME('%Y', all_dates.date) >= STRFTIME('%Y', '{current_date}', '-{intervalo}')
                """

        df = pd.read_sql_query(query, conn)

        soma_apostas = df['apostas'].sum()

        if soma_apostas > 0:
            if periodo == 'semana':
                df = df.drop(df.index[-1])

            # Gerar a coluna saldo_bethouse que é a soma cumulativa de saldo_periodo
            df['saldo_bethouse'] = round(saldo_anterior + df['saldo_periodo'].cumsum(), 2)
            df['media_investimento'] = round(df['investimento'] / df['apostas'], 2)

            # Concatenar os resultados no dataframe df_saldos_periodos
            df_saldos = pd.concat([df_saldos, df])

    # Agrupar por 'dia' e combinar os valores de 'ids' em uma única linha, ignorando valores None
    df_apostas_periodo = df_saldos.groupby(periodo)['ids'].apply(lambda x: ','.join([str(i) for i in x if i is not None])).reset_index()
    lista_periodos = list(df_saldos[periodo][:range_val])
    df_apostas_periodo = df_apostas_periodo.sort_values(by=periodo, key=lambda x: x.map({k: i for i, k in enumerate(lista_periodos)})).reset_index(drop=True)

    # Transformar cada linha em um set e remover valores menores que 11 caracteres
    df_apostas_periodo['ids'] = df_apostas_periodo['ids'].apply(lambda x: set(x.split(','))).apply(lambda x: set(item for item in x if len(str(item)) == 11))

    # Criar a coluna 'num_apostas' com o tamanho de cada set
    df_apostas_periodo['num_apostas'] = df_apostas_periodo['ids'].apply(len)

    df_apostas_periodo = df_apostas_periodo[df_apostas_periodo['num_apostas'] != 0]
    df_saldos = df_saldos[df_saldos[periodo].isin(df_apostas_periodo[periodo])]

    return df_saldos, df_apostas_periodo

def agrup_esportes(conn, tempo):
    # Definindo a data atual e a data de 3 meses atrá
    data_3_meses_atras = (datetime.today() - timedelta(days=tempo)).strftime('%Y-%m-%d')

    # Consulta SQL para contar os esportes na coluna 'esporte' nos últimos 3 meses
    query = f"""
        SELECT esporte, COUNT(*) AS total, SUM(lucro_real) AS lucro_total
        FROM apostas
        WHERE data_entrada >= date('{data_3_meses_atras}')
        GROUP BY esporte
    """

    # Executando a consulta
    resultado = pd.read_sql_query(query, conn)

    # Exibindo o DataFrame com os resultados
    return resultado

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

def contar_bethouses(conn, tempo=None):
    if tempo:
        query = f"""
            SELECT bethouse, SUM(total) AS total_ocorrencias, SUM(investimento) AS total_investimento, SUM(win) AS vitoria, SUM(loss) AS loss, SUM(return) AS void
            FROM (
                SELECT bethouse1 AS bethouse, COUNT(*) AS total, SUM(aposta1) AS investimento,
                    SUM(CASE WHEN resultado1 = 'win' OR resultado1 = 'half-win' THEN 1 ELSE 0 END) AS win,
                    SUM(CASE WHEN resultado1 = 'loss' OR resultado1 = 'half-loss' THEN 1 ELSE 0 END) AS loss,
                    SUM(CASE WHEN resultado1 = 'return' THEN 1 ELSE 0 END) AS return
                FROM apostas
                WHERE data_entrada >= date('now', '-{tempo} days') AND bethouse1 IS NOT NULL
                GROUP BY bethouse1
    
                UNION ALL
    
                SELECT bethouse2 AS bethouse, COUNT(*) AS total, SUM(aposta2) AS investimento,
                    SUM(CASE WHEN resultado2 = 'win' OR resultado2 = 'half-win' THEN 1 ELSE 0 END) AS win,
                    SUM(CASE WHEN resultado2 = 'loss' OR resultado2 = 'half-loss' THEN 1 ELSE 0 END) AS loss,
                    SUM(CASE WHEN resultado2 = 'return' THEN 1 ELSE 0 END) AS return
                FROM apostas
                WHERE data_entrada >= date('now', '-{tempo} days') AND bethouse2 IS NOT NULL
                GROUP BY bethouse2
    
                UNION ALL
    
                SELECT bethouse3 AS bethouse, COUNT(*) AS total, SUM(aposta3) AS investimento,
                    SUM(CASE WHEN resultado3 = 'win' OR resultado3 = 'half-win' THEN 1 ELSE 0 END) AS win,
                    SUM(CASE WHEN resultado3 = 'loss' OR resultado3 = 'half-loss' THEN 1 ELSE 0 END) AS loss,
                    SUM(CASE WHEN resultado3 = 'return' THEN 1 ELSE 0 END) AS return
                FROM apostas
                WHERE data_entrada >= date('now', '-{tempo} days') AND bethouse3 IS NOT NULL
                GROUP BY bethouse3
            ) AS subquery
            GROUP BY bethouse
        """
    else:
        query = f"""
                    SELECT bethouse, SUM(total) AS total_ocorrencias, SUM(investimento) AS total_investimento, SUM(win) AS vitoria, SUM(loss) AS loss, SUM(return) AS void
                    FROM (
                        SELECT bethouse1 AS bethouse, COUNT(*) AS total, SUM(aposta1) AS investimento,
                            SUM(CASE WHEN resultado1 = 'win' OR resultado1 = 'half-win' THEN 1 ELSE 0 END) AS win,
                            SUM(CASE WHEN resultado1 = 'loss' OR resultado1 = 'half-loss' THEN 1 ELSE 0 END) AS loss,
                            SUM(CASE WHEN resultado1 = 'return' THEN 1 ELSE 0 END) AS return
                        FROM apostas
                        WHERE AND bethouse1 IS NOT NULL
                        GROUP BY bethouse1

                        UNION ALL

                        SELECT bethouse2 AS bethouse, COUNT(*) AS total, SUM(aposta2) AS investimento,
                            SUM(CASE WHEN resultado2 = 'win' OR resultado2 = 'half-win' THEN 1 ELSE 0 END) AS win,
                            SUM(CASE WHEN resultado2 = 'loss' OR resultado2 = 'half-loss' THEN 1 ELSE 0 END) AS loss,
                            SUM(CASE WHEN resultado2 = 'return' THEN 1 ELSE 0 END) AS return
                        FROM apostas
                        WHERE AND bethouse2 IS NOT NULL
                        GROUP BY bethouse2

                        UNION ALL

                        SELECT bethouse3 AS bethouse, COUNT(*) AS total, SUM(aposta3) AS investimento,
                            SUM(CASE WHEN resultado3 = 'win' OR resultado3 = 'half-win' THEN 1 ELSE 0 END) AS win,
                            SUM(CASE WHEN resultado3 = 'loss' OR resultado3 = 'half-loss' THEN 1 ELSE 0 END) AS loss,
                            SUM(CASE WHEN resultado3 = 'return' THEN 1 ELSE 0 END) AS return
                        FROM apostas
                        WHERE AND bethouse3 IS NOT NULL
                        GROUP BY bethouse3
                    ) AS subquery
                    GROUP BY bethouse
                """

    c = conn.cursor()
    c.execute(query)
    result = c.fetchall()

    df = pd.DataFrame(result, columns=['bethouse', 'ocorrencias', 'investimento', 'vitoria', 'derrota', 'retorno'])
    df['%win'] = round(df['vitoria'] / (df['vitoria'] + df['derrota'] + df['retorno']), 6)
    df['%loss'] = round(df['derrota'] / (df['vitoria'] + df['derrota'] + df['retorno']), 6)
    df['%retorno'] = round(df['retorno'] / (df['vitoria'] + df['derrota'] + df['retorno']), 6)
    df['media_investimento'] = round(df['investimento'] / df['ocorrencias'], 2)
    return df

def odds_resultados(conn, tempo=None, round=3, min=0, min_percent=0):
    if tempo:
        query = f"""
            SELECT odd1 AS odds, resultado1 AS resultados
                FROM apostas
                WHERE data_entrada >= date('now', '-{tempo} days') AND odd1 AND odd1 > 0  IS NOT NULL AND resultado1 IS NOT NULL
                UNION ALL
            SELECT odd2 AS odds, resultado2 AS resultados
                FROM apostas
                WHERE data_entrada >= date('now', '-{tempo} days') AND odd2 AND odd2 > 0  IS NOT NULL AND resultado2 IS NOT NULL
                UNION ALL
            SELECT odd3 AS odds, resultado3 AS resultados
                FROM apostas
                WHERE data_entrada >= date('now', '-{tempo} days') AND odd3 AND odd3 > 0  IS NOT NULL AND resultado3 IS NOT NULL
            """
    else:
        query = f"""
            SELECT odd1 AS odds, resultado1 AS resultados
                FROM apostas
                WHERE odd1 IS NOT NULL AND odd1 > 0 AND resultado1 IS NOT NULL
                UNION ALL
            SELECT odd2 AS odds, resultado2 AS resultados
                FROM apostas
                WHERE odd2 IS NOT NULL AND odd2 > 0  AND resultado2 IS NOT NULL
                UNION ALL
            SELECT odd3 AS odds, resultado3 AS resultados
                FROM apostas
                WHERE odd3 IS NOT NULL AND odd3 > 0  AND resultado3 IS NOT NULL
            """
    df = pd.read_sql_query(query, conn)
    df['odds'] = df['odds'].round(round)
    df_grouped = df.groupby('odds')['resultados'].value_counts().unstack().fillna(0).assign(total=lambda x: x.sum(axis=1)).reset_index()
    if 'win' in df_grouped.columns:
        df_grouped['win'] = df_grouped['win'].astype(int)
    if 'loss' in df_grouped.columns:
        df_grouped['loss'] = df_grouped['loss'].astype(int)
    if 'return' in df_grouped.columns:
        df_grouped['return'] = df_grouped['return'].astype(int)
    df_grouped['total'] = df_grouped['total'].astype(int)
    df_grouped['%win'] = ((((df_grouped['win'] if 'win' in df_grouped.columns else 0) + (df_grouped['half-win'] if 'half-win' in df_grouped.columns else 0)) / df_grouped['total']) * 100).round(2)
    df_grouped['%loss'] = ((((df_grouped['loss'] if 'loss' in df_grouped.columns else 0) + (df_grouped['half-loss'] if 'half-loss' in df_grouped.columns else 0)) / df_grouped['total']) * 100).round(2)
    df_grouped['%return'] = (((df_grouped['return'] if 'return' in df_grouped.columns else 0) / df_grouped['total']) * 100).round(2)
    media = df['odds'].mean()
    desvio = df['odds'].std()
    df_grouped['padrao'] = df_grouped.index.map(lambda odd: (odd - media) / desvio)
    if min > 0:
        df_grouped = df_grouped[df_grouped['total'] > min]
    if min_percent > 0:
        df_grouped = df_grouped[(df_grouped['%win'] > min_percent) & (df_grouped['%win'] < 100 - min_percent) & (
                    (df_grouped['%loss'] > min_percent) & df_grouped['%loss'] < 100 - min_percent) & (
                    df_grouped['%return'] > min_percent) & (df_grouped['%return'] < 100 - min_percent)]


    return df_grouped

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
#view_column(sql_data, '_1xBet_saldos')
#del_column(sql_data, 'apostas', 'id_novo')
#del_table(sql_data, 'apostas')
#del_line(sql_data, 'apostas', id=20230630020)
#del_line(sql_data, 'Ex_BetFair_saldos', id=20230615049)
#del_line(sql_data, 'FavBet_saldos', id=2306250301)
#del_line(sql_data, 'apostas', id=20230630015)
#del_line(sql_data, 'BWin_saldos', id=20230630020)
#del_line(sql_data, 'SportyBet_saldos', id=696)
#del_line(sql_data, 'Pinnacle_saldos', id=2303040101)
#view_tables(sql_data)
#view_column(sql_data, 'apostas')
#view_last_lines(sql_data, 'apostas', 3)
#view_last_lines(sql_data, 'apostas_antigas', 3)
#view_last_lines(sql_data, 'BWin_saldos', 3)
#view_last_lines(sql_data, 'FavBet_saldos', 3)
#view_last_lines(sql_data, 'Ex_BetFair_saldos', 3)
#sum_lucro_estimado(sql_data, 'apostas')

#df['saldo'] = round(df['balanco'].cumsum(), 2)

#print(df)
#print(df[['aposta', 'odd', 'resultado', 'balanco', 'dif_real', 'saldo']])

#df = pd.read_csv('/Users/sergioeblutzer/PycharmProjects/Gerenciamento_Bolsa_Esportiva/apostas_antigas.csv')
#print(df)
