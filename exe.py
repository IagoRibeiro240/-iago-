i = True

while  i:
    nota = int(input("Digite uma nota entre 0 e 10:"))
    if nota > 0 and nota <=10:
        print(f'Valor informado válido: {nota}')
        break
    else:
        print("Informe um valor válido entre 0 e 10")

