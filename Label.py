elif mode == 'e':
saldo_df = pd.read_csv(saldo_file)  # Ler o arquivo CSV existente como DataFrame

# Contar a quantidade de vezes que 'bethouse_key' aparece em dados
count = dados[dados['bethouse1'] == bethouse_key].shape[0]

# Apagar as linhas do DataFrame 'saldo_df' que possuem o mesmo id de dados['id']
saldo_df = saldo_df[~saldo_df['id'].isin(dados['id'])]

# Adicionar as linhas atualizadas de 'dados' ao DataFrame 'saldo_df'
for i in range(1, count + 1):
    bethouse_key = dados[f'bethouse{i}'].iloc[0]
    saldo = {
        'id': dados['id'].iloc[0],
        'data_entrada': dados['add'].iloc[0],
        'data_fim': dados['datetime'].iloc[0],
        'bethouse': bethouse_key,
        'odd': dados[f'odd{i}'].iloc[0],
        'odd_real': (dados[f'odd{i}'].iloc[0] - 1) * (1 - options[bethouse_key]['taxa']) + 1 if
        dados[f'mercado{i}'].iloc[0] != 'Lay' else (dados[f'odd{i}'].iloc[0] / (
                dados[f'odd{i}'].iloc[0] - 1) - 1) * (1 - options[bethouse_key]['taxa']) + 1,
        'aposta': dados[f'aposta{i}'].iloc[0],
        'resultado': '',
        'balanco': -dados[f'aposta{i}'].iloc[0],
        'dif_real': 0
    }
    saldo_df = saldo_df.append(saldo, ignore_index=True)

saldo_df.sort_values(by='id', inplace=True)  # Organizar o DataFrame em ordem de 'id'
saldo_df.to_csv(saldo_file, mode='w', header=True, index=False)  # Reescrever o arquivo CSV






####### GRÁFICO DE HORA ########

# Defina as colunas_agg, colun_data e metodos
colunas_agg_hora = 'lucro_estimado'
colun_data_hora = 'data_entrada'

# Função para atualizar o gráfico interativamente
def atualizar_grafico_hora():
    # Obtenha os valores selecionados dos widgets de entrada
    range_val = int(range_entry.get())
    periodo_tempo = periodo_var.get()
    metodo = metodo_var.get()

    # Define os métodos de acordo com a opção selecionada
    if metodo == 'total':
        metodos = 'sum'
    elif metodo == 'média':
        metodos = 'mean'

    # Chame a função agregação de datas para obter os dados agregados
    apostas_hora = agregar_datas(df_tabela, colun_data_hora, periodo_tempo, colunas_agg_hora, metodos=metodos, range_val=range_val, cont_hora=True)

    # Crie um gráfico de barras usando o Matplotlib
    fig = plt.Figure(figsize=(7, 2.7))
    ax = fig.add_subplot(1, 1, 1)
    apostas_hora = apostas_hora.reset_index()
    sns.barplot(data=apostas_hora, x='hora', y='count', palette='viridis', ax=ax, label='Apostas por Hora')

    # Adicione o gráfico ao frameStatus
    canvas = FigureCanvasTkAgg(fig, master=frameStatus)
    canvas.get_tk_widget().grid(row=1, column=4, columnspan=5)

# Crie uma caixa de entrada para o range_val
range_label = tk.Label(frameStatus, text="Range:")
range_label.grid(row=0, column=4)
range_entry = tk.Entry(frameStatus, width=4)
range_entry.grid(row=0, column=5)
range_entry.insert(0, 5)
range_entry.bind("<FocusOut>", lambda event: atualizar_grafico_hora())

# Crie uma caixa de seleção para o período
periodo_var = tk.StringVar(frameStatus)
periodo_var.set("dia")  # Valor padrão
def atualizar_grafico_periodo_hora(*args):
    atualizar_grafico_hora()

periodo_var.trace("w", atualizar_grafico_periodo_hora)
periodo_dropdown = tk.OptionMenu(frameStatus, periodo_var, "dia", "semana", "mes", "trimestre", "semestre", "ano")
periodo_dropdown.grid(row=0, column=6)
periodo_dropdown.configure(width=7)

# Crie uma caixa de seleção para o método
metodo_var = tk.StringVar(frameStatus)
metodo_var.set("total")  # Valor padrão
def atualizar_grafico_metodo_hora(*args):
    atualizar_grafico_hora()

metodo_var.trace("w", atualizar_grafico_metodo_hora)
metodo_dropdown = tk.OptionMenu(frameStatus, metodo_var, "total", "média")
metodo_dropdown.grid(row=0, column=8)
metodo_dropdown.configure(width=6)
atualizar_grafico_hora()