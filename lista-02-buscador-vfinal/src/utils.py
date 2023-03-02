def gerar_lista_simples(lista):
    if isinstance(lista, list):
        return [sub_elem for elem in lista for sub_elem in gerar_lista_simples(elem)]
    else:
        return [lista]

