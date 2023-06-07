import pandas as pd

def convert_to_numeric(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        try:
            return float(value)
        except (TypeError, ValueError):
            return value

def convert_mes(valor, extenso=False):
    mes_id_map = {
        'Jan': ('Janeiro', 1),
        'Fev': ('Fevereiro', 2),
        'Mar': ('Março', 3),
        'Abr': ('Abril', 4),
        'Mai': ('Maio', 5),
        'Jun': ('Junho', 6),
        'Jul': ('Julho', 7),
        'Ago': ('Agosto', 8),
        'Set': ('Setembro', 9),
        'Out': ('Outubro', 10),
        'Nov': ('Novembro', 11),
        'Dez': ('Dezembro', 12)
    }

    if isinstance(valor, str):
        valor = valor.capitalize()
        if extenso:
            return mes_id_map.get(valor)[0]
        else:
            return mes_id_map.get(valor)[1]
    elif isinstance(valor, int):
        if extenso:
            return mes_id_map.get(list(mes_id_map.keys())[valor - 1])[0]
        else:
            return list(mes_id_map.keys())[valor - 1]
    return None

def convert_ms_to_datetime(file, column):
    dataframe = pd.read_csv(file, parse_dates=[column])
    dataframe[column] = dataframe[column].apply(
        lambda x: pd.to_datetime(int(x)/10**9, unit='s') if str(x).startswith("16") else x)
    dataframe.to_csv("Apostas.csv", index=False)
    return dataframe


def converter_esporte(sport):
    sport = sport.lower().strip().split('\n')[0]
    if sport in {'soccer', 'football', 'футбол'}:
        return 'Futebol'
    elif sport in {'basketball', 'basket', 'баскетбол'}:
        return 'Basquetebol'
    elif sport == 'volleyball':
        return 'Voleibol'
    elif sport == 'бейсбол':
        return 'Baseball'
    elif sport in {'handball', 'гандбол'}:
        return 'Handebol'
    elif sport in {'dota2', 'esports', 'esport', 'e-sports', 'cybersports'}:
        return 'E-Sports'
    elif sport in {'ice hockey', 'хоккей'}:
        return 'Hockey'
    elif sport in {'tennis', 'теннис'}:
        return 'Tênis'
    elif sport in {'darts', 'dart', 'дартс'}:
        return 'Dardos'
    elif sport in {'table tennis', 'tabletennis'}:
        return 'Tênis de Mesa'
    elif sport == 'boxing':
        return 'Boxe'
    elif sport == 'футзал':
        return 'Futsal'
    else:
        return sport.capitalize()
