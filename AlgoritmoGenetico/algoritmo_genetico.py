import random
import matplotlib.pyplot as plt # type: ignore

# Dados dos itens (pesos em kg e valores em $)
pesos = [
    4.607428571428572e-05, 0.00032255714285714284, 0.0006688057142857142, 0.0006992771428571429,
    5.0548571428571424e-05, 0.0003794142857142857, 0.0007113014285714286, 0.0011435614285714287,
    0.0011765371428571429, 0.0007888600000000001, 0.00046231142857142853, 0.0005469228571428572,
    6.382285714285715e-05, 0.00024248285714285715, 0.0008726799999999999, 0.0012202714285714285,
    0.0009587471428571428, 0.0009973999999999998, 0.0006378814285714285, 0.0012994571428571427,
    0.001292597142857143, 0.0010429442857142859, 0.0013313314285714286, 0.0013605142857142857,
    0.0013228900000000002, 0.001398177142857143
]
valores = [
    68.674, 471.01, 944.62, 962.094, 78.344, 579.152, 902.698, 1686.515, 1688.691, 1056.157,
    677.562, 833.132, 99.192, 376.418, 1253.986, 1853.562, 1320.297, 1301.637, 859.835, 1677.534,
    1910.501, 1528.646, 1827.477, 2068.204, 1746.556, 2100.851
]
capacidade_mochila = 9.1488285714  # Capacidade máxima da mochila em kg
n_itens = len(pesos)       # Número de itens

# Parâmetros do Algoritmo Genético
tamanho_populacao = 50
taxa_mutacao = 0.02
numero_maximo_geracoes = 1000
limiar_melhora = 0.02
n_geracoes_sem_melhora = 10

# Função para calcular o fitness de um indivíduo
def calcular_fitness(individuo):
    peso_total = sum(pesos[i] * individuo[i] for i in range(n_itens))
    valor_total = sum(valores[i] * individuo[i] for i in range(n_itens))
    if peso_total > capacidade_mochila:
        return 0  # Penaliza soluções inválidas
    return valor_total

# Função para criar a população inicial
def criar_populacao():
    return [[random.randint(0, 1) for _ in range(n_itens)] for _ in range(tamanho_populacao)]

# Função de seleção por roleta viciada
def selecao_roleta(populacao, fitness):
    total_fitness = sum(fitness)
    probabilidades = [f / total_fitness for f in fitness]
    return random.choices(populacao, weights=probabilidades, k=2)

# Função de crossover de um ponto
def crossover(pai1, pai2):
    ponto = random.randint(1, n_itens - 1)
    filho1 = pai1[:ponto] + pai2[ponto:]
    filho2 = pai2[:ponto] + pai1[ponto:]
    return filho1, filho2

# Função de mutação bitflip
def mutacao(individuo):
    for i in range(n_itens):
        if random.random() < taxa_mutacao:
            individuo[i] = 1 - individuo[i]
    return individuo

# Algoritmo Genético
def algoritmo_genetico():
    populacao = criar_populacao()
    melhor_fitness_historico = []
    geracoes_sem_melhora = 0

    for geracao in range(numero_maximo_geracoes):
        fitness = [calcular_fitness(individuo) for individuo in populacao]
        melhor_fitness = max(fitness)
        melhor_fitness_historico.append(melhor_fitness)

        # Critérios de parada
        if melhor_fitness == sum(valores):
            print(f"Valor máximo possível atingido na geração {geracao + 1}.")
            break
        if geracao > 0:
            melhora = melhor_fitness_historico[geracao] - melhor_fitness_historico[geracao - 1]
            if melhora < limiar_melhora:
                geracoes_sem_melhora += 1
            else:
                geracoes_sem_melhora = 0
            if geracoes_sem_melhora >= n_geracoes_sem_melhora:
                print(f"Melhora mínima não atingida por {n_geracoes_sem_melhora} gerações consecutivas.")
                break

        # Exibir o melhor fitness da geração atual
        print(f"Geração {geracao + 1}: Melhor Fitness = {melhor_fitness:.2f}")

        # Criar nova população
        nova_populacao = []
        for _ in range(tamanho_populacao // 2):
            pai1, pai2 = selecao_roleta(populacao, fitness)
            filho1, filho2 = crossover(pai1, pai2)
            nova_populacao.append(mutacao(filho1))
            nova_populacao.append(mutacao(filho2))
        populacao = nova_populacao

    # Plotar a evolução do fitness
    plt.plot(melhor_fitness_historico)
    plt.title("Evolução do Melhor Fitness por Geração")
    plt.xlabel("Geração")
    plt.ylabel("Melhor Fitness")
    plt.show()

    # Retornar o melhor indivíduo
    melhor_individuo = populacao[fitness.index(max(fitness))]
    return melhor_individuo

# Executar o algoritmo
melhor_solucao = algoritmo_genetico()
print("\nMelhor solução encontrada:")
print("Itens selecionados:", [i+1 for i, val in enumerate(melhor_solucao) if val == 1])
print("Valor total:", sum(valores[i] for i, val in enumerate(melhor_solucao) if val == 1))
print("Peso total:", sum(pesos[i] for i, val in enumerate(melhor_solucao) if val == 1))