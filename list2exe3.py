nome = input("Digite o seu nome: ")
idade = int(input("Digite sua idade: "))
salario = float(input("Digite o seu salário: "))
sexo = input("Digite o [M]asculino [F]eminino: ")
estado_civil = input("Digite o seu estado civil [S]olteiro, [C]asado, [V]iúvo, [D]ivorciado: ")

qtd_letras_nome = len(nome)
if qtd_letras_nome <= 3:
    print("Digite um nome com mais de 3 caracteres ")
else:
    print(f'O nome "{nome}" está disponivel')

if idade > 0 and idade <150:
    print(f'{idade} anos é uma idade válida')
else:
    print(f'Digite uma idade válida')

if salario <= 0:
    print("Digite um salário válido")
else:
    print(f'O seu salário é de R${salario}')

if sexo == "f" or sexo == "F":
    print(f'Você é do sexo FEMININO')
else:
    print(f'Você é do sexo MASCULINO')

if estado_civil == "S" or sexo == "s":
    print(f'Seu estado civil é SOLTEIRO')
elif estado_civil == "C" or sexo == "c":
    print(f'Seu estado civil é CASADO')
elif estado_civil == "V" or sexo == "v":
    print(f'Seu estado civil é VIÚVO')
elif estado_civil == "D" or sexo == "d":
    print(f'Seu estado civil é DIVORCIADO')
