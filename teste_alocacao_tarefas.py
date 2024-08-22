import requests
from alocador import AlocadorTarefas
from tarefa import Tarefa
from servidor import Servidor

EXAUSTIVO = "exaustivo"

def criar_tarefas_de_api(tarefas_data):
    """
    Constrói uma lista de objetos Tarefa com base nos dados recebidos da API.

    :param tarefas_data: Dados JSON contendo as tarefas, seus tempos de execução e criticidade.
    :return: Lista de objetos Tarefa.
    """
    tarefas = []
    for tarefa_data in tarefas_data:
        tarefa = Tarefa(
            id=tarefa_data['id'],
            descricao=tarefa_data['descricao'],
            tempo_execucao=tarefa_data['tempo_execucao'],
            criticidade=tarefa_data['criticidade']
        )
        tarefas.append(tarefa)
    return tarefas

def main():
    """
    Função principal para simular a alocação de tarefas em servidores.
    """
    exemplo_id = "exemplo1" 
    url = f"http://127.0.0.1:5000/api/tarefas/{exemplo_id}"
    response = requests.get(url)
    if response.status_code == 200:
        print("Conexão Estabelecida")
        tarefas_data = response.json()['tarefas']
        tarefas = criar_tarefas_de_api(tarefas_data)
        print(f"Tarefas Criadas: {tarefas}")

        # Priorizar as tarefas primeiro pela criticidade, depois pelo tempo de execução
        tarefas.sort(key=lambda x: (x.criticidade, x.tempo_execucao), reverse=True)

        # Definindo o número de servidores de forma mais dinâmica
        num_servidores = min(len(tarefas), 2)  # Usa até 3 servidores, mas não mais que o número de tarefas
        servidores = [Servidor(id=i+1) for i in range(num_servidores)]

        alocador = AlocadorTarefas(tarefas, servidores)
        melhor_alocacao, melhor_makespan = alocador.alocar_guloso()

        print(f"Simulação de Alocação de Tarefas - {exemplo_id.upper()}")
        print("=" * 50)
        print(f"Número de Servidores Utilizados: {num_servidores}")
        print(f"Tempo Total de Execução (Makespan): {melhor_makespan} unidades de tempo\n")
        print(f"Melhor alocação: {melhor_alocacao}")
    else:
        print("Erro ao obter dados da API.")

if __name__ == "__main__":
    main()
