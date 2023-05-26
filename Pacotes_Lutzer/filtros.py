import pandas as pd
import numpy as np

def agregar_datas(df, colun_data, periodo_tempo, colunas_agg, metodos='sum', range_val=None, groupby_cols=None, fusion=False, cont_hora=False):
    # Converter a coluna colun_data para o tipo datetime
    dataframe = df.copy()

    dataframe[colun_data] = pd.to_datetime(dataframe[colun_data])
    dataframe['dia'] = dataframe[colun_data].dt.floor('D')

    if cont_hora:
        # Create a new column for each hour
        dataframe['hora'] = dataframe[colun_data].dt.hour
        if periodo_tempo == 'hora':
            dataframe = dataframe.set_index('hora')
            dataframe = dataframe.tail(range_val) if range_val is not None else dataframe
            resultado = dataframe.groupby('hora').size()
            resultado = resultado.reindex(range(24), fill_value=0)  # Fill hours without data with 0
            resultado = resultado.to_frame()
            resultado.columns = ['count']
        else:
            if periodo_tempo == 'dia':
                start_date = dataframe[periodo_tempo].max() - pd.DateOffset(days=range_val)
            elif periodo_tempo == 'semana':
                start_date = dataframe['dia'].max() - pd.DateOffset(days=range_val * 7) + pd.DateOffset(weekday=6)
            elif periodo_tempo == 'mes':
                start_date = dataframe['dia'].max() - pd.DateOffset(days=(range_val - 1) * 30) + pd.DateOffset(day=1)
            elif periodo_tempo == 'trimestre':
                start_date = dataframe['dia'].max() - pd.DateOffset(days=(range_val - 1) * 90)
                start_date = start_date.replace(month=((start_date.replace(day=1)).month - 1) // 3 * 3 + 1, day=1)
            elif periodo_tempo == 'semestre':
                start_date = dataframe['dia'].max() - pd.DateOffset(days=(range_val - 1) * 180)
                start_date = start_date.replace(month=((start_date.replace(day=1)).month - 1) // 6 * 6 + 1, day=1)
            elif periodo_tempo == 'ano':
                start_date = dataframe['dia'].max() - pd.DateOffset(days=(range_val - 1) * 360) + pd.DateOffset(month=1, day=1)

            mask = (dataframe['dia'] > start_date)
            dataframe = dataframe.loc[mask]
            # Group by hour and calculate sum over all days within specified time period
            if metodos == 'mean':
                # Group by hour and calculate the mean over all days within specified time period
                total_dias = dataframe[dataframe['dia'] >= start_date]['dia'].nunique()
                print(total_dias)
                resultado = dataframe.groupby('hora').size()
                resultado = resultado.reindex(range(24), fill_value=0)  # Fill hours without data with 0
                resultado = resultado / total_dias
                resultado = resultado.to_frame()
                resultado.columns = ['count']
            else:
                # Group by hour and calculate the sum over all days within specified time period
                resultado = dataframe.groupby('hora').size()
                resultado = resultado.reindex(range(24), fill_value=0)  # Fill hours without data with 0
                resultado = resultado.to_frame()
                resultado.columns = ['count']

    else:

        # Criar uma nova coluna para cada timeframe
        dataframe['hora'] = dataframe[colun_data].dt.floor('H')
        if periodo_tempo == 'semana':
            dataframe[periodo_tempo] = dataframe[colun_data].dt.to_period('W')
        elif periodo_tempo == 'mes':
            dataframe[periodo_tempo] = dataframe[colun_data].dt.to_period('M')
        elif periodo_tempo == 'trimestre':
            dataframe[periodo_tempo] = dataframe[colun_data].dt.to_period('Q')
        elif periodo_tempo == 'semestre':
            dataframe[periodo_tempo] = dataframe[colun_data].dt.to_period('2Q')
        elif periodo_tempo == 'ano':
            dataframe[periodo_tempo] = dataframe[colun_data].dt.to_period('Y')

        # Converter as colunas para numérico
        if isinstance(colunas_agg, str):
            pd.to_numeric(dataframe[colunas_agg])
        else:
            for coluna in colunas_agg:
                dataframe[coluna] = pd.to_numeric(dataframe[coluna])

        # Criar um DataFrame groupby e aplicar os métodos de agregação para cada coluna
        resultado = pd.DataFrame()
        if fusion:
            combined_values = list(pd.concat([dataframe[col] for col in dataframe[groupby_cols]], ignore_index=True).dropna().unique())
            for value in combined_values:
                new_column = value  # Nome da nova coluna
                dataframe[new_column] = dataframe[groupby_cols].eq(value).sum(axis=1)
            colunas_agg = colunas_agg + combined_values
            for i, coluna in enumerate(colunas_agg):
                if i < len(metodos):
                    metodo = metodos[i]
                else:
                    metodo = "sum"
                grupo_coluna = dataframe.groupby(periodo_tempo).agg({coluna: metodo})
                resultado = pd.concat([resultado, grupo_coluna], axis=1)
        else:
            if groupby_cols is None:
                groupby_cols = [periodo_tempo]
            else:
                groupby_cols.insert(0, periodo_tempo)
            if isinstance(colunas_agg, str):
                grupo_coluna = dataframe.groupby(groupby_cols).agg({colunas_agg: metodos})
                resultado = pd.concat([resultado, grupo_coluna], axis=1)
            else:
                for i, coluna in enumerate(colunas_agg):
                    metodo = metodos[i]
                    grupo_coluna = dataframe.groupby(groupby_cols).agg({coluna: metodo})
                    resultado = pd.concat([resultado, grupo_coluna], axis=1)

        # Verificar se o parâmetro de range foi fornecido
        if range_val is not None:
            # Limitar o dataframe ao número de linhas especificado pelo range
            resultado = resultado.loc[resultado.index.get_level_values(0).unique()[-range_val:]]

        # Alterar o nome do índice de cada linha
        if periodo_tempo == 'dia':
            resultado.index = resultado.index.strftime('%d %b')
        elif periodo_tempo == 'semana':
            start_date = resultado.index.to_timestamp().strftime('%d')
            end_date = resultado.index.strftime('%d %b')
            resultado.index = start_date + '-' + end_date
        elif periodo_tempo == 'mes':
            resultado.index = resultado.index.strftime('%b %Y')
        elif periodo_tempo == 'trimestre':
            start_date = resultado.index.to_timestamp().strftime('%b')
            end_date = resultado.index.strftime('%b %Y')
            resultado.index = start_date + '-' + end_date
        elif periodo_tempo == 'semestre':
            start_date = (resultado.index.to_timestamp() - pd.DateOffset(months=3)).strftime('%b')
            end_date = resultado.index.strftime('%b %Y')
            resultado.index = start_date + '-' + end_date
        elif periodo_tempo == 'ano':
            resultado.index = resultado.index.strftime('%Y')

    return resultado