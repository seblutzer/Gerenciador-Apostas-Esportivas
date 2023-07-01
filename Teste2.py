def calcular_apostas(odd_1, odd_2, odd_3, aposta_conhecida, tipo_aposta_conhecida):
    if tipo_aposta_conhecida == 1:
        aposta1 = aposta_conhecida
        aposta3 = (aposta1 * odd_1) / (odd_3 + odd_2)
        aposta2 = (aposta1 * odd_1 - aposta3 * odd_3) / odd_2
    elif tipo_aposta_conhecida == 2:
        aposta2 = aposta_conhecida
        aposta1 = (aposta2 * odd_2 + aposta3 * odd_3) / odd_1
        aposta3 = (aposta1 * odd_1 - aposta2 * odd_2) / odd_3
    elif tipo_aposta_conhecida == 3:
        aposta3 = aposta_conhecida
        aposta1 = (aposta2 * odd_2 + aposta3 * odd_3) / odd_1
        aposta2 = (aposta1 * odd_1 - aposta3 * odd_3) / odd_2
    return (aposta1, aposta2, aposta3)

resultados = calcular_apostas(3, 2, 1.5, 13, 1)
print(resultados)