import numpy as np

odd1 = 1.492
odd2 = 2.12
odd3 = 5.6
aposta1 = 0
aposta2 = 0
aposta3 = 4.89
mercado1 = "AH1"
mercado2 = "AH2"
mercado3 = "2"
valor1 = 0
valor2 = -0.5
valor3 = ""
def calc_apostas(aposta1, aposta2, aposta3, odd1, odd2, odd3, mercado1, mercado2, mercado3, valor1, valor2, valor3, bethouse_options1, bethouse_options2, bethouse_options3, arred_var):
    odd_1 = ((odd1 - 1) * (1 - bethouse_options1) +1)
    odd_2 = ((odd2 - 1) * (1 - bethouse_options2) +1)
    odd_3 = ((odd3 - 1) * (1 - bethouse_options3) +1)
    if aposta1 > 0.0:
        aposta2 = odd_1 * aposta1 / odd_2
        aposta3 = odd_1 * aposta1 / odd_3
    elif aposta2 > 0.0:
        aposta1 = odd_2 * aposta2 / odd_1
        aposta3 = odd_2 * aposta2 / odd_3
    elif aposta3 > 0.0:
        aposta1 = odd_3 * aposta3 / odd_1
        aposta2 = odd_3 * aposta3 / odd_2
    retorno1 = odd_1 * aposta1
    retorno2 = odd_2 * aposta2
    retorno3 = odd_3 * aposta3
    retornos = [retorno1, retorno2, retorno3]
    max_retorno = max(retornos)
    seg_retorno = max([r for r in retornos if r != max_retorno])
    min_retorno = min(retornos)
    if max_retorno == retorno1:
        max_odd = odd_1
        max_aposta = max_retorno / odd_1
    elif max_retorno == retorno2:
        max_odd = odd_2
        max_aposta = max_retorno / odd_2
    else:
        max_odd = odd_3
        max_aposta = max_retorno / odd_3
    if min_retorno == retorno1:
        min_odd = odd_1
        min_aposta = max_retorno / odd_1
    elif min_retorno == retorno2:
        min_odd = odd_2
        min_aposta = max_retorno / odd_2
    else:
        min_odd = odd_3
        min_aposta = max_retorno / odd_3
    if seg_retorno == retorno1:
        seg_odd = odd_1
        seg_aposta = max_retorno / odd_1
    elif seg_retorno == retorno2:
        seg_odd = odd_2
        seg_aposta = max_retorno / odd_2
    else:
        seg_odd = odd_3
        seg_aposta = max_retorno / odd_3
    mean_return = np.mean([retorno1, retorno2, retorno3])
    if abs(retorno1 - mean_return) <= 0.01 * mean_return and abs(retorno2 - mean_return) <= 0.05 * mean_return and abs(retorno3 - mean_return) <= 0.05 * mean_return:
        tipo = "padrão"
    return max_retorno, seg_retorno, min_retorno, mean_return

print(calc_apostas(aposta1, aposta2, aposta3, odd1, odd2, odd3, mercado1, mercado2, mercado3, valor1, valor2, valor3, 0.0, 0.0, 0.0, 0.01))