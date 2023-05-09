import tkinter as tk
from tkinter import ttk

###################### NÚMEROS ######################
def validate_num(var, dig=4, dec=2):
    if not var:
        return True
    var = str(var).replace(',', '.')
    if ' ' in var:
        return False
    if dec == 0 and '.' in var:
        return False
    try:
        num = float(var)
    except ValueError:
        return False
    if dec == 0 and num != int(num):
        return False
    if len(str(int(num))) > dig:
        return False
    if dec > 0 and len(str(num).split('.')[1]) > dec:
        return False
    return True

def on_entry_change(entry):
    current_text = entry.get()
    if ',' in current_text:
        current_text = current_text.replace(',', '.')
        entry.delete(0, tk.END)
        entry.insert(0, current_text)
        entry.icursor(len(current_text))

def create_float_entry(parent, row, column, label_text=None, width=7, dig=4, dec=2, startwith=None, value=None):
    if label_text:
        label = tk.Label(parent, text=label_text)
        label.grid(row=row, column=column)
        column += 1
    var = tk.DoubleVar(value=value if value is not None else "")
    if startwith is not None:
        var.set(startwith)
    vcmd = (parent.register(lambda s: validate_num(s, dig=dig, dec=dec)), '%P')
    entry = tk.Entry(parent, textvariable=var, validate="key", validatecommand=vcmd, width=width, justify="right")
    entry.grid(row=row, column=column, padx=5, pady=5, sticky=tk.W)
    entry.bind("<KeyRelease>", lambda event: on_entry_change(entry))
    return entry, var




###################### COMBOBOX ######################
def on_combobox_focus_out(event, combobox_var, combobox_options, combobox):
    current_input = combobox_var.get()
    matching_options = [opt for opt in combobox_options if opt.lower().startswith(current_input.lower())]
    if len(matching_options) > 0:
        combobox_var.set(matching_options[0])
        combobox.current(0)
        combobox.event_generate("<<ComboboxSelected>>")

def update_combobox(event, combobox_var, combobox_options, combobox):
    current_input = combobox_var.get()
    matching_options = list(combobox_options)
    for i, char in enumerate(current_input):
        if not any(len(opt) > i for opt in matching_options):
            combobox_var.set(current_input[:-1])
            return
        allowed_chars = [opt[i].upper() for opt in matching_options if len(opt) > i]
        if char.upper() not in allowed_chars:
            combobox_var.set(current_input[:-1])
            return
        matching_options = [opt for opt in matching_options if opt.lower().startswith(current_input[:i+1].lower())]
    combobox['values'] = matching_options
    if len(matching_options) == 1:
        combobox_var.set(matching_options[0])
        combobox.icursor(tk.END)

def create_combobox(parent, options, row, column, label_text=None, width=7):
    if label_text:
        label = tk.Label(parent, text=label_text)
        label.grid(row=row, column=column)
        column += 1
    combobox_var = tk.StringVar(value=None)
    combobox = ttk.Combobox(parent, textvariable=combobox_var, values=options, width=width)
    combobox.grid(row=row, column=column, padx=5, pady=5, sticky=tk.W)
    combobox.bind("<KeyRelease>", lambda event: update_combobox(event, combobox_var, options, combobox))
    combobox.bind("<FocusOut>", lambda event: on_combobox_focus_out(event, combobox_var, options, combobox))
    return combobox, combobox_var
