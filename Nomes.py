lista = []
contador = 1
while contador <= 5:
	nomes = str(input("Digite os nomes dos usuarios: "))
	lista.append(nomes)
	contador = contador + 1
for elementos in lista:
	print(elementos)
tamanho = len(lista)
print(f"A lista possui {tamanho} nomes na lista")
print(lista)