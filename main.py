import tkinter as tk
from tkinter import ttk
import datetime

# cria uma janela
janela = tk.Tk()

# Cria o frame
frame = tk.Frame(janela, padx=10, pady=10)
frame.grid(row=0, column=0)

# Botão Arredondamento
arred_label = tk.Label(frame, text="Arredondamento")
arred_label.grid(row=2, column=0)
arred_options = [0.01, 0.05, 0.1, 0.5, 1]
arred_var = tk.DoubleVar(value=arred_options[0])
arred_combobox = ttk.Combobox(frame, textvariable=arred_var, values=arred_options, width=3, state="readonly")
arred_combobox.grid(row=2, column=3, padx=5, pady=5, sticky=tk.W)

# Adiciona campo Jogo
jogo_label = tk.Label(frame, text="Jogo")
jogo_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
jogo_entry = tk.Entry(frame)
jogo_entry.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

# Adiciona campo Data
def validate_day(text):
    if text.isdigit() or text == "":
        if len(text) > 2:
            return False
        if text == "":
            return True
        if int(text) < 1 or int(text) > 31:
            return False
    else:
        return False
    return True

def validate_hour(text):
    if text.isdigit() or text == "":
        if len(text) > 2:
            return False
        if text == "":
            return True
        if int(text) < 0 or int(text) > 23:
            return False
    else:
        return False
    return True

def validate_minute(text):
    if text.isdigit() or text == "":
        if len(text) > 2:
            return False
        if text == "":
            return True
        if int(text) < 0 or int(text) > 59:
            return False
    else:
        return False
    return True

data_label = tk.Label(frame, text="Data")
data_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

# Configurar o box dia
dia_entry = tk.Entry(frame, width=2, validate="key", validatecommand=(frame.register(validate_day), "%P"))
dia_atual = datetime.date.today().day
dia_entry.insert(0, dia_atual)
dia_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

barra_label1 = tk.Label(frame, text="/")
barra_label1.grid(row=1, column=2)

# Configurar o box mês
mes_options = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
# Obtenha o mês atual
mes_atual = datetime.datetime.now().strftime('%b')

def validate_month(text):
    if text in mes_options:
        return True
    else:
        return False

def update_combobox(event):
    current_input = mes_combobox.get()
    matching_options = [opt for opt in mes_options if opt.startswith(current_input)]
    if len(matching_options) > 0:
        new_option = matching_options[0]
        mes_combobox.set(new_option)
        mes_combobox.icursor(len(current_input))
    else:
        mes_combobox.set("")
        mes_combobox.icursor(0)

mes_atual_pt = {'Jan': 'Jan', 'Feb': 'Fev', 'Mar': 'Mar', 'Apr': 'Abr', 'May': 'Mai', 'Jun': 'Jun', 'Jul': 'Jul', 'Aug': 'Ago', 'Sep': 'Set', 'Oct': 'Out', 'Nov': 'Nov', 'Dec': 'Dez'}[mes_atual]
mes_combobox = ttk.Combobox(frame, values=mes_options, width=3, validate="key", validatecommand=(frame.register(validate_month), "%P"))
if mes_atual_pt in mes_options:
    mes_combobox.current(mes_options.index(mes_atual_pt))
else:
    mes_combobox.set(mes_options[0])
mes_combobox.bind("<KeyRelease>", update_combobox)
mes_combobox.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)

as_label1 = tk.Label(frame, text="as")
as_label1.grid(row=1, column=4)

# Configurar o box Hora
hora_label = tk.Label(frame, text="Hora")
hora_label.grid(row=0, column=5)
hora_entry = tk.Entry(frame, width=2, validate="key", validatecommand=(frame.register(validate_hour), "%P"))
hora_entry.grid(row=1, column=5, padx=5, pady=5, sticky=tk.W)

doispontos_label = tk.Label(frame, text=":")
doispontos_label.grid(row=1, column=6)

# Configurar o box minuto
minuto_entry = tk.Entry(frame, width=2, validate="key", validatecommand=(frame.register(validate_minute), "%P"), justify="right")
minuto_entry.insert(0, "00")
minuto_entry.grid(row=1, column=7, padx=5, pady=5, sticky=tk.W)

# Adiciona campo BetHouse
bethouse_label = tk.Label(frame, text="BetHouse")
bethouse_label.grid(row=0, column=9)
bethouse_options = {"Bet365": 0, "BetFair": 0, "BetFairEx": 0.065, "BetWay": 0, "FavBet": 0, "Pinnacle": 0, "VBet": 0}
def validate_bethouse(text):
    return text in bethouse_options.keys() or not text
def update_bethouse_combobox(event):
    current_input = bethouse_var.get()
    matching_options = [opt for opt in bethouse_options.keys() if opt.lower().startswith(current_input.lower())]
    bethouse_combobox['values'] = matching_options
    if len(matching_options) == 1:
        bethouse_var.set(matching_options[0])
        bethouse_combobox.icursor(tk.END)
def update_bethouse_combobox2(event):
    current_input = bethouse_var2.get()
    matching_options = [opt for opt in bethouse_options.keys() if opt.lower().startswith(current_input.lower())]
    bethouse_combobox2['values'] = matching_options
    if len(matching_options) == 1:
        bethouse_var2.set(matching_options[0])
        bethouse_combobox2.icursor(tk.END)
def update_bethouse_combobox3(event):
    current_input = bethouse_var3.get()
    matching_options = [opt for opt in bethouse_options.keys() if opt.lower().startswith(current_input.lower())]
    bethouse_combobox3['values'] = matching_options
    if len(matching_options) == 1:
        bethouse_var3.set(matching_options[0])
        bethouse_combobox3.icursor(tk.END)
bethouse_var = tk.StringVar(value=None)
bethouse_combobox = ttk.Combobox(frame, textvariable=bethouse_var, values=list(bethouse_options.keys()), width=7)
bethouse_combobox.bind("<KeyRelease>", update_bethouse_combobox)
bethouse_combobox.grid(row=1, column=9, padx=5, pady=5, sticky=tk.W)

bethouse_var2 = tk.StringVar(value=None)
bethouse_combobox2 = ttk.Combobox(frame, textvariable=bethouse_var2, values=list(bethouse_options.keys()), width=7)
bethouse_combobox2.bind("<KeyRelease>", update_bethouse_combobox2)
bethouse_combobox2.grid(row=2, column=9, padx=5, pady=5, sticky=tk.W)

bethouse_var3 = tk.StringVar(value=None)
# cria o botão de alternância
num_bets = 2
def alternar_bets():
    global num_bets
    if num_bets == 2:
        num_bets = 3
    else:
        num_bets = 2
    if num_bets == 3:
        bethouse_combobox3.grid()
        mercado_combobox3.grid()
        valor_entry3.grid()
        odd_entry3.grid()
        real_label3.grid()
        aposta_entry3.grid()
        palpite3_label.grid()
        lucro3_label.grid()
    else:
        bethouse_combobox3.grid_remove()
        mercado_combobox3.grid_remove()
        valor_entry3.grid_remove()
        odd_entry3.grid_remove()
        real_label3.grid_remove()
        aposta_entry3.grid_remove()
        palpite3_label.grid_remove()
        lucro3_label.grid_remove()
alternar_bets_btn = tk.Button(frame, text="Triplo", command=alternar_bets)
alternar_bets_btn.grid(row=3, column=5, columnspan=4)
if num_bets == 3:
    bethouse_combobox3 = ttk.Combobox(frame, textvariable=bethouse_var3, values=list(bethouse_options.keys()), width=7)
    bethouse_combobox3.bind("<KeyRelease>", update_bethouse_combobox3)
    bethouse_combobox3.grid(row=3, column=9, padx=5, pady=5, sticky=tk.W)
else:
    bethouse_combobox3 = ttk.Combobox(frame, textvariable=bethouse_var3, values=list(bethouse_options.keys()), width=7)
    bethouse_combobox3.bind("<KeyRelease>", update_bethouse_combobox3)
    bethouse_combobox3.grid(row=3, column=9, padx=5, pady=5, sticky=tk.W)
    bethouse_combobox3.grid_remove()

# Adiciona campo Mercado
mercado_label = tk.Label(frame, text="Mercado")
mercado_label.grid(row=0, column=10)
mercado_options = ["1", "12", "1X", "X", "X2", "2", "AH1", "AH2", "ClearSheet1", "ClearSheet2", "DNB1", "DNB2", "EH1", "EH2", "EHX", "Exactly", "Lay", "Not", "Removal", "ScoreBoth", "TO", "TU", "WinNil1", "WinNil2"]
def validate_mercado(text):
    return text in mercado_options or not text

def update_mercado_combobox(event):
    current_input = mercado_var.get()
    matching_options = [opt for opt in mercado_options if opt.lower().startswith(current_input.lower())]
    mercado_combobox['values'] = matching_options
    if len(matching_options) == 1:
        mercado_var.set(matching_options[0])
        mercado_combobox.icursor(tk.END)

def update_mercado_combobox2(event):
    current_input = mercado_var2.get()
    matching_options = [opt for opt in mercado_options if opt.lower().startswith(current_input.lower())]
    mercado_combobox2['values'] = matching_options
    if len(matching_options) == 1:
        mercado_var2.set(matching_options[0])
        mercado_combobox2.icursor(tk.END)

def update_mercado_combobox3(event):
    current_input = mercado_var3.get()
    matching_options = [opt for opt in mercado_options if opt.lower().startswith(current_input.lower())]
    mercado_combobox3['values'] = matching_options
    if len(matching_options) == 1:
        mercado_var3.set(matching_options[0])
        mercado_combobox3.icursor(tk.END)

mercado_var = tk.StringVar(value=None)
mercado_combobox = ttk.Combobox(frame, textvariable=mercado_var, values=mercado_options, width=7)
mercado_combobox.bind("<KeyRelease>", lambda event: (update_mercado_combobox(event), update_columns()))
mercado_combobox.grid(row=1, column=10, padx=5, pady=5, sticky=tk.W)

# Adiciona campo Valor
def on_validate_valor(P):
    if not P:
        return True
    P = P.replace(',', '.')
    if not P.replace('.', '', 1).isdigit():
        return False
    if len(P.split('.')[0]) > 3:
        return False
    if '.' in P and len(P.split('.')[1]) > 2:
        return False
    return True
def on_entry_change_valor(entry):
    current_text = entry.get()
    if ',' in current_text:
        current_text = current_text.replace(',', '.')
        entry.delete(0, tk.END)
        entry.insert(0, current_text)
        entry.icursor(len(current_text))
valor_var = tk.DoubleVar(value=None)
vcmd_valor = (frame.register(on_validate_valor), '%P')
valor_entry = tk.Entry(frame, textvariable=valor_var, validate="key", validatecommand=vcmd_valor, width=4, justify="right")
valor_entry.bind("<KeyRelease>", lambda event: on_entry_change_valor(valor_entry))
valor_entry.grid(row=1, column=11, padx=5, pady=5, sticky=tk.W)

mercado_var2 = tk.StringVar(value=None)
mercado_combobox2 = ttk.Combobox(frame, textvariable=mercado_var2, values=mercado_options, width=7)
mercado_combobox2.bind("<KeyRelease>", lambda event: (update_mercado_combobox2(event), update_columns()))
mercado_combobox2.grid(row=2, column=10, padx=5, pady=5, sticky=tk.W)

# Adiciona campo Valor2
def on_entry_change_valor2(entry):
    current_text = entry.get()
    if ',' in current_text:
        current_text = current_text.replace(',', '.')
        entry.delete(0, tk.END)
        entry.insert(0, current_text)
        entry.icursor(len(current_text))
valor_var2 = tk.DoubleVar(value=None)
valor_entry2 = tk.Entry(frame, textvariable=valor_var2, validate="key", validatecommand=vcmd_valor, width=4, justify="right")
valor_entry2.bind("<KeyRelease>", lambda event: on_entry_change_valor2(valor_entry2))
valor_entry2.grid(row=2, column=11, padx=5, pady=5, sticky=tk.W)

mercado_var3 = tk.StringVar(value=None)
if num_bets == 3:
    mercado_combobox3 = ttk.Combobox(frame, textvariable=mercado_var3, values=mercado_options, width=7)
    mercado_combobox3.bind("<KeyRelease>", update_mercado_combobox3)
    mercado_combobox3.grid(row=3, column=10, padx=5, pady=5, sticky=tk.W)
else:
    mercado_combobox3 = ttk.Combobox(frame, textvariable=mercado_var3, values=mercado_options, width=7)
    mercado_combobox3.bind("<KeyRelease>", update_mercado_combobox3)
    mercado_combobox3.grid(row=3, column=10, padx=5, pady=5, sticky=tk.W)
    mercado_combobox3.grid_remove()

# Adiciona campo Valor3
valor_var3 = tk.DoubleVar(value=None)
if num_bets == 3:
    def on_entry_change_valor3(entry):
        current_text = entry.get()
        if ',' in current_text:
            current_text = current_text.replace(',', '.')
            entry.delete(0, tk.END)
            entry.insert(0, current_text)
            entry.icursor(len(current_text))
    valor_entry3 = tk.Entry(frame, textvariable=valor_var3, validate="key", validatecommand=vcmd_valor, width=4, justify="right")
    valor_entry3.bind("<KeyRelease>", lambda event: on_entry_change_valor3(valor_entry3))
    valor_entry3.grid(row=3, column=11, padx=5, pady=5, sticky=tk.W)
else:
    valor_entry3 = tk.Entry(frame, textvariable=valor_var3, validate="key", validatecommand=vcmd_valor, width=4,justify="right")
    valor_entry3.grid(row=3, column=11, padx=5, pady=5, sticky=tk.W)
    valor_entry3.grid_remove()

# Adiciona campo ODD
odd_label = tk.Label(frame, text="ODD")
odd_label.grid(row=0, column=12)
def on_validate_odd(P):
    if not P:
        return True
    P = P.replace(',', '.')
    if not P.replace('.', '', 1).isdigit():
        return False
    if len(P.split('.')[0]) > 3:
        return False
    if '.' in P and len(P.split('.')[1]) > 3:
        return False
    return True
def on_entry_change_odd(entry):
    current_text = entry.get()
    if ',' in current_text:
        current_text = current_text.replace(',', '.')
        entry.delete(0, tk.END)
        entry.insert(0, current_text)
        entry.icursor(len(current_text))
odd_var = tk.DoubleVar(value=None)
vcmd_odd = (frame.register(on_validate_odd), '%P')
entry = tk.Entry(frame, textvariable=odd_var, validate="key", validatecommand=vcmd_odd, width=4, justify="right")
entry.bind("<KeyRelease>", lambda event: on_entry_change_odd(entry))
entry.grid(row=1, column=12, padx=5, pady=5, sticky=tk.W)

# Adiciona campo ODD2
def on_entry_change_odd2(entry):
    current_text = entry.get()
    if ',' in current_text:
        current_text = current_text.replace(',', '.')
        entry.delete(0, tk.END)
        entry.insert(0, current_text)
        entry.icursor(len(current_text))
odd_var2 = tk.DoubleVar(value=None)
odd_entry2 = tk.Entry(frame, textvariable=odd_var2, validate="key", validatecommand=vcmd_odd, width=4, justify="right")
odd_entry2.bind("<KeyRelease>", lambda event: on_entry_change_odd2(odd_entry2))
odd_entry2.grid(row=2, column=12, padx=5, pady=5, sticky=tk.W)

# Adiciona campo ODD3
odd_var3 = tk.DoubleVar(value=None)
if num_bets == 3:
    def on_entry_change_odd3(entry):
        current_text = entry.get()
        if ',' in current_text:
            current_text = current_text.replace(',', '.')
            entry.delete(0, tk.END)
            entry.insert(0, current_text)
            entry.icursor(len(current_text))
    odd_entry3 = tk.Entry(frame, textvariable=odd_var3, validate="key", validatecommand=vcmd_odd, width=4, justify="right")
    odd_entry3.bind("<KeyRelease>", lambda event: on_entry_change_odd3(odd_entry3))
    odd_entry3.grid(row=3, column=12, padx=5, pady=5, sticky=tk.W)
else:
    odd_entry3 = tk.Entry(frame, textvariable=odd_var3, validate="key", validatecommand=vcmd_odd, width=4,justify="right")
    odd_entry3.grid(row=3, column=12, padx=5, pady=5, sticky=tk.W)
    odd_entry3.grid_remove()

# Adiciona campo Aposta
real_label = tk.Label(frame, text="R$")
real_label.grid(row=1, column=13)
label_aposta = tk.Label(frame, text="Aposta")
label_aposta.grid(row=0, column=14, padx=5, pady=5, sticky=tk.W)
def on_validate_aposta(P):
    if not P:
        return True
    P = P.replace(',', '.')
    if not P.replace('.', '', 1).isdigit():
        return False
    if len(P.split('.')[0]) > 4:
        return False
    if '.' in P and len(P.split('.')[1]) > 2:
        return False
    return True
def on_entry_change_aposta(entry):
    current_text = entry.get()
    if ',' in current_text:
        current_text = current_text.replace(',', '.')
        entry.delete(0, tk.END)
        entry.insert(0, current_text)
        entry.icursor(len(current_text))
aposta_var = tk.DoubleVar(value=None)
vcmd_aposta = (frame.register(on_validate_aposta), '%P')
aposta_entry = tk.Entry(frame, validate="key", validatecommand=vcmd_aposta, textvariable=aposta_var, width=5, justify="right")
aposta_entry.bind("<KeyRelease>", lambda event: on_entry_change_aposta(aposta_entry))
aposta_entry.grid(row=1, column=14, padx=5, pady=5, sticky=tk.W)

#Adicionar aposta2
real_label2 = tk.Label(frame, text="R$")
real_label2.grid(row=2, column=13)
def on_entry_change_aposta2(entry):
    current_text = entry.get()
    if ',' in current_text:
        current_text = current_text.replace(',', '.')
        entry.delete(0, tk.END)
        entry.insert(0, current_text)
        entry.icursor(len(current_text))
aposta_var2 = tk.DoubleVar(value=None)
aposta_entry2 = tk.Entry(frame, validate="key", validatecommand=vcmd_aposta, textvariable=aposta_var2, width=5, justify="right")
aposta_entry2.bind("<KeyRelease>", lambda event: on_entry_change_aposta2(aposta_entry2))
aposta_entry2.grid(row=2, column=14, padx=5, pady=5, sticky=tk.W)

#Adicionar aposta3
real_label3 = tk.Label(frame, text="R$")
aposta_var3 = tk.DoubleVar(value=None)
if num_bets == 3:
    real_label3.grid(row=3, column=13)
    def on_entry_change_aposta3(entry):
        current_text = entry.get()
        if ',' in current_text:
            current_text = current_text.replace(',', '.')
            entry.delete(0, tk.END)
            entry.insert(0, current_text)
            entry.icursor(len(current_text))
    aposta_entry3 = tk.Entry(frame, validate="key", validatecommand=vcmd_aposta, textvariable=aposta_var3, width=5, justify="right")
    aposta_entry3.bind("<KeyRelease>", lambda event: on_entry_change_aposta3(aposta_entry3))
    aposta_entry3.grid(row=3, column=14, padx=5, pady=5, sticky=tk.W)
else:
    real_label3.grid(row=3, column=13)
    real_label3.grid_remove()
    aposta_entry3 = tk.Entry(frame, validate="key", validatecommand=vcmd_aposta, textvariable=aposta_var3, width=5, justify="right")
    aposta_entry3.grid(row=3, column=14, padx=5, pady=5, sticky=tk.W)
    aposta_entry3.grid_remove()

#Adicionando cálculos
def on_variable_change(*args):
    odds = [odd_var.get(), odd_var2.get(), odd_var3.get()]
    apostas = [aposta_var.get(), aposta_var2.get(), aposta_var3.get()]
    bethouses = [bethouse_options.get(bethouse_var.get(), 0.0), bethouse_options.get(bethouse_var2.get(), 0.0), bethouse_options.get(bethouse_var3.get(), 0.0)]
    if (len([odd for odd in odds if odd != 0.0]) >= 2) and (len([aposta for aposta in apostas if aposta != 0.0]) >= 1):
        calc_apostas(apostas[0], apostas[1], apostas[2], odds[0], odds[1], odds[2], mercado_var.get(), mercado_var2.get(), bethouses[0], bethouses[1], bethouses[2], arred_var.get())
        resultado = calc_apostas(apostas[0], apostas[1], apostas[2], odds[0], odds[1], odds[2], mercado_var.get(),mercado_var2.get(), bethouses[0], bethouses[1], bethouses[2], arred_var.get())
        palpite1_label.config(text=f"R$ {format(round(resultado[0],2), '.2f')}" if resultado[0] is not None else "")
        palpite2_label.config(text=f"R$ {format(round(resultado[1],2), '.2f')}" if resultado[1] is not None else "")
        palpite3_label.config(text=f"R$ {format(round(resultado[2],2), '.2f')}" if resultado[2] is not None else "")
        lucro1_label.config(text=f"R$ {format(round(resultado[4],2), '.2f')}" if resultado[4] is not None else "", fg='seagreen' if resultado[4] > 0 else ('red' if resultado[4] < 0 else 'gray'), font=("Arial", 14, "bold"))
        lucro2_label.config(text=f"R$ {format(round(resultado[5],2), '.2f')}" if resultado[5] is not None else "", fg='seagreen' if resultado[5] > 0 else ('red' if resultado[6] < 0 else 'gray'), font=("Arial", 14, "bold"))
        lucro3_label.config(text=f"R$ {format(round(resultado[6],2), '.2f')}" if resultado[6] is not None else "", fg='seagreen' if resultado[6] > 0 else ('red' if resultado[7] < 0 else 'gray'), font=("Arial", 14, "bold"))
        liability_label1.config(text=f"R$ {format(round(resultado[3],2), '.2f')}" if resultado[3] is not None else "")
        liability_label2.config(text=f"R$ {format(round(resultado[3],2), '.2f')}" if resultado[3] is not None else "")
        lucro_percent_label1.config(text=f"{round(resultado[7],2)}%" if resultado[4] is not None else "", fg='seagreen' if resultado[4] > 0 else ('red' if resultado[4] < 0 else 'gray'), font=("Arial", 20, "bold"))
# associando a função on_variable_change para as variáveis
odd_var.trace_add('write', on_variable_change)
odd_var2.trace_add('write', on_variable_change)
odd_var3.trace_add('write', on_variable_change)
aposta_var.trace_add('write', on_variable_change)
aposta_var2.trace_add('write', on_variable_change)
aposta_var3.trace_add('write', on_variable_change)
bethouse_var.trace_add('write', on_variable_change)
bethouse_var2.trace_add('write', on_variable_change)
bethouse_var3.trace_add('write', on_variable_change)
arred_var.trace_add('write', on_variable_change)
mercado_var.trace_add('write', on_variable_change)
mercado_var2.trace_add('write', on_variable_change)
mercado_var3.trace_add('write', on_variable_change)

#Palpites
palpite_label = tk.Label(frame, text='Palpites')
palpite_label.grid(row=0, column=15, padx=5, pady=5, sticky=tk.W)
palpite1_label = tk.Label(frame, text="")
palpite1_label.grid(row=1, column=15)
palpite2_label = tk.Label(frame, text="")
palpite2_label.grid(row=2, column=15)
palpite3_label = tk.Label(frame, text="")

#Lucro
liability_label = tk.Label(frame, text='Liability')
liability_label1 = tk.Label(frame, text='')
liability_label2 = tk.Label(frame, text='')
lucro_label = tk.Label(frame, text='Lucro')
lucro_label.grid(row=0, column=16, padx=5, pady=5, sticky=tk.W)
lucro1_label = tk.Label(frame, text="")
lucro1_label.grid(row=1, column=16)
lucro2_label = tk.Label(frame, text="")
lucro2_label.grid(row=2, column=16)
lucro3_label = tk.Label(frame, text="")
lucro_percent_label = tk.Label(frame, text='Lucro %')
lucro_percent_label.grid(row=0, column=17, padx=5, pady=5, sticky=tk.W)
lucro_percent_label1 = tk.Label(frame, text="", font=("Arial", 20, "bold"))
lucro_percent_label1.grid(row=1, column=17, rowspan=2)
def update_columns():
    if mercado_var.get() == "Lay" or mercado_var2.get() =="Lay":
        liability_label.grid(row=0, column=16, padx=5, pady=5, sticky=tk.W)
        lucro_label.grid(row=0, column=17, padx=5, pady=5, sticky=tk.W)
        lucro1_label.grid(row=1, column=17)
        lucro2_label.grid(row=2, column=17)
        lucro_percent_label.grid(row=0, column=18, padx=5, pady=5, sticky=tk.W)
        lucro_percent_label1.grid(row=1, column=18, rowspan=2)
        if mercado_var.get() == "Lay":
            liability_label1.grid(row=1, column=16, padx=5, pady=5, sticky=tk.W)
            liability_label2.grid_remove()
            lucro_percent_label.grid(row=0, column=18, padx=5, pady=5, sticky=tk.W)
            lucro_percent_label1.grid(row=1, column=18, rowspan=2)
        else:
            liability_label2.grid(row=2, column=16, padx=5, pady=5, sticky=tk.W)
            liability_label1.grid_remove()
            lucro_percent_label.grid(row=0, column=18, padx=5, pady=5, sticky=tk.W)
            lucro_percent_label1.grid(row=1, column=18, rowspan=2)
    else:
        liability_label.grid_forget()
        lucro_label.grid(row=0, column=16, padx=5, pady=5, sticky=tk.W)
        lucro1_label.grid(row=1, column=16)
        lucro2_label.grid(row=2, column=16)
        lucro_percent_label.grid(row=0, column=17, padx=5, pady=5, sticky=tk.W)
        lucro_percent_label1.grid(row=1, column=17, rowspan=2)

if num_bets == 3:
    palpite3_label.grid(row=3, column=15)
    lucro3_label.grid(row=3, column=16)
else:
    palpite3_label.grid(row=3, column=15)
    lucro3_label.grid(row=3, column=16)
    palpite3_label.grid_remove()
    lucro3_label.grid_remove()

#Para Calcular apostas
def calc_apostas(aposta1, aposta2, aposta3, odd1, odd2, odd3, mercado1, mercado2, bethouse_options1, bethouse_options2, bethouse_options3, arred_var):
    if aposta1 + aposta2 + aposta3 == 0.0 or (odd2 == 0.0 and odd3 == 0.0):
        return
    if odd3 > 0.0:
        if mercado1 == "TO" or mercado1 == "TU" or mercado1 == "AH1" or mercado1 == "AH2":
            odd_1 = ((odd1 - 1) * (1 - bethouse_options1)+1)
            odd_2 = ((odd2 - 1) * (1 - bethouse_options2)+1)
            odd_3 = ((odd3 - 1) * (1 - bethouse_options3)+1)
            if aposta1 > 0.0:
                aposta3 = round(aposta1 / odd3, 2)
                aposta2 = round((odd_1 * aposta1 - odd_3 * aposta3) / odd_2, 2)
            elif aposta2 > 0.0:
                aposta3 = 0.0
                while True:
                    if aposta3 * odd_3 + aposta2 * odd_2 <= aposta3 * odd_3 * odd_1:
                        aposta3 = round(aposta3, 2)
                        break
                    aposta3 += 0.01
                aposta1 = round(aposta3 * odd_3, 2)
            elif aposta3 > 0.0:
                aposta1 = round(aposta3 * odd_3, 2)
                aposta2 = round((odd_1 * aposta1 - odd_3 * aposta3) / odd_2, 2)
            percent1 = aposta1 / (aposta1 + aposta2 + aposta3)
            percent2 = aposta2 / (aposta1 + aposta2 + aposta3)
            percent3 = aposta3 / (aposta1 + aposta2 + aposta3)
        else:
            percent1 = (((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd3 - 1) * (1 - bethouse_options3) + 1)) / ((odd1 - 1) * (1 - bethouse_options1) + 1) / ((((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd3 - 1) * (1 - bethouse_options3) + 1)) / ((odd1 - 1) * (1 - bethouse_options1) + 1) + (((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd3 - 1) * (1 - bethouse_options3) + 1)) / ((odd2 - 1) * (1 - bethouse_options2) + 1) + (((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd3 - 1) * (1 - bethouse_options3) + 1)) / ((odd3 - 1) * (1 - bethouse_options3) + 1))
            percent2 = (((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd3 - 1) * (1 - bethouse_options3) + 1)) / ((odd2 - 1) * (1 - bethouse_options2) + 1) / ((((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd3 - 1) * (1 - bethouse_options3) + 1)) / ((odd1 - 1) * (1 - bethouse_options1) + 1) + (((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd3 - 1) * (1 - bethouse_options3) + 1)) / ((odd2 - 1) * (1 - bethouse_options2) + 1) + (((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd3 - 1) * (1 - bethouse_options3) + 1)) / ((odd3 - 1) * (1 - bethouse_options3) + 1))
            percent3 = (((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd3 - 1) * (1 - bethouse_options3) + 1)) / ((odd3 - 1) * (1 - bethouse_options3) + 1) / ((((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd3 - 1) * (1 - bethouse_options3) + 1)) / ((odd1 - 1) * (1 - bethouse_options1) + 1) + (((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd3 - 1) * (1 - bethouse_options3) + 1)) / ((odd2 - 1) * (1 - bethouse_options2) + 1) + (((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd3 - 1) * (1 - bethouse_options3) + 1)) / ((odd3 - 1) * (1 - bethouse_options3) + 1))
    else:
        percent3 = 0.0
        if mercado2 == "Lay":
            if mercado1 == "Lay":
                percent1 = ((odd2 / (odd2 - 1) - 1) * (1 - bethouse_options2) + 1) / (((odd2 / (odd2 - 1) - 1) * (1 - bethouse_options2) + 1) + ((odd1 / (odd1 - 1) - 1) * (1 - bethouse_options1)+1))
                percent2 = ((odd1 / (odd1 - 1) - 1) * (1 - bethouse_options1) + 1) / (((odd1 / (odd1 - 1) - 1) * (1 - bethouse_options1) + 1) + ((odd2 / (odd2 - 1) - 1) * (1 - bethouse_options2)+1))
            else:
                percent1 = ((odd2 / (odd2 - 1) - 1) * (1 - bethouse_options2) + 1) / (((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 / (odd2 - 1) - 1) * (1 - bethouse_options2) + 1))
                percent2 = ((odd1 - 1) * (1 - bethouse_options1) + 1) / (((odd1 - 1) * (1 - bethouse_options1) + 1) + ((odd2 / (odd2 - 1) - 1) * (1 - bethouse_options2) + 1))
        elif mercado1 == "Lay":
            percent1 = ((odd2 - 1) * (1 - bethouse_options2) + 1) / (((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd1 / (odd1 - 1) - 1) * (1 - bethouse_options1) + 1))
            percent2 = ((odd1 / (odd1 - 1) - 1) * (1 - bethouse_options1) + 1) / (((odd2 - 1) * (1 - bethouse_options2) + 1) + ((odd1 / (odd1 - 1) - 1) * (1 - bethouse_options1) + 1))
        else:
            percent1 = ((odd2 - 1)*(1 - bethouse_options2) + 1) / (((odd2 - 1)*(1-bethouse_options2) + 1) + ((odd1 - 1) * (1 - bethouse_options1) + 1))
            percent2 = ((odd1 - 1)*(1 - bethouse_options1) + 1) / (((odd1 - 1)*(1-bethouse_options1) + 1) + ((odd2 - 1) * (1 - bethouse_options2) + 1))
    if aposta2 > 0.0:
        aposta1 = round(((aposta2 * percent1) / percent2) / arred_var) * arred_var
        aposta3 = round(((aposta2 * percent3) / percent2) / arred_var) * arred_var
    elif aposta1 > 0.0:
        aposta2 = round(((aposta1 * percent2) / percent1) / arred_var) * arred_var
        aposta3 = round(((aposta2 * percent3) / percent2) / arred_var) * arred_var
    elif aposta3 > 0.0:
        aposta1 = round(((aposta2 * percent1) / percent2) / arred_var) * arred_var
        aposta2 = round(((aposta1 * percent2) / percent1) / arred_var) * arred_var
    if mercado2 == "Lay":
        liability = round((aposta2 * (odd2 / (odd2 - 1)) - aposta2), 2)
        lucro1 = round(((aposta1 * odd1 - aposta1) * (1 - bethouse_options1) + aposta1) - aposta1 - aposta2 - aposta3, 2)
        lucro2 = round(((aposta2 * (odd2 / (odd2 - 1)) - aposta2) * (1 - bethouse_options2) + aposta2) - aposta1 - aposta2 - aposta3, 2)
    elif mercado1 == "Lay":
        liability = round((aposta1 * (odd1 / (odd1 - 1)) - aposta1), 2)
        lucro1 = round(((aposta1 * (odd1 / (odd1 - 1)) - aposta1) * (1 - bethouse_options1) + aposta1) - aposta1 - aposta2 - aposta3, 2)
        lucro2 = round(((aposta2 * odd2 - aposta2) * (1 - bethouse_options2) + aposta2) - aposta1 - aposta2 - aposta3,2)
    else:
        liability = None
        lucro1 = round(((aposta1 * odd1 - aposta1) * (1 - bethouse_options1) + aposta1) - aposta1 - aposta2 - aposta3,2)
        lucro2 = round(((aposta2 * odd2 - aposta2) * (1 - bethouse_options2) + aposta2) - aposta1 - aposta2 - aposta3,2)
    if odd3 > 0.0:
        lucro3 = round(((aposta3 * odd3 - aposta3) * (1 - bethouse_options3) + aposta3) - aposta1 - aposta2 - aposta3, 2)
        lucro_percent = round(((lucro1 + lucro2 + lucro3) / 3) / (aposta1 + aposta2 + aposta3) * 100, 2)
    else: lucro3 = 0
    lucro_percent = round(((lucro1 + lucro2) / 2) / (aposta1 + aposta2) * 100, 2)

    return aposta1, aposta2, aposta3, liability, lucro1, lucro2, lucro3, lucro_percent
#resultado = calc_apostas(aposta_var, aposta_var2, aposta_var3, odd_var, odd_var2, odd_var3, mercado_var, mercado_var2, bethouse_options.get(bethouse_var.get(), 0), bethouse_options.get(bethouse_var2.get(), 0), bethouse_options.get(bethouse_var3.get(), 0), arred_var)

# cria o botão de gravação
def gravar():
    # código para salvar os dados em um arquivo CSV
    pass

gravar_button = tk.Button(janela, text="Gravar", command=gravar)
gravar_button.grid(row=1, column=0)

# cria a lista com as últimas 50 apostas
# código para preencher a lista com dados do arquivo CSV
lista = tk.Listbox(janela)
lista.grid(row=2, column=0, columnspan=10)

# inicia o loop da janela
janela.mainloop()