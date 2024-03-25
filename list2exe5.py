while True:
 nome = input("Digite o nome: ")
 senha = input("Digite a senha: ")

 if senha != nome:
    print("Usuario e senha gravados com sucesso")
    break
 else:
    print("ERRO        DIGITE A SENHA DIFERENTE DO NOME INFORMADO")

a = int(input("Insira a populçação A: "))
txa = float(input("Insira a taxa de crescimento da população A: "))
b = int(input("Insira a população B: "))
txb = float(input("Insira a taxa de crescimento da população B: "))

ano = 0

while a <= b:
	a += a * (txa / 100)
	b += b * (txb / 100) 
	ano += 1

print (f"A ultrapassa ou iguala a B em {ano} anos")
