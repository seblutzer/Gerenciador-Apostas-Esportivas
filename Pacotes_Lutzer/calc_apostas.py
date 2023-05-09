def calc_apostas(aposta1, aposta2, aposta3, odd1, odd2, odd3, mercado1, mercado2, mercado3, valor1, valor2, valor3, bethouse_options1, bethouse_options2, bethouse_options3, arred_var):
    odd_1 = ((odd1 - 1) * (1 - bethouse_options1) +1)
    odd_2 = ((odd2 - 1) * (1 - bethouse_options2) +1)
    odd_3 = ((odd3 - 1) * (1 - bethouse_options3) +1)
    retorno1 = odd_1 * aposta1
    retorno2 = odd_2 * aposta2
    retorno3 = odd_3 * aposta3
    retornos = [retorno1, retorno2, retorno3]
    if aposta1 + aposta2 + aposta3 == 0.0 or (odd2 == 0.0 and odd3 == 0.0):
        return
    if odd3 > 0.0:
        mercados = [mercado1, mercado2, mercado3]
        if (mercado2 == "X") and (
                (mercado1 == "DNB1" or (mercado1 == "AH1" and valor1 == 0)) and (
                mercado3 == "2" or (mercado3 == "AH2" and valor2 == -0.5))
                or (mercado1 == "DNB2" or (mercado1 == "AH2" and valor1 == 0)) and (
                        mercado3 == "2" or (mercado3 == "AH1" and valor2 == -0.5))
                or (mercado1 == "1" or (mercado1 == "AH1" and valor1 == -0.5)) and (
                        mercado3 == "DNB2" or (mercado3 == "AH2" and valor2 == 0))
                or (mercado1 == "2" or (mercado1 == "AH2" and valor1 == -0.5)) and (
                        mercado3 == "DNB1" or (mercado3 == "AH1" and valor2 == 0))):
            if aposta1 > 0.0:
                aposta3 = round((aposta1 * odd_1) / odd_3, 2)
                if mercado1 in ['DNB1', 'DNB2'] or (mercado1 == 'AH1' and valor1 == 0) or (
                        mercado1 == 'AH2' and valor1 == 0):
                    aposta2 = round((retorno3 - aposta1) / odd_2, 2)
                elif mercado3 in ['DNB1', 'DNB2'] or (mercado3 == 'AH1' and valor3 == 0) or (
                        mercado3 == 'AH2' and valor3 == 0):
                    aposta2 = round(((retorno1 - aposta3) / odd_2) / arred_var) * arred_var
            elif aposta3 > 0.0:
                aposta1 = round(((aposta3 * odd_3) / odd_1) / arred_var) * arred_var
                if mercado1 in ['DNB1', 'DNB2'] or (mercado1 == 'AH1' and valor1 == 0) or (mercado1 == 'AH2' and valor1 == 0):
                    aposta2 = round(((retorno3 - aposta1) / odd_2) / arred_var) * arred_var
                elif mercado3 in ['DNB1', 'DNB2'] or (mercado3 == 'AH1' and valor3 == 0) or (mercado3 == 'AH2' and valor3 == 0):
                    aposta2 = round(((retorno1 - aposta3) / odd_2) / arred_var) * arred_var
            elif aposta2 > 0.0:
                if mercado1 in ['DNB1', 'DNB2'] or (mercado1 == 'AH1' and valor1 == 0) or (mercado1 == 'AH2' and valor1 == 0):
                    aposta3 = round(retorno2 / odd3, 2)
                    while True:
                        aposta1 = round(retorno3 / odd_1, 2)
                        if aposta3 * odd_3 >= round((retorno2 + aposta1), 2):
                            aposta3 = round((aposta3) / arred_var) * arred_var
                            aposta1 = round(((odd_2 * aposta3) / odd_1) / arred_var) * arred_var
                            break
                        aposta3 += 0.01
                elif mercado3 in ['DNB1', 'DNB2'] or (mercado3 == 'AH1' and valor3 == 0) or (mercado3 == 'AH2' and valor3 == 0):
                    aposta1 = round(retorno2 / odd1, 2)
                    while True:
                        aposta3 = round(retorno1 / odd_3, 2)
                        if aposta1 * odd_1 >= round((retorno2 + aposta3), 2):
                            aposta1 = round(aposta1 / arred_var) * arred_var
                            aposta3 = round(((odd_2 * aposta1) / odd_3) / arred_var) * arred_var
                            break
                        aposta1 += 0.01
            lucro1 = round(aposta1 * odd_1 - aposta1 - aposta2 - aposta3, 2)
            if mercado1 in ['DNB1', 'DNB2'] or (mercado1 == 'AH1' and valor1 == 0) or (mercado1 == 'AH2' and valor1 == 0):
                lucro2 = round(aposta2 * odd_2 - aposta2 - aposta3, 2)
            elif mercado3 in ['DNB1', 'DNB2'] or (mercado3 == 'AH1' and valor3 == 0) or (mercado3 == 'AH2' and valor3 == 0):
                lucro2 = round(aposta2 * odd_2 - aposta2 - aposta1, 2)
            lucro3 = round(aposta3 * odd3 - aposta1 - aposta2 - aposta3, 2)
            lucro_percent = round((((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3)) * 100, 2)
        elif all(mercado in ["TO", "TU"] for mercado in mercados) or all(mercado in ["TO1", "TU1"] for mercado in mercados) or all (mercado in ["TO2", "TU2"] for mercado in mercados) or all(mercado in ["AH1", "AH2"] for mercado in mercados) or ((mercado2 == "1X" or (mercado2 == "AH1" and valor2 == 0.5)) or (mercado2 == "X2" or (mercado2 == "AH2" and valor2 == 0.5)) and ((mercado1 == "1" or (mercado1 == "AH1" and valor1 == -0.5)) and (mercado3 == "DNB2" or (mercado3 == "AH2" and valor1 == 0))) or ((mercado1 == "DNB2" or (mercado1 == "AH2" and valor1 == 0)) and (mercado3 == "1" or (mercado3 == "AH1" and valor1 == -0.5))) or ((mercado1 == "DNB1" or (mercado1 == "AH1" and valor1 == 0)) and (mercado3 == "2" or (mercado3 == "AH2" and valor1 == -0.5)))):
            if aposta1 > 0.0:
                aposta3 = round((aposta1 / odd3) / arred_var) * arred_var
                aposta2 = round(((retorno1 - retorno3) / odd_2) / arred_var) * arred_var
            elif aposta2 > 0.0:
                aposta3 = 0.0
                while True:
                    if aposta3 * odd_3 + aposta2 * odd_2 <= aposta3 * odd_3 * odd_1:
                        aposta3 = round(aposta3, 2)
                        break
                    aposta3 += 0.01
                aposta1 = round((aposta3 * odd_3) / arred_var) * arred_var
            elif aposta3 > 0.0:
                aposta1 = round((aposta3 * odd_3) / arred_var) * arred_var
                aposta2 = (retorno1 - retorno3) / odd_2
            lucro1 = round((retorno1 - aposta1 - aposta2 - aposta3), 2)
            lucro2 = round((retorno2 - aposta2 - aposta3), 2)
            lucro3 = round((retorno3 + retorno2 - aposta1 - aposta2 - aposta3), 2)
            lucro_percent = round((lucro1 + lucro2 + lucro3) / 3, 2)
        elif (mercado2 == "X" and ((mercado1 == "1" or mercado1 == "AH1") and valor1 == -0.5 and (mercado3 == "2" or mercado3 == "AH2") and valor3 == -0.5)) or ((mercado2 == "X") and ((mercado1 == "2" or mercado1 == "AH2") and valor1 == -0.5 and (mercado3 == "1" or mercado3 == "AH1") and valor3 == -0.5)) or ((mercado2 == "Exactly") and (((mercado1 == "TU" and mercado3 == "TO") or (mercado1 == "TO" and mercado3 == "TU")))):
            if aposta1 > 0.0:
                aposta2 = round(retorno1 / odd_2 / arred_var) * arred_var
                aposta3 = round(retorno1 / odd_3 / arred_var) * arred_var
            elif aposta2 > 0.0:
                aposta1 = round(retorno2 / odd_1 / arred_var) * arred_var
                aposta3 = round(retorno2 / odd_3 / arred_var) * arred_var
            elif aposta3 > 0.0:
                aposta1 = round(retorno3 / odd_1 / arred_var) * arred_var
                aposta2 = round(retorno3 / odd_2 / arred_var) * arred_var
            lucro1 = round ((retorno1 - aposta1 - aposta2 - aposta3), 2)
            lucro2 = round ((retorno2 - aposta1 - aposta2 - aposta3), 2)
            lucro3 = round ((retorno3 - aposta1 - aposta2 - aposta3), 2)
            lucro_percent = round((((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3)) * 100, 2)
        else:
            if aposta1 > 0.0:
                aposta2 = round(retorno1 / odd_2 / arred_var) * arred_var
                aposta3 = round(retorno1 / odd_3 / arred_var) * arred_var
            elif aposta2 > 0.0:
                aposta1 = round(retorno2 / odd_1 / arred_var) * arred_var
                aposta3 = round(retorno2 / odd_3 / arred_var) * arred_var
            elif aposta3 > 0.0:
                aposta1 = round(retorno3 / odd_1 / arred_var) * arred_var
                aposta2 = round(retorno3 / odd_2 / arred_var) * arred_var
            max_retorno = max(retornos)
#            seg_retorno = max([r for r in retornos if r != max_retorno])
#            min_retorno = min(retornos)
#            if max_retorno == retorno1:
#                retorno_odd = odd_1
#                retorno_aposta = max_retorno / odd_1
#            elif max_retorno == retorno2:
#                retorno_odd = odd_2
#                retorno_aposta = max_retorno / odd_2
#            else:
#                retorno_odd = odd_3
#                retorno_aposta = max_retorno / odd_3

            lucro1, lucro2, lucro3 = round((max_retorno - aposta1 - aposta2 - aposta3), 2)
            lucro_percent = round((lucro1 / (aposta1 + aposta2 + aposta3)) * 100, 2)
        return aposta1, aposta2, aposta3, None, lucro1, lucro2, lucro3, lucro_percent, None
    else:
        if mercado2 == "Lay":
            if mercado1 == "Lay":
                odd_1 = (odd1 / (odd1 - 1) - 1) * (1 - bethouse_options2) + 1
                odd_2 = (odd2 / (odd2 - 1) - 1) * (1 - bethouse_options2) + 1
                if aposta1 > 0.0:
                    aposta2 = round((retorno1 / odd_2) / arred_var) * arred_var
                    liability2 = round((aposta2 * (odd2 / (odd2 - 1)) - aposta2), 2)
                    liability = round((aposta1 * (odd1 / (odd1 - 1)) - aposta1), 2)
                elif aposta2 > 0.0:
                    aposta1 = round((retorno2 / odd_1) / arred_var) * arred_var
                    liability = round((aposta1 * (odd1 / (odd1 - 1)) - aposta1), 2)
                    liability2 = round((aposta2 * (odd2 / (odd2 - 1)) - aposta2), 2)
            else:
                odd_2 = (odd2 / (odd2 - 1) - 1) * (1 - bethouse_options2) + 1
                liability = None
                if aposta1 > 0.0:
                    aposta2 = round((retorno1 / odd_2) / arred_var) * arred_var
                    liability2 = round((aposta2 * (odd2 / (odd2 - 1)) - aposta2), 2)
                elif aposta2 > 0.0:
                    aposta1 = round((retorno2 / odd_1) / arred_var) * arred_var
                    liability2 = round((aposta2 * (odd2 / (odd2 - 1)) - aposta2), 2)
        elif mercado1 == "Lay":
            odd_1 = (odd1 / (odd1 - 1) - 1) * (1 - bethouse_options2) + 1
            liability2 = None
            if aposta1 > 0.0:
                aposta2 = round((retorno1 / odd_2) / arred_var) * arred_var
                liability = round((aposta1 * (odd1 / (odd1 - 1)) - aposta1), 2)
            elif aposta2 > 0.0:
                aposta1 = round((retorno2 / odd_1) / arred_var) * arred_var
                liability = round((aposta1 * (odd1 / (odd1 - 1)) - aposta1), 2)
        else:
            liability = None
            liability2 = None
        if aposta1 > 0.0:
            aposta2 = round((retorno1 / odd_2) / arred_var) * arred_var
        elif aposta2 > 0.0:
            aposta1 = round((retorno2 / odd_1) / arred_var) * arred_var
        lucro1 = round((retorno1 - aposta1 - aposta2) / arred_var) * arred_var
        lucro2 = round((retorno2 - aposta1 - aposta2) / arred_var) * arred_var
        lucro3 = 0
        lucro_percent = round((((lucro1 + lucro2) / 2) / (aposta1 + aposta2)) * 100, 2)
    return aposta1, aposta2, aposta3, liability, lucro1, lucro2, lucro3, lucro_percent, liability2