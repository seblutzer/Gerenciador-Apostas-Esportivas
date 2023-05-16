import math
def calc_apostas(aposta1, aposta2, aposta3, odd1, odd2, odd3, mercado1, mercado2, mercado3, valor1, valor2, valor3, bethouse_options1, bethouse_options2, bethouse_options3, arred_var):
    odd_1 = ((odd1 - 1) * (1 - bethouse_options1) +1)
    odd_2 = ((odd2 - 1) * (1 - bethouse_options2) +1)
    odd_3 = ((odd3 - 1) * (1 - bethouse_options3) +1)
    def retorno1():
        return odd_1 * aposta1
    def retorno2():
        return odd_2 * aposta2
    def retorno3():
        return odd_3 * aposta3
    retornos = [retorno1(), retorno2(), retorno3()]
    if aposta1 + aposta2 + aposta3 == 0.0 or (odd2 == 0.0 and odd3 == 0.0):
        return
    if odd3 > 0.0:
        mercados = [mercado1, mercado2, mercado3]
        valores = [valor1, valor2, valor3]
        if (mercado1 == mercado2 and valor1 == valor2) or (mercado1 == mercado3 and valor1 == valor3) or (mercado2 == mercado3 and valor2 == valor3):
            if mercado1 == mercado2 and valor1 == valor2:
                if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                    pass
                elif aposta1 > 0 and aposta2 > 0:
                    aposta3 = round(((retorno1() + retorno2()) / odd_3) / arred_var) * arred_var
                elif aposta1 > 0 and aposta3 > 0:
                    aposta2 = round(((retorno3() - retorno1()) / odd_2) / arred_var) * arred_var
                elif aposta2 > 0 and aposta3 > 0:
                    aposta1 = round(((retorno3() - retorno2()) / odd_1) / arred_var) * arred_var
                elif aposta1 > 0:
                    aposta2 = round((retorno1() / odd_2) / arred_var) * arred_var
                    aposta3 = round(((retorno1() + retorno2()) / odd_3) / arred_var) * arred_var
                elif aposta2 > 0:
                    aposta1 = round((retorno2() / odd_1) / arred_var) * arred_var
                    aposta3 = round(((retorno1() + retorno2()) / odd_3) / arred_var) * arred_var
                else:
                    aposta1 = round(((retorno3() / 2) / odd_1) / arred_var) * arred_var
                    aposta2 = round(((retorno3() / 2) / odd_2) / arred_var) * arred_var
                lucro1 = round((retorno1() + retorno2() - aposta1 - aposta2- aposta3), 2)
                lucro2 = lucro1
                lucro3 = round((retorno3() - aposta1 - aposta2 - aposta3), 2)
                lucro_percent = round((((lucro1 + lucro3) / 2) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            elif mercado1 == mercado3 and valor1 == valor3:
                if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                    pass
                elif aposta1 > 0 and aposta2 > 0:
                    aposta3 = round(((retorno2() - retorno1()) / odd_3) / arred_var) * arred_var
                elif aposta1 > 0 and aposta3 > 0:
                    aposta2 = round(((retorno1() + retorno3()) / odd_2) / arred_var) * arred_var
                elif aposta2 > 0 and aposta3 > 0:
                    aposta1 = round(((retorno2() - retorno3()) / odd_1) / arred_var) * arred_var
                elif aposta1 > 0:
                    aposta3 = round((retorno1() / odd_3) / arred_var) * arred_var
                    aposta2 = round(((retorno1() + retorno3()) / odd_2) / arred_var) * arred_var
                elif aposta2 > 0:
                    aposta1 = round(((retorno2() / 2) / odd_1) / arred_var) * arred_var
                    aposta3 = round(((retorno2() / 2) / odd_3) / arred_var) * arred_var
                else:
                    aposta1 = round((retorno3() / odd_1) / arred_var) * arred_var
                    aposta2 = round(((retorno1() + retorno3()) / odd_2) / arred_var) * arred_var
                lucro1 = round((retorno1() + retorno3() - aposta1 - aposta2 - aposta3), 2)
                lucro2 = round((retorno2() - aposta1 - aposta2 - aposta3), 2)
                lucro3 = lucro1
                lucro_percent = round((((lucro1 + lucro2) / 2) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            else:
                if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                    pass
                elif aposta1 > 0 and aposta2 > 0:
                    aposta3 = round(((retorno1() - retorno2()) / odd_3) / arred_var) * arred_var
                elif aposta1 > 0 and aposta3 > 0:
                    aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var) * arred_var
                elif aposta2 > 0 and aposta3 > 0:
                    aposta1 = round(((retorno2() + retorno3()) / odd_1) / arred_var) * arred_var
                elif aposta1 > 0:
                    aposta2 = round(((retorno1() / 2) / odd_2) / arred_var) * arred_var
                    aposta3 = round(((retorno1() / 2) / odd_3) / arred_var) * arred_var
                elif aposta2 > 0:
                    aposta3 = round((retorno2() / odd_3) / arred_var) * arred_var
                    aposta1 = round(((retorno2() + retorno3()) / odd_1) / arred_var) * arred_var
                else:
                    aposta2 = round((retorno3() / odd_2) / arred_var) * arred_var
                    aposta1 = round(((retorno2() + retorno3()) / odd_1) / arred_var) * arred_var
                lucro1 = round((retorno1() - aposta1 - aposta2 - aposta3), 2)
                lucro2 = round((retorno2() + retorno3() - aposta1 - aposta2 - aposta3), 2)
                lucro3 = lucro2
                lucro_percent = round((((lucro1 + lucro2) / 2) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            return aposta1, aposta2, aposta3, None, lucro1, lucro2, lucro3, lucro_percent, None
        elif (mercado2 == "X" and ((mercado1.startswith("DNB") or (mercado1.startswith("AH") and valor1 == 0)) and (mercado3 == "2" or mercado3 == "1" or (mercado3.startswith("AH") and valor2 == -0.5)) or (mercado1 == "1" or mercado1 == "2" or (mercado1.startswith("AH") and valor1 == -0.5)) and (mercado3.startswith("DNB") or (mercado3.startswith("AH") and valor2 == 0)))) or \
                (mercado2 == "EHX" and ((mercado1.startswith("AH") and valor1.is_integer()) and mercado3.startswith("EH")) or ((mercado3.startswith("AH") and valor3.is_integer()) and mercado1.startswith("EH"))) or \
                (mercado2 == "Exactly" and ((mercado1.startswith("T") and mercado3.startswith("T") and (valor1.is_integer() or valor3.is_integer())))): #
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                aposta3 = round((aposta1 * odd_1) / odd_3, 2)
            elif aposta1 > 0 and aposta3 > 0:
                if mercado1.startswith("DNB") or (mercado1.startswith("AH") and (valor1 == 0 or valor1.is_integer)) or (mercado1.startswith("T") and valor1.is_integer()):
                    aposta2 = round((retorno3() - aposta1) / odd_2, 2)
                elif mercado3.startswith("DNB") or (mercado3.startswith("AH") and (valor3 == 0 or valor3.is_integer)) or (mercado3.startswith("T") and valor3.is_integer()):
                    aposta2 = round(((retorno1() - aposta3) / odd_2) / arred_var) * arred_var
            elif aposta2 > 0 and aposta3 > 0:
                aposta1 = round(((aposta3 * odd_3) / odd_1) / arred_var) * arred_var
            elif aposta1 > 0.0:
                aposta3 = round((aposta1 * odd_1) / odd_3, 2)
                if mercado1.startswith("DNB") or (mercado1.startswith("AH") and (valor1 == 0 or valor1.is_integer)) or (mercado1.startswith("T") and valor1.is_integer()):
                    aposta2 = round((retorno3() - aposta1) / odd_2, 2)
                elif mercado3.startswith("DNB") or (mercado3.startswith("AH") and (valor3 == 0 or valor3.is_integer)) or (mercado3.startswith("T") and valor3.is_integer()):
                    aposta2 = round(((retorno1() - aposta3) / odd_2) / arred_var) * arred_var
            elif aposta3 > 0.0:
                aposta1 = round(((aposta3 * odd_3) / odd_1) / arred_var) * arred_var
                if mercado1.startswith("DNB") or (mercado1.startswith("AH") and (valor1 == 0 or valor1.is_integer)) or (mercado1.startswith("T") and valor1.is_integer()):
                    aposta2 = round(((retorno3() - aposta1) / odd_2) / arred_var) * arred_var
                elif mercado3.startswith("DNB") or (mercado3.startswith("AH") and (valor3 == 0 or valor3.is_integer)) or (mercado3.startswith("T") and valor3.is_integer()):
                    aposta2 = round(((retorno1() - aposta3) / odd_2) / arred_var) * arred_var
            elif aposta2 > 0.0:
                if mercado1.startswith("DNB") or (mercado1.startswith("AH") and (valor1 == 0 or valor1.is_integer)) or (mercado1.startswith("T") and valor1.is_integer()):
                    aposta3 = round(retorno2() / odd3, 2)
                    while True:
                        aposta1 = round(retorno3() / odd_1, 2)
                        if aposta3 * odd_3 >= round((retorno2() + aposta1), 2):
                            aposta3 = round((aposta3) / arred_var) * arred_var
                            aposta1 = round(((odd_2 * aposta3) / odd_1) / arred_var) * arred_var
                            break
                        aposta3 += 0.01
                elif mercado3.startswith("DNB") or (mercado3.startswith("AH") and (valor3 == 0 or valor3.is_integer)) or (mercado3.startswith("T") and valor3.is_integer()):
                    aposta1 = round(retorno2() / odd1, 2)
                    while True:
                        aposta3 = round(retorno1() / odd_3, 2)
                        if aposta1 * odd_1 >= round((retorno2() + aposta3), 2):
                            aposta1 = round(aposta1 / arred_var) * arred_var
                            aposta3 = round(((odd_2 * aposta1) / odd_3) / arred_var) * arred_var
                            break
                        aposta1 += 0.01
            lucro1 = round(aposta1 * odd_1 - aposta1 - aposta2 - aposta3, 2)
            if mercado1.startswith("DNB") or (mercado1.startswith("AH") and (valor1 == 0 or valor1.is_integer)) or (mercado1.startswith("T") and valor1.is_integer()):
                lucro2 = round(aposta2 * odd_2 - aposta2 - aposta3, 2)
            elif mercado3.startswith("DNB") or (mercado3.startswith("AH") and (valor3 == 0 or valor3.is_integer)) or (mercado3.startswith("T") and valor3.is_integer()):
                lucro2 = round(aposta2 * odd_2 - aposta2 - aposta1, 2)
            lucro3 = round(aposta3 * odd3 - aposta1 - aposta2 - aposta3, 2)
            lucro_percent = round((((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3)) * 100, 2)
        elif (all(mercado.startswith("T") for mercado in mercados) and (sum(valor.is_integer() for valor in valores) == 1 and sum(str(valor).endswith('.5') for valor in valores) == 2)) or \
                (all(mercado.startswith("AH") for mercado in mercados) and (sum(valor.is_integer() for valor in valores) == 1 and sum(str(valor).endswith('.5') for valor in valores) == 2)) or \
                (mercado2 in ["1X", "X2"] or (mercado2.startswith("AH") and valor2 == 0.5) and ((mercado1 == "1" or (mercado1 == "AH1" and valor1 == -0.5)) and (mercado3 == "DNB2" or (mercado3 == "AH2" and valor1 == 0))) or ((mercado1 == "DNB2" or (mercado1 == "AH2" and valor1 == 0)) and (mercado3 == "1" or (mercado3 == "AH1" and valor1 == -0.5))) or ((mercado1 == "DNB1" or (mercado1 == "AH1" and valor1 == 0)) and (mercado3 == "2" or (mercado3 == "AH2" and valor1 == -0.5)))):
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                aposta3 = round((aposta1 / odd3) / arred_var) * arred_var
            elif aposta1 > 0 and aposta3 > 0:
                aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var) * arred_var
            elif aposta2 > 0 and aposta3 > 0:
                aposta1 = round((aposta3 * odd_3) / arred_var) * arred_var
            elif aposta1 > 0.0:
                aposta3 = round((aposta1 / odd3) / arred_var) * arred_var
                aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var) * arred_var
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
                aposta2 = (retorno1() - retorno3()) / odd_2
            lucro1 = round((retorno1() - aposta1 - aposta2 - aposta3), 2)
            lucro2 = round((retorno2() - aposta2 - aposta3), 2)
            lucro3 = round((retorno3() + retorno2() - aposta1 - aposta2 - aposta3), 2)
            lucro_percent = round((lucro1 + lucro2 + lucro3) / 3, 2)
        elif (mercado2 == "X" and ((mercado1 == "1" or mercado1 == "AH1") and valor1 == -0.5 and (mercado3 == "2" or mercado3 == "AH2") and valor3 == -0.5)) or ((mercado2 == "X") and ((mercado1 == "2" or mercado1 == "AH2") and valor1 == -0.5 and (mercado3 == "1" or mercado3 == "AH1") and valor3 == -0.5)) or ((mercado2 == "Exactly") and (((mercado1 == "TU" and mercado3 == "TO") or (mercado1 == "TO" and mercado3 == "TU")))):
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                aposta3 = round(retorno1() / odd_3 / arred_var) * arred_var
            elif aposta1 > 0 and aposta3 > 0:
                aposta2 = round(retorno1() / odd_2 / arred_var) * arred_var
            elif aposta2 > 0 and aposta3 > 0:
                aposta1 = round(retorno3() / odd_1 / arred_var) * arred_var
            elif aposta1 > 0.0:
                aposta2 = round(retorno1() / odd_2 / arred_var) * arred_var
                aposta3 = round(retorno1() / odd_3 / arred_var) * arred_var
            elif aposta2 > 0.0:
                aposta1 = round(retorno2() / odd_1 / arred_var) * arred_var
                aposta3 = round(retorno2() / odd_3 / arred_var) * arred_var
            elif aposta3 > 0.0:
                aposta1 = round(retorno3() / odd_1 / arred_var) * arred_var
                aposta2 = round(retorno3() / odd_2 / arred_var) * arred_var
            lucro1 = round ((retorno1() - aposta1 - aposta2 - aposta3), 2)
            lucro2 = round ((retorno2() - aposta1 - aposta2 - aposta3), 2)
            lucro3 = round ((retorno3() - aposta1 - aposta2 - aposta3), 2)
            lucro_percent = round((((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3)) * 100, 2)
        else:
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                aposta3 = round((((retorno1() + retorno2()) / 2) / odd_3) / arred_var) * arred_var
            elif aposta1 > 0 and aposta3 > 0:
                aposta2 = round((((retorno1() + retorno3()) / 2) / odd_2) / arred_var) * arred_var
            elif aposta2 > 0 and aposta3 > 0:
                aposta1 = round((((retorno2() + retorno3()) / 2) / odd_1) / arred_var) * arred_var
            elif aposta1 > 0.0:
                aposta2 = round(retorno1() / odd_2 / arred_var) * arred_var
                aposta3 = round(retorno1() / odd_3 / arred_var) * arred_var
            elif aposta2 > 0.0:
                aposta1 = round(retorno2() / odd_1 / arred_var) * arred_var
                aposta3 = round(retorno2() / odd_3 / arred_var) * arred_var
            elif aposta3 > 0.0:
                aposta1 = round(retorno3() / odd_1 / arred_var) * arred_var
                aposta2 = round(retorno3() / odd_2 / arred_var) * arred_var
            max_retorno = max(retornos)
            lucro1 = round((max_retorno - aposta1 - aposta2 - aposta3), 2)
            lucro2 = lucro1
            lucro3 = lucro1
            lucro_percent = round((lucro1 / (aposta1 + aposta2 + aposta3)) * 100, 2)
        return aposta1, aposta2, aposta3, None, lucro1, lucro2, lucro3, lucro_percent, None
    else:
        if mercado2 == "Lay":
            if mercado1 == "Lay":
                odd_1 = (odd1 / (odd1 - 1) - 1) * (1 - bethouse_options2) + 1
                odd_2 = (odd2 / (odd2 - 1) - 1) * (1 - bethouse_options2) + 1
                if aposta1 > 0 and aposta2 > 0:
                    pass
                elif aposta1 > 0.0:
                    aposta2 = round((retorno1() / odd_2) / arred_var) * arred_var
                elif aposta2 > 0.0:
                    aposta1 = round((retorno2() / odd_1) / arred_var) * arred_var
                liability = round((aposta1 * (odd1 / (odd1 - 1)) - aposta1), 2)
                liability2 = round((aposta2 * (odd2 / (odd2 - 1)) - aposta2), 2)
            else:
                odd_2 = (odd2 / (odd2 - 1) - 1) * (1 - bethouse_options2) + 1
                liability = None
                if aposta1 > 0 and aposta2 > 0:
                    pass
                elif aposta1 > 0.0:
                    aposta2 = round((retorno1() / odd_2) / arred_var) * arred_var
                elif aposta2 > 0.0:
                    aposta1 = round((retorno2() / odd_1) / arred_var) * arred_var
                liability2 = round((aposta2 * (odd2 / (odd2 - 1)) - aposta2), 2)
        elif mercado1 == "Lay":
            odd_1 = (odd1 / (odd1 - 1) - 1) * (1 - bethouse_options2) + 1
            liability2 = None
            if aposta1 > 0 and aposta2 > 0:
                pass
            elif aposta1 > 0.0:
                aposta2 = round((retorno1() / odd_2) / arred_var) * arred_var
            elif aposta2 > 0.0:
                aposta1 = round((retorno2() / odd_1) / arred_var) * arred_var
            liability = round((aposta1 * (odd1 / (odd1 - 1)) - aposta1), 2)
        else:
            liability = None
            liability2 = None
            if aposta1 > 0 and aposta2 > 0:
                pass
            elif aposta1 > 0.0:
                aposta2 = round((retorno1() / odd_2) / arred_var) * arred_var
            elif aposta2 > 0.0:
                aposta1 = round((retorno2() / odd_1) / arred_var) * arred_var
        lucro1 = round((retorno1() - aposta1 - aposta2), 2)
        lucro2 = round((retorno2() - aposta1 - aposta2), 2)
        lucro3 = 0
        lucro_percent = round((((lucro1 + lucro2) / 2) / (aposta1 + aposta2)) * 100, 2)
    return aposta1, aposta2, aposta3, liability, lucro1, lucro2, lucro3, lucro_percent, liability2