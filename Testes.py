aposta1 = 0
aposta2 = 31
aposta3 = 0
odd1 = 1.111111
odd2 = 10
odd3 = 0
mercado1 = '1'
mercado2 = '2'
mercado3 = ''
valor1 = 0
valor2 = ''
valor3 = ''
taxa1 = 0
taxa2 = 0
taxa3 = 0
arreds = [0.01, 0.01, 0.01]
bonus = [False, True, False]

def calc_apostas(aposta1, aposta2, aposta3, odd1, odd2, odd3, mercado1, mercado2, mercado3, valor1, valor2, valor3, bethouse_options1, bethouse_options2, bethouse_options3, arred_var, bonus):
    if aposta1 == '':
        aposta1 = 0
    if aposta2 == '':
        aposta2 = 0
    odd_1 = (odd1 - 1) * (1 - bethouse_options1) + 1
    odd_2 = (odd2 - 1) * (1 - bethouse_options2) + 1
    odd_3 = (odd3 - 1) * (1 - bethouse_options3) + 1
    tem_bonus = any(item is True for item in bonus)
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
    def if_bonus(num, neg=False, alt=None):
        if alt:
            if neg:
                if num == 1:
                    return alt if not bonus[0] else 0
                elif num == 2:
                    return alt if not bonus[1] else 0
                elif num == 3:
                    return alt if not bonus[2] else 0
                else:
                    return 0
            else:
                if num == 1:
                    return alt if bonus[0] else 0
                elif num == 2:
                    return alt if bonus[1] else 0
                elif num == 3:
                    return alt if bonus[2] else 0
                else:
                    return 0
        else:
            if neg:
                if num == 1:
                    return aposta1 if not bonus[0] else 0
                elif num == 2:
                    return aposta2 if not bonus[1] else 0
                elif num == 3:
                    return aposta3 if not bonus[2] else 0
                else:
                    return 0
            else:
                if num == 1:
                    return aposta1 if bonus[0] else 0
                elif num == 2:
                    return aposta2 if bonus[1] else 0
                elif num == 3:
                    return aposta3 if bonus[2] else 0
                else:
                    return 0
    if mercado2 == "Lay":
        if tem_bonus:
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
        else:
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
        if aposta1 > 0 and aposta2 > 0:
            pass
        if tem_bonus:
            if bonus[0]:
                if aposta1 > 0.0:
                    aposta2 = round(((retorno1() - aposta1) / odd_2) / arred_var[1]) * arred_var[1]
                else:
                    aposta1 = round((retorno2() / (odd_1 - 1)) / arred_var[0]) * arred_var[0]
                lucro1 = round((retorno1() - aposta1 - aposta2), 2)
                lucro2 = round((retorno2() - aposta2), 2)
            else:
                if aposta1 > 0.0:
                    aposta2 = round((retorno1() / (odd_2 - 1)) / arred_var[1]) * arred_var[1]
                else:
                    aposta1 = round((retorno2() - aposta2) / (odd_1) / arred_var[0]) * arred_var[0]
                lucro1 = round((retorno1() - aposta1), 2)
                lucro2 = round((retorno2() - aposta1 - aposta2), 2)
            lucro3 = 0
            lucro_percent = round((((lucro1 + lucro2) / 2) / (aposta1 + aposta2)) * 100, 2)
        else:
            liability = None
            liability2 = None
            if aposta1 > 0.0 and aposta2 > 0.0:
                pass
            elif aposta1 > 0.0:
                aposta2 = round(((retorno1() - if_bonus(1)) / (odd_2 - if_bonus(1, alt=1))) / arred_var[1]) * arred_var[
                    1]
            elif aposta2 > 0.0:
                aposta1 = round(((retorno2() - if_bonus(2)) / (odd_1 - if_bonus(2, alt=1))) / arred_var[0]) * arred_var[
                    0]
        lucro1 = round((retorno1() - aposta1 - if_bonus(2, neg=True)), 2)
        lucro2 = round((retorno2() - if_bonus(1, neg=True) - aposta2), 2)
        lucro3 = 0
        lucro_percent = round((((lucro1 + lucro2) / 2) / (aposta1 + aposta2)) * 100, 2)
    return aposta1, aposta2, aposta3, liability, lucro1, lucro2, lucro3, lucro_percent, liability2


resultado = calc_apostas(aposta1, aposta2, aposta3, odd1, odd2, odd3, mercado1,mercado2, mercado3, valor1, valor2, valor3, taxa1, taxa2, taxa3, arreds, bonus)
print(resultado)