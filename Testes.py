from Pacotes_Lutzer.calc_resultados import calc_resultados
from Pacotes_Lutzer.validate import check_margin

def calc_apostas(aposta1, aposta2, aposta3, odd1, odd2, odd3, mercado1, mercado2, mercado3, valor1, valor2, valor3, bethouse_options1, bethouse_options2, bethouse_options3, arred_var, bonus):
    if aposta1 == '':
        aposta1 = 0
    if aposta2 == '':
        aposta2 = 0
    if aposta3 == '':
        aposta3 = 0
    if aposta1 + aposta2 + aposta3 == 0.0 or (odd2 == 0.0 and odd3 == 0.0):
        return

    def calcular_odd(mercado, odd, bethouse_options):
        if mercado == 'Lay':
            return (odd / (odd - 1) - 1) * (1 - bethouse_options) + 1
        else:
            return (odd - 1) * (1 - bethouse_options) + 1

    odd_1 = calcular_odd(mercado1, odd1, bethouse_options1)
    odd_2 = calcular_odd(mercado2, odd2, bethouse_options2)
    odd_3 = calcular_odd(mercado3, odd3, bethouse_options3)

    def calc_liability(mercado, odd, aposta):
        if mercado == 'Lay':
            liability = round((aposta * (odd / (odd - 1)) - aposta), 2)
            return liability
        return None

    def retorno1():
        return odd_1 * aposta1
    def retorno2():
        return odd_2 * aposta2
    def retorno3():
        return odd_3 * aposta3
    def retorno1_halfwin():
        return aposta1 / 2 + (aposta1 / 2) * odd_1
    def retorno2_halfwin():
        return aposta2 / 2 + (aposta2 / 2) * odd_2
    def retorno3_halfwin():
        return aposta3 / 2 + (aposta3 / 2) * odd_3
    def retorno1_halfloss():
        return aposta1 / 2
    def retorno2_halfloss():
        return aposta2 / 2
    def retorno3_halfloss():
        return aposta3 / 2
    retornos = [retorno1(), retorno2(), retorno3()]

    if odd3 > 0.0:
        mercados = [mercado1, mercado2, mercado3]
        valores = [valor1, valor2, valor3]
        odds = [odd_1, odd_2, odd_3]
        apostas = [aposta1, aposta2, aposta3]
        padrao, ordem, surebet = calc_resultados(mercados, valores)
        if not padrao:
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                aposta3 = round((((retorno1() + retorno2()) / 2) / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta1 > 0 and aposta3 > 0:
                aposta2 = round((((retorno1() + retorno3()) / 2) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0 and aposta3 > 0:
                aposta1 = round((((retorno2() + retorno3()) / 2) / odd_1) / arred_var[0]) * arred_var[0]
            elif aposta1 > 0.0:
                aposta2 = round((retorno1() / odd_2) / arred_var[1]) * arred_var[1]
                aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta2 > 0.0:
                aposta1 = round((retorno2() / odd_1) / arred_var[0]) * arred_var[0]
                aposta3 = round((retorno2() / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta3 > 0.0:
                aposta1 = round((retorno3() / odd_1) / arred_var[0]) * arred_var[0]
                aposta2 = round((retorno3() / odd_2) / arred_var[1]) * arred_var[1]
            max_retorno = max(retornos)
            lucro1 = round((max_retorno - aposta1 - aposta2 - aposta3), 2)
            lucro2 = lucro1
            lucro3 = lucro1
            lucro_percent = round((lucro1 / (aposta1 + aposta2 + aposta3)) * 100, 2)
            return aposta1, aposta2, aposta3, None, lucro1, lucro2, lucro3, lucro_percent, None # Sem Padrão
        def reordenar(odds_lucro, apostas, ordem):
            new_odds_lucro = [0] * len(odds_lucro)
            new_apostas = [0] * len(apostas)
            for i, o in enumerate(ordem):
                new_odds_lucro[o-1] = odds_lucro[i]
                new_apostas[o-1] = apostas[i]
            return new_odds_lucro, new_apostas
        new_odds, new_apostas = reordenar(odds, apostas, ordem)
        aposta1, aposta2, aposta3 = new_apostas
        odd_1, odd_2, odd_3 = new_odds
        ordem_inversa = [0] * len(ordem)
        for i, o in enumerate(ordem):
            ordem_inversa[o - 1] = i + 1
        if padrao == '1-X-2':
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                aposta3 = round(retorno1() / odd_3 / arred_var[2]) * arred_var[2]
            elif aposta1 > 0 and aposta3 > 0:
                aposta2 = round(retorno1() / odd_2 / arred_var[1]) * arred_var[1]
            elif aposta2 > 0 and aposta3 > 0:
                aposta1 = round(retorno3() / odd_1 / arred_var[0]) * arred_var[0]
            elif aposta1 > 0.0:
                aposta2 = round(retorno1() / odd_2 / arred_var[1]) * arred_var[1]
                aposta3 = round(retorno1() / odd_3 / arred_var[2]) * arred_var[2]
            elif aposta2 > 0.0:
                aposta1 = round(retorno2() / odd_1 / arred_var[0]) * arred_var[0]
                aposta3 = round(retorno2() / odd_3 / arred_var[2]) * arred_var[2]
            elif aposta3 > 0.0:
                aposta1 = round(retorno3() / odd_1 / arred_var[0]) * arred_var[0]
                aposta2 = round(retorno3() / odd_2 / arred_var[1]) * arred_var[1]
            lucro1 = round ((retorno1() - aposta1 - aposta2 - aposta3), 2)
            lucro2 = round ((retorno2() - aposta1 - aposta2 - aposta3), 2)
            lucro3 = round ((retorno3() - aposta1 - aposta2 - aposta3), 2)
            lucro_percent = round((((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            apostas = [aposta1, aposta2, aposta3]
            lucros = [lucro1, lucro2, lucro3]
            lucros, apostas = reordenar(lucros, apostas, ordem)
            return apostas[0], apostas[1], apostas[2], None, lucros[0], lucros[1], lucros[2], lucro_percent, None, None
        elif padrao == '0-X-2' or padrao == '1-X-0':
            if padrao == '1-X-0':
                aposta1, aposta2, aposta3 = aposta3, aposta2, aposta1
                odd_1, odd_2, odd_3 = odd_3, odd_2, odd_1
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                aposta3 = round(((aposta1 * odd_1) / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta1 > 0 and aposta3 > 0:
                aposta2 = round(((retorno3() - aposta1) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0 and aposta3 > 0:
                aposta1 = round(((aposta3 * odd_3) / odd_1) / arred_var[0]) * arred_var[0]
            elif aposta1 > 0.0:
                aposta3 = round(((aposta1 * odd_1) / odd_3) / arred_var[2]) * arred_var[2]
                aposta2 = round(((retorno3() - aposta1) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta3 > 0.0:
                aposta1 = round(((aposta3 * odd_3) / odd_1) / arred_var[0]) * arred_var[0]
                aposta2 = round(((retorno3() - aposta1) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0.0:
                aposta3 = round(retorno2() / odd_3, 2)
                while True:
                    aposta1 = round(retorno3() / odd_1, 2)
                    if aposta3 * odd_3 >= round((retorno2() + aposta1), 2):
                        aposta3 = round((aposta3) / arred_var[2]) * arred_var[2]
                        aposta1 = round(((odd_3 * aposta3) / odd_1) / arred_var[0]) * arred_var[0]
                        break
                    aposta3 += 0.01

            lucro1 = round(aposta1 * odd_1 - aposta1 - aposta2 - aposta3, 2)
            lucro2 = round(aposta2 * odd_2 - aposta2 - aposta3, 2)
            lucro3 = round(aposta3 * odd_3 - aposta1 - aposta2 - aposta3, 2)
            lucro_percent = round((((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            apostas = [aposta1, aposta2, aposta3]
            lucros = [lucro1, lucro2, lucro3]
            if padrao == '1-X-0':
                inverso = [3, 2, 1]
                lucros, apostas = reordenar(lucros, apostas, inverso)
            lucros, apostas = reordenar(lucros, apostas, ordem_inversa)
            return apostas[0], apostas[1], apostas[2], None, lucros[0], lucros[1], lucros[2], lucro_percent, None, None
        elif padrao == '0-X2-2' or padrao == '1-1X-0':
            if padrao == '1-1X-0':
                aposta1, aposta2, aposta3 = aposta3, aposta2, aposta1
                odd_1, odd_2, odd_3 = odd_3, odd_2, odd_1
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                aposta3 = round((aposta1 / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta1 > 0 and aposta3 > 0:
                aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0 and aposta3 > 0:
                aposta1 = round((aposta3 * odd_3) / arred_var[0]) * arred_var[0]
            elif aposta1 > 0.0:
                aposta3 = round((aposta1 / odd_3) / arred_var[2]) * arred_var[2]
                aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0.0:
                aposta3 = 0.0
                while True:
                    if aposta3 * odd_3 + aposta2 * odd_2 <= aposta3 * odd_3 * odd_1:
                        aposta3 = round(aposta3, 2)
                        break
                    aposta3 += 0.01
                aposta1 = round((aposta3 * odd_3) / arred_var[0]) * arred_var[0]
            elif aposta3 > 0.0:
                aposta1 = round((aposta3 * odd_3) / arred_var[0]) * arred_var[0]
                aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
            lucro1 = round((retorno1() - aposta1 - aposta2 - aposta3), 2)
            lucro2 = round((retorno2() - aposta2 - aposta3), 2)
            lucro3 = round((retorno3() + retorno2() - aposta1 - aposta2 - aposta3), 2)
            lucro_percent = round((lucro1 + lucro2 + lucro3) / 3, 2)
            apostas = [aposta1, aposta2, aposta3]
            lucros = [lucro1, lucro2, lucro3]
            if padrao == '1-1X-0':
                inverso = [3, 2, 1]
                lucros, apostas = reordenar(lucros, apostas, inverso)
            lucros, apostas = reordenar(lucros, apostas, ordem_inversa)
            return apostas[0], apostas[1], apostas[2], None, lucros[0], lucros[1], lucros[2], lucro_percent, None, None
        elif padrao == '0.25-X2-2' or padrao == '1-1X-0.25':
            if padrao == '1-1X-0.25':
                aposta1, aposta2, aposta3 = aposta3, aposta2, aposta1
                odd_1, odd_2, odd_3 = odd_3, odd_2, odd_1
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                aposta3 = round((retorno1_halfwin() / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta1 > 0 and aposta3 > 0:
                aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0 and aposta3 > 0:
                aposta1 = round(((retorno2() + retorno3()) / odd_1) / arred_var[0]) * arred_var[0]
            elif aposta1 > 0:
                aposta3 = round((retorno1_halfwin() / odd_3) / arred_var[2]) * arred_var[2]
                aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0:
                aposta3 = aposta2
                aposta1 = 0
                while retorno1() < retorno2() + retorno3():
                    aposta3 += 0.01
                    aposta1 = round((retorno3() / (0.5 + odd_1 / 2)) / arred_var[0]) * arred_var[0]
            elif aposta3 > 0:
                aposta1 = round((retorno3() / (0.5 + odd_1 / 2)) / arred_var[0]) * arred_var[0]
                aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
            lucro1 = round((retorno1() - aposta1 - aposta2 - aposta3), 2)
            lucro3 = round((retorno2() + retorno3() - aposta1 - aposta2 - aposta3), 2)
            lucro2 = round((retorno2() + retorno1_halfwin() - aposta1 - aposta2 - aposta3), 2)
            lucro_percent = round((((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            apostas = [aposta1, aposta2, aposta3]
            lucros = [lucro1, lucro2, lucro3]
            if padrao == '1-1X-0.25':
                inverso = [3, 2, 1]
                lucros, apostas = reordenar(lucros, apostas, inverso)
            lucros, apostas = reordenar(lucros, apostas, ordem_inversa)
            return apostas[0], apostas[1], apostas[2], None, lucros[0], lucros[1], lucros[2], lucro_percent, None, None
        elif padrao == '-0.25-X2-2' or padrao == '1-1X--0.25':
            if padrao == '1-1X--0.25':
                aposta1, aposta2, aposta3 = aposta3, aposta2, aposta1
                odd_1, odd_2, odd_3 = odd_3, odd_2, odd_1
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                aposta3 = round(((retorno1() - retorno2()) / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta1 > 0 and aposta3 > 0:
                aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0 and aposta3 > 0:
                aposta1 = round(((retorno2() + retorno3()) / odd_1) / arred_var[0]) * arred_var[0]
            elif aposta1 > 0:
                aposta3 = round((retorno1_halfloss() / odd_3) / arred_var[2]) * arred_var[2]
                aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0:
                aposta1 = 0
                aposta3 = 0
                while retorno1() < retorno2() + retorno3():
                    aposta3 += 0.01
                    aposta1 = round((retorno3() * 2) / arred_var[0]) * arred_var[0]
            elif aposta3 > 0:
                aposta1 = round((retorno3() * 2) / arred_var[0]) * arred_var[0]
                aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
            lucro1 = round((retorno1() - aposta1 - aposta2 - aposta3), 2)
            lucro3 = round((retorno2() + retorno3() - aposta1 - aposta2 - aposta3), 2)
            lucro2 = round((retorno2() + retorno1_halfloss() - aposta1 - aposta2 - aposta3), 2)
            lucro_percent = round((((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            apostas = [aposta1, aposta2, aposta3]
            lucros = [lucro1, lucro2, lucro3]
            if padrao == '1-1X--0.25':
                inverso = [3, 2, 1]
                lucros, apostas = reordenar(lucros, apostas, inverso)
            lucros, apostas = reordenar(lucros, apostas, ordem_inversa)
            return apostas[0], apostas[1], apostas[2], None, lucros[0], lucros[1], lucros[2], lucro_percent, None, None
        elif padrao == '-0.25-X-0' or padrao == '0-X--0.25':
            if padrao == '0-X--0.25':
                aposta1, aposta2, aposta3 = aposta3, aposta2, aposta1
                odd_1, odd_2, odd_3 = odd_3, odd_2, odd_1
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta1 > 0 and aposta3 > 0:
                aposta2 = round(((retorno1() - aposta1 / 2 - aposta3) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0 and aposta3 > 0:
                aposta1 = round((retorno3() / odd_1) / arred_var[0]) * arred_var[0]
            elif aposta1 > 0:
                aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
                aposta2 = round(((retorno1() - aposta1 / 2 - aposta3) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0:
                aposta1 = round((retorno2() / (odd_1 - 0.5 - odd_1 / odd_3)) / arred_var[0]) * arred_var[0]
                aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta3 > 0:
                aposta1 = round((retorno3() / odd_1) / arred_var[0]) * arred_var[0]
                aposta2 = round(((retorno1() - aposta1 / 2 - aposta3) / odd_2) / arred_var[1]) * arred_var[1]
            lucro1 = round((retorno1() - aposta1 - aposta2 - aposta3), 2)
            lucro3 = round((retorno3() - aposta1 - aposta2 - aposta3), 2)
            lucro2 = round((retorno2() + retorno1_halfloss() - aposta1 - aposta2), 2)
            lucro_percent = round((((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            apostas = [aposta1, aposta2, aposta3]
            lucros = [lucro1, lucro2, lucro3]
            if padrao == '0-X--0.25':
                inverso = [3, 2, 1]
                lucros, apostas = reordenar(lucros, apostas, inverso)
            lucros, apostas = reordenar(lucros, apostas, ordem_inversa)
            return apostas[0], apostas[1], apostas[2], None, lucros[0], lucros[1], lucros[2], lucro_percent, None, None
        elif padrao == '0.25-X-2' or padrao == '1-X-0.25':
            if padrao == '1-X-0.25':
                aposta1, aposta2, aposta3 = aposta3, aposta2, aposta1
                odd_1, odd_2, odd_3 = odd_3, odd_2, odd_1
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta1 > 0 and aposta3 > 0:
                aposta2 = round(((retorno1() - retorno1_halfwin()) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0 and aposta3 > 0:
                aposta1 = round((retorno3() / odd_1) / arred_var[0]) * arred_var[0]
            elif aposta1 > 0:
                aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
                aposta2 = round(((retorno1() - retorno1_halfwin()) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0:
                aposta1 = retorno2() / odd_1
                while retorno2() + retorno1_halfwin() > retorno1():
                    aposta1 += 0.01
                aposta1 = round(aposta1 / arred_var[0]) * arred_var[0]
                aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta3 > 0:
                aposta1 = retorno3() / odd_1
                aposta2 = round(((retorno1() - retorno1_halfwin()) / odd_2) / arred_var[1]) * arred_var[1]
            lucro1 = round((retorno1() - aposta1 - aposta2 - aposta3), 2)
            lucro3 = round((retorno3() - aposta1 - aposta2 - aposta3), 2)
            lucro2 = round((retorno2() + retorno1_halfwin() - aposta1 - aposta2 - aposta3), 2)
            lucro_percent = round((((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            apostas = [aposta1, aposta2, aposta3]
            lucros = [lucro1, lucro2, lucro3]
            if padrao == '1-X-0.25':
                inverso = [3, 2, 1]
                lucros, apostas = reordenar(lucros, apostas, inverso)
            lucros, apostas = reordenar(lucros, apostas, ordem_inversa)
            return apostas[0], apostas[1], apostas[2], None, lucros[0], lucros[1], lucros[2], lucro_percent, None, None
        elif padrao == '-0.25-X-2' or padrao == '1-X--0.25':
            if padrao == '1-X--0.25':
                aposta1, aposta2, aposta3 = aposta3, aposta2, aposta1
                odd_1, odd_2, odd_3 = odd_3, odd_2, odd_1
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta1 > 0 and aposta3 > 0:
                aposta2 = round(((retorno1() - retorno1_halfloss()) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0 and aposta3 > 0:
                aposta1 = round((retorno3() / odd_1) / arred_var[0]) * arred_var[0]
            elif aposta1 > 0:
                aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
                aposta2 = round(((retorno1() - retorno1_halfloss()) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0:
                aposta1 = retorno2() / odd_1
                while retorno2() + retorno1_halfloss() > retorno1():
                    aposta1 += 0.01
                aposta1 = round(aposta1 / arred_var[0]) * arred_var[0]
                aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta3 > 0:
                aposta1 = retorno3() / odd_1
                aposta2 = round(((retorno1() - retorno1_halfloss()) / odd_2) / arred_var[1]) * arred_var[1]
            lucro1 = round((retorno1() - aposta1 - aposta2 - aposta3), 2)
            lucro3 = round((retorno3() - aposta1 - aposta2 - aposta3), 2)
            lucro2 = round((retorno2() + retorno1_halfloss() - aposta1 - aposta2 - aposta3), 2)
            lucro_percent = round((((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            apostas = [aposta1, aposta2, aposta3]
            lucros = [lucro1, lucro2, lucro3]
            if padrao == '1-X--0.25':
                inverso = [3, 2, 1]
                lucros, apostas = reordenar(lucros, apostas, inverso)
            lucros, apostas = reordenar(lucros, apostas, ordem_inversa)
            return apostas[0], apostas[1], apostas[2], None, lucros[0], lucros[1], lucros[2], lucro_percent, None, None
        elif padrao == '-0.25-X--0.25':
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta1 > 0 and aposta3 > 0:
                aposta2 = round(((retorno1() - aposta1 / 2 - aposta3 / 2) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0 and aposta3 > 0:
                aposta1 = round((retorno3() / odd_1) / arred_var[0]) * arred_var[0]
            elif aposta1 > 0:
                aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
                aposta2 = round(((retorno1() - aposta1 / 2 - aposta3 / 2) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0:
                aposta1 = round((retorno2() / (odd_1 - 0.5 - odd_1 / odd_3)) / arred_var[0]) * arred_var[0]
                aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta3 > 0:
                aposta1 = round((retorno3() / odd_1) / arred_var[0]) * arred_var[0]
                aposta2 = round(((retorno1() - aposta1 / 2 - aposta3 / 2) / odd_2) / arred_var[1]) * arred_var[1]
            lucro1 = round((retorno1() - aposta1 - aposta2 - aposta3), 2)
            lucro3 = round((retorno3() - aposta1 - aposta2 - aposta3), 2)
            lucro2 = round((retorno2() + retorno1_halfloss() + retorno3_halfloss() - aposta1 - aposta2 - aposta3), 2)
            lucro_percent = round((((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            apostas = [aposta1, aposta2, aposta3]
            lucros = [lucro1, lucro2, lucro3]
            lucros, apostas = reordenar(lucros, apostas, ordem_inversa)
            return apostas[0], apostas[1], apostas[2], None, lucros[0], lucros[1], lucros[2], lucro_percent, None, None
        elif padrao == '-0.25-1X--0.25' or padrao == '-0.25-X2--0.25':
            if padrao == '-0.25-1X--0.25':
                aposta1, aposta2, aposta3 = aposta3, aposta2, aposta1
                odd_1, odd_2, odd_3 = odd_3, odd_2, odd_1
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                aposta3 = round(((retorno1() - retorno2()) / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta1 > 0 and aposta3 > 0:
                aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0 and aposta3 > 0:
                aposta1 = round(((retorno2() + retorno3()) / odd_1) / arred_var[0]) * arred_var[0]
            elif aposta1 > 0:
                aposta3 = round((aposta1 / (2 * odd_3 - 1)) / arred_var[2]) * arred_var[2]
                aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0:
                aposta1 = 0
                aposta3 = 0
                while retorno1() < retorno2() + retorno3():
                    aposta3 += 0.01
                    aposta1 = round(aposta3 * (2 * odd_3 - 1) / arred_var[0]) * arred_var[0]
            elif aposta3 > 0:
                aposta1 = aposta3 * (2 * odd_3 - 1)
                aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
            lucro1 = round((retorno1() - aposta1 - aposta2 - aposta3), 2)
            lucro3 = round((retorno2() + retorno3() - aposta1 - aposta2 - aposta3), 2)
            lucro2 = round((retorno2() + retorno1_halfloss() - aposta1 - aposta2 - aposta3), 2)
            lucro_percent = round((((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            apostas = [aposta1, aposta2, aposta3]
            lucros = [lucro1, lucro2, lucro3]
            if padrao == '-0.25-1X--0.25':
                inverso = [3, 2, 1]
                lucros, apostas = reordenar(lucros, apostas, inverso)
            lucros, apostas = reordenar(lucros, apostas, ordem_inversa)
            return apostas[0], apostas[1], apostas[2], None, lucros[0], lucros[1], lucros[2], lucro_percent, None, None
        elif padrao == '0-X2--0.25' or padrao == '-0.25-1X-0':
            if padrao == '-0.25-1X-0':
                aposta1, aposta2, aposta3 = aposta3, aposta2, aposta1
                odd_1, odd_2, odd_3 = odd_3, odd_2, odd_1
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                aposta3 = round(((retorno1() - retorno2())/ odd_3) / arred_var[2]) * arred_var[2]
            elif aposta1 > 0 and aposta3 > 0:
                aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0 and aposta3 > 0:
                aposta1 = round(((retorno2() + retorno3()) / odd_1) / arred_var[0]) * arred_var[0]
            elif aposta1 > 0:
                aposta3 = aposta1 / odd_3
                while not check_margin([retorno1() - aposta1, retorno3() + retorno2() - aposta1, retorno2() + retorno3_halfloss()], [0.0038 * (sum(new_odds)-odd_1), 0.0038 * (sum(new_odds)-odd_2), 0.0038 * (sum(new_odds)-odd_3)]):
                    aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
                    aposta3 += 0.01
                aposta3 = round((aposta3 - 0.01) / arred_var[2]) * arred_var[2]
            elif aposta2 > 0:
                aposta1 = aposta2
                while not check_margin([retorno1() - aposta1, retorno3() + retorno2() - aposta1, retorno2() + retorno3_halfloss()], [0.0038 * (sum(new_odds)-odd_1), 0.0038 * (sum(new_odds)-odd_2), 0.0038 * (sum(new_odds)-odd_3)]):
                    aposta3 = round(((retorno1() - retorno2())/ odd_3) / arred_var[2]) * arred_var[2]
                    aposta1 += 0.01
                aposta1 = round((aposta1 - 0.01) / arred_var[2]) * arred_var[2]
            elif aposta3 > 0:
                aposta1 = aposta3 / odd_3
                while not check_margin([retorno1() - aposta1, retorno3() + retorno2() - aposta1, retorno2() + retorno3_halfloss()], [0.0038 * (sum(new_odds)-odd_1), 0.0038 * (sum(new_odds)-odd_2), 0.0038 * (sum(new_odds)-odd_3)]):
                    aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
                    aposta1 += 0.01
                aposta1 = round((aposta1) / arred_var[2]) * arred_var[2]
            lucro1 = round((retorno1() - aposta1 - aposta2 - aposta3), 2)
            lucro3 = round((retorno3() + retorno2() - aposta1 - aposta2 - aposta3), 2)
            lucro2 = round((retorno2() + retorno3_halfloss() - aposta3 - aposta2), 2)
            lucro_percent = round((((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            apostas = [aposta1, aposta2, aposta3]
            lucros = [lucro1, lucro2, lucro3]
            if padrao == '-0.25-1X-0':
                inverso = [3, 2, 1]
                lucros, apostas = reordenar(lucros, apostas, inverso)
            lucros, apostas = reordenar(lucros, apostas, ordem_inversa)
            return apostas[0], apostas[1], apostas[2], None, lucros[0], lucros[1], lucros[2], lucro_percent, None, None
        elif padrao == '-0.25-X2-0' or padrao == '0-1X--0.25':
            if padrao == '0-1X--0.25':
                aposta1, aposta2, aposta3 = aposta3, aposta2, aposta1
                odd_1, odd_2, odd_3 = odd_3, odd_2, odd_1
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                aposta3 = round(((retorno1() - retorno2())/ odd_3) / arred_var[2]) * arred_var[2]
            elif aposta1 > 0 and aposta3 > 0:
                aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0 and aposta3 > 0:
                aposta1 = round(((retorno2() + retorno3()) / odd_1) / arred_var[0]) * arred_var[0]
            elif aposta1 > 0:
                aposta3 = aposta1 / odd_3
                while not check_margin([retorno1() - aposta1 - aposta2 - aposta3, retorno3() + retorno2() - aposta1 - aposta2 - aposta3, retorno2() + retorno1_halfloss() - aposta1 - aposta2], [0.0038 * (sum(new_odds)-odd_1), 0.0038 * (sum(new_odds)-odd_2), 0.0038 * (sum(new_odds)-odd_3)]):
                    aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
                    aposta3 += 0.01
                aposta3 = round((aposta3 - 0.01) / arred_var[2]) * arred_var[2]
            elif aposta2 > 0:
                aposta1 = aposta2
                while not check_margin([retorno1() - aposta1 - aposta2 - aposta3, retorno3() + retorno2() - aposta1 - aposta2 - aposta3, retorno2() + retorno1_halfloss() - aposta1 - aposta2], [0.0038 * (sum(new_odds)-odd_1), 0.0038 * (sum(new_odds)-odd_2), 0.0038 * (sum(new_odds)-odd_3)]):
                    aposta3 = round(((retorno1() - retorno2())/ odd_3) / arred_var[2]) * arred_var[2]
                    aposta1 += 0.01
                aposta1 = round((aposta1 - 0.01) / arred_var[2]) * arred_var[2]
            elif aposta3 > 0:
                aposta1 = aposta3 / odd_3
                while not check_margin([retorno1() - aposta1 - aposta2 - aposta3, retorno3() + retorno2() - aposta1 - aposta2 - aposta3, retorno2() + retorno1_halfloss() - aposta1 - aposta2], [0.0038 * (sum(new_odds)-odd_1), 0.0038 * (sum(new_odds)-odd_2), 0.0038 * (sum(new_odds)-odd_3)]):
                    aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
                    aposta1 += 0.01
                aposta1 = round((aposta1) / arred_var[2]) * arred_var[2]
            lucro1 = round((retorno1() - aposta1 - aposta2 - aposta3), 2)
            lucro3 = round((retorno3() + retorno2() - aposta1 - aposta2 - aposta3), 2)
            lucro2 = round((retorno2() + retorno1_halfloss() - aposta1 - aposta2), 2)
            lucro_percent = round((((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            apostas = [aposta1, aposta2, aposta3]
            lucros = [lucro1, lucro2, lucro3]
            if padrao == '0-1X--0.25':
                inverso = [3, 2, 1]
                lucros, apostas = reordenar(lucros, apostas, inverso)
            lucros, apostas = reordenar(lucros, apostas, ordem_inversa)
            return apostas[0], apostas[1], apostas[2], None, lucros[0], lucros[1], lucros[2], lucro_percent, None, None
        elif padrao == '0.25-12-X2' or padrao == '1X-12-0.25':
            if padrao == '1X-12-0.25':
                aposta1, aposta2, aposta3 = aposta3, aposta2, aposta1
                odd_1, odd_2, odd_3 = odd_3, odd_2, odd_1
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta1 > 0 and aposta3 > 0:
                aposta2 = round((retorno1_halfwin() / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0 and aposta3 > 0:
                aposta1 = round((retorno3() / odd_1) / arred_var[0]) * arred_var[0]
            elif aposta1 > 0:
                aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
                aposta2 = round((retorno1_halfwin() / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0:
                aposta1 = round(((aposta2 * odd_2) / (1/2 + odd_1/2)) / arred_var[2]) * arred_var[2]
                aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta3 > 0:
                aposta1 = retorno3() / odd_1
                aposta2 = round((retorno1_halfwin() / odd_2) / arred_var[1]) * arred_var[1]
            lucro1 = round((retorno1() + retorno2() - aposta1 - aposta2 - aposta3), 2)
            lucro2 = round((retorno3() + retorno1_halfwin() - aposta1 - aposta2 - aposta3), 2)
            lucro3 = round((retorno3() + retorno2() - aposta1 - aposta2 - aposta3), 2)
            lucro_percent = round((((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            apostas = [aposta1, aposta2, aposta3]
            lucros = [lucro1, lucro2, lucro3]
            if padrao == '1X-12-0.25':
                inverso = [3, 2, 1]
                lucros, apostas = reordenar(lucros, apostas, inverso)
            lucros, apostas = reordenar(lucros, apostas, ordem_inversa)
            return apostas[0], apostas[1], apostas[2], None, lucros[0], lucros[1], lucros[2], lucro_percent, None, None
        elif padrao == '0.25-12-0.25':
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta1 > 0 and aposta3 > 0:
                aposta2 = 0
                while not check_margin([retorno1() + retorno2(), retorno3_halfwin() + retorno1_halfwin(), retorno1() + retorno2()], [0.0038 * (sum(new_odds) - odd_1), 0.0038 * (sum(new_odds) - odd_2), 0.0038 * (sum(new_odds) - odd_3)]):
                    aposta2 += 0.01
            elif aposta2 > 0 and aposta3 > 0:
                aposta1 = round((retorno3() / odd_1) / arred_var[0]) * arred_var[0]
            elif aposta1 > 0:
                aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
                aposta2 = 0
                while not check_margin(
                        [retorno1() + retorno2(), retorno3_halfwin() + retorno1_halfwin(), retorno1() + retorno2()],
                        [0.0038 * (sum(new_odds) - odd_1), 0.0038 * (sum(new_odds) - odd_2),
                         0.0038 * (sum(new_odds) - odd_3)]):
                    aposta2 += 0.01
            elif aposta2 > 0:
                aposta1 = 0
                while not check_margin(
                        [retorno1() + retorno2(), retorno3_halfwin() + retorno1_halfwin(), retorno1() + retorno2()],
                        [0.0038 * (sum(new_odds) - odd_1), 0.0038 * (sum(new_odds) - odd_2),
                         0.0038 * (sum(new_odds) - odd_3)]):
                    aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
                    aposta1 += 0.01
            elif aposta3 > 0:
                aposta1 = retorno3() / odd_1
                aposta2 = 0
                while not check_margin(
                        [retorno1() + retorno2(), retorno3_halfwin() + retorno1_halfwin(), retorno1() + retorno2()],
                        [0.0038 * (sum(new_odds) - odd_1), 0.0038 * (sum(new_odds) - odd_2),
                         0.0038 * (sum(new_odds) - odd_3)]):
                    aposta2 += 0.01
            lucro1 = round((retorno1() + retorno2() - aposta1 - aposta2 - aposta3), 2)
            lucro2 = round((retorno3_halfwin() + retorno1_halfwin() - aposta1 - aposta2 - aposta3), 2)
            lucro3 = round((retorno3() + retorno2() - aposta1 - aposta2 - aposta3), 2)
            lucro_percent = round((((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            apostas = [aposta1, aposta2, aposta3]
            lucros = [lucro1, lucro2, lucro3]
            lucros, apostas = reordenar(lucros, apostas, ordem_inversa)
            return apostas[0], apostas[1], apostas[2], None, lucros[0], lucros[1], lucros[2], lucro_percent, None, None
        elif padrao == '0-12-X2' or padrao == '1X-12-0':
            if padrao == '1X-12-0':
                aposta1, aposta2, aposta3 = aposta3, aposta2, aposta1
                odd_1, odd_2, odd_3 = odd_3, odd_2, odd_1
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta1 > 0 and aposta3 > 0:
                aposta2 = round((aposta1 / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0 and aposta3 > 0:
                aposta1 = round((retorno3() / odd_1) / arred_var[0]) * arred_var[0]
            elif aposta1 > 0:
                aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
                aposta2 = round((aposta1 / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0:
                aposta1 = round(retorno2() / arred_var[2]) * arred_var[2]
                aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta3 > 0:
                aposta1 = retorno3() / odd_1
                aposta2 = round((aposta1 / odd_2) / arred_var[1]) * arred_var[1]
            lucro1 = round((retorno1() + retorno2() - aposta1 - aposta2 - aposta3), 2)
            lucro2 = round((retorno3() + retorno1_halfwin() - aposta1 - aposta2 - aposta3), 2)
            lucro3 = round((retorno3() + retorno2() - aposta1 - aposta2 - aposta3), 2)
            lucro_percent = round((((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            apostas = [aposta1, aposta2, aposta3]
            lucros = [lucro1, lucro2, lucro3]
            if padrao == '1X-12-0':
                inverso = [3, 2, 1]
                lucros, apostas = reordenar(lucros, apostas, inverso)
            lucros, apostas = reordenar(lucros, apostas, ordem_inversa)
            return apostas[0], apostas[1], apostas[2], None, lucros[0], lucros[1], lucros[2], lucro_percent, None, None
        elif padrao == 'U1.25-O0.75-O1.5':
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                aposta3 = round(((retorno1() - retorno2()) / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta1 > 0 and aposta3 > 0:
                aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var[2]) * arred_var[2]
            elif aposta2 > 0 and aposta3 > 0:
                aposta1 = round(((retorno2() + retorno3()) / odd_1) / arred_var[0]) * arred_var[0]
            elif aposta1 > 0:
                aposta2 = 0
                while not check_margin(
                        [retorno1(), retorno1_halfwin() + retorno2_halfwin(), retorno2() + retorno3()],
                        [0.0038 * (sum(new_odds) - odd_1), 0.0038 * (sum(new_odds) - odd_2),
                         0.0038 * (sum(new_odds) - odd_3)]):
                    aposta2 += 0.01
                    aposta3 = (retorno1() - retorno2()) / odd_3
                aposta2 = round((aposta2 + 0.01) / arred_var[1]) * arred_var[1]
                aposta3 = round((aposta3 - 0.01) / arred_var[1]) * arred_var[2]
            elif aposta2 > 0:
                aposta1 = 0
                while not check_margin(
                        [retorno1(), retorno1_halfwin() + retorno2_halfwin(), retorno2() + retorno3()],
                        [0.0038 * (sum(new_odds) - odd_1), 0.0038 * (sum(new_odds) - odd_2),
                         0.0038 * (sum(new_odds) - odd_3)]):
                    aposta1 += 0.01
                    aposta3 = (retorno1() - retorno2()) / odd_3
                aposta1 = round((aposta1 + 0.01) / arred_var[1]) * arred_var[0]
                aposta3 = round((aposta3 - 0.01) / arred_var[1]) * arred_var[2]
            elif aposta3 > 0:
                aposta1 = retorno3() / odd_1
                aposta2 = 0
                while not check_margin(
                        [retorno1(), retorno1_halfwin() + retorno2_halfwin(), retorno2() + retorno3()],
                        [0.0038 * (sum(new_odds) - odd_1), 0.0038 * (sum(new_odds) - odd_2),
                         0.0038 * (sum(new_odds) - odd_3)]):
                    aposta1 += 0.01
                    aposta2 = (retorno1() - retorno3()) / odd_2
                aposta1 = round((aposta1 + 0.01) / arred_var[1]) * arred_var[0]
                aposta2 = round((aposta2 - 0.01) / arred_var[1]) * arred_var[1]
            lucro1 = round((retorno1() - aposta1 - aposta2 - aposta3), 2)
            lucro2 = round((retorno1_halfwin() + retorno2_halfwin() - aposta1 - aposta2 - aposta3), 2)
            lucro3 = round((retorno3() + retorno2() - aposta1 - aposta2 - aposta3), 2)
            lucro_percent = round((((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            apostas = [aposta1, aposta2, aposta3]
            lucros = [lucro1, lucro2, lucro3]
            lucros, apostas = reordenar(lucros, apostas, ordem_inversa)
            return apostas[0], apostas[1], apostas[2], None, lucros[0], lucros[1], lucros[2], lucro_percent, None, None
        elif padrao == '112' or padrao == '112X' or padrao == '112W' or padrao == '112L':
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                aposta3 = round(((retorno1() + retorno2()) / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta1 > 0 and aposta3 > 0:
                aposta2 = round(((retorno3() - retorno1()) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0 and aposta3 > 0:
                aposta1 = round(((retorno3() - retorno2()) / odd_1) / arred_var[0]) * arred_var[0]
            elif aposta1 > 0:
                aposta2 = round((retorno1() / odd_2) / arred_var[1]) * arred_var[1]
                aposta3 = round(((retorno1() + retorno2()) / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta2 > 0:
                aposta1 = round((retorno2() / odd_1) / arred_var[0]) * arred_var[0]
                aposta3 = round(((retorno1() + retorno2()) / odd_3) / arred_var[2]) * arred_var[2]
            else:
                aposta1 = round(((retorno3() / 2) / odd_1) / arred_var[0]) * arred_var[0]
                aposta2 = round(((retorno3() / 2) / odd_2) / arred_var[1]) * arred_var[1]
            lucro1 = round((retorno1() + retorno2() - aposta1 - aposta2 - aposta3), 2)
            if padrao == '112':
                lucro2 = lucro1
            elif padrao == '112X':
                lucro2 = 0
            else:
                lucro2 = round(lucro1 / 2, 2)
            lucro3 = round((retorno3() - aposta1 - aposta2 - aposta3), 2)
            lucro_percent = round((((lucro1 + lucro3) / 2) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            liability1 = calc_liability(mercado1, odd1, aposta1)
            liability2 = calc_liability(mercado2, odd2, aposta2)
            liability3 = calc_liability(mercado3, odd3, aposta3)
            apostas = [aposta1, aposta2, aposta3]
            lucros = [lucro1, lucro2, lucro3]
            lucros, apostas = reordenar(lucros, apostas, ordem_inversa)
            return apostas[0], apostas[1], apostas[2], liability1, lucros[0], lucros[1], lucros[2], lucro_percent, liability2, liability3
    else:
        if aposta1 > 0.0 and aposta2 > 0.0:
            pass
        elif aposta1 > 0.0:
            aposta2 = round(((retorno1() - (aposta1 if bonus[0] else 0)) / (odd_2 - (1 if bonus[1] else 0))) / arred_var[1]) * arred_var[1]
        elif aposta2 > 0.0:
            aposta1 = round(((retorno2() - (aposta2 if bonus[1] else 0)) / (odd_1 - (1 if bonus[0] else 0))) / arred_var[0]) * arred_var[0]
        lucro1 = round((retorno1() - aposta1 - (aposta2 if not bonus[1] else 0)), 2)
        lucro2 = round((retorno2() - (aposta1 if not bonus[0] else 0) - aposta2), 2)
        lucro3 = 0
        liability1 = calc_liability(mercado1, odd1, aposta1)
        liability2 = calc_liability(mercado2, odd2, aposta2)
        liability3 = None
        lucro_percent = round((((lucro1 + lucro2) / 2) / (aposta1 + aposta2)) * 100, 2)
        return aposta1, aposta2, aposta3, liability1, lucro1, lucro2, lucro3, lucro_percent, liability2, liability3

def gerar_dados(mercados, odds, apostas, valores, tipo='padrao', time='padrao'):
    if time == 'oposto':
        for i, mercado in enumerate(mercados):
            if mercado == '1X':
                mercados[i] = 'X2'
            elif mercado == 'X2':
                mercados[i] = '1X'
            elif mercado == '12':
                pass
            elif mercado.endswith('1'):
                comeco = mercado[:-1]
                mercados[i] = f'{comeco}2'
            elif mercado.endswith('2'):
                comeco = mercado[:-1]
                mercados[i] = f'{comeco}1'
    if tipo == 'padrao':
        aposta1 = apostas[0]
        aposta2 = apostas[1]
        aposta3 = apostas[2]
        odd1 = odds[0]
        odd2 = odds[1]
        odd3 = odds[2]
        mercado1 = mercados[0]
        mercado2 = mercados[1]
        mercado3 = mercados[2]
        valor1 = valores[0]
        valor2 = valores[1]
        valor3 = valores[2]
        taxa1 = 0
        taxa2 = 0
        taxa3 = 0
        arreds = [0.01, 0.01, 0.01]
        bonus = [False, False, True]
    elif tipo == 'inverso':
        aposta1 = apostas[2]
        aposta2 = apostas[1]
        aposta3 = apostas[0]
        odd1 = odds[2]
        odd2 = odds[1]
        odd3 = odds[0]
        mercado1 = mercados[2]
        mercado2 = mercados[1]
        mercado3 = mercados[0]
        valor1 = valores[2]
        valor2 = valores[1]
        valor3 = valores[0]
        taxa1 = 0
        taxa2 = 0
        taxa3 = 0
        arreds = [0.01, 0.01, 0.01]
        bonus = [False, False, False]
    elif tipo == '312':
        aposta1 = apostas[2]
        aposta2 = apostas[0]
        aposta3 = apostas[1]
        odd1 = odds[2]
        odd2 = odds[0]
        odd3 = odds[1]
        mercado1 = mercados[2]
        mercado2 = mercados[0]
        mercado3 = mercados[1]
        valor1 = valores[2]
        valor2 = valores[0]
        valor3 = valores[1]
        taxa1 = 0
        taxa2 = 0
        taxa3 = 0
        arreds = [0.01, 0.01, 0.01]
        bonus = [False, False, False]
    mercados = [mercado1, mercado2, mercado3]
    valores = [valor1, valor2, valor3]
    odds = [odd1, odd2, odd3]
    apostas = [aposta1, aposta2, aposta3]
    print(mercados, odds, apostas, valores)
    return aposta1, aposta2, aposta3, odd1, odd2, odd3, mercado1, mercado2, mercado3, valor1, valor2, valor3, taxa1, taxa2, taxa3, arreds, bonus
mercados = ['TU', 'TO', 'TO']
valores = [45.0, 44.5, 45.5]
odds = [2.08, 1.95, 2.33]
apostas = [0, 5.92, 0]
tipo = 'padrao'
#tipo = 'inverso'
#tipo = '312'
time = 'padrao'
#time = 'oposto'
aposta1, aposta2, aposta3, odd1, odd2, odd3, mercado1, mercado2, mercado3, valor1, valor2, valor3, taxa1, taxa2, taxa3, arreds, bonus = gerar_dados(mercados, odds, apostas, valores)
resultado1 = calc_apostas(aposta1, aposta2, aposta3, odd1, odd2, odd3, mercado1, mercado2, mercado3, valor1, valor2, valor3, taxa1, taxa2, taxa3, arreds, bonus)
print(resultado1)
print('')
def resto():
    aposta1, aposta2, aposta3, odd1, odd2, odd3, mercado1, mercado2, mercado3, valor1, valor2, valor3, taxa1, taxa2, taxa3, arreds, bonus = gerar_dados(mercados, odds, apostas, valores, tipo='inverso')
    resultado2 = calc_apostas(aposta1, aposta2, aposta3, odd1, odd2, odd3, mercado1, mercado2, mercado3, valor1, valor2, valor3, taxa1, taxa2, taxa3, arreds, bonus)
    print(resultado2)
    check2 = [resultado2[2], resultado2[1], resultado2[0], resultado2[3], resultado2[6], resultado2[5], resultado2[4], resultado2[7], resultado2[8]]
    print(check2 == list(resultado1))
    print('')

    aposta1, aposta2, aposta3, odd1, odd2, odd3, mercado1, mercado2, mercado3, valor1, valor2, valor3, taxa1, taxa2, taxa3, arreds, bonus = gerar_dados(mercados, odds, apostas, valores, tipo='312')
    resultado3 = calc_apostas(aposta1, aposta2, aposta3, odd1, odd2, odd3, mercado1, mercado2, mercado3, valor1, valor2, valor3, taxa1, taxa2, taxa3, arreds, bonus)
    print(resultado3)
    check3 = [resultado3[1], resultado3[2], resultado3[0], resultado3[3], resultado3[5], resultado3[6], resultado3[4], resultado3[7], resultado3[8]]
    print(check3 == list(resultado1))
    print('')

    aposta1, aposta2, aposta3, odd1, odd2, odd3, mercado1, mercado2, mercado3, valor1, valor2, valor3, taxa1, taxa2, taxa3, arreds, bonus = gerar_dados(mercados, odds, apostas, valores, time='oposto')
    resultado4 = calc_apostas(aposta1, aposta2, aposta3, odd1, odd2, odd3, mercado1, mercado2, mercado3, valor1, valor2, valor3, taxa1, taxa2, taxa3, arreds, bonus)
    print(resultado4)
    print('')

    aposta1, aposta2, aposta3, odd1, odd2, odd3, mercado1, mercado2, mercado3, valor1, valor2, valor3, taxa1, taxa2, taxa3, arreds, bonus = gerar_dados(mercados, odds, apostas, valores, tipo='inverso', time='oposto')
    resultado5 = calc_apostas(aposta1, aposta2, aposta3, odd1, odd2, odd3, mercado1, mercado2, mercado3, valor1, valor2, valor3, taxa1, taxa2, taxa3, arreds, bonus)
    print(resultado5)
    check2 = [resultado5[2], resultado5[1], resultado5[0], resultado5[3], resultado5[6], resultado5[5], resultado5[4], resultado5[7], resultado5[8]]
    print(check2 == list(resultado4))
    print('')

    aposta1, aposta2, aposta3, odd1, odd2, odd3, mercado1, mercado2, mercado3, valor1, valor2, valor3, taxa1, taxa2, taxa3, arreds, bonus = gerar_dados(mercados, odds, apostas, valores, tipo='312', time='oposto')
    resultado6 = calc_apostas(aposta1, aposta2, aposta3, odd1, odd2, odd3, mercado1, mercado2, mercado3, valor1, valor2, valor3, taxa1, taxa2, taxa3, arreds, bonus)
    print(resultado6)
    check3 = [resultado6[1], resultado6[2], resultado6[0], resultado6[3], resultado6[5], resultado6[6], resultado6[4], resultado6[7], resultado6[8]]
    print(check3 == list(resultado4))
    print('')

#resto()