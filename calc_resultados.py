def resultado_handicap(handicap: float, diferenca_pontos: int, over=True, draw=False) -> str:
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
teste = -0
AH1 = 0
EHX2 = 0
EH2 = 0
result1 = resultado_handicap(AH1, teste)
result2 = resultado_handicap(EHX2, -teste, draw=True)
result3 = resultado_handicap(EH2-0.5, -teste)
#print(result1)
#print(result2)
#print(result3)
def all_handicaps(mercado1, valor1, mercado2, valor2, mercado3, valor3):
    valores = [valor1, valor2, valor3]
    mercados = [mercado1, mercado2, mercado3]
    valores_abs = [abs(valor) for valor in valores]
    resultados_possiveis = set()
    total_max = round(max(valores_abs)) + 2
    total_min = round(min(valores_abs)) - 1
    indice_maior_valor = valores.index(max(valores))
    mercado_maior_valor = mercados[indice_maior_valor]
    ultimo_caractere = mercado_maior_valor[-1]
    if ultimo_caractere == '1':
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
            if mercado.startswith('EHX'):
                draw = True
            elif mercado.startswith('EH'):
                valor -= 0.5
            diferenca_pontos = ponto
            if mercado.endswith('2'):
                diferenca_pontos = -ponto
            print(valor, diferenca_pontos, draw)
            resultado = resultado_handicap(valor, diferenca_pontos, draw=draw)
            resultados.append(resultado)
        resultados_possiveis.add(' '.join(resultados))

    return resultados_possiveis
resultados_possiveis = all_handicaps('AH1', -0.5, 'EHX1', 0, 'AH2', -0.5)
print(resultados_possiveis)

def resultado_total_asiatico(total: float, diferenca_pontos: int, over=True) -> str:
    diferenca_pontos = abs(diferenca_pontos)
    if isinstance(total, int):
        if diferenca_pontos == total:
            return 'return'
        elif diferenca_pontos > total:
            if over:
                return 'win'
            return 'loss'
        elif diferenca_pontos < total:
            if over:
                return 'loss'
            return 'win'
    else:
        if diferenca_pontos + 0.25 == total:
            if over:
                return 'half-win'
            return 'half-loss'
        elif diferenca_pontos - 0.25 == total:
            if over:
                return 'half-loss'
            return 'half-win'
        elif diferenca_pontos > total:
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
    resultados_possiveis = set()
    total_max = round(max(valores)) + 2
    total_min = round(min(valores)) - 1

    for diferenca_pontos in range(total_min, total_max):
        resultados = []
        for i in range(len(valores)):
            valor = valores[i]
            mercado = mercados[i]
            if mercado.startswith('TO') and mercado.endswith('(3-way)'):
                valor += 0.5
            elif mercado.startswith('TU') and mercado.endswith('(3-way)'):
                valor -= 0.5
            over = mercado.startswith('TO')
            resultado = resultado_total_asiatico(valor, diferenca_pontos, over)
            resultados.append(resultado)
        resultados_possiveis.add(' '.join(resultados))
    return resultados_possiveis

valores = [5, 4.5, 5.5]
mercados = ['TO1', 'TU1', 'TU1']
resultados_possiveis = all_totals(mercados[0], valores[0], mercados[1], valores[1],mercados[2], valores[2])

#print(resultados_possiveis)
mercado1 = '1'
mercados = []
if mercado1.isnumeric():
    mercados[0] = f'AH{mercado1}'
print(mercados)