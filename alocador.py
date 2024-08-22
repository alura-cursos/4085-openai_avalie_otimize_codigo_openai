import time
import psutil
import pandas as pd
from itertools import permutations


class AlocadorTarefas:
    '''
    Classe responsável por encontrar a melhor alocação de tarefas em servidores.
    '''

    def __init__(self, tarefas, servidores):
        '''
        Inicializa o alocador com uma lista de tarefas e uma lista de servidores.
        :param tarefas: Lista de objetos Tarefa.
        :param servidores: Lista de objetos Servidor.
        '''
        self.tarefas = tarefas
        self.servidores = servidores
        self._monitorando = False 

    def alocar_exaustivo(self, nome_arquivo = "padrao"):
        '''
        Método que realiza a alocação exaustiva de tarefas nos servidores.
        :return: Melhor alocação de tarefas e o tempo total mínimo de execução.
        '''
        start_time = time.time()
        self.memoria_registros = []
        self.memoria_maxima = 0
        self.iteracoes = 0
        self.registro_iteracoes = []
        print("Alocando de forma exaustiva...")
        self._monitorando = True
        
        melhor_tempo = float('inf')
        melhor_alocacao = None

        for tentativa in permutations(self.tarefas):
            self.iteracoes += 1
           
            for servidor in self.servidores:
                servidor.tarefas.clear()

            for i, tarefa in enumerate(tentativa):
                self.servidores[i % len(self.servidores)].adicionar_tarefa(tarefa)

            tempo_atual = max(servidor.tempo_total_execucao() for servidor in self.servidores)
            memoria_atual = psutil.virtual_memory().percent
            self.memoria_registros.append(memoria_atual)
            self.registro_iteracoes.append(self.iteracoes)

            if memoria_atual > self.memoria_maxima:
                self.memoria_maxima = memoria_atual

            if tempo_atual < melhor_tempo:
                melhor_tempo = tempo_atual
                melhor_alocacao = [[tarefa.id for tarefa in servidor.tarefas] for servidor in self.servidores]

        self.tempo_total_execucao = time.time() - start_time
        self._monitorando = False
 
        self._salvar_resultados(nome_arquivo=nome_arquivo)

        print(f"Melhor tempo de execução: {melhor_tempo}")
        print(f"Melhor alocação: {melhor_alocacao}")

        return melhor_alocacao, melhor_tempo

    def _salvar_resultados(self, nome_arquivo = "padrao"):
        '''
        Método que salva os resultados do monitoramento em um arquivo CSV.
        '''
        media_memoria = sum(self.memoria_registros) / len(self.memoria_registros) if self.memoria_registros else 0
        dados = {
            'numero_iteracoes': self.iteracoes,
            'tempo_total': self.tempo_total_execucao,
            'qtd_media_memoria': media_memoria,
            'qtd_memoria_maxima': self.memoria_maxima,
        }
        df = pd.DataFrame([dados])
        df.to_csv(f'{nome_arquivo}.csv', index=False, sep=',')

        dados = {
            'iteracao': self.registro_iteracoes,
            'percentual_memoria': self.memoria_registros
        }
        df = pd.DataFrame(dados)
        df.to_csv(f'{nome_arquivo}-memoria.csv', index=False, sep=',')
