def pesquisar_palavras_letras(letras, ordem=False, range=(0, 0), inicial=False, ordem_arranjo=False, ordem_formato="abc"):
    with open("br_sem_acentos", "r") as arquivo:
        palavras_encontradas = []

        for linha in arquivo:
            palavra = linha.strip().lower()

            # Verifica tamanho mínimo e máximo da palavra
            tamanho = len(palavra)
            if range[0] != 0 and (tamanho < range[0] or tamanho > range[1]):
                continue

            # Verifica se a primeira letra da palavra é a inicial
            if inicial and palavra[0] not in letras:
                continue

            # Verifica se todas as letras estão presentes na palavra
            if all(letra in palavra for letra in letras):
                if ordem:
                    # Verifica se as letras estão na ordem exata
                    posicoes = [palavra.index(letra) for letra in letras]
                    if sorted(posicoes) == posicoes:
                        palavras_encontradas.append(palavra)
                else:
                    palavras_encontradas.append(palavra)

        if ordem_arranjo:
            palavras_encontradas.sort(key=len)

        if ordem_formato == "zyx":
            palavras_encontradas.sort(reverse=True)

    return palavras_encontradas

resultado = pesquisar_palavras_letras("mga")
print(resultado)
