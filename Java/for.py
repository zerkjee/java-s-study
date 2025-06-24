class Tarefa:
    def __init__(self, descricao):
        self.descricao = descricao
        self.concluida = False

    def mostrar(self):
        status = "Concluída" if self.concluida else "Pendente"
        print(f"Tarefa: {self.descricao} - Status: {status}")

    def concluir(self):
        self.concluida = True

# Lista de tarefas
tarefas = []

# Adiciona 3 tarefas
for i in range(3):
    desc = input(f"Digite a descrição da tarefa {i+1}: ")
    tarefas.append(Tarefa(desc))

# Mostra todas as tarefas
print("\nLista de Tarefas:")
for i, t in enumerate(tarefas):
    print(f"{i+1}. ", end="")
    t.mostrar()

# Pergunta qual tarefa deseja marcar como concluída
opcao = int(input("\nDigite o número da tarefa que deseja concluir: ")) - 1
tarefas[opcao].concluir()

# Mostra a lista atualizada
print("\nTarefas Atualizadas:")
for i, t in enumerate(tarefas):
    print(f"{i+1}. ", end="")
    t.mostrar()
