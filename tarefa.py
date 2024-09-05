class Tarefa:
    '''
    Classe que representa uma tarefa que precisa ser alocada a um servidor.
    '''

    def __init__(self, id, descricao, tempo_execucao, criticidade):
        '''
        Inicializa a tarefa com os parâmetros fornecidos.
        :param id: Identificador único da tarefa.
        :param descricao: Descrição da tarefa.
        :param tempo_execucao: Tempo de execução necessário para a tarefa.
        :param criticidade: Nível de criticidade da tarefa (1 a 5, sendo 5 a mais crítica).
        '''
        self.id = id
        self.descricao = descricao
        self.tempo_execucao = tempo_execucao
        self.criticidade = criticidade

    def __repr__(self):
        '''
        Representação textual da tarefa, usada para exibição e debug.
        '''
        return f"Tarefa(id={self.id}, descricao='{self.descricao}', tempo_execucao={self.tempo_execucao}, criticidade={self.criticidade})"
