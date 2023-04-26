odd1 = 1.74
odd2 = 2.5
odd3 = 3.5
aposta1 = 34.26
bethouse_options1 = 0.0
bethouse_options2 = 0.0
arred_var = 0.01
mercado1 = "TO"
class GerenciadorDeJogo:
    def __init__(self, aposta1, aposta2, aposta3, odd1, odd2, odd3, mercado1, mercado2, bethouse_options1, bethouse_options2, bethouse_options3, arred_var):
        self.aposta1 = aposta1
        self.aposta2 = aposta2
        self.aposta3 = aposta3
        self.odd1 = odd1
        self.odd2 = odd2
        self.odd3 = odd3
        self.mercado1 = mercado1
        self.mercado2 = mercado2
        self.bethouse_options1 = bethouse_options1
        self.bethouse_options2 = bethouse_options2
        self.bethouse_options3 = bethouse_options3
        self.arred_var = arred_var

    def atualizar(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    #Para Calcular apostas
    def calc_apostas(self):
        if self.odd3 is not None and self.odd3 != "":
            if self.mercado1 == "TO" or self.mercado1 == "TU" or self.mercado1 == "AH1" or self.mercado1 == "AH2":
                odd_1 = ((self.odd1 - 1) * (1 - self.bethouse_options1)+1)
                odd_2 = ((self.odd2 - 1) * (1 - self.bethouse_options2)+1)
                odd_3 = ((self.odd3 - 1) * (1 - self.bethouse_options3)+1)
                if self.aposta1 != "" and self.aposta1 is not None:
                    self.aposta3 = round(self.aposta1 / self.odd3, 2)
                    self.aposta2 = round((odd_1 * self.aposta1 - odd_3 * self.aposta3) / odd_2, 2)
                elif self.aposta2 != "" and self.aposta2 is not None:
                    self.aposta3 = round(self.aposta2, 2)
                    while True:
                        if self.aposta3 * odd_3 + self.aposta2 * odd_2 >= self.aposta3 * odd_3 * odd_1:
                            self.aposta3 = round(self.aposta3, 2)
                            break
                        self.aposta3 -= 0.01
                    self.aposta1 = round(self.aposta3 * odd_3, 2)
                elif self.aposta3 != "" and self.aposta3 is not None:
                    self.aposta1 = round(self.aposta3 * odd_3, 2)
                    self.aposta2 = round((odd_1 * self.aposta1 - odd_3 * self.aposta3) / odd_2, 2)
                percent1 = self.aposta1 / (self.aposta1 + self.aposta2 + self.aposta3)
                percent2 = self.aposta2 / (self.aposta1 + self.aposta2 + self.aposta3)
                percent3 = self.aposta3 / (self.aposta1 + self.aposta2 + self.aposta3)
            else:
                percent1 = (((self.odd1 - 1) * (1 - self.bethouse_options1) + 1) + ((self.odd2 - 1) * (1 - self.bethouse_options2) + 1) + ((self.odd3 - 1) * (1 - self.bethouse_options3) + 1)) / ((self.odd1 - 1) * (1 - self.bethouse_options1) + 1) / ((((self.odd1 - 1) * (1 - self.bethouse_options1) + 1) + ((self.odd2 - 1) * (1 - self.bethouse_options2) + 1) + ((self.odd3 - 1) * (1 - self.bethouse_options3) + 1)) / ((self.odd1 - 1) * (1 - self.bethouse_options1) + 1) + (((self.odd1 - 1) * (1 - self.bethouse_options1) + 1) + ((self.odd2 - 1) * (1 - self.bethouse_options2) + 1) + ((self.odd3 - 1) * (1 - self.bethouse_options3) + 1)) / ((self.odd2 - 1) * (1 - self.bethouse_options2) + 1) + (((self.odd1 - 1) * (1 - self.bethouse_options1) + 1) + ((self.odd2 - 1) * (1 - self.bethouse_options2) + 1) + ((self.odd3 - 1) * (1 - self.bethouse_options3) + 1)) / ((self.odd3 - 1) * (1 - self.bethouse_options3) + 1))
                percent2 = (((self.odd1 - 1) * (1 - self.bethouse_options1) + 1) + ((self.odd2 - 1) * (1 - self.bethouse_options2) + 1) + ((self.odd3 - 1) * (1 - self.bethouse_options3) + 1)) / ((self.odd2 - 1) * (1 - self.bethouse_options2) + 1) / ((((self.odd1 - 1) * (1 - self.bethouse_options1) + 1) + ((self.odd2 - 1) * (1 - self.bethouse_options2) + 1) + ((self.odd3 - 1) * (1 - self.bethouse_options3) + 1)) / ((self.odd1 - 1) * (1 - self.bethouse_options1) + 1) + (((self.odd1 - 1) * (1 - self.bethouse_options1) + 1) + ((self.odd2 - 1) * (1 - self.bethouse_options2) + 1) + ((self.odd3 - 1) * (1 - self.bethouse_options3) + 1)) / ((self.odd2 - 1) * (1 - self.bethouse_options2) + 1) + (((self.odd1 - 1) * (1 - self.bethouse_options1) + 1) + ((self.odd2 - 1) * (1 - self.bethouse_options2) + 1) + ((self.odd3 - 1) * (1 - self.bethouse_options3) + 1)) / ((self.odd3 - 1) * (1 - self.bethouse_options3) + 1))
                percent3 = (((self.odd1 - 1) * (1 - self.bethouse_options1) + 1) + ((self.odd2 - 1) * (1 - self.bethouse_options2) + 1) + ((self.odd3 - 1) * (1 - self.bethouse_options3) + 1)) / ((self.odd3 - 1) * (1 - self.bethouse_options3) + 1) / ((((self.odd1 - 1) * (1 - self.bethouse_options1) + 1) + ((self.odd2 - 1) * (1 - self.bethouse_options2) + 1) + ((self.odd3 - 1) * (1 - self.bethouse_options3) + 1)) / ((self.odd1 - 1) * (1 - self.bethouse_options1) + 1) + (((self.odd1 - 1) * (1 - self.bethouse_options1) + 1) + ((self.odd2 - 1) * (1 - self.bethouse_options2) + 1) + ((self.odd3 - 1) * (1 - self.bethouse_options3) + 1)) / ((self.odd2 - 1) * (1 - self.bethouse_options2) + 1) + (((self.odd1 - 1) * (1 - self.bethouse_options1) + 1) + ((self.odd2 - 1) * (1 - self.bethouse_options2) + 1) + ((self.odd3 - 1) * (1 - self.bethouse_options3) + 1)) / ((self.odd3 - 1) * (1 - self.bethouse_options3) + 1))
        else:
            percent3 = 0
            if self.mercado2 == "Lay":
                if self.mercado1 == "Lay":
                    percent1 = ((self.odd2 / (self.odd2 - 1) - 1) * (1 - self.bethouse_options2) + 1) / (((self.odd2 / (self.odd2 - 1) - 1) * (1 - self.bethouse_options2) + 1) + ((self.odd1 / (self.odd1 - 1) - 1) * (1 - self.bethouse_options1)+1))
                    percent2 = ((self.odd1 / (self.odd1 - 1) - 1) * (1 - self.bethouse_options1) + 1) / (((self.odd1 / (self.odd1 - 1) - 1) * (1 - self.bethouse_options1) + 1) + ((self.odd2 / (self.odd2 - 1) - 1) * (1 - self.bethouse_options2)+1))
                else:
                    percent1 = ((self.odd2 / (self.odd2 - 1) - 1) * (1 - self.bethouse_options2) + 1) / (((self.odd1 - 1) * (1 - self.bethouse_options1) + 1) + ((self.odd2 / (self.odd2 - 1) - 1) * (1 - self.bethouse_options2) + 1))
                    percent2 = ((self.odd1 - 1) * (1 - self.bethouse_options1) + 1) / (((self.odd1 - 1) * (1 - self.bethouse_options1) + 1) + ((self.odd2 / (self.odd2 - 1) - 1) * (1 - self.bethouse_options2) + 1))
            elif self.mercado1 == "Lay":
                percent1 = ((self.odd2 - 1) * (1 - self.bethouse_options2) + 1) / (((self.odd2 - 1) * (1 - self.bethouse_options2) + 1) + ((self.odd1 / (self.odd1 - 1) - 1) * (1 - self.bethouse_options1) + 1))
                percent2 = ((self.odd1 / (self.odd1 - 1) - 1) * (1 - self.bethouse_options1) + 1) / (((self.odd2 - 1) * (1 - self.bethouse_options2) + 1) + ((self.odd1 / (self.odd1 - 1) - 1) * (1 - self.bethouse_options1) + 1))
            else:
                percent1 = ((self.odd2 - 1)*(1 - self.bethouse_options2) + 1) / (((self.odd2 - 1)*(1-self.bethouse_options2) + 1) + ((self.odd1 - 1) * (1 - self.bethouse_options1) + 1))
                percent2 = ((self.odd1 - 1)*(1 - self.bethouse_options1) + 1) / (((self.odd1 - 1)*(1-self.bethouse_options1) + 1) + ((self.odd2 - 1) * (1 - self.bethouse_options2) + 1))
        if self.aposta2 != 0 and self.aposta2 is not None:
            self.aposta1 = round(((self.aposta2 * percent1) / percent2) / self.arred_var) * self.arred_var
            self.aposta3 = round(((self.aposta2 * percent3) / percent2) / self.arred_var) * self.arred_var
        elif self.aposta1 != 0 and self.aposta1 is not None:
            self.aposta2 = round(((self.aposta1 * percent2) / percent1) / self.arred_var) * self.arred_var
            self.aposta3 = round(((self.aposta2 * percent3) / percent2) / self.arred_var) * self.arred_var
        elif self.aposta3 != 0 and self.aposta3 is not None:
            self.aposta1 = round(((self.aposta2 * percent1) / percent2) / self.arred_var) * self.arred_var
            self.aposta2 = round(((self.aposta1 * percent2) / percent1) / self.arred_var) * self.arred_var
        lucro1 = round(((self.aposta1 * self.odd1 - self.aposta1) * (1 - self.bethouse_options1) + self.aposta1) - self.aposta1 - self.aposta2 - self.aposta3, 2)
        lucro2 = round(((self.aposta2 * self.odd2 - self.aposta2) * (1 - self.bethouse_options2) + self.aposta2) - self.aposta1 - self.aposta2 - self.aposta3, 2)
        if self.mercado2 == "Lay":
            liability = round((self.aposta2 * (self.odd2 / (self.odd2 - 1)) - self.aposta2), 2)
        elif self.mercado1 == "Lay":
            liability = round((self.aposta1 * (self.odd1 / (self.odd1 - 1)) - self.aposta1), 2)
        else:
            liability = None
        if self.odd3 != "" and self.odd3 is not None:
            lucro3 = round(((self.aposta3 * self.odd3 - self.aposta3) * (1 - self.bethouse_options3) + self.aposta3) - self.aposta1 - self.aposta2 - self.aposta3, 2)
            lucro_percent = round(((lucro1 + lucro2 + lucro3) / 3) / (self.aposta1 + self.aposta2 + self.aposta3) * 100, 2)
        else: lucro3 = 0
        lucro_percent = round(((lucro1 + lucro2) / 2) / (self.aposta1 + self.aposta2) * 100, 2)
        return self.aposta1, self.aposta2, self.aposta3, liability, lucro1, lucro2, lucro3, lucro_percent
resultado = calc_apostas(aposta_var, aposta_var2, aposta_var3, odd_var, odd_var2, odd_var3, mercado_var, mercado_var2, bethouse_options[bethouse_var], bethouse_options[bethouse_var2], bethouse_options[bethouse_var3], self.arred_var)
print(resultado)