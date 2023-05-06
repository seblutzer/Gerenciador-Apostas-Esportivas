def validate_num(var, dig, dec):
    if dec == 0:
        # O número deve ser inteiro
        if '.' in var or ',' in var:
            return False
    else:
        # O número pode ter casas decimais
        var = var.replace(',', '.')
        if not var.replace('.', '', 1).isdigit():
            return False
        if '.' in var and len(var.split('.')[1]) > dec:
            return False

    if len(var.split('.')[0]) > dig:
        return False

    return True
