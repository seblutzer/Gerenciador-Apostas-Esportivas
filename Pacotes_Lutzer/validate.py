import tkinter as tk
from tkinter import ttk
import _tkinter
from Pacotes_Lutzer.convert import converter_esporte
from language import trans_dicas


###################### NÚMEROS ######################
def validate_num(var, dig=4, dec=2, negative=True, restrict=None):
    if not var:
        return True
    if (var == '-' and negative) or (var == '-,' and negative) or (var == '-.' and negative):
        return True
    if var == ',' or var == '.':
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
    if not negative and num < 0:
        return False
    if dec == 0 and num != int(num):
        return False
    if len(str(int(abs(num)))) > dig:
        return False
    decimal = str(num).split('.')[1]
    if restrict == 'half':
        dec = 1
        if len(decimal) > dec or (num * 10) % 5 != 0:
            return False
    elif restrict == 'quarter':
        dec = 2
        if decimal == '51' or decimal == '52' or decimal == '53' or decimal == '54' or decimal == '55' or decimal == '56' or decimal == '57' or decimal == '58' or decimal == '59' or decimal == '50':
            return False
        if len(decimal) > dec or (num * 100) % 25 != 0:
            if int(decimal[0]) not in [2, 5, 7] or len(decimal) > dec:
                return False
    elif dec > 0 and len(decimal) > dec:
        return False
    return True

def on_entry_change(entry, restrict=None):
    current_text = entry.get()
    if current_text == ',' or current_text == '.':
        current_text = '0.'
        entry.delete(0, tk.END)
        entry.insert(0, current_text)
        entry.icursor(len(current_text))
    elif current_text == '-,' or current_text == '-.':
        current_text = '-0.'
        entry.delete(0, tk.END)
        entry.insert(0, current_text)
        entry.icursor(len(current_text))
    if ',' in current_text:
        current_text = current_text.replace(',', '.')
        entry.delete(0, tk.END)
        entry.insert(0, current_text)
        entry.icursor(len(current_text))
    if restrict == 'quarter':
        if '.' in current_text:
            int_part, dec_part = current_text.split('.')
            if dec_part == '25' or dec_part == '75':
                pass
            elif dec_part == '2':
                dec_part = '25'
                current_text = f'{int_part}.{dec_part}'
                entry.delete(0, tk.END)
                entry.insert(0, current_text)
                entry.icursor(len(current_text))
            elif dec_part == '7':
                dec_part = '75'
                current_text = f'{int_part}.{dec_part}'
                entry.delete(0, tk.END)
                entry.insert(0, current_text)
                entry.icursor(len(current_text))

def create_float_entry(parent, row, column, label_text=None, width=7, dig=4, dec=2, startwith=None, value=None, negative=True, restrict=None):
    if label_text:
        label = tk.Label(parent, text=label_text)
        label.grid(row=row, column=column)
        column += 1
    var = tk.DoubleVar(value=value if value is not None else "")
    if startwith is not None:
        var.set(startwith)
    vcmd = (parent.register(lambda s: validate_num(s, dig=dig, dec=dec, negative=negative, restrict=restrict)), '%P')
    entry = tk.Entry(parent, textvariable=var, validate="key", validatecommand=vcmd, width=width, justify="right")
    entry.grid(row=row, column=column, padx=5, pady=5, sticky=tk.W)
    entry.bind("<KeyRelease>", lambda event: on_entry_change(entry, restrict=restrict))
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

def float_error(valor, erro):
    try:
        valor_float = valor.get()
    except _tkinter.TclError:
        return erro
    except AttributeError:
        return erro
    if valor_float == '':
        return erro
    return valor_float

def gerar_mensagem(mercado_var: str, valor_var: str, esporte: str, idioma) -> str:
    esporte = converter_esporte(esporte)
    plural = ''
    set = 'set'
    if esporte == 'Tênis' or esporte == 'Tênis de Mesa' or esporte == 'Dardos':
        equipe = trans_dicas['o jogador'][idioma]
        equipes = trans_dicas['os jogadores'][idioma]
    elif esporte == 'Boxe' or esporte == 'MMA':
        equipe = trans_dicas['o lutado'][idioma]
        equipes = trans_dicas['os lutadores'][idioma]
    else:
        equipe = trans_dicas['o time'][idioma]
        equipes = trans_dicas['os times'][idioma]
    if esporte == 'Futebol':
        set = trans_dicas['tempo'][idioma]
        sets = trans_dicas['tempos'][idioma]
        ponto = trans_dicas['gol'][idioma]
        pontos = trans_dicas['gols'][idioma]
    else:
        set = trans_dicas['set'][idioma]
        set = trans_dicas['sets'][idioma]
        ponto = trans_dicas['ponto'][idioma]
        pontos = trans_dicas['pontos'][idioma]
    if esporte == 'E-Sports':
        set = trans_dicas['jogo'][idioma]
        sets = trans_dicas['jogos'][idioma]
        ponto = trans_dicas['ponto'][idioma]
        pontos = trans_dicas['pontos'][idioma]

    if mercado_var.startswith('T') or mercado_var.startswith('Exac'):
        tipo = 'total'
    elif mercado_var.startswith(('AH', 'EH', '1', '2', '1X', 'X2', 'X', 'DNB')):
        if mercado_var.startswith(('1', '2')):
            valor_var = -0.5
        elif mercado_var.startswith(('1X', 'X2')):
            valor_var = 0.5
        elif mercado_var.startswith('X'):
            mercado_var = 'EHX'
            valor_var = 0
        elif mercado_var.startswith('DNB'):
            valor_var = 0
        tipo = 'handicap'
    else:
        tipo = 'especial'

    str_valor = str(valor_var)
    if str_valor == '':
        valor_tipo = 'vazio'
    elif str_valor.endswith('.5'):
        valor_tipo = 'meio'
    elif str_valor.endswith('.25'):
        valor_tipo = 'but_quart'
    elif str_valor.endswith('.75'):
        valor_tipo = 'top_quart'
    elif mercado_var.endswith('(3-way)') or mercado_var.startswith('EH'):
        valor_tipo = 'europeu'
    else:
        valor_tipo = 'inteiro'

    if valor_var != '':
        valor = float(valor_var)
        arredondado_para_cima = int(valor) + 1
        arredondado_para_baixo = int(valor)
        if tipo == 'total':
            if mercado_var.startswith('TEv'):
                return f"{trans_dicas['Vence se'][idioma]} {trans_dicas['Total de pontos ímpar'][idioma]}\n{trans_dicas['Perde se'][idioma]} {trans_dicas['Total de pontos par'][idioma]}"
            elif mercado_var.startswith('TOd'):
                return f"{trans_dicas['Vence se'][idioma]} {trans_dicas['Total de pontos par'][idioma]}\n{trans_dicas['Perde se'][idioma]} {trans_dicas['Total de pontos ímpar'][idioma]}"
            elif valor_tipo == 'meio':
                if mercado_var.startswith('TO'):
                    return f"{trans_dicas['Vence com'][idioma]} {arredondado_para_cima} {trans_dicas['ou mais'][idioma]} {pontos}\n{trans_dicas['Perde com'][idioma]} {arredondado_para_baixo} {trans_dicas['ou menos'][idioma]} {pontos}"
                elif mercado_var.startswith('TU'):
                    return f"{trans_dicas['Vence com'][idioma]} {arredondado_para_baixo} {trans_dicas['ou menos'][idioma]} {pontos}\n{trans_dicas['Perde com'][idioma]} {arredondado_para_cima} {trans_dicas['ou mais'][idioma]} {pontos}"
            elif valor_tipo == 'but_quart':
                if mercado_var.startswith('TO'):
                    return f"{trans_dicas['Vence com'][idioma]} {arredondado_para_cima} {trans_dicas['ou mais'][idioma]} {pontos}\n{trans_dicas['Meia Vitória com'][idioma]} {arredondado_para_baixo} {pontos}\n{trans_dicas['Perde com'][idioma]} {arredondado_para_baixo - 1} {trans_dicas['ou menos'][idioma]} {pontos}"
                elif mercado_var.startswith('TU'):
                    return f"{trans_dicas['Vence com'][idioma]} {arredondado_para_baixo - 1} {trans_dicas['ou menos'][idioma]} {pontos}\n{trans_dicas['Meia Derrota com'][idioma]} {arredondado_para_baixo} {pontos}\n{trans_dicas['Perde com'][idioma]} {arredondado_para_cima} {trans_dicas['ou mais'][idioma]} {pontos}"
            elif valor_tipo == 'top_quart':
                if mercado_var.startswith('TO'):
                    return f"{trans_dicas['Vence com'][idioma]} {arredondado_para_cima + 1} {trans_dicas['ou mais'][idioma]} {pontos}\n{trans_dicas['Meia Derrota com'][idioma]} {arredondado_para_cima} {pontos}\n{trans_dicas['Perde com'][idioma]} {arredondado_para_baixo} {trans_dicas['ou menos'][idioma]} {pontos}"
                elif mercado_var.startswith('TU'):
                    return f"{trans_dicas['Vence com'][idioma]} {arredondado_para_baixo} {trans_dicas['ou menos'][idioma]} {pontos}\n{trans_dicas['Meia Vitória com'][idioma]} {arredondado_para_cima} {pontos}\n{trans_dicas['Perde com'][idioma]} {arredondado_para_cima + 1} {trans_dicas['ou mais'][idioma]} {pontos}"
            elif valor_tipo == 'europeu':
                if mercado_var.startswith('TO'):
                    return f"{trans_dicas['Vence com'][idioma]} {arredondado_para_cima} {trans_dicas['ou mais'][idioma]} {pontos}\n{trans_dicas['Perde com'][idioma]} {arredondado_para_baixo} {trans_dicas['ou menos'][idioma]} {pontos}"
                elif mercado_var.startswith('TU'):
                    return f"{trans_dicas['Vence com'][idioma]} {arredondado_para_baixo - 1} {trans_dicas['ou menos'][idioma]} {pontos}\n{trans_dicas['Perde com'][idioma]} {arredondado_para_baixo} {trans_dicas['ou mais'][idioma]} {pontos}"
            elif valor_tipo == 'inteiro':
                if mercado_var.startswith('TO'):
                    return f"{trans_dicas['Vence com'][idioma]} {arredondado_para_cima} {trans_dicas['ou mais'][idioma]} {pontos}\n{trans_dicas['Anula com'][idioma]} {arredondado_para_baixo} {pontos}\n{trans_dicas['Perde com'][idioma]} {arredondado_para_baixo - 1} {trans_dicas['ou menos'][idioma]} {pontos}"
                elif mercado_var.startswith('TU'):
                    return f"{trans_dicas['Vence com'][idioma]} {arredondado_para_baixo - 1} {trans_dicas['ou menos'][idioma]} {pontos}\n{trans_dicas['Anula com'][idioma]} {arredondado_para_baixo} {pontos}\n{trans_dicas['Perde com'][idioma]} {arredondado_para_cima} {trans_dicas['ou mais'][idioma]} {pontos}"
                else:
                    return f"{trans_dicas['Vence com'][idioma]} {arredondado_para_baixo} {pontos}\n{trans_dicas['Perde com'][idioma]} {trans_dicas['Qualquer outra pontuação'][idioma]}"

        elif tipo == 'handicap':
            if valor_tipo == 'meio':
                if valor == 0.5:
                    return f"{trans_dicas['Vence se'][idioma]} {equipe} {trans_dicas['empatar ou vencer'][idioma]}\n{trans_dicas['Perde se'][idioma]} {equipe} {trans_dicas['perder'][idioma]}"
                elif valor == -0.5:
                    return f"{trans_dicas['Vence se'][idioma]} {equipe} {trans_dicas['vencer'][idioma]}\n{trans_dicas['Perde se'][idioma]} {equipe} {trans_dicas['empatar ou perder'][idioma]}"
                elif valor > 0.5:
                    return f"{trans_dicas['Vence se'][idioma]} {equipe} {trans_dicas['perder por'][idioma]} {arredondado_para_baixo} {trans_dicas['ou menos'][idioma]} {pontos}\n{trans_dicas['Perde se'][idioma]} {equipe} {trans_dicas['perder por'][idioma]} {arredondado_para_cima} {trans_dicas['ou mais'][idioma]} {pontos}"
                else:
                    return f"{trans_dicas['Vence se'][idioma]} {equipe} {trans_dicas['vencer por'][idioma]} {-arredondado_para_baixo + 1} {trans_dicas['ou mais'][idioma]} {pontos}\n{trans_dicas['Perde se'][idioma]} {equipe} {trans_dicas['vencer por'][idioma]} {-arredondado_para_baixo} {trans_dicas['ou menos'][idioma]} {pontos}"
            elif valor_tipo == 'but_quart':
                if valor > 0:
                    return f"{trans_dicas['Vence se'][idioma]} {equipe} {trans_dicas['perder por'][idioma]} {arredondado_para_baixo - 1} {trans_dicas['ou menos'][idioma]} {pontos}\n{trans_dicas['Meia Vitória se'][idioma]} {equipe} {trans_dicas['perder por'][idioma]} {arredondado_para_baixo} {pontos}\n{trans_dicas['Perde se'][idioma]} {equipe} {trans_dicas['perder por'][idioma]} {arredondado_para_cima} {trans_dicas['ou mais'][idioma]} {pontos}"
                else:
                    return f"{trans_dicas['Vence se'][idioma]} {equipe} {trans_dicas['vencer por'][idioma]} {-arredondado_para_baixo + 1} {trans_dicas['ou mais'][idioma]} {pontos}\n{trans_dicas['Meia Derrota se'][idioma]} {equipe} {trans_dicas['vencer por'][idioma]} {-arredondado_para_baixo} {pontos}\n{trans_dicas['Perde se'][idioma]} {equipe} {trans_dicas['vencer por'][idioma]} {-arredondado_para_baixo - 1} {trans_dicas['ou menos'][idioma]} {pontos}"
            elif valor_tipo == 'top_quart':
                if valor > 0:
                    return f"{trans_dicas['Vence se'][idioma]} {equipe} {trans_dicas['perder por'][idioma]} {arredondado_para_baixo} {trans_dicas['ou menos'][idioma]} {pontos}\n{trans_dicas['Meia Derrota se'][idioma]} {equipe} {trans_dicas['perder por'][idioma]} {arredondado_para_cima} {pontos}\n{trans_dicas['Perde se'][idioma]} {equipe} {trans_dicas['perder por'][idioma]} {arredondado_para_cima + 1} {trans_dicas['ou mais'][idioma]} {pontos}"
                else:
                    return f"{trans_dicas['Vence se'][idioma]} {equipe} {trans_dicas['vencer por'][idioma]} {-arredondado_para_baixo + 2} {trans_dicas['ou mais'][idioma]} {pontos}\n{trans_dicas['Meia Vitória se'][idioma]} {equipe} {trans_dicas['vencer por'][idioma]} {-arredondado_para_baixo + 1} {pontos}\n{trans_dicas['Perde se'][idioma]} {equipe} {trans_dicas['vencer por'][idioma]} {-arredondado_para_baixo} {trans_dicas['ou menos'][idioma]} {pontos}"
            elif valor_tipo == 'europeu':
                if valor > 0:
                    if mercado_var.startswith('EHX'):
                        return f"{trans_dicas['Vence se'][idioma]} {equipe} {trans_dicas['perder por'][idioma]} {arredondado_para_baixo} {pontos}\nPerde por {trans_dicas['Qualquer outra pontuação'][idioma]}"
                    if valor == 1:
                        return f"{trans_dicas['Vence se'][idioma]} {equipe} {trans_dicas['empatar ou vencer'][idioma]}\n{trans_dicas['Perde se'][idioma]} {equipe} {trans_dicas['perder'][idioma]}"
                    return f"{trans_dicas['Vence se'][idioma]} {equipe} {trans_dicas['perder por'][idioma]} {arredondado_para_baixo - 1} {trans_dicas['ou menos'][idioma]} {pontos}\n{trans_dicas['Perde se'][idioma]} {equipe} {trans_dicas['perder por'][idioma]} {arredondado_para_baixo} {trans_dicas['ou mais'][idioma]} {pontos}"
                elif valor < 0:
                    if mercado_var.startswith('EHX'):
                        return f"{trans_dicas['Vence se'][idioma]} {equipe} {trans_dicas['vencer por'][idioma]} {-arredondado_para_baixo} {pontos}\nPerde por {trans_dicas['Qualquer outra pontuação'][idioma]}"
                    return f"{trans_dicas['Vence se'][idioma]} {equipe} {trans_dicas['vencer por'][idioma]} {-arredondado_para_baixo + 1} {trans_dicas['ou mais'][idioma]} {pontos}\n{trans_dicas['Perde se'][idioma]} {equipe} {trans_dicas['vencer por'][idioma]} {-arredondado_para_baixo} {trans_dicas['ou menos'][idioma]} {pontos}"
                else:
                    if mercado_var.startswith('EHX'):
                        return f"{trans_dicas['Vence se'][idioma]} {equipe} {trans_dicas['empatar sem'][idioma]} {pontos}\n{trans_dicas['Perde com'][idioma]} {trans_dicas['Qualquer outra pontuação'][idioma]}"
                    return f"{trans_dicas['Vence se'][idioma]} {equipe} {trans_dicas['vencer'][idioma]}\n{trans_dicas['Perde se'][idioma]} {equipe} {trans_dicas['empatar ou perder'][idioma]}"
            elif valor_tipo == 'inteiro':
                if valor > 0:
                    return f"{trans_dicas['Vence se'][idioma]} {equipe} {trans_dicas['perder por'][idioma]} {arredondado_para_baixo - 1} {trans_dicas['ou menos'][idioma]} {pontos}\nAnula se o {equipe} {trans_dicas['perder por'][idioma]} {arredondado_para_baixo} {pontos}\n{trans_dicas['Perde se'][idioma]} {equipe} {trans_dicas['perder por'][idioma]} {arredondado_para_cima} {trans_dicas['ou mais'][idioma]} {pontos}"
                elif valor < 0:
                    return f"{trans_dicas['Vence se'][idioma]} {equipe} {trans_dicas['vencer por'][idioma]} {-arredondado_para_baixo + 1} {trans_dicas['ou mais'][idioma]} {pontos}\nAnula se o {equipe} {trans_dicas['vencer por'][idioma]} {-arredondado_para_baixo} {pontos}\n{trans_dicas['Perde se'][idioma]} {equipe} {trans_dicas['vencer por'][idioma]} {-arredondado_para_cima} {trans_dicas['ou menos'][idioma]} {pontos}"
                else:
                    return f"{trans_dicas['Vence se'][idioma]} {equipe} {trans_dicas['vencer'][idioma]}\nAnula se {trans_dicas['empatar'][idioma]}\n{trans_dicas['Perde se'][idioma]} {equipe} {trans_dicas['perder'][idioma]}"
    else:
        if mercado_var.startswith('Clear'):
            return f"{trans_dicas['Vence se'][idioma]} {equipe} {trans_dicas['não sofrer nenhum'][idioma]} {ponto}\n{trans_dicas['Perde se'][idioma]} {equipe} {trans_dicas['sofrer qualquer'][idioma]} {ponto}"
        elif mercado_var.startswith('WinNil'):
            return f"{trans_dicas['Vence se'][idioma]} {equipe} {trans_dicas['vencer sem sofrer nenhum'][idioma]} {ponto}\n{trans_dicas['Perde se'][idioma]} {equipe} {trans_dicas['sofrer qualquer'][idioma]} {ponto}"
        elif mercado_var.startswith('Score'):
            return f"{trans_dicas['Vence se'][idioma]} {trans_dicas['ambos os'][idioma]} {equipes} {trans_dicas['marcarem pelo menos um'][idioma]} {ponto}\n{trans_dicas['Perde se'][idioma]} {trans_dicas['ao menos um dos'][idioma]} {equipes} {trans_dicas['não marcar ao menos um'][idioma]} {ponto}"
        elif mercado_var.startswith('WinLeas'):
            return f"{trans_dicas['Vence se'][idioma]} {equipe} {trans_dicas['vencer pelo menos um'][idioma]} {set}\n{trans_dicas['Perde se'][idioma]} {equipe} {trans_dicas['não vencer nenhum'][idioma]} {set}"
        elif mercado_var.startswith('WinAll'):
            return f"{trans_dicas['Vence se'][idioma]} {equipe} {trans_dicas['vencer todos os'][idioma]} {sets}\n{trans_dicas['Perde se'][idioma]} {equipe} {trans_dicas['não vencer ao menos um'][idioma]} {set}"
        elif mercado_var.startswith('Not') or mercado_var.startswith('Lay'):
            return f"{trans_dicas['Vence se'][idioma]} {trans_dicas['a outra aposta'][idioma]} não {trans_dicas['vencer'][idioma]}\n{trans_dicas['Perde se'][idioma]} {trans_dicas['a outra aposta'][idioma]} {trans_dicas['perder'][idioma]}"
        elif mercado_var.startswith('Q'):
            return f"{trans_dicas['Vence se'][idioma]} {equipe} {trans_dicas['se qualificar para a próxima etapa'][idioma]}\n{trans_dicas['Perde se'][idioma]} {equipe} {trans_dicas['não se qualificar para a próxima etapa'][idioma]}"
        elif mercado_var.startswith('Remo'):
            return f"{trans_dicas['Vence se'][idioma]} {trans_dicas['houver expulsão'][idioma]}\n{trans_dicas['Perde se'][idioma]} {trans_dicas['não houver expulsão'][idioma]}"
        elif mercado_var.startswith('TEv'):
            return f"{trans_dicas['Vence se'][idioma]} {trans_dicas['Total de pontos ímpar'][idioma]}\n{trans_dicas['Perde se'][idioma]} {trans_dicas['Total de pontos par'][idioma]}"
        elif mercado_var.startswith('TOd'):
            return f"{trans_dicas['Vence se'][idioma]} {trans_dicas['Total de pontos par'][idioma]}\n{trans_dicas['Perde se'][idioma]} {trans_dicas['Total de pontos ímpar'][idioma]}"
    return ''


def check_margin(nums, margins):
    media = sum(nums) / len(nums)
    for num, margin in zip(nums, margins):
        if num > media + margin or num < media - margin:
            return False

    return True


def check_margin2(nums, margin):
    media = sum(nums) / len(nums)
    for num in nums:
        if num > media + margin or num < media - margin:
            return False
    return True