import math
def calc_apostas(aposta1, aposta2, aposta3, odd1, odd2, odd3, mercado1, mercado2, mercado3, valor1, valor2, valor3, bethouse_options1, bethouse_options2, bethouse_options3, arred_var, bonus):
    if aposta1 == '':
        aposta1 = 0
    if aposta2 == '':
        aposta2 = 0
    odd_1 = (odd1 - 1) * (1 - bethouse_options1) + 1
    odd_2 = (odd2 - 1) * (1 - bethouse_options2) + 1
    odd_3 = (odd3 - 1) * (1 - bethouse_options3) + 1
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

    if aposta1 + aposta2 + aposta3 == 0.0 or (odd2 == 0.0 and odd3 == 0.0):
        return
    if odd3 > 0.0:
        if aposta3 == '':
            aposta3 = 0
        mercados = [mercado1, mercado2, mercado3]
        valores = [valor1, valor2, valor3]

        # 2 resultados, modelo duas apostas contra 1
        if (mercado1 == mercado2 and valor1 == valor2) or (mercado1 == mercado3 and valor1 == valor3) or (
                mercado2 == mercado3 and valor2 == valor3):
            if mercado1 == mercado2 and valor1 == valor2:
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
                lucro2 = lucro1
                lucro3 = round((retorno3() - aposta1 - aposta2 - aposta3), 2)
                lucro_percent = round((((lucro1 + lucro3) / 2) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            elif mercado1 == mercado3 and valor1 == valor3:
                if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                    pass
                elif aposta1 > 0 and aposta2 > 0:
                    aposta3 = round(((retorno2() - retorno1()) / odd_3) / arred_var[2]) * arred_var[2]
                elif aposta1 > 0 and aposta3 > 0:
                    aposta2 = round(((retorno1() + retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
                elif aposta2 > 0 and aposta3 > 0:
                    aposta1 = round(((retorno2() - retorno3()) / odd_1) / arred_var[0]) * arred_var[0]
                elif aposta1 > 0:
                    aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
                    aposta2 = round(((retorno1() + retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
                elif aposta2 > 0:
                    aposta1 = round(((retorno2() / 2) / odd_1) / arred_var[0]) * arred_var[0]
                    aposta3 = round(((retorno2() / 2) / odd_3) / arred_var[2]) * arred_var[2]
                else:
                    aposta1 = round((retorno3() / odd_1) / arred_var[0]) * arred_var[0]
                    aposta2 = round(((retorno1() + retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
                lucro1 = round((retorno1() + retorno3() - aposta1 - aposta2 - aposta3), 2)
                lucro2 = round((retorno2() - aposta1 - aposta2 - aposta3), 2)
                lucro3 = lucro1
                lucro_percent = round((((lucro1 + lucro2) / 2) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            else:
                if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                    pass
                elif aposta1 > 0 and aposta2 > 0:
                    aposta3 = round(((retorno1() - retorno2()) / odd_3) / arred_var[2]) * arred_var[2]
                elif aposta1 > 0 and aposta3 > 0:
                    aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
                elif aposta2 > 0 and aposta3 > 0:
                    aposta1 = round(((retorno2() + retorno3()) / odd_1) / arred_var[0]) * arred_var[0]
                elif aposta1 > 0:
                    aposta2 = round(((retorno1() / 2) / odd_2) / arred_var[1]) * arred_var[1]
                    aposta3 = round(((retorno1() / 2) / odd_3) / arred_var[2]) * arred_var[2]
                elif aposta2 > 0:
                    aposta3 = round((retorno2() / odd_3) / arred_var[2]) * arred_var[2]
                    aposta1 = round(((retorno2() + retorno3()) / odd_1) / arred_var[0]) * arred_var[0]
                else:
                    aposta2 = round((retorno3() / odd_2) / arred_var[1]) * arred_var[1]
                    aposta1 = round(((retorno2() + retorno3()) / odd_1) / arred_var[0]) * arred_var[0]
                lucro1 = round((retorno1() - aposta1 - aposta2 - aposta3), 2)
                lucro2 = round((retorno2() + retorno3() - aposta1 - aposta2 - aposta3), 2)
                lucro3 = lucro2
                lucro_percent = round((((lucro1 + lucro2) / 2) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            return aposta1, aposta2, aposta3, None, lucro1, lucro2, lucro3, lucro_percent, None

        # Modelo: AH1(0.25), X2, 2
        # Modelo: TO(5.25), TU(4.5), TU(5.5)
        # Modelo: AH1(5.25), AH2(-4.5), AH2(-5.5)
        elif ((mercado2 == "1X" or mercado2 == "X2") and (mercado1.startswith('AH') and valor1 == 0.25 and (mercado3 == '1' or mercado3 == '2' or (mercado3.startswith('AH') and valor3 == -0.5))) or (mercado3.startswith('AH') and valor3 == 0.25 and (mercado1 == '1' or mercado1 == '2' or (mercado1.startswith('AH') and valor1 == -0.5)))) or\
                (all(mercado.startswith("T") for mercado in mercados) and ((str(valor1).endswith('.25') and str(valor2).endswith('.5') and str(valor3).endswith('.5')) or (str(valor3).endswith('.25') and str(valor1).endswith('.5') and str(valor2).endswith('.5')))) or\
                (all(mercado.startswith("AH") for mercado in mercados) and ((str(valor1).endswith('.25') and str(valor2).endswith('.5') and str(valor3).endswith('.5')) or (str(valor3).endswith('.25') and str(valor1).endswith('.5') and str(valor2).endswith('.5')))):
            aposta1_quarter = (mercado1.startswith('AH') and valor1 == 0.25 and (mercado3 == '1' or mercado3 == '2' or (mercado3.startswith('AH') and valor3 == -0.5))) or (str(valor1).endswith('.25') and str(valor2).endswith('.5') and str(valor3).endswith('.5'))
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                if aposta1_quarter:
                    aposta3 = round((retorno1_halfwin() / odd_3) / arred_var[2]) * arred_var[2]
                else:
                    aposta3 = round(((retorno1() + retorno2()) / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta1 > 0 and aposta3 > 0:
                if aposta1_quarter:
                    aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
                else:
                    aposta2 = round(((retorno3() - retorno1()) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0 and aposta3 > 0:
                if aposta1_quarter:
                    aposta1 = round(((retorno2() + retorno3()) / odd_1) / arred_var[0]) * arred_var[0]
                else:
                    aposta1 = round((retorno3_halfwin() / odd_1) / arred_var[0]) * arred_var[0]
            elif aposta1 > 0:
                if aposta1_quarter:
                    aposta3 = round((retorno1_halfwin() / odd_3) / arred_var[2]) * arred_var[2]
                    aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
                else:
                    aposta3 = round((retorno1() / (0.5 + odd_3 / 2)) / arred_var[2]) * arred_var[2]
                    aposta2 = round(((retorno3() - retorno1()) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0:
                if aposta1_quarter:
                    aposta3 = aposta2
                    aposta1 = 0
                    while retorno1() < retorno2() + retorno3():
                        aposta3 += 0.01
                        aposta1 = round((retorno3() / (0.5 + odd_1 / 2)) / arred_var[0]) * arred_var[0]
                else:
                    aposta1 = aposta2
                    aposta3 = 0
                    while retorno3() < retorno2() + retorno1():
                        aposta1 += 0.01
                        aposta3 = round((retorno1() / (0.5 + odd_3 / 2)) / arred_var[2]) * arred_var[2]
            elif aposta3 > 0:
                if aposta1_quarter:
                    aposta1 = round((retorno3() / (0.5 + odd1 / 2)) / arred_var[0]) * arred_var[0]
                    aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
                else:
                    aposta1 = round((retorno3_halfwin() / odd_1) / arred_var[0]) * arred_var[0]
                    aposta2 = round(((retorno3() - retorno1()) / odd_2) / arred_var[1]) * arred_var[1]

            if aposta1_quarter:
                lucro1 = round((retorno1() - aposta1 - aposta2 - aposta3), 2)
                lucro3 = round((retorno2() + retorno3() - aposta1 - aposta2 - aposta3), 2)
                lucro2 = round((retorno2() + retorno1_halfwin() - aposta1 - aposta2 - aposta3), 2)
            else:
                lucro1 = round((retorno2() + retorno1() - aposta1 - aposta2 - aposta3), 2)
                lucro3 = round((retorno3() - aposta1 - aposta2 - aposta3), 2)
                lucro2 = round((retorno2() + retorno3_halfwin() - aposta1 - aposta2 - aposta3), 2)
            lucro_percent = round((((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            return aposta1, aposta2, aposta3, None, lucro1, lucro2, lucro3, lucro_percent, None

        # Modelo: AH1(-0.25) X2 2
        # Modelo: TO(5.75) TU(5.5) TU(6.5)
        # Modelo: AH1(5.75) AH2(-5.5) AH2(-6.5)
        # Modelo: AH1(-5.25) AH2(5.5) AH3(4.5)
        elif ((mercado2 == "1X" or mercado2 == "X2") and (mercado1.startswith('AH') and valor1 == -0.25 and (mercado3 == '1' or mercado3 == '2' or (mercado3.startswith('AH') and valor3 == -0.5))) or (mercado3.startswith('AH') and valor3 == -0.25 and (mercado1 == '1' or mercado1 == '2' or (mercado1.startswith('AH') and valor1 == -0.5)))) or \
                (all(mercado.startswith("T") for mercado in mercados) and (str(valor1).endswith('.75') and str(valor2).endswith('.5') and str(valor3).endswith('.5')) or (str(valor3).endswith('.75') and str(valor1).endswith('.5') and str(valor2).endswith('.5'))) or \
                (all(mercado.startswith("AH") for mercado in mercados) and ((str(valor1).endswith('.75') or (str(valor1).endswith('.25') and str(valor1).startswith('-'))) and str(valor2).endswith('.5') and str(valor3).endswith('.5')) or ((str(valor3).endswith('.75') or (str(valor3).endswith('.25') and str(valor3).startswith('-'))) and str(valor1).endswith('.5') and str(valor2).endswith('.5'))):
            aposta1_quarter = (mercado1.startswith('AH') and valor1 == -0.25 and (mercado3 == '1' or mercado3 == '2' or (mercado3.startswith('AH') and valor3 == -0.5))) or (str(valor1).endswith('.75') and str(valor2).endswith('.5') and str(valor3).endswith('.5'))
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                if aposta1_quarter:
                    aposta3 = round(((retorno1() - retorno2()) / odd_3) / arred_var[2]) * arred_var[2]
                else:
                    aposta3 = round(((retorno1() + retorno2()) / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta1 > 0 and aposta3 > 0:
                if aposta1_quarter:
                    aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
                else:
                    aposta2 = round(((retorno3() - retorno1()) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0 and aposta3 > 0:
                if aposta1_quarter:
                    aposta1 = round(((retorno2() + retorno3()) / odd_1) / arred_var[0]) * arred_var[0]
                else:
                    aposta1 = round((retorno3() - retorno2() / odd_1) / arred_var[0]) * arred_var[0]
            elif aposta1 > 0:
                if aposta1_quarter:
                    aposta3 = round((retorno1_halfloss() / odd_3) / arred_var[2]) * arred_var[2]
                    aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
                else:
                    aposta3 = round((retorno1() * 2) / arred_var[2]) * arred_var[2]
                    aposta2 = round(((retorno3() - retorno1()) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0:
                if aposta1_quarter:
                    aposta1 = 0
                    aposta3 = 0
                    while retorno1() < retorno2() + retorno3():
                        aposta3 += 0.01
                        aposta1 = round((retorno3() * 2) / arred_var[0]) * arred_var[0]
                else:
                    aposta3 = 0
                    aposta1 = 0
                    while retorno3() < retorno2() + retorno1():
                        aposta1 += 0.01
                        aposta3 = round((retorno1() * 2) / arred_var[2]) * arred_var[2]
            elif aposta3 > 0:
                if aposta1_quarter:
                    aposta1 = round((retorno3() * 2) / arred_var[0]) * arred_var[0]
                    aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
                else:
                    aposta1 = round((retorno3_halfloss() / odd_1) / arred_var[0]) * arred_var[0]
                    aposta2 = round(((retorno3() - retorno1()) / odd_2) / arred_var[1]) * arred_var[1]
            if aposta1_quarter:
                lucro1 = round((retorno1() - aposta1 - aposta2 - aposta3), 2)
                lucro3 = round((retorno2() + retorno3() - aposta1 - aposta2 - aposta3), 2)
                lucro2 = round((retorno2() + retorno1_halfloss() - aposta1 - aposta2 - aposta3), 2)
            else:
                lucro1 = round((retorno2() + retorno1() - aposta1 - aposta2 - aposta3), 2)
                lucro3 = round((retorno3() - aposta1 - aposta2 - aposta3), 2)
                lucro2 = round((retorno2() + retorno3_halfloss() - aposta1 - aposta2 - aposta3), 2)
            lucro_percent = round((((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            return aposta1, aposta2, aposta3, None, lucro1, lucro2, lucro3, lucro_percent, None

        # Modelo: AH1(-0.25) X AH2(0)
        elif mercado2 == 'X' and (((mercado1.startswith('AH') and valor1 == -0.25) and ((mercado3.startswith('AH') and valor3 == 0) or mercado3.startswith('DNB'))) or ((mercado3.startswith('AH') and valor3 == -0.25) and ((mercado1.startswith('AH') and valor1 == 0) or mercado1.startswith('DNB')))):
            aposta1_quarter = (mercado1.startswith('AH') and valor1 == -0.25) and ((mercado3.startswith('AH') and valor3 == 0) or mercado3.startswith('DNB'))
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta1 > 0 and aposta3 > 0:
                if aposta1_quarter:
                    aposta2 = round(((retorno1() - aposta1 / 2 - aposta3) / odd_2) / arred_var[1]) * arred_var[1]
                else:
                    aposta2 = round(((retorno3() - aposta3 / 2 - aposta1) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0 and aposta3 > 0:
                aposta1 = round((retorno3() / odd_1) / arred_var[0]) * arred_var[0]
            elif aposta1 > 0:
                aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
                if aposta1_quarter:
                    aposta2 = round(((retorno1() - aposta1 / 2 - aposta3) / odd_2) / arred_var[1]) * arred_var[1]
                else:
                    aposta2 = round(((retorno3() - aposta3 / 2 - aposta1) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0:
                if aposta1_quarter:
                    aposta1 = round((retorno2() / (odd_1 - 0.5 - odd_1 / odd3)) / arred_var[0]) * arred_var[0]
                    aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
                else:
                    aposta3 = round((retorno2() / (odd_3 - 0.5 - odd_3 / odd1)) / arred_var[2]) * arred_var[2]
                    aposta1 = round((retorno3() / odd_1) / arred_var[0]) * arred_var[0]
            elif aposta3 > 0:
                aposta1 = round((retorno3() / odd_1) / arred_var[0]) * arred_var[0]
                if aposta1_quarter:
                    aposta2 = round(((retorno1() - aposta1 / 2 - aposta3) / odd_2) / arred_var[1]) * arred_var[1]
                else:
                    aposta2 = round(((retorno3() - aposta3 / 2 - aposta1) / odd_2) / arred_var[1]) * arred_var[1]
            lucro1 = round((retorno1() - aposta1 - aposta2 - aposta3), 2)
            lucro3 = round((retorno3() - aposta1 - aposta2 - aposta3), 2)
            if aposta1_quarter:
                lucro2 = round((retorno2() + retorno1_halfloss() - aposta1 - aposta2), 2)
            else:
                lucro2 = round((retorno2() + retorno3_halfloss() - aposta2 - aposta3), 2)
            lucro_percent = round((((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            return aposta1, aposta2, aposta3, None, lucro1, lucro2, lucro3, lucro_percent, None


        # Modelo: AH1(0.25) X 2
        elif mercado2 == "X" and (mercado1.startswith('AH') and valor1 == 0.25 and (mercado3 == '1' or mercado3 == '2' or (mercado3.startswith('AH') and valor3 == -0.5))) or (mercado3.startswith('AH') and valor3 == 0.25 and (mercado1 == '1' or mercado1 == '2' or (mercado1.startswith('AH') and valor1 == -0.5))):
            aposta1_quarter = (mercado1.startswith('AH') and valor1 == 0.25 and (mercado3 == '1' or mercado3 == '2' or (mercado3.startswith('AH') and valor3 == -0.5)))
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta1 > 0 and aposta3 > 0:
                if aposta1_quarter:
                    aposta2 = round(((retorno1() - retorno1_halfwin()) / odd_2) / arred_var[1]) * arred_var[1]
                else:
                    aposta2 = round(((retorno3() - retorno3_halfwin()) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0 and aposta3 > 0:
                aposta1 = round((retorno3() / odd_1) / arred_var[0]) * arred_var[0]
            elif aposta1 > 0:
                aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
                if aposta1_quarter:
                    aposta2 = round(((retorno1() - retorno1_halfwin()) / odd_2) / arred_var[1]) * arred_var[1]
                else:
                    aposta2 = round(((retorno3() - retorno3_halfwin()) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0:
                if aposta1_quarter:
                    aposta1 = retorno2() / odd_1
                    while retorno2() + retorno1_halfwin() > retorno1():
                        aposta1 += 0.01
                    aposta1 = round(aposta1 / arred_var[0]) * arred_var[0]
                    aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
                else:
                    aposta3 = retorno2() / odd_3
                    while retorno2() + retorno3_halfwin() > retorno3():
                        aposta3 += 0.01
                    aposta3 = round(aposta3 / arred_var[2]) * arred_var[2]
                    aposta1 = round((retorno3() / odd_1) / arred_var[0]) * arred_var[0]
            elif aposta3 > 0:
                aposta1 = retorno3() / odd_1
                if aposta1_quarter:
                    aposta2 = round(((retorno1() - retorno1_halfwin()) / odd_2) / arred_var[1]) * arred_var[1]
                else:
                    aposta2 = round(((retorno3() - retorno3_halfwin()) / odd_2) / arred_var[1]) * arred_var[1]
            lucro1 = round((retorno1() - aposta1 - aposta2 - aposta3), 2)
            lucro3 = round((retorno3() - aposta1 - aposta2 - aposta3), 2)
            if aposta1_quarter:
                lucro2 = round((retorno2() + retorno1_halfwin() - aposta1 - aposta2), 2)
            else:
                lucro2 = round((retorno2() + retorno3_halfwin() - aposta2 - aposta3), 2)
            lucro_percent = round((((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            return aposta1, aposta2, aposta3, None, lucro1, lucro2, lucro3, lucro_percent, None

        # Modelo AH1(-0.25) X 2
        elif mercado2 == "X" and (mercado1.startswith('AH') and valor1 == -0.25 and (mercado3 == '1' or mercado3 == '2' or (mercado3.startswith('AH') and valor3 == -0.5))) or (mercado3.startswith('AH') and valor3 == -0.25 and (mercado1 == '1' or mercado1 == '2' or (mercado1.startswith('AH') and valor1 == -0.5))):
            aposta1_quarter = (mercado1.startswith('AH') and valor1 == -0.25 and (mercado3 == '1' or mercado3 == '2' or (mercado3.startswith('AH') and valor3 == -0.5)))
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta1 > 0 and aposta3 > 0:
                if aposta1_quarter:
                    aposta2 = round(((retorno1() - retorno1_halfloss()) / odd_2) / arred_var[1]) * arred_var[1]
                else:
                    aposta2 = round(((retorno3() - retorno3_halfloss()) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0 and aposta3 > 0:
                aposta1 = round((retorno3() / odd_1) / arred_var[0]) * arred_var[0]
            elif aposta1 > 0:
                aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
                if aposta1_quarter:
                    aposta2 = round(((retorno1() - retorno1_halfloss()) / odd_2) / arred_var[1]) * arred_var[1]
                else:
                    aposta2 = round(((retorno3() - retorno3_halfloss()) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0:
                if aposta1_quarter:
                    aposta1 = retorno2() / odd_1
                    while retorno2() + retorno1_halfloss() > retorno1():
                        aposta1 += 0.01
                    aposta1 = round(aposta1 / arred_var[0]) * arred_var[0]
                    aposta3 = round((retorno1() / odd_3) / arred_var[2]) * arred_var[2]
                else:
                    aposta3 = retorno2() / odd_3
                    while retorno2() + retorno3_halfloss() > retorno3():
                        aposta3 += 0.01
                    aposta3 = round(aposta3 / arred_var[2]) * arred_var[2]
                    aposta1 = round((retorno3() / odd_1) / arred_var[0]) * arred_var[0]
            elif aposta3 > 0:
                aposta1 = retorno3() / odd_1
                if aposta1_quarter:
                    aposta2 = round(((retorno1() - retorno1_halfloss()) / odd_2) / arred_var[1]) * arred_var[1]
                else:
                    aposta2 = round(((retorno3() - retorno3_halfloss()) / odd_2) / arred_var[1]) * arred_var[1]
            lucro1 = round((retorno1() - aposta1 - aposta2 - aposta3), 2)
            lucro3 = round((retorno3() - aposta1 - aposta2 - aposta3), 2)
            if aposta1_quarter:
                lucro2 = round((retorno2() + retorno1_halfloss() - aposta1 - aposta2 - aposta3), 2)
            else:
                lucro2 = round((retorno2() + retorno3_halfloss() - aposta1 - aposta2 - aposta3), 2)
            lucro_percent = round((((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            return aposta1, aposta2, aposta3, None, lucro1, lucro2, lucro3, lucro_percent, None

        # Modelo: AH1(0) X 2
        # Modelo: AH1(5) EHX(5) EH2(-5)
        # Modelo: TO(5) Exactly(5) TU(4.5)
        if (mercado2 == "X" and ((mercado1.startswith("DNB") or (mercado1.startswith("AH") and valor1 == 0)) and (
                mercado3 == "2" or mercado3 == "1" or (mercado3.startswith("AH") and valor2 == -0.5)) or (
                                         mercado1 == "1" or mercado1 == "2" or (
                                         mercado1.startswith("AH") and valor1 == -0.5)) and (
                                         mercado3.startswith("DNB") or (mercado3.startswith("AH") and valor2 == 0)))) or \
                (mercado2 == "EHX" and (
                        (mercado1.startswith("AH") and valor1.is_integer()) and mercado3.startswith("EH")) or (
                         (mercado3.startswith("AH") and valor3.is_integer()) and mercado1.startswith("EH"))) or \
                (mercado2 == "Exactly" and ((mercado1.startswith("T") and mercado3.startswith("T") and (
                        valor1.is_integer() or valor3.is_integer())))):  #
            dnb1 = (mercado1.startswith("DNB") or (mercado1.startswith("AH") and valor1 == 0)) or (
                        (mercado1.startswith("AH") and valor1.is_integer()) and mercado3.startswith("EH")) or (
                               mercado1.startswith("T") and valor1.is_integer())
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                aposta3 = round(((aposta1 * odd_1) / odd_3) / arred_var[2]) * arred_var[2]
            elif aposta1 > 0 and aposta3 > 0:
                if dnb1:
                    aposta2 = round(((retorno3() - aposta1) / odd_2) / arred_var[1]) * arred_var[1]
                else:
                    aposta2 = round(((retorno1() - aposta3) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0 and aposta3 > 0:
                aposta1 = round(((aposta3 * odd_3) / odd_1) / arred_var[0]) * arred_var[0]
            elif aposta1 > 0.0:
                aposta3 = round(((aposta1 * odd_1) / odd_3) / arred_var[2]) * arred_var[2]
                if dnb1:
                    aposta2 = round(((retorno3() - aposta1) / odd_2) / arred_var[1]) * arred_var[1]
                else:
                    aposta2 = round(((retorno1() - aposta3) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta3 > 0.0:
                aposta1 = round(((aposta3 * odd_3) / odd_1) / arred_var[0]) * arred_var[0]
                if dnb1:
                    aposta2 = round(((retorno3() - aposta1) / odd_2) / arred_var[1]) * arred_var[1]
                else:
                    aposta2 = round(((retorno1() - aposta3) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0.0:
                if dnb1:
                    aposta3 = round(retorno2() / odd_3, 2)
                    while True:
                        aposta1 = round(retorno3() / odd_1, 2)
                        if aposta3 * odd_3 >= round((retorno2() + aposta1), 2):
                            aposta3 = round((aposta3) / arred_var[2]) * arred_var[2]
                            aposta1 = round(((odd_3 * aposta3) / odd_1) / arred_var[0]) * arred_var[0]
                            break
                        aposta3 += 0.01
                else:
                    aposta1 = round(retorno2() / odd_1, 2)
                    while True:
                        aposta3 = round(retorno1() / odd_3, 2)
                        if aposta1 * odd_1 >= round((retorno2() + aposta3), 2):
                            aposta1 = round(aposta1 / arred_var[0]) * arred_var[0]
                            aposta3 = round(((odd_1 * aposta1) / odd_3) / arred_var[2]) * arred_var[2]
                            break
                        aposta1 += 0.01
            lucro1 = round(aposta1 * odd_1 - aposta1 - aposta2 - aposta3, 2)
            if dnb1:
                lucro2 = round(aposta2 * odd_2 - aposta2 - aposta3, 2)
            else:
                lucro2 = round(aposta2 * odd_2 - aposta2 - aposta1, 2)
            lucro3 = round(aposta3 * odd3 - aposta1 - aposta2 - aposta3, 2)
            lucro_percent = round((((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3)) * 100, 2)
            return aposta1, aposta2, aposta3, None, lucro1, lucro2, lucro3, lucro_percent, None

        # Modelo: TO(5) TU(4.5) TU(5.5)
        # Modelo: AH1(5) AH2(-4.5) AH2(-5.5)
        # Modelo: AH1(0) X2 2
        elif (all(mercado.startswith("T") for mercado in mercados) and (sum(valor.is_integer() for valor in valores) == 1 and sum(str(valor).endswith('.5') for valor in valores) == 2)) or \
                (all(mercado.startswith("AH") for mercado in mercados) and (sum(valor.is_integer() for valor in valores) == 1 and sum(str(valor).endswith('.5') for valor in valores) == 2)) or \
                (mercado2 in ["1X", "X2"] or (mercado2.startswith("AH") and valor2 == 0.5) and ((mercado1 == "1" or (mercado1 == "AH1" and valor1 == -0.5)) and (mercado3 == "DNB2" or (mercado3 == "AH2" and valor1 == 0))) or ((mercado1 == "DNB2" or (mercado1 == "AH2" and valor1 == 0)) and (mercado3 == "1" or (mercado3 == "AH1" and valor1 == -0.5))) or ((mercado1 == "DNB1" or (mercado1 == "AH1" and valor1 == 0)) and (mercado3 == "2" or (mercado3 == "AH2" and valor1 == -0.5)))):
            if aposta1 > 0 and aposta2 > 0 and aposta3 > 0:
                pass
            elif aposta1 > 0 and aposta2 > 0:
                aposta3 = round((aposta1 / odd3) / arred_var[2]) * arred_var[2]
            elif aposta1 > 0 and aposta3 > 0:
                aposta2 = round(((retorno1() - retorno3()) / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0 and aposta3 > 0:
                aposta1 = round((aposta3 * odd_3) / arred_var[0]) * arred_var[0]
            elif aposta1 > 0.0:
                aposta3 = round((aposta1 / odd3) / arred_var[2]) * arred_var[2]
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

        # Modelo: 1 X 2
        # Modelo: TO(5.5) Exactly(5) TU(4.5)
        # Modelo AH1(5.5) EHX(5) AH2(-4.5)
        elif (mercado2 == "X" and ((mercado1 == "1" or (mercado1 == "AH1" and valor1 == -0.5)) and (mercado3 == "2" or (mercado3 == "AH2" and valor3 == -0.5)))) or ((mercado2 == "X") and ((mercado1 == "2" or (mercado1 == "AH2" and valor1 == -0.5)) and (mercado3 == "1" or (mercado3 == "AH1" and valor3 == -0.5)))) or \
                ((mercado2 == "Exactly") and (((mercado1 == "TU" and mercado3 == "TO") or (mercado1 == "TO" and mercado3 == "TU")))) or \
            ((mercado2.startswith('EHX')) and (((mercado1 == "TU" and mercado3 == "TO") or (mercado1 == "TO" and mercado3 == "TU")))):
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

        #Todos os outros resultados)
        else:
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
        return aposta1, aposta2, aposta3, None, lucro1, lucro2, lucro3, lucro_percent, None
    else:
        if mercado2 == "Lay":
            if mercado1 == "Lay":
                odd_1 = (odd1 / (odd1 - 1) - 1) * (1 - bethouse_options1) + 1
                odd_2 = (odd2 / (odd2 - 1) - 1) * (1 - bethouse_options2) + 1
                if aposta1 > 0 and aposta2 > 0:
                    pass
                elif aposta1 > 0.0:
                    aposta2 = round((retorno1() / odd_2) / arred_var[1]) * arred_var[1]
                elif aposta2 > 0.0:
                    aposta1 = round((retorno2() / odd_1) / arred_var[0]) * arred_var[0]
                liability = round((aposta1 * (odd1 / (odd1 - 1)) - aposta1), 2)
                liability2 = round((aposta2 * (odd2 / (odd2 - 1)) - aposta2), 2)
            else:
                odd_2 = (odd2 / (odd2 - 1) - 1) * (1 - bethouse_options2) + 1
                liability = None
                if aposta1 > 0 and aposta2 > 0:
                    pass
                elif aposta1 > 0.0:
                    aposta2 = round((retorno1() / odd_2) / arred_var[1]) * arred_var[1]
                elif aposta2 > 0.0:
                    aposta1 = round((retorno2() / odd_1) / arred_var[0]) * arred_var[0]
                liability2 = round((aposta2 * (odd2 / (odd2 - 1)) - aposta2), 2)
        elif mercado1 == "Lay":
            odd_1 = (odd1 / (odd1 - 1) - 1) * (1 - bethouse_options1) + 1
            liability2 = None
            if aposta1 > 0 and aposta2 > 0:
                pass
            elif aposta1 > 0.0:
                aposta2 = round((retorno1() / odd_2) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0.0:
                aposta1 = round((retorno2() / odd_1) / arred_var[0]) * arred_var[0]
            liability = round((aposta1 * (odd1 / (odd1 - 1)) - aposta1), 2)
        else:
            liability = None
            liability2 = None
            if aposta1 > 0.0 and aposta2 > 0.0:
                pass
            elif aposta1 > 0.0:
                aposta2 = round(((retorno1() - (aposta1 if bonus[0] else 0)) / (odd_2 - (1 if bonus[1] else 0))) / arred_var[1]) * arred_var[1]
            elif aposta2 > 0.0:
                aposta1 = round(((retorno2() - (aposta2 if bonus[1] else 0)) / (odd_1 - (1 if bonus[0] else 0))) / arred_var[0]) * arred_var[0]
        lucro1 = round((retorno1() - aposta1 - (aposta2 if not bonus[1] else 0)), 2)
        lucro2 = round((retorno2() - (aposta1 if not bonus[0] else 0) - aposta2), 2)
        lucro3 = 0
        lucro_percent = round((((lucro1 + lucro2) / 2) / (aposta1 + aposta2)) * 100, 2)
    return aposta1, aposta2, aposta3, liability, lucro1, lucro2, lucro3, lucro_percent, liability2