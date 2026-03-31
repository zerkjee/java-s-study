Nomes = []
contador = 1
while contador <= 5:
	adc = str(input("Digite os nomes: "))
	Nomes.append(adc.lower())
	contador = contador + 1
psq = str(input("digite o nome que você quer pesquisar: ").lower())
if psq in Nomes:
    print(psq)
    posicao = Nomes.index(psq)
    print(posicao + 1)
else:
    print("Nome nao existe na lista")