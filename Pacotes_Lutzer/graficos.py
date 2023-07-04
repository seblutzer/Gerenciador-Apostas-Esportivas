import pandas as pd
import sqlite3
import json
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from language import trans_graficos
import datetime
from datetime import date, datetime, timedelta
import re

global bethouse_options_total
with open('/Users/sergioeblutzer/PycharmProjects/Gerenciamento_Bolsa_Esportiva/bethouse_options.json', 'r') as f:
    data = json.load(f)
    bethouse_options_total = data.get("bethouse_options", {})
################ LUCRO POR TEMPO ################
def lucros_por_tempo(range_val, periodo, conn, idioma):
    if periodo == trans_graficos['dia'][idioma]:
        query = f"""
            SELECT STRFTIME('%d', data_entrada) || '/' ||
            (CASE STRFTIME('%m', data_entrada)
                WHEN '01' THEN '{trans_graficos['Jan'][idioma]}'
                WHEN '02' THEN '{trans_graficos['Fev'][idioma]}'
                WHEN '03' THEN '{trans_graficos['Mar'][idioma]}'
                WHEN '04' THEN '{trans_graficos['Abr'][idioma]}'
                WHEN '05' THEN '{trans_graficos['Mai'][idioma]}'
                WHEN '06' THEN '{trans_graficos['Jun'][idioma]}'
                WHEN '07' THEN '{trans_graficos['Jul'][idioma]}'
                WHEN '08' THEN '{trans_graficos['Ago'][idioma]}'
                WHEN '09' THEN '{trans_graficos['Set'][idioma]}'
                WHEN '10' THEN '{trans_graficos['Out'][idioma]}'
                WHEN '11' THEN '{trans_graficos['Nov'][idioma]}'
                WHEN '12' THEN '{trans_graficos['Dez'][idioma]}'
            END) AS {periodo},
            SUM(lucro_estimado) AS lucro_estimado, SUM(lucro_real) AS lucro_real, SUM(CASE WHEN lucro_real IS NULL THEN lucro_estimado ELSE 0 END) AS aberto FROM apostas WHERE DATE(data_entrada) >= DATE('now', '-{range_val + 1} day') GROUP BY {periodo} ORDER BY DATE(data_entrada) ASC"""
    elif periodo == trans_graficos['semana'][idioma]:
        range_val = (range_val - 1) * 7 + datetime.today().isoweekday()
        query = f"""
            SELECT STRFTIME('%d', MIN(data_entrada)) || '-' || STRFTIME('%d', MAX(data_entrada)) || '/' || 
            (CASE STRFTIME('%m', data_entrada)
                WHEN '01' THEN '{trans_graficos['Jan'][idioma]}'
                WHEN '02' THEN '{trans_graficos['Fev'][idioma]}'
                WHEN '03' THEN '{trans_graficos['Mar'][idioma]}'
                WHEN '04' THEN '{trans_graficos['Abr'][idioma]}'
                WHEN '05' THEN '{trans_graficos['Mai'][idioma]}'
                WHEN '06' THEN '{trans_graficos['Jun'][idioma]}'
                WHEN '07' THEN '{trans_graficos['Jul'][idioma]}'
                WHEN '08' THEN '{trans_graficos['Ago'][idioma]}'
                WHEN '09' THEN '{trans_graficos['Set'][idioma]}'
                WHEN '10' THEN '{trans_graficos['Out'][idioma]}'
                WHEN '11' THEN '{trans_graficos['Nov'][idioma]}'
                WHEN '12' THEN '{trans_graficos['Dez'][idioma]}'
        END) AS {periodo}, SUM(lucro_estimado) AS lucro_estimado, SUM(lucro_real) AS lucro_real, SUM(CASE WHEN lucro_real IS NULL THEN lucro_estimado ELSE 0 END) AS aberto FROM apostas WHERE DATE(data_entrada) >= DATE('now', '-{range_val} day') GROUP BY STRFTIME('%Y-%W', data_entrada, 'weekday 6') ORDER BY DATE(data_entrada) ASC
        """
    elif periodo == trans_graficos['mês'][idioma]:
        query = f"""
        SELECT (CASE STRFTIME('%m', data_entrada)
            WHEN '01' THEN '{trans_graficos['Jan'][idioma]}'
            WHEN '02' THEN '{trans_graficos['Fev'][idioma]}'
            WHEN '03' THEN '{trans_graficos['Mar'][idioma]}'
            WHEN '04' THEN '{trans_graficos['Abr'][idioma]}'
            WHEN '05' THEN '{trans_graficos['Mai'][idioma]}'
            WHEN '06' THEN '{trans_graficos['Jun'][idioma]}'
            WHEN '07' THEN '{trans_graficos['Jul'][idioma]}'
            WHEN '08' THEN '{trans_graficos['Ago'][idioma]}'
            WHEN '09' THEN '{trans_graficos['Set'][idioma]}'
            WHEN '10' THEN '{trans_graficos['Out'][idioma]}'
            WHEN '11' THEN '{trans_graficos['Nov'][idioma]}'
            WHEN '12' THEN '{trans_graficos['Dez'][idioma]}'
        END) || '/' || STRFTIME('%Y', data_entrada) AS {periodo}, SUM(lucro_estimado) AS lucro_estimado, SUM(lucro_real) AS lucro_real, SUM(CASE WHEN lucro_real IS NULL THEN lucro_estimado ELSE 0 END) AS aberto FROM apostas WHERE DATE(data_entrada) >= DATE('now', '-{range_val - 1} month', 'start of month') GROUP BY {periodo} ORDER BY DATE(data_entrada) ASC
        """
    elif periodo == trans_graficos['trimestre'][idioma]:
        query = f"""
        SELECT (CASE 
            WHEN STRFTIME('%m', data_entrada) BETWEEN '01' AND '03' THEN '1{periodo[0].upper()}/' || STRFTIME('%Y', data_entrada) 
            WHEN STRFTIME('%m', data_entrada) BETWEEN '04' AND '06' THEN '2{periodo[0].upper()}/' || STRFTIME('%Y', data_entrada) 
            WHEN STRFTIME('%m', data_entrada) BETWEEN '07' AND '09' THEN '3{periodo[0].upper()}/' || STRFTIME('%Y', data_entrada) 
            ELSE '4{periodo[0].upper()}/' || STRFTIME('%Y', data_entrada) 
        END) AS {periodo}, SUM(lucro_estimado) AS lucro_estimado, SUM(lucro_real) AS lucro_real, SUM(CASE WHEN lucro_real IS NULL THEN lucro_estimado ELSE 0 END) AS aberto FROM apostas WHERE DATE(data_entrada) >= DATE('now', '-{range_val * 3 + 1} month') GROUP BY {periodo} ORDER BY DATE(data_entrada) ASC
        """
    elif periodo == trans_graficos['semestre'][idioma]:
        query = f"""
        SELECT (CASE 
            WHEN STRFTIME('%m', data_entrada) >= '07' THEN '2{periodo[0].upper()}/' || STRFTIME('%Y', data_entrada) 
            ELSE '1{periodo[0].upper()}/' || STRFTIME('%Y', data_entrada) 
        END) AS {periodo}, SUM(lucro_estimado) AS lucro_estimado, SUM(lucro_real) AS lucro_real, SUM(CASE WHEN lucro_real IS NULL THEN lucro_estimado ELSE 0 END) AS aberto FROM apostas WHERE DATE(data_entrada) >= DATE('now', '-{range_val * 6 + 1} month') GROUP BY {periodo} ORDER BY DATE(data_entrada) ASC
        """
    else:
        query = f"SELECT STRFTIME('%Y', data_entrada) AS {periodo}, SUM(lucro_estimado) AS lucro_estimado, SUM(lucro_real) AS lucro_real, SUM(CASE WHEN lucro_real IS NULL THEN lucro_estimado ELSE 0 END) AS aberto FROM apostas WHERE DATE(data_entrada) >= DATE('now', '-{range_val - 1} year', 'start of year') GROUP BY {periodo} ORDER BY DATE(data_entrada) ASC"

    df = pd.read_sql_query(query, conn)
    return df
def lucro_tempo(range_val, periodo, conn, idioma, cambio, media=3):
    df = lucros_por_tempo(range_val, periodo, conn, idioma)

    df['media_movel_estimado'] = df['lucro_estimado'].rolling(media, min_periods=1).mean()
    df['media_movel_real'] = df['lucro_real'].rolling(media, min_periods=1).mean()

    fig = go.Figure()

    fig.add_trace(
        go.Bar(x=df[periodo], y=df['lucro_estimado'], name=trans_graficos['Lucro Estimado'][idioma], offset=-0.2, width=0.4))
    fig.add_trace(go.Bar(x=df[periodo], y=df['lucro_real'], name=trans_graficos['Lucro Real'][idioma], offset=0.2, width=0.4))
    fig.add_trace(go.Bar(x=df[periodo], y=df['aberto'], name=trans_graficos['Em aberto'][idioma], base=df['lucro_real'], offset=0.2, width=0.4))

    fig.add_trace(go.Scatter(x=df[periodo], y=df['media_movel_estimado'],
                             name=f"{trans_graficos['Lucro Estimado'][idioma]} ({trans_graficos['Média'][idioma]})", mode='lines', line=dict(width = 4)))
    fig.add_trace(go.Scatter(x=df[periodo], y=df['media_movel_real'],
                             name=f"{trans_graficos['Lucro Real'][idioma]} ({trans_graficos['Média'][idioma]})", mode='lines', line=dict(width = 4)))
    # fomatar o eixo Y
    if periodo == trans_graficos['dia'][idioma]:
        fig.update_layout(title=f"{trans_graficos['Lucro diário dos últimos'][idioma]} {range_val} {trans_graficos['dia'][idioma]}", yaxis_tickprefix=cambio, yaxis_tickformat=',.2f')
    elif periodo == trans_graficos['semana'][idioma]:
        fig.update_layout(title=f"{trans_graficos['Lucro semanal das últimas'][idioma]} {range_val} {trans_graficos['semanas'][idioma]}", yaxis_tickprefix=cambio, yaxis_tickformat=',.2f')
    elif periodo == trans_graficos['mês'][idioma]:
        fig.update_layout(title=f"{trans_graficos['Lucro mensal dos últimos'][idioma]} {range_val} {trans_graficos['meses'][idioma]}", yaxis_tickprefix=cambio, yaxis_tickformat=',.2f')
    elif periodo == trans_graficos['trimestre'][idioma]:
        fig.update_layout(title=f"{trans_graficos['Lucro trimestral dos últimos'][idioma]} {range_val} {trans_graficos['trimestres'][idioma]}", yaxis_tickprefix=cambio, yaxis_tickformat=',.2f')
    elif periodo == trans_graficos['semestre'][idioma]:
        fig.update_layout(title=f"{trans_graficos['Lucro semestral dos últimos'][idioma]} {range_val} {trans_graficos['semestres'][idioma]}", yaxis_tickprefix=cambio, yaxis_tickformat=',.2f')
    elif periodo == trans_graficos['ano'][idioma]:
        fig.update_layout(title=f"{trans_graficos['Lucro anual dos últimos'][idioma]} {range_val} {trans_graficos['anos'][idioma]}", yaxis_tickprefix=cambio, yaxis_tickformat=',.2f')

    fig.show()
################ APOSTAS POR HORA ################
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
def apostas_hora(conn, tempo, idioma):
    df = count_hora(conn, tempo)
    media = df[df['media_apostas'] > 0]['media_apostas'].mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['hora'], y=[media] * len(df['hora']),
                             name=f"{trans_graficos['Apostas Diárias'][idioma]} ({trans_graficos['Média'][idioma]})", mode='lines', line=dict(width=1)))
    fig.add_trace(go.Bar(
        x=df['hora'],
        y=df['media_apostas'],
        name=trans_graficos['Média de Apostas'][idioma],
        hovertemplate=(
            f"{trans_graficos['Hora'][idioma]}" + ": %{x}<br>" +
            f"{trans_graficos['Total de Apostas'][idioma]}" + ": %{customdata}<extra></extra><br>" +
            f"{trans_graficos['Média de Apostas'][idioma]}" + ": %{y}"
        ),
        customdata=df['total_apostas'],
        marker=dict(
            color=df['total_apostas'],
            colorscale=[[0, 'blue'], [1, 'red']],
            line=dict(width=0)
        )
    ))
    fig.add_trace(go.Scatter(
        x=df['hora'],
        y=df['media_lucro'],
        name=trans_graficos['Lucro Médio'][idioma],
        line=dict(width=2),
        hovertemplate=f"{trans_graficos['Hora'][idioma]}" + ": %{x}<br>" +
                  f"{trans_graficos['Lucro Médio'][idioma]}" + ": R$%{y:.2f}<br>"
    ))
    fig.add_trace(go.Bar(
        x=df['hora'],
        y=-((df['desvio_padrao'] / df['total_apostas']) * df['media_apostas']),
        name=trans_graficos['Desvio Padrão'][idioma],
        hovertemplate=f"{trans_graficos['Desvio Padrão'][idioma]}" + ": " + df['desvio_padrao'].round(2).astype(str) + "<br>" + f"{trans_graficos['Desvio Padrão'][idioma]} ({trans_graficos['Média'][idioma]}): " + round((df['desvio_padrao'] / df['total_apostas']) * df['media_apostas'], 2).astype(str),
        width=0.3
    ))

    if tempo == 0:
        fig.update_layout(title=trans_graficos['Número médio de apostas por hora hoje'][idioma], barmode='stack',)
    elif tempo == 1:
        fig.update_layout(title=trans_graficos['Número médio de apostas por hora desde ontem'][idioma], barmode='stack',)
    else:
        fig.update_layout(title=f"{trans_graficos['Número médio de apostas por hora nos últimos'][idioma]} {tempo} {trans_graficos['dias'][idioma]}", barmode='stack',)
    fig.show()
################ SALDOS ################
def saldo_bethouses(conn, range_val, periodo, idioma):
    c = conn.cursor()

    # Dataframe para armazenar os resultados
    df_saldos = pd.DataFrame()
    current_date = date.today()
    current_month = current_date.month
    condition = ''
    if periodo == trans_graficos['dia'][idioma]:
        intervalo = f'{range_val - 1} days'
    elif periodo == trans_graficos['semana'][idioma]:
            intervalo = f'{(range_val - 1) * 7 + (current_date.weekday() + 1)} days'
    elif periodo == trans_graficos['mês'][idioma]:
        intervalo = f'{range_val - 1} month'
        condition = "'start of month',"
    elif periodo == trans_graficos['trimestre'][idioma]:
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
    elif periodo == trans_graficos['semestre'][idioma]:
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
        if periodo == trans_graficos['dia'][idioma]:
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
                    WHEN '01' THEN '{trans_graficos['Jan'][idioma]}'
                    WHEN '02' THEN '{trans_graficos['Fev'][idioma]}'
                    WHEN '03' THEN '{trans_graficos['Mar'][idioma]}'
                    WHEN '04' THEN '{trans_graficos['Abr'][idioma]}'
                    WHEN '05' THEN '{trans_graficos['Mai'][idioma]}'
                    WHEN '06' THEN '{trans_graficos['Jun'][idioma]}'
                    WHEN '07' THEN '{trans_graficos['Jul'][idioma]}'
                    WHEN '08' THEN '{trans_graficos['Ago'][idioma]}'
                    WHEN '09' THEN '{trans_graficos['Set'][idioma]}'
                    WHEN '10' THEN '{trans_graficos['Out'][idioma]}'
                    WHEN '11' THEN '{trans_graficos['Nov'][idioma]}'
                    WHEN '12' THEN '{trans_graficos['Dez'][idioma]}'
                END) AS {periodo},
                '{bethouse}' AS bethouse, ROUND(COALESCE(SUM({tabela_aposta}.balanco), 0), 2) AS saldo_periodo, CASE WHEN SUM(aposta) IS NULL THEN COUNT(*) - 1 ELSE COUNT(*) END AS apostas, SUM(aposta) AS investimento, GROUP_CONCAT({tabela_aposta}.id) AS ids, GROUP_CONCAT({tabela_aposta}.id) AS ids
            FROM all_dates
            LEFT JOIN {tabela_aposta} ON all_dates.date = DATE({tabela_aposta}.data_entrada)
            GROUP BY all_dates.date
            """
        elif periodo == trans_graficos['semana'][idioma]:
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
                        WHEN '01' THEN '{trans_graficos['Jan'][idioma]}'
                        WHEN '02' THEN '{trans_graficos['Fev'][idioma]}'
                        WHEN '03' THEN '{trans_graficos['Mar'][idioma]}'
                        WHEN '04' THEN '{trans_graficos['Abr'][idioma]}'
                        WHEN '05' THEN '{trans_graficos['Mai'][idioma]}'
                        WHEN '06' THEN '{trans_graficos['Jun'][idioma]}'
                        WHEN '07' THEN '{trans_graficos['Jul'][idioma]}'
                        WHEN '08' THEN '{trans_graficos['Ago'][idioma]}'
                        WHEN '09' THEN '{trans_graficos['Set'][idioma]}'
                        WHEN '10' THEN '{trans_graficos['Out'][idioma]}'
                        WHEN '11' THEN '{trans_graficos['Nov'][idioma]}'
                        WHEN '12' THEN '{trans_graficos['Dez'][idioma]}'
                    END) AS {periodo},
                    '{bethouse}' AS bethouse,
                    ROUND(COALESCE(SUM({tabela_aposta}.balanco), 0), 2) AS saldo_periodo, CASE WHEN SUM(aposta) IS NULL THEN COUNT(*) - 1 ELSE COUNT(*) END AS apostas, SUM(aposta) AS investimento, GROUP_CONCAT({tabela_aposta}.id) AS ids
                FROM all_weeks
                LEFT JOIN {tabela_aposta} ON {tabela_aposta}.data_entrada > all_weeks.start_of_week AND {tabela_aposta}.data_entrada <= DATE(all_weeks.start_of_week, '+7 days')
                GROUP BY STRFTIME('%Y-%W', all_weeks.start_of_week)
                HAVING {periodo} IS NOT NULL
                """
        elif periodo == trans_graficos['mês'][idioma]:
            query = f"""
                    WITH all_dates AS (
                        SELECT DATE('{current_date}') AS date
                        UNION ALL
                        SELECT date(date, 'start of month', '-1 month') AS date
                        FROM all_dates
                        WHERE date > DATE('{current_date}', 'start of month', '-{intervalo}')
                    )
                    SELECT (CASE STRFTIME('%m', all_dates.date)
                                WHEN '01' THEN '{trans_graficos['Jan'][idioma]}'
                                WHEN '02' THEN '{trans_graficos['Fev'][idioma]}'
                                WHEN '03' THEN '{trans_graficos['Mar'][idioma]}'
                                WHEN '04' THEN '{trans_graficos['Abr'][idioma]}'
                                WHEN '05' THEN '{trans_graficos['Mai'][idioma]}'
                                WHEN '06' THEN '{trans_graficos['Jun'][idioma]}'
                                WHEN '07' THEN '{trans_graficos['Jul'][idioma]}'
                                WHEN '08' THEN '{trans_graficos['Ago'][idioma]}'
                                WHEN '09' THEN '{trans_graficos['Set'][idioma]}'
                                WHEN '10' THEN '{trans_graficos['Out'][idioma]}'
                                WHEN '11' THEN '{trans_graficos['Nov'][idioma]}'
                                WHEN '12' THEN '{trans_graficos['Dez'][idioma]}'
                            END) || '/' || SUBSTR(STRFTIME('%Y', all_dates.date), 3) AS {periodo},
                           '{bethouse}' AS bethouse,
                           ROUND(COALESCE(SUM({tabela_aposta}.balanco), 0), 2) AS saldo_periodo, CASE WHEN SUM(aposta) IS NULL THEN COUNT(*) - 1 ELSE COUNT(*) END AS apostas, SUM(aposta) AS investimento, GROUP_CONCAT({tabela_aposta}.id) AS ids
                    FROM all_dates
                    LEFT JOIN {tabela_aposta} ON STRFTIME('%m/%Y', all_dates.date) = STRFTIME('%m/%Y', {tabela_aposta}.data_entrada)
                    GROUP BY STRFTIME('%Y-%m', all_dates.date)
                """
        elif periodo == trans_graficos['trimestre'][idioma]:
            query = f"""
                WITH all_quarters AS (
                    SELECT DATE('{current_date}', 'start of month') AS start_of_quarter,
                           (CASE STRFTIME('%m', DATE('{current_date}', 'start of month'))
                                WHEN '01' THEN '1{trans_graficos['trimestre'][idioma][0].upper()}'
                                WHEN '04' THEN '2{trans_graficos['trimestre'][idioma][0].upper()}'
                                WHEN '07' THEN '3{trans_graficos['trimestre'][idioma][0].upper()}'
                                WHEN '10' THEN '4{trans_graficos['trimestre'][idioma][0].upper()}'
                            END) || ' ' || STRFTIME('%Y', DATE('{current_date}', 'start of month')) AS quarter_name
                    UNION ALL
                    SELECT DATE(start_of_quarter, '-3 months') AS start_of_quarter,
                           (CASE STRFTIME('%m', DATE(start_of_quarter, '-3 months'))
                                WHEN '01' THEN '1{trans_graficos['trimestre'][idioma][0].upper()}'
                                WHEN '04' THEN '2{trans_graficos['trimestre'][idioma][0].upper()}'
                                WHEN '07' THEN '3{trans_graficos['trimestre'][idioma][0].upper()}'
                                WHEN '10' THEN '4{trans_graficos['trimestre'][idioma][0].upper()}'
                            END) || ' ' || STRFTIME('%Y', DATE(start_of_quarter, '-3 months')) AS quarter_name
                    FROM all_quarters
                    WHERE start_of_quarter > DATE('{current_date}', 'start of month', '-{intervalo}')
                )
                SELECT CASE
                   WHEN {tabela_aposta}.data_entrada IS NULL THEN all_quarters.quarter_name
                   ELSE all_quarters.quarter_name END AS {periodo}, '{bethouse}' AS bethouse,
                   ROUND(COALESCE(SUM({tabela_aposta}.balanco), 0), 2) AS saldo_periodo, CASE WHEN SUM(aposta) IS NULL THEN COUNT(*) - 1 ELSE COUNT(*) END AS apostas, SUM(aposta) AS investimento, GROUP_CONCAT({tabela_aposta}.id) AS ids
                FROM all_quarters
                LEFT JOIN {tabela_aposta} ON {tabela_aposta}.data_entrada >= all_quarters.start_of_quarter AND {tabela_aposta}.data_entrada < DATE(all_quarters.start_of_quarter, '+3 months')
                GROUP BY STRFTIME('%Y-%m', all_quarters.start_of_quarter)
                """
        elif periodo == trans_graficos['semestre'][idioma]:
            query = f"""
                WITH all_semesters AS (
                    SELECT DATE('{current_date}', 'start of month') AS start_of_semester,
                           (CASE STRFTIME('%m', DATE('{current_date}', 'start of month'))
                                WHEN '01' THEN '1{trans_graficos['semestre'][idioma][0].upper()}'
                                WHEN '07' THEN '2{trans_graficos['semestre'][idioma][0].upper()}'
                            END) || ' ' || STRFTIME('%Y', DATE('{current_date}', 'start of month')) AS semester_name
                    UNION ALL
                    SELECT DATE(start_of_semester, '-6 months') AS start_of_semester,
                        (CASE STRFTIME('%m', DATE(start_of_semester, '-6 months'))
                            WHEN '01' THEN '1{trans_graficos['semestre'][idioma][0].upper()}'
                            WHEN '07' THEN '2{trans_graficos['semestre'][idioma][0].upper()}'
                        END) || ' ' || STRFTIME('%Y', DATE(start_of_semester, '-6 months')) AS semester_name
                    FROM all_semesters
                    WHERE start_of_semester > DATE('{current_date}', 'start of month', '-{intervalo}')
                )
                SELECT CASE
                   WHEN {tabela_aposta}.data_entrada IS NULL THEN all_semesters.semester_name
                   ELSE all_semesters.semester_name END AS {periodo}, '{bethouse}' AS bethouse,
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
            if periodo == trans_graficos['semana'][idioma]:
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
def calc_saldo_bethouse(conn, range, periodo, bethouse_options_total, idioma, cambio):
    df, total_apostas = saldo_bethouses(conn, range, periodo, idioma)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df[periodo].unique(),
        y=df.groupby(periodo)['saldo_bethouse'].mean(),
        name=trans_graficos['Saldo Médio'][idioma],
        marker=dict(color='rgba(0,0,0,0.8)'),
        opacity=0.5
    ))
    for bethouse in df['bethouse'].unique():
        df_bethouse = df[df['bethouse'] == bethouse]
        fig.add_trace(go.Scatter(x=df_bethouse[periodo], y=df_bethouse['saldo_bethouse'], name=bethouse,
                                 marker=dict(color=bethouse_options_total[bethouse]['background_color']),
                                 line=dict(color=bethouse_options_total[bethouse]['text_color'],
                                           width = 6)))
    if periodo == trans_graficos['dia'][idioma]:
        fig.update_layout(title=trans_graficos['Variação diária'][idioma], yaxis_tickprefix=f'{cambio} ', yaxis_tickformat=',.2f')
    elif periodo == trans_graficos['semana'][idioma]:
        fig.update_layout(title=trans_graficos['Variação semanal'][idioma], yaxis_tickprefix=f'{cambio} ', yaxis_tickformat=',.2f')
    elif periodo == trans_graficos['mês'][idioma]:
        fig.update_layout(title=trans_graficos['Variação mensal'][idioma], yaxis_tickprefix=f'{cambio} ', yaxis_tickformat=',.2f')
    elif periodo == trans_graficos['trimestre'][idioma]:
        fig.update_layout(title=trans_graficos['Variação trimestral'][idioma], yaxis_tickprefix=f'{cambio} ', yaxis_tickformat=',.2f')
    elif periodo == trans_graficos['semestre'][idioma]:
        fig.update_layout(title=trans_graficos['Variação semestral'][idioma], yaxis_tickprefix=f'{cambio} ', yaxis_tickformat=',.2f')
    elif periodo == trans_graficos['ano'][idioma]:
        fig.update_layout(title=trans_graficos['Variação anual'][idioma], yaxis_tickprefix=f'{cambio} ', yaxis_tickformat=',.2f')
    fig.show()
################ APOSTAS POR BETHOUSE ################
def apostas_bethouses(conn, range, periodo, bethouse_options_total, idioma, top=0, bottom=0):
    df, total_apostas = saldo_bethouses(conn, range, periodo, idioma)

    # Define the top_bethouses and bottom_bethouses variables
    top_bethouses = df.groupby('bethouse')['apostas'].sum().nlargest(top).index if top > 0 else []
    bottom_bethouses = df.groupby('bethouse')['apostas'].sum().nsmallest(bottom).index if bottom > 0 else []

    # Filter the data based on the top and bottom parameters
    if top > 0:
        df_top = df[df['bethouse'].isin(top_bethouses)]
    if bottom > 0:
        df_bottom = df[df['bethouse'].isin(bottom_bethouses)]

    if top > 0:
        if bottom > 0:
            df_others = df[~df['bethouse'].isin(top_bethouses) & ~df['bethouse'].isin(bottom_bethouses)]
            df = pd.concat([df_top, df_bottom], ignore_index=True)
        else:
            df_others = df[~df['bethouse'].isin(top_bethouses)]
            df = df_top
        df_others = df_others.groupby(periodo)['apostas'].sum().reset_index()
        df_others['bethouse'] = 'Outras'
        df_others = df_others.set_index(periodo)
        df_others = df_others.reindex(df[periodo].iloc[:range])
        df_others = df_others.reset_index()
        df = pd.concat([df, df_others], ignore_index=True)
        bethouse_options_total['Outras'] = {
            'background_color': 'pink',
            'text_color': 'gray'}
        pass
    elif bottom > 0:
        df = df_bottom

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=total_apostas[periodo].unique(),
        y=total_apostas['num_apostas'],
        name=trans_graficos['Total de Apostas'][idioma],
        marker=dict(color='rgba(0,0,0,0.8)'),
        opacity=0.5
    ))
    for bethouse in df['bethouse'].unique():
        df_bethouse = df[df['bethouse'] == bethouse]

        fig.add_trace(go.Scatter(
            x=df_bethouse[periodo],
            y=df_bethouse['apostas'],
            name=bethouse,
            hovertemplate=(
                f"{bethouse} " + trans_graficos['em'][idioma] + " %{x}<br>" +
                "%{y} " + trans_graficos['apostas'][idioma] + "<br>" +
                "%{customdata:.2f}% " + trans_graficos['das apostas'][idioma] + "<extra></extra>"
            ),
            customdata=df_bethouse['apostas'] / total_apostas['num_apostas'] * 100,
            marker=dict(color=bethouse_options_total[bethouse]['background_color']),
            line=dict(
                color=bethouse_options_total[bethouse]['text_color'],
                width=5
            )
        ))
    if periodo == trans_graficos['dia'][idioma]:
        fig.update_layout(title=trans_graficos['Quantidade diária'][idioma])
    elif periodo == trans_graficos['semana'][idioma]:
        fig.update_layout(title=trans_graficos['Quantidade semanal'][idioma])
    elif periodo == trans_graficos['mês'][idioma]:
        fig.update_layout(title=trans_graficos['Quantidade mensal'][idioma])
    elif periodo == trans_graficos['trimestre'][idioma]:
        fig.update_layout(title=trans_graficos['Quantidade trimestral'][idioma])
    elif periodo == trans_graficos['semestre'][idioma]:
        fig.update_layout(title=trans_graficos['Quantidade semestral'][idioma])
    elif periodo == trans_graficos['ano'][idioma]:
        fig.update_layout(title=trans_graficos['Quantidade anual'][idioma])

    fig.show()
################ ESPORTES ################
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
def relacao_esportes(conn, range_val, idioma, cambio, valor=False):
    df = agrup_esportes(conn, range_val)
    df['esporte'] = df['esporte'].apply(lambda x: trans_graficos[x][idioma] if x in linguagem else x)

    fig = make_subplots(rows=2, cols=2,
                        specs=[[{'type': 'domain', 'colspan': 2}, None], [{'type': 'domain'}, {'type': 'domain'}]])

    fig.add_trace(go.Pie(labels=df['esporte'], values=df['total'], name=trans_graficos['Total'][idioma]), 1, 1)
    fig.add_trace(go.Pie(labels=df['esporte'], values=df['lucro_total'], name=trans_graficos['Lucro Total'][idioma]), 2, 1)
    fig.add_trace(go.Pie(labels=df['esporte'], values=df['lucro_total'] / df['total'], name=trans_graficos['Lucro Médio'][idioma]), 2, 2)

    if valor:
        fig.data[1].texttemplate = cambio + ' %{value:,.2f}'
    fig.data[2].texttemplate = cambio + ' %{value:,.2f}'

    fig.update_layout(title=f"{trans_graficos['Apostas por Esportes dos ultimos'][idioma]} {range_val} {trans_graficos['dias'][idioma]}")

    fig.show()
################ VITÓRIA VS DERROTA POR BETHOUSE ################
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
def eficiencia_bethouses(conn, idioma, tempo=None):
    df = contar_bethouses(conn, tempo=tempo)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['bethouse'],
        y=df['%win'],
        name=trans_graficos['Vitória'][idioma],
        marker_color='blue',
        hovertemplate=(
                "%{x}<br>" +
                trans_graficos['Vitórias'][idioma] + ": %{customdata}<extra></extra><br>" +
                f"{trans_graficos['Vitória'][idioma]}(%): " + "%{y}<br>"),
        customdata=df['vitoria']
    ))
    fig.add_trace(go.Bar(
        x=df['bethouse'],
        y=df['%retorno'],
        name=trans_graficos['Retorno'][idioma],
        marker_color='gray',
        hovertemplate = (
            "%{x}<br>" +
            trans_graficos['Retornos'][idioma] + ": %{customdata}<extra></extra><br>" +
            f"{trans_graficos['Retorno'][idioma]}(%): " + "%{y}<br>"),
        customdata = df['retorno']
    ))
    fig.add_trace(go.Bar(
        x=df['bethouse'],
        y=df['%loss'],
        name=trans_graficos['Derrota'][idioma],
        marker_color='red',
        hovertemplate = (
            "%{x}<br>" +
            trans_graficos['Derrotas'][idioma] + ": %{customdata}<extra></extra><br>" +
            f"{trans_graficos['Derrota'][idioma]}(%): " + "%{y}<br>"),
        customdata = df['derrota']
    ))
    fig.update_layout(
        title=trans_graficos['Resultados por Betting House'][idioma],
        xaxis=dict(title='BetHouse'),
        yaxis=dict(title=trans_graficos['Percentual'][idioma], tickformat='.0%'),
        barmode='stack'
    )
    fig.show()
################ BETHOUSE ################
def relacao_bethouses(conn, range, idioma, cambio):
    df = contar_bethouses(conn, range)
    fig = make_subplots(rows=2, cols=2,
                        specs=[[{'type': 'domain', 'colspan': 2}, None], [{'type': 'domain'}, {'type': 'domain'}]])

    fig.add_trace(go.Pie(
        labels=df['bethouse'],
        values=df['ocorrencias'],
        name=trans_graficos['Total de Apostas'][idioma],
        marker=dict(
            colors=[bethouse_options_total[bethouse]['background_color'] for bethouse in df['bethouse']],
            line=dict(
                color=[bethouse_options_total[bethouse]['text_color'] for bethouse in df['bethouse']],
                width=3
            )
        )
    ), 1, 1)
    fig.add_trace(go.Pie(
        labels=df['bethouse'],
        values=df['investimento'],
        name=trans_graficos['Investimento'][idioma],
        marker=dict(
            colors=[bethouse_options_total[bethouse]['background_color'] for bethouse in df['bethouse']],
            line=dict(
                color=[bethouse_options_total[bethouse]['text_color'] for bethouse in df['bethouse']],
                width=3
            )
        )
    ), 2, 1)
    fig.add_trace(go.Pie(
        labels=df['bethouse'],
        values=df['media_investimento'],
        name=trans_graficos['Média de Investimento'][idioma],
        marker=dict(
            colors=[bethouse_options_total[bethouse]['background_color'] for bethouse in df['bethouse']],
            line=dict(
                color=[bethouse_options_total[bethouse]['text_color'] for bethouse in df['bethouse']],
                width=3
            )
        )
    ), 2, 2)

    fig.data[1].texttemplate = cambio +' %{value:,.2f}'
    fig.data[2].texttemplate = cambio +' %{value:,.2f}'

    fig.update_layout(title=f"{trans_graficos['Relação de volume'][idioma]} {range} {trans_graficos['dias'][idioma]}")

    fig.show()
################ ODDS ################
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
def odds_x_resultado(conn, idioma, tempo=None, round=0, min=0, min_percent=0):
    df = odds_resultados(conn, tempo=tempo, round=round, min=min, min_percent=min_percent)

    # Calcular a média móvel
    window_size = 10  # Tamanho da janela para a média móvel
    rolling_win = df['%win'].rolling(window=window_size, min_periods=1).mean()
    rolling_loss = df['%loss'].rolling(window=window_size, min_periods=1).mean()
    rolling_return = df['%return'].rolling(window=window_size, min_periods=1).mean()

    # Criação dos traces para cada coluna
    trace_win = go.Scatter(
        x=df['odds'],
        y=df['%win'],
        hovertemplate=trans_graficos['Odd'][idioma] + ': %{x}<br>' + df['win'].astype(str) + ' / ' + df['total'].astype(
            str) + ' ' + trans_graficos['apostas'][idioma] + '<br>%{y}% ' + trans_graficos['apostas ganhas'][idioma],
        name='%' + trans_graficos['Vitória'][idioma],
        mode='markers',
        line=dict(color='green')
    )

    trace_loss = go.Scatter(
        x=df['odds'],
        y=df['%loss'],
        name='%' + trans_graficos['Derrota'][idioma],
        hovertemplate=trans_graficos['Odd'][idioma] + ': %{x}<br>' + df['loss'].astype(str) + ' / ' + df['total'].astype(
            str) + ' ' + trans_graficos['apostas'][idioma] + '<br>%{y}% ' + trans_graficos['apostas perdidas'][idioma],
        mode='markers',
        line=dict(color='red')
    )

    trace_return = go.Scatter(
        x=df['padrao'],
        y=df['%return'],
        hovertemplate='Odd: %{x}<br>' + df['return'].astype(str) + ' / ' + df['total'].astype(
            str) + ' ' + trans_graficos['apostas'][idioma] + '<br>%{y}% ' + trans_graficos['apostas anuladas'][idioma],
        name='%' + trans_graficos['Retorno'][idioma],
        mode='markers',
        line=dict(color='gray')
    )

    # Average lines
    average_win = go.Scatter(
        x=df['padrao'],
        y=rolling_win,
        name=trans_graficos['Média de vitória'][idioma],
        mode='lines',
        line=dict(color='green', dash='dash')
    )

    average_loss = go.Scatter(
        x=df['padrao'],
        y=rolling_loss,
        name=trans_graficos['Média de derrota'][idioma],
        mode='lines',
        line=dict(color='red', dash='dash')
    )

    average_return = go.Scatter(
        x=df['odds'],
        y=rolling_return,
        name=trans_graficos['Média de retorno'][idioma],
        mode='lines',
        line=dict(color='gray', dash='dash')
    )

    # Criação do layout do gráfico
    layout = go.Layout(title=trans_graficos['Relação de Odds sempre'][idioma] if not tempo else f"{trans_graficos['Relação de Odds'][idioma]} {tempo} {trans_graficos['dias'][idioma]}", xaxis=dict(title='Odds'), yaxis=dict(title='Porcentagem'))

    # Criação da figura e adição dos traces ao layout
    fig = go.Figure(data=[trace_win, trace_loss, trace_return, average_win, average_loss, average_return], layout=layout)
    customdata = df[['odds', 'total']].T.values.tolist()
    fig.update_traces(customdata=customdata)

    # Exibição do gráfico
    fig.show()


#conn = sqlite3.connect('/Users/sergioeblutzer/PycharmProjects/Gerenciamento_Bolsa_Esportiva/dados.db')
#c = conn.cursor()
#lucro_tempo(20, 'dia', conn, media=10)
#apostas_hora(conn, 10)
#calc_saldo_bethouse(conn, 4, 'semestre', bethouse_options_total, 'Português', 'R$')
#apostas_bethouses(conn, 5, 'quarter', bethouse_options_total, 'English')
#relacao_esportes(conn, 180, 'Italiano', 'R$', valor=True)
#eficiencia_bethouses(conn, 'English', 30)
#relacao_bethouses(conn, 90, 'English', 'USS')
#odds_x_resultado(conn, 'English', tempo=900, round=1, min=3, min_percent=1)
