# Função para atualizar o gráfico interativamente
def lucros_por_tempo():
    # Obtenha os valores selecionados dos widgets de entrada
    range_val = int(range1_entry.get())
    periodo = periodo1_var.get()

    if periodo == 'dia':
        query = f"SELECT strftime('%d/%m', data_entrada) AS dia, SUM(lucro_estimado) AS lucro_estimado, SUM(lucro_real) AS lucro_real FROM apostas WHERE DATE(data_entrada) >= DATE('now', '-{range_val + 1} day') GROUP BY dia ORDER BY DATE(data_entrada) ASC"
    elif periodo == 'semana':
        query = f"SELECT STRFTIME('%d', MIN(data_entrada)) || '-' || STRFTIME('%d', MAX(data_entrada)) || '/' || STRFTIME('%m', data_entrada) AS semana, SUM(lucro_estimado) AS lucro_estimado, SUM(lucro_real) AS lucro_real FROM apostas WHERE DATE(data_entrada) >= DATE('now', '-{range_val * 7 + 1} day') GROUP BY STRFTIME('%Y-%W', data_entrada) ORDER BY DATE(data_entrada) ASC"
    elif periodo == 'mes':
        query = f"SELECT STRFTIME('%m/%Y', data_entrada) AS mes, SUM(lucro_estimado) AS lucro_estimado, SUM(lucro_real) AS lucro_real FROM apostas WHERE DATE(data_entrada) >= DATE('now', '-{range_val + 1} month') GROUP BY mes ORDER BY DATE(data_entrada) ASC"
    elif periodo == 'trimestre':
        query = f"SELECT STRFTIME('%m', MIN(data_entrada)) || '-' || STRFTIME('%m', MAX(data_entrada)) || '/' || STRFTIME('%Y', data_entrada) AS trimestre, SUM(lucro_estimado) AS lucro_estimado, SUM(lucro_real) AS lucro_real FROM apostas WHERE DATE(data_entrada) >= DATE('now', '-{range_val * 3 + 1} month') GROUP BY STRFTIME('%Y-%m', data_entrada, 'start of quarter') ORDER BY DATE(data_entrada) ASC"
    elif periodo == 'semestre':
        query = f"SELECT CASE WHEN STRFTIME('%m', data_entrada) >= '07' THEN STRFTIME('%m', data_entrada) || '-12/' || STRFTIME('%Y', data_entrada) ELSE '01-06/' || STRFTIME('%Y', data_entrada) END AS semestre, SUM(lucro_estimado) AS lucro_estimado, SUM(lucro_real) AS lucro_real FROM apostas WHERE DATE(data_entrada) >= DATE('now', '-{range_val * 6 + 1} month') GROUP BY semestre ORDER BY DATE(data_entrada) ASC"
    else:
        query = f"SELECT STRFTIME('%Y', data_entrada) || '-01' AS ano, SUM(lucro_estimado) AS lucro_estimado, SUM(lucro_real) AS lucro_real FROM apostas WHERE DATE(data_entrada) >= DATE('now', '-{range_val + 1} year') GROUP BY ano ORDER BY DATE(data_entrada) ASC"

    df_lucro_por_tempo = pd.read_sql_query(query, conn)

    # Criar uma figura e um eixo para o gráfico
    fig, ax = plt.subplots(figsize=(2.5, 1.2))
    # Defina o tamanho da fonte desejado
    plt.rcParams.update({'font.size': 4})
    ax.tick_params(axis='x', labelsize=4)  # Ajuste o tamanho dos valores do eixo x
    ax.tick_params(axis='y', labelsize=4)  # Ajuste o tamanho dos valores do eixo y

    # Plotar as linhas de lucro_estimado e lucro_real
    ax.plot(df_lucro_por_tempo[periodo], df_lucro_por_tempo['lucro_estimado'], label='Lucro Estimado')
    ax.plot(df_lucro_por_tempo[periodo], df_lucro_por_tempo['lucro_real'], label='Lucro Real')

    # Adicionar título e legendas aos eixos
    ax.set_title('Lucro por Tempo')
    ax.set_xlabel('Período')
    ax.set_ylabel('Lucro (R$)')
    #ax.set_xticklabels(ax.get_xticklabels(), fontsize=5)
    ax.yaxis.get_label().set_fontsize(5)  # Define o tamanho da fonte para 10
    ax.legend()

    # Criar uma instância de FigureCanvasTkAgg passando a figura
    canvas = FigureCanvasTkAgg(fig, master=frameStatus)

    # Limpar o frameStatus antes de adicionar o gráfico
    frameStatus.grid_forget()

    # Adicionar o gráfico ao frameStatus
    canvas.get_tk_widget().grid(row=1, column=0, columnspan=4)

    # Atualizar a interface tkinter
    frameStatus.update()


# Crie uma caixa de entrada para o range_val
range1_label = tk.Label(frameStatus, text="Range:")
range1_label.grid(row=0, column=0)
range1_entry = tk.Entry(frameStatus, width=4)
range1_entry.grid(row=0, column=1)
range1_entry.insert(0, 5)
range1_entry.bind("<FocusOut>", lambda event: lucros_por_tempo())

def atualizar_lucros_por_tempo(event):
    lucros_por_tempo()

# Crie uma caixa de seleção para o período
periodo1_var = tk.StringVar(frameStatus)
periodo1_var.set("dia")  # Valor padrão
periodo1_dropdown = tk.OptionMenu(frameStatus, periodo1_var, "dia", "semana", "mes", "trimestre", "semestre", "ano", command=atualizar_lucros_por_tempo)
periodo1_dropdown.grid(row=0, column=3)
periodo1_dropdown.configure(width=4)
lucros_por_tempo()









######## Balanços BetHouses ##########

def saldo_bethouses():
    # Obtenha os valores selecionados dos widgets de entrada
    range_val = int(range2_entry.get())
    periodo = periodo2_var.get()

    # Dataframe para armazenar os resultados
    df_saldos = pd.DataFrame()

    # Loop através das chaves do dicionário bethouse_options
    for bethouse in bethouse_options.keys():
        tabela_aposta = f"{bethouse}_saldos"
        tabela_aposta = re.sub(r'\W+', '_', tabela_aposta)

        # Consulta para obter a soma de dif_real e Valor agrupados por dia
        if periodo == 'dia':
            query = f"""
            SELECT DATE({tabela_aposta}.data_fim) AS data, '{bethouse}' AS bethouse, SUM({tabela_aposta}.dif_real) AS saldo_periodo
            FROM {tabela_aposta}
            GROUP BY DATE({tabela_aposta}.data_fim)
            """
        elif periodo == 'semana':
            query = f"""
            SELECT STRFTIME('%Y-%W', data_fim) AS periodo, '{bethouse}' AS bethouse, SUM(dif_real) AS saldo_periodo
            FROM {tabela_aposta}
            GROUP BY STRFTIME('%Y-%W', data_fim)
            """
        elif periodo == 'mes':
            query = f"""
            SELECT STRFTIME('%Y-%m', data_fim) AS periodo, '{bethouse}' AS bethouse, SUM(dif_real) AS saldo_periodo
            FROM {tabela_aposta}
            GROUP BY STRFTIME('%Y-%m', data_fim)
            """
        elif periodo == 'trimestre':
            query = f"""
            SELECT STRFTIME('%Y-%m', data_fim, 'start of quarter') AS periodo, '{bethouse}' AS bethouse, SUM(dif_real) AS saldo_periodo
            FROM {tabela_aposta}
            GROUP BY STRFTIME('%Y-%m', data_fim, 'start of quarter')
            """
        elif periodo == 'semestre':
            consulta = f"""
            SELECT CASE WHEN STRFTIME('%m', data_fim) >= '07' THEN STRFTIME('%Y', data_fim) || '-12' ELSE STRFTIME('%Y', data_fim) || '-01' END AS periodo, '{bethouse}' AS bethouse, SUM(dif_real) AS saldo_periodo
            FROM {tabela_aposta}
            GROUP BY CASE WHEN STRFTIME('%m', data_fim) >= '07' THEN STRFTIME('%Y', data_fim) || '-12' ELSE STRFTIME('%Y', data_fim) || '-01' END
            """
        else:
            query = f"""
            SELECT STRFTIME('%Y', data_fim) AS periodo, '{bethouse}' AS bethouse, SUM(dif_real) AS saldo_periodo
            FROM {tabela_aposta}
            GROUP BY STRFTIME('%Y', data_fim)
            """

        df = pd.read_sql_query(query, conn)

        # Gerar a coluna saldo_bethouse que é a soma cumulativa de saldo_periodo
        df['saldo_bethouse'] = df['saldo_periodo'].cumsum()

        # Concatenar os resultados no dataframe df_saldos_periodos
        df_saldos = pd.concat([df_saldos, df])

    # Converter coluna 'data' para datetime
    df_saldos['data'] = pd.to_datetime(df_saldos['data'], format='%Y-%m-%d')

    # Filtrar os resultados dos últimos 15 dias
    df_saldos_periodos = df_saldos[df_saldos['data'] > datetime.combine(datetime.now().date() - timedelta(days=range_val), datetime.min.time())]

    # Defina o estilo do seaborn
    sns.set(style="darkgrid")

    # Crie o gráfico de linhas com hue
    fig, ax = plt.subplots(figsize=(2.5, 1.2))

    sns.lineplot(data=df_saldos_periodos, x='data', y='saldo_bethouse', hue='bethouse', ax=ax)
    ax.set_xlabel('Data')
    ax.set_ylabel('Saldo do Bethouse')
    plt.rcParams.update({'font.size': 4})
    ax.tick_params(axis='x', labelsize=4)  # Ajuste o tamanho dos valores do eixo x
    ax.tick_params(axis='y', labelsize=4)

    # Crie uma instância de FigureCanvasTkAgg passando a figura
    canvas = FigureCanvasTkAgg(fig, master=frameStatus)

    ax.yaxis.get_label().set_fontsize(5)
    # Adicione o gráfico ao frameStatus na célula específica usando o método grid
    canvas.get_tk_widget().grid(row=6, column=0, columnspan=6)

    # Atualize a interface tkinter
    frameStatus.update()

# Crie uma caixa de entrada para o range_val
range2_label = tk.Label(frameStatus, text="Range:")
range2_label.grid(row=5, column=0)
range2_entry = tk.Entry(frameStatus, width=4)
range2_entry.grid(row=5, column=1)
range2_entry.insert(0, 5)
range2_entry.bind("<FocusOut>", lambda event: saldo_bethouses())

def atualizar_saldo_bethouses(event):
    saldo_bethouses()

# Crie uma caixa de seleção para o período
periodo2_var = tk.StringVar(frameStatus)
periodo2_var.set("dia")  # Valor padrão
periodo2_dropdown = tk.OptionMenu(frameStatus, periodo1_var, "dia", "semana", "mes", "trimestre", "semestre", "ano", command=atualizar_saldo_bethouses)
periodo2_dropdown.grid(row=5, column=3)
periodo2_dropdown.configure(width=4)
saldo_bethouses()