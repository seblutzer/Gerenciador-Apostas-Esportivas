import pandas as pd
import sqlite3
from Pacotes_Lutzer.sqlite_commands import lucros_por_tempo, count_hora, saldo_bethouses, agrup_esportes, contar_bethouses, odds_resultados
import json
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
import numpy as np

global bethouse_options_total
with open('/Users/sergioeblutzer/PycharmProjects/Gerenciamento_Bolsa_Esportiva/bethouse_options.json', 'r') as f:
    data = json.load(f)
    bethouse_options_total = data.get("bethouse_options", {})

def lucro_tempo(range_val, periodo, conn, media=3):
    df = lucros_por_tempo(range_val, periodo, conn)

    df['media_movel_estimado'] = df['lucro_estimado'].rolling(media, min_periods=1).mean()
    df['media_movel_real'] = df['lucro_real'].rolling(media, min_periods=1).mean()

    fig = go.Figure()

    fig.add_trace(
        go.Bar(x=df[periodo], y=df['lucro_estimado'], name='Lucro Estimado', offset=-0.2, width=0.4))
    fig.add_trace(go.Bar(x=df[periodo], y=df['lucro_real'], name='Lucro Real', offset=0.2, width=0.4))
    fig.add_trace(go.Bar(x=df[periodo], y=df['aberto'], name='Em aberto', base=df['lucro_real'], offset=0.2, width=0.4))

    fig.add_trace(go.Scatter(x=df[periodo], y=df['media_movel_estimado'],
                             name='Lucro Estimado (Média)', mode='lines', line=dict(width = 4)))
    fig.add_trace(go.Scatter(x=df[periodo], y=df['media_movel_real'],
                             name='Lucro Real (Média)', mode='lines', line=dict(width = 4)))
    gen = 'o'
    if periodo == 'dia':
        periodico = 'diário'
    elif periodo == 'semana':
        periodico = 'semanal'
        gen = 'a'
    elif periodo == 'mes':
        periodico = 'mensal'
    elif periodo == 'trimestre':
        periodico = 'trimestral'
    elif periodo == 'semestre':
        periodico = 'semestral'
    elif periodo == 'ano':
        periodico = 'anual'
    # Formatar o eixo Y
    fig.update_layout(title=f'Lucro {periodico} d{gen}s ultim{gen}s {range_val} {periodo}s', yaxis_tickprefix='R$', yaxis_tickformat=',.2f')

    fig.show()

def apostas_hora(conn, tempo):
    df = count_hora(conn, tempo)
    media = df[df['media_apostas'] > 0]['media_apostas'].mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['hora'], y=[media] * len(df['hora']),
                             name='Média de Apostas Diária', mode='lines', line=dict(width=1)))
    fig.add_trace(go.Bar(
        x=df['hora'],
        y=df['media_apostas'],
        name='Média de Apostas',
        hovertemplate=(
            "Hora: %{x}<br>" +
            "Total de Apostas: %{customdata}<extra></extra><br>" +
            "Média de Apostas: %{y}"
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
        name='Lucro médio',
        line=dict(width=2),
        hovertemplate="Hora: %{x}<br>" +
                  "Lucro médio: R$%{y:.2f}<br>"
    ))
    fig.add_trace(go.Bar(
        x=df['hora'],
        y=-((df['desvio_padrao'] / df['total_apostas']) * df['media_apostas']),
        name='Desvio padrão',
        hovertemplate="Desvio padrão: " + df['desvio_padrao'].round(2).astype(str) + "<br>Desvio padrão médio: " + round((df['desvio_padrao'] / df['total_apostas']) * df['media_apostas'], 2).astype(str),
        width=0.3
    ))

    if tempo == 0:
        fig.update_layout(title=f"Número médio de apostas por hora hoje", barmode='stack',)
    elif tempo == 1:
        fig.update_layout(title=f"Número médio de apostas por hora desde ontem", barmode='stack',)
    else:
        fig.update_layout(title=f"Número médio de apostas por hora nos últimos {tempo} dias", barmode='stack',)
    fig.show()

def calc_saldo_bethouse(conn, range, periodo, bethouse_options_total):
    df, total_apostas = saldo_bethouses(conn, range, periodo)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df[periodo].unique(),
        y=df.groupby(periodo)['saldo_bethouse'].mean(),
        name='Saldo Médio',
        marker=dict(color='rgba(0,0,0,0.8)'),
        opacity=0.5
    ))
    for bethouse in df['bethouse'].unique():
        df_bethouse = df[df['bethouse'] == bethouse]
        fig.add_trace(go.Scatter(x=df_bethouse[periodo], y=df_bethouse['saldo_bethouse'], name=bethouse,
                                 marker=dict(color=bethouse_options_total[bethouse]['background_color']),
                                 line=dict(color=bethouse_options_total[bethouse]['text_color'],
                                           width = 6)))
    if periodo == 'dia':
        periodico = 'diário'
    elif periodo == 'semana':
        periodico = 'semanal'
    elif periodo == 'mes':
        periodico = 'mensal'
    elif periodo == 'trimestre':
        periodico = 'trimestral'
    elif periodo == 'semestre':
        periodico = 'semestral'
    elif periodo == 'ano':
        periodico = 'anual'
    fig.update_layout(title=f'Variação {periodico} do Saldo das BetHouses', yaxis_tickprefix='R$ ', yaxis_tickformat=',.2f')
    fig.show()

def apostas_bethouses(conn, range, periodo, bethouse_options_total, top=0, bottom=0):
    df, total_apostas = saldo_bethouses(conn, range, periodo)

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
        name='Total de Apostas',
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
                f"{bethouse}" + " em %{x}<br>" +
                "%{y} apostas<br>" +
                "%{customdata:.2f}% das apostas<extra></extra>"
            ),
            customdata=df_bethouse['apostas'] / total_apostas['num_apostas'] * 100,
            marker=dict(color=bethouse_options_total[bethouse]['background_color']),
            line=dict(
                color=bethouse_options_total[bethouse]['text_color'],
                width=5
            )
        ))
    if periodo == 'dia':
        periodico = 'diária'
    elif periodo == 'semana':
        periodico = 'semanal'
    elif periodo == 'mês':
        periodico = 'mensal'
    elif periodo == 'trimestre':
        periodico = 'trimestral'
    elif periodo == 'semestre':
        periodico = 'semestral'
    elif periodo == 'ano':
        periodico = 'anual'
    fig.update_layout(title=f"Quantidade {periodico} de Apostas em cada BetHouses")

    fig.show()


def relacao_esportes(conn, range, valor=False):
    df = agrup_esportes(conn, range)
    fig = make_subplots(rows=2, cols=2,
                        specs=[[{'type': 'domain', 'colspan': 2}, None], [{'type': 'domain'}, {'type': 'domain'}]])

    fig.add_trace(go.Pie(labels=df['esporte'], values=df['total'], name="Total"), 1, 1)
    fig.add_trace(go.Pie(labels=df['esporte'], values=df['lucro_total'], name="Lucro Total"), 2, 1)
    fig.add_trace(go.Pie(labels=df['esporte'], values=df['lucro_total'] / df['total'], name="Lucro Médio"), 2, 2)

    if valor:
        fig.data[1].texttemplate = 'R$ %{value:,.2f}'
    fig.data[2].texttemplate = 'R$ %{value:,.2f}'

    fig.update_layout(title=f"Apostas por Esportes dos ultimos {range} dias")

    fig.show()

def eficiencia_bethouses(conn, tempo=None):
    df = contar_bethouses(conn, tempo=tempo)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['bethouse'],
        y=df['%win'],
        name='Vitória',
        marker_color='blue',
        hovertemplate=(
                "%{x}<br>" +
                "Vitórias: %{customdata}<extra></extra><br>" +
                "Vitória(%): %{y}<br>"),
        customdata=df['vitoria']
    ))
    fig.add_trace(go.Bar(
        x=df['bethouse'],
        y=df['%retorno'],
        name='Retorno',
        marker_color='gray',
        hovertemplate = (
            "%{x}<br>" +
            "Retornos: %{customdata}<extra></extra><br>" +
            "Retorno(%): %{y}<br>"),
        customdata = df['retorno']
    ))
    fig.add_trace(go.Bar(
        x=df['bethouse'],
        y=df['%loss'],
        name='Derrota',
        marker_color='red',
        hovertemplate = (
            "%{x}<br>" +
            "Derrotas: %{customdata}<extra></extra><br>" +
            "Derrota(%): %{y}<br>"),
        customdata = df['derrota']
    ))
    fig.update_layout(
        title='Resultados por Betting House',
        xaxis=dict(title='Betting House'),
        yaxis=dict(title='Percentual', tickformat='.0%'),
        barmode='stack'
    )
    fig.show()

def relacao_bethouses(conn, range):
    df = contar_bethouses(conn, range)
    fig = make_subplots(rows=2, cols=2,
                        specs=[[{'type': 'domain', 'colspan': 2}, None], [{'type': 'domain'}, {'type': 'domain'}]])

    fig.add_trace(go.Pie(
        labels=df['bethouse'],
        values=df['ocorrencias'],
        name="Total de Apostas",
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
        name="Investimento",
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
        name="Média de Investimento",
        marker=dict(
            colors=[bethouse_options_total[bethouse]['background_color'] for bethouse in df['bethouse']],
            line=dict(
                color=[bethouse_options_total[bethouse]['text_color'] for bethouse in df['bethouse']],
                width=3
            )
        )
    ), 2, 2)

    fig.data[1].texttemplate = 'R$ %{value:,.2f}'
    fig.data[2].texttemplate = 'R$ %{value:,.2f}'

    fig.update_layout(title=f"Relação de volume de Apostas por BetHouses do últimos {range} dias")

    fig.show()

def odds_x_resultado(conn, tempo=None, round=0, min=0, min_percent=0):
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
        hovertemplate='Odd: %{x}<br>' + df['win'].astype(str) + ' / ' + df['total'].astype(
            str) + ' apostas<br>%{y}% apostas ganhas',
        name='%win',
        mode='markers',
        line=dict(color='green')
    )

    trace_loss = go.Scatter(
        x=df['odds'],
        y=df['%loss'],
        name='%loss',
        hovertemplate='Odd: %{x}<br>' + df['loss'].astype(str) + ' / ' + df['total'].astype(
            str) + ' apostas<br>%{y}% apostas perdidas',
        mode='markers',
        line=dict(color='red')
    )

    trace_return = go.Scatter(
        x=df['padrao'],
        y=df['%return'],
        hovertemplate='Odd: %{x}<br>' + df['return'].astype(str) + ' / ' + df['total'].astype(
            str) + ' apostas<br>%{y}% apostas anuladas',
        name='%return',
        mode='markers',
        line=dict(color='gray')
    )

    # Average lines
    average_win = go.Scatter(
        x=df['padrao'],
        y=rolling_win,
        name='Média de vitória',
        mode='lines',
        line=dict(color='green', dash='dash')
    )

    average_loss = go.Scatter(
        x=df['padrao'],
        y=rolling_loss,
        name='Média de derrota',
        mode='lines',
        line=dict(color='red', dash='dash')
    )

    average_return = go.Scatter(
        x=df['odds'],
        y=rolling_return,
        name='Média de anulação',
        mode='lines',
        line=dict(color='gray', dash='dash')
    )

    # Criação do layout do gráfico
    layout = go.Layout(title='Relação de Odds com Resultados desde sempre' if not tempo else f'Relação de Odds com Resultados nos últimos {tempo} dias', xaxis=dict(title='Odds'), yaxis=dict(title='Porcentagem'))

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
#calc_saldo_bethouse(conn, 10, 'dia', bethouse_options_total)
#apostas_bethouses(conn, 5, 'semestre', bethouse_options_total)
#relacao_esportes(conn, 180, valor=True)
#eficiencia_bethouses(conn, 30)
#relacao_bethouses(conn, 90)
#odds_x_resultado(conn, tempo=900, round=1, min=3, min_percent=1)
