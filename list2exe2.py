
while True:
 nome = input("Digite o nome: ")
 senha = input("Digite a senha: ")

 if senha != nome:
    print("Usuario e senha gravados com sucesso")
    break
 else:
    print("ERRO        DIGITE A SENHA DIFERENTE DO NOME INFORMADO")
