import tkinter as tk
from tkinter import ttk
import datetime
import re

# cria uma janela
janela = tk.Tk()

# Cria o frame
frame = tk.Frame(janela, padx=10, pady=10)
frame.grid(row=0, column=0)

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
bethouse_combobox3 = ttk.Combobox(frame, textvariable=bethouse_var3, values=list(bethouse_options.keys()), width=7)
bethouse_combobox3.bind("<KeyRelease>", update_bethouse_combobox3)
bethouse_combobox3.grid(row=3, column=9, padx=5, pady=5, sticky=tk.W)

def update_bethouse_values(*args):
    global bethouse1, bethouse2, bethouse3
    bethouse1 = bethouse_options.get(bethouse_var.get(), 0)
    bethouse2 = bethouse_options.get(bethouse_var2.get(), 0)
    bethouse3 = bethouse_options.get(bethouse_var3.get(), 0)
    print(bethouse1, bethouse2, bethouse3)
    print(type(bethouse1), type(bethouse2), type(bethouse3))
bethouse_var.trace_add('write', update_bethouse_values)
bethouse_var2.trace_add('write', update_bethouse_values)
bethouse_var3.trace_add('write', update_bethouse_values)



# inicia o loop da janela
janela.mainloop()