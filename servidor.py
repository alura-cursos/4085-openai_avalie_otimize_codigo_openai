class Servidor:
    '''
    Classe que representa um servidor no qual as tarefas serão alocadas.
    '''

    def __init__(self, id):
        '''
        Inicializa o servidor com um identificador único e uma lista de tarefas vazia.
        :param id: Identificador único do servidor.
        '''
        self.id = id
        self.tarefas = []

    def adicionar_tarefa(self, tarefa):
        '''
        Adiciona uma tarefa ao servidor.
        :param tarefa: Objeto Tarefa a ser adicionado ao servidor.
        '''
        self.tarefas.append(tarefa)

    def tempo_total_execucao(self):
        '''
        Calcula o tempo total de execução de todas as tarefas alocadas ao servidor.
        :return: Tempo total de execução.
        '''
        return sum(tarefa.tempo_execucao for tarefa in self.tarefas)
