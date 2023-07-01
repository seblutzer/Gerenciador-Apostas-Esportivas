from collections import OrderedDict
import math
from itertools import permutations
import numpy as np


def resultado_handicap(handicap: float, diferenca_pontos: int, over=True, draw=False, um_ou_outro=False) -> str:
    if um_ou_outro:
        if diferenca_pontos == 0:
            return 'loss'
        return 'win'
    if draw:
        if diferenca_pontos == -handicap:
            return 'win'
        return 'loss'
    if isinstance(handicap, int):
        if diferenca_pontos == -handicap:
            return 'return'
        elif diferenca_pontos > -handicap:
            if over:
                return 'win'
            return 'loss'
        elif diferenca_pontos < -handicap:
            if over:
                return 'loss'
            return 'win'
    else:
        if diferenca_pontos - 0.25 == -handicap:
            if over:
                return 'half-win'
            return 'half-loss'
        elif diferenca_pontos + 0.25 == -handicap:
            if over:
                return 'half-loss'
            return 'half-win'
        elif diferenca_pontos > -handicap:
            if over:
                return 'win'
            return 'loss'
        else:
            if over:
                return 'loss'
            return 'win'

def all_handicaps(mercado1, valor1, mercado2, valor2, mercado3, valor3):
    valores = [valor1, valor2, valor3]
    mercados = [mercado1, mercado2, mercado3]
    for i, mercado in enumerate(mercados):
        if mercado == '1' or mercado == '2':
            mercados[i] = f'AH{mercado}'
            valores[i] = -0.5
        elif mercado.startswith('DNB'):
            time = mercado[-1]
            mercados[i] = f'AH{time}'
            valores[i] = 0
        elif mercado == '1X':
            mercados[i] = 'AH1'
            valores[i] = 0.5
        elif mercado == 'X2':
            mercados[i] = 'AH2'
            valores[i] = 0.5
        elif mercado == 'X':
            mercados[i] = 'EHX2'
            valores[i] = 0
        elif mercado == '12':
            valores[i] = 0

    conjunto = set()
    for valor in valores:
        valor = abs(valor)
        if valor % 1 == 0.5:
            numero_anterior = math.floor(valor)
            numero_posterior = math.ceil(valor)

            conjunto.add(numero_anterior)
            conjunto.add(numero_posterior)
        else:
            numero_anterior = int(valor) - 1
            numero_atual = int(valor)
            numero_posterior = int(valor) + 1

            conjunto.add(numero_anterior)
            conjunto.add(numero_atual)
            conjunto.add(numero_posterior)
    total_max = round(max(conjunto)) + 1
    total_min = round(min(conjunto))
    resultados_possiveis = []
    indice_maior_valor = valores.index(max(valores))
    mercado_maior_valor = mercados[indice_maior_valor]
    time = mercado_maior_valor[-1]
    if time == '1':
        maximo = -total_max
        minimo = -total_min
        total_min = min(maximo, minimo) + 1
        total_max = max(maximo, minimo) + 1

    for ponto in range(total_min, total_max):
        resultados = []
        for i in range(len(valores)):
            mercado = mercados[i]
            valor = valores[i]
            draw = False
            um_ou_outro = False
            if mercado.startswith('EHX'):
                draw = True
            elif mercado.startswith('EH'):
                valor -= 0.5
            elif mercado == '12':
                um_ou_outro = True
            diferenca_pontos = ponto
            if mercado.endswith('2'):
                diferenca_pontos = -ponto
            resultado = resultado_handicap(valor, diferenca_pontos, draw=draw, um_ou_outro=um_ou_outro)
            resultados.append(resultado)
        if resultados not in resultados_possiveis:
            resultados_possiveis.insert(0, resultados)

    return resultados_possiveis

def resultado_total_asiatico(total: float, dif_pontos: int, over=True, draw=False) -> str:
    dif_pontos = abs(dif_pontos)
    if draw:
        if dif_pontos == total:
            return 'win'
        return 'loss'
    if isinstance(total, int):
        if dif_pontos == total:
            return 'return'
        elif dif_pontos > total:
            if over:
                return 'win'
            return 'loss'
        elif dif_pontos < total:
            if over:
                return 'loss'
            return 'win'
    else:
        if dif_pontos + 0.25 == total:
            if over:
                return 'half-loss'
            return 'half-win'
        elif dif_pontos - 0.25 == total:
            if over:
                return 'half-win'
            return 'half-loss'
        elif dif_pontos > total:
            if over:
                return 'win'
            return 'loss'
        else:
            if over:
                return 'loss'
            return 'win'
def all_totals(mercado1, valor1, mercado2, valor2, mercado3, valor3):
    valores = [valor1, valor2, valor3]
    mercados = [mercado1, mercado2, mercado3]
    resultados_possiveis = []
    total_max = round(max(valores)) + 2
    total_min = round(min(valores)) - 1

    for dif_pontos in range(total_min, total_max):
        resultados = []
        for i in range(len(valores)):
            valor = valores[i]
            mercado = mercados[i]
            draw = False
            time = valor[2] if mercado.startswith(('TO1', 'TU1', 'TO2', 'TU2')) else ''
            if mercado.startswith('Exac'):
                draw = True
            if mercado.startswith('TO') and mercado.endswith('(3-way)'):
                valor += 0.5
            elif mercado.startswith('TU') and mercado.endswith('(3-way)'):
                valor -= 0.5
            over = mercado.startswith('TO')
            resultado = resultado_total_asiatico(valor, dif_pontos, over, draw)
            resultados.append(resultado)
        if not resultados in resultados_possiveis:
            resultados_possiveis.append(resultados)

    return resultados_possiveis

def especiais(mercado1, mercado2, mercado3):
    mercados = [mercado1, mercado2, mercado3]
    if any(x.startswith('WinN') for x in mercados) and any(x.startswith('TU') for x in mercados) and any(x.startswith('Score') for x in mercados):
        return [['win', 'loss', 'loss'], ['loss', 'win', 'loss'], ['loss', 'loss', 'win']]
    elif any(x == 'Lay' for x in mercados):
        count_lay = sum(1 for x in mercados if x == 'Lay')
        if count_lay == 1:
            if mercado1 == 'Lay':
                return [['loss', 'win', 'win'], ['win', 'loss', 'loss']]
            elif mercado2 == 'Lay':
                return [['win', 'loss', 'win'], ['loss', 'win', 'loss']]
            else:
                return [['win', 'win', 'loss'], ['loss', 'loss', 'win']]
        elif count_lay == 2:
            if mercado1 == mercado2:
                return [['win', 'win', 'loss'], ['loss', 'loss', 'win']]
            elif mercado1 == mercado3:
                return [['win', 'loss', 'win'], ['loss', 'win', 'loss']]
            else:
                return [['loss', 'win', 'win'], ['win', 'loss', 'loss']]
        return False
    else:
        return False

def calc_resultados(mercados, valores):
    if all(x in ['1', '2', '1X', 'X', 'X2', '12', 'DNB1', 'DNB2', 'AH1', 'AH2', 'EH1', 'EH2', 'EHX2'] for x in mercados):
        resultados_possiveis = all_handicaps(mercados[0], valores[0], mercados[1], valores[1], mercados[2], valores[2])
    elif all(x.startswith(('T', 'Exac')) for x in mercados):
        resultados_possiveis = all_totals(mercados[0], valores[0], mercados[1], valores[1], mercados[2], valores[2])
    else:
        resultados_possiveis = especiais(mercados[0], mercados[1],mercados[2])
    if resultados_possiveis:
        sure_bets = verificar_surebets(resultados_possiveis)
        resultados = resultados_possiveis
        sub_result = []

        # Determinar o número de sublistas e o tamanho de cada sublista
        num_sublistas = len(resultados[0])
        tamanho_sublista = len(resultados)

        # Criar as sublistas em sub_padrao
        for i in range(num_sublistas):
            sublista = []
            for j in range(tamanho_sublista):
                sublista.append(resultados[j][i])
            sub_result.append(sublista)

        padroes = {'1-X-2': [['win', 'loss', 'loss'], ['loss', 'win', 'loss'], ['loss', 'loss', 'win']],
           '0-X-2': [['win', 'loss', 'loss'], ['return', 'win', 'loss'], ['loss', 'loss', 'win']],
                '1-X-0': [['win', 'loss', 'loss'], ['loss', 'win', 'return'], ['loss', 'loss', 'win']],
           '0-X2-2': [['win', 'loss', 'loss'], ['return', 'win', 'loss'], ['loss', 'win', 'win']],
                '1-1X-0': [['win', 'win', 'loss'], ['loss', 'win', 'return'], ['loss', 'loss', 'win']],
           '0.25-X2-2': [['win', 'loss', 'loss'], ['half-win', 'win', 'loss'], ['loss', 'win', 'win']],
                '1-1X-0.25': [['win', 'win', 'loss'], ['loss', 'win', 'half-win'], ['loss', 'loss', 'win']],
           '-0.25-X2-2': [['win', 'loss', 'loss'], ['half-loss', 'win', 'loss'], ['loss', 'win', 'win']],
                '1-1X--0.25': [['win', 'win', 'loss'], ['loss', 'win', 'half-loss'], ['loss', 'loss', 'win']],
           '-0.25-X2-0': [['win', 'loss', 'loss'], ['half-loss', 'win', 'return'], ['loss', 'win', 'win']],
                '0-1X--0.25': [['win', 'win', 'loss'], ['return', 'win', 'half-loss'], ['loss', 'loss', 'win']],
           '-0.25-X-0': [['win', 'loss', 'loss'], ['half-loss', 'win', 'return'], ['loss', 'loss', 'win']],
                '0-X--0.25': [['win', 'loss', 'loss'], ['return', 'win', 'half-loss'], ['loss', 'loss', 'win']],
           '0.25-X-2': [['win', 'loss', 'loss'], ['half-win', 'win', 'loss'], ['loss', 'loss', 'win']],
                '1-X-0.25': [['win', 'loss', 'loss'], ['loss', 'win', 'half-win'], ['loss', 'loss', 'win']],
           '-0.25-X-2': [['win', 'loss', 'loss'], ['half-loss', 'win', 'loss'], ['loss', 'loss', 'win']],
                '1-X--0.25': [['win', 'loss', 'loss'], ['loss', 'win', 'half-loss'], ['loss', 'loss', 'win']],
           '-0.25-X--0.25': [['win', 'loss', 'loss'], ['half-loss', 'win', 'half-loss'], ['loss', 'loss', 'win']],
           '-0.25-1X--0.25': [['win', 'win', 'loss'], ['half-loss', 'win', 'half-loss'], ['loss', 'loss', 'win']],
                '-0.25-X2--0.25': [['win', 'loss', 'loss'], ['half-loss', 'win', 'half-loss'], ['loss', 'win', 'win']],
           '0-X2--0.25': [['win', 'loss', 'loss'], ['return', 'win', 'half-loss'], ['loss', 'win', 'win']],
                '-0.25-1X-0': [['win', 'win', 'loss'], ['half-loss', 'win', 'return'], ['loss', 'loss', 'win']],
           '0.25-12-X2': [['win', 'win', 'loss'], ['half-win', 'loss', 'win'], ['loss', 'win', 'win']],
                '1X-12-0.25': [['win', 'win', 'loss'], ['win', 'loss', 'half-win'], ['loss', 'win', 'win']],
           '0.25-12-0.25': [['win', 'win', 'loss'], ['half-win', 'loss', 'half-win'], ['loss', 'win', 'win']],
           '0-12-X2': [['win', 'win', 'loss'], ['return', 'loss', 'win'], ['loss', 'win', 'win']],
                '1X-12-0': [['win', 'win', 'loss'], ['win', 'loss', 'return'], ['loss', 'win', 'win']],
           'U1.25-O0.75-O1.5': [['win', 'loss', 'loss'], ['half-win', 'half-win', 'loss'], ['loss', 'win', 'win']],
           '112': [['win', 'win', 'loss'], ['loss', 'loss', 'win']],
                '112X': [['win', 'win', 'loss'], ['return', 'return', 'return'], ['loss', 'loss', 'win']],
                '112W': [['win', 'win', 'loss'], ['half-win', 'half-win', 'half-loss'], ['loss', 'loss', 'win']],
                '112L': [['win', 'win', 'loss'], ['half-loss', 'half-loss', 'half-win'], ['loss', 'loss', 'win']]

           }
        padrao, ordem = identifica_e_ordena_padrao(padroes, sub_result)
    else:
        padrao = False
        ordem = False
        sure_bets = False
    return padrao, ordem, sure_bets

def verificar_surebets(resultados_possiveis):
    sure_bets = []
    for lista in resultados_possiveis:
        if 'win' in lista or ('half-win' in lista and ('return' in lista or 'half-loss' in lista or lista.count('half-win') > 1)):
            sure_bets.append(True)
        else:
            sure_bets.append(False)
    if all(sure_bets):
        return True
    else:
        return False

def verifica_padrao(padrao, resultados):
    padrao_set = {tuple(lista) for lista in padrao}
    resultados_set = {tuple(lista) for lista in resultados}

    return padrao_set == resultados_set

def obter_ordem(sub_padrao, sub_result):
    ordem = []
    for lista_result in sub_result:
        for i, lista_padrao in enumerate(sub_padrao):
            if lista_result == lista_padrao:
                ordem.append(i+1)
                break
    if len(set(ordem)) != len(ordem):
        if ordem[0] == ordem[1]:
            ordem[0] = 1
            ordem[1] = 2
            ordem[2] = 3
        elif ordem[0] == ordem[2]:
            ordem[0] = 1
            ordem[1] = 3
            ordem[2] = 2
        elif ordem[1] == ordem[2]:
            ordem[0] = 3
            ordem[1] = 1
            ordem[2] = 2
    return ordem




def obter_ordem2(sub_padrao, sub_result):
    ordem = []
    for lista_result in sub_result:
        for i, lista_padrao in enumerate(sub_padrao):
            if lista_result == lista_padrao:
                ordem.append(i+1)
                break
    return ordem

def identifica_e_ordena_padrao(padroes, sub_result):
    for nome, padrao in padroes.items():
        sub_padrao = []

        # Determinar o número de sublistas e o tamanho de cada sublista
        num_sublistas = len(padrao[0])
        tamanho_sublista = len(padrao)
        # Criar as sublistas em sub_padrao
        for i in range(num_sublistas):
            sublista = []
            for j in range(tamanho_sublista):
                sublista.append(padrao[j][i])
            sub_padrao.append(sublista)

        if verifica_padrao(sub_padrao, sub_result):
            ordem_resultados = obter_ordem(sub_padrao, sub_result)
            return nome, ordem_resultados
    return 'Nenhum', 'Nenhuma'

def verifica_mesmos_valores(padroes):
    chaves = list(padroes.keys())
    for i in range(len(chaves)):
        for j in range(i + 1, len(chaves)):
            chave1 = chaves[i]
            chave2 = chaves[j]
            valores1 = padroes[chave1]
            valores2 = padroes[chave2]
            if valores1 == valores2:
                return chave1, chave2

    return None
#mercados = ['WinNil1', 'TU1', 'ScoreBoth']
#valores = ['', 0.5, '']
#padrao, ordem, surebets = calc_resultados(mercados, valores)
#print(padrao, ordem, surebets)
#mercados = ['AH2', 'AH2', 'AH1']
#valores = [2.5, 2.5, -2.5]
#padrao, ordem, surebets = calc_resultados(mercados, valores)
#print(padrao, ordem, surebets)
