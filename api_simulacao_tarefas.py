from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/tarefas/exemplo1', methods=['GET'])
def exemplo1():
    """
    API endpoint para fornecer um exemplo de lista de tarefas com tempos de execução, descrições e criticidade.

    :return: JSON contendo uma lista de tarefas.
    """
    return jsonify({
        "tarefas": [
            {"id": 1, "descricao": "Compilar módulo A", "tempo_execucao": 10, "criticidade": 3},
            {"id": 2, "descricao": "Rodar testes unitários", "tempo_execucao": 20, "criticidade": 4},
            {"id": 3, "descricao": "Gerar relatório de cobertura", "tempo_execucao": 15, "criticidade": 2}
        ]
    })

@app.route('/api/tarefas/exemplo2', methods=['GET'])
def exemplo2():
    """
    API endpoint para fornecer um exemplo mais complexo de lista de tarefas com tempos de execução, descrições e criticidade.
    Este exemplo é criado para gerar maior complexidade computacional.

    :return: JSON contendo uma lista de tarefas.
    """
    return jsonify({
        "tarefas": [
            {"id": 1, "descricao": "Compilar módulo A", "tempo_execucao": 50, "criticidade": 4},
            {"id": 2, "descricao": "Rodar testes unitários", "tempo_execucao": 120, "criticidade": 3},
            {"id": 3, "descricao": "Gerar relatório de cobertura", "tempo_execucao": 90, "criticidade": 2},
            {"id": 4, "descricao": "Deploy no ambiente de staging", "tempo_execucao": 180, "criticidade": 5},
            {"id": 5, "descricao": "Verificação de segurança", "tempo_execucao": 150, "criticidade": 5},
            {"id": 6, "descricao": "Compilar módulo B", "tempo_execucao": 60, "criticidade": 3},
            {"id": 7, "descricao": "Rodar testes de integração", "tempo_execucao": 110, "criticidade": 4},
            {"id": 8, "descricao": "Auditoria de dependências", "tempo_execucao": 70, "criticidade": 2},
            {"id": 9, "descricao": "Verificação de desempenho", "tempo_execucao": 130, "criticidade": 4},
            {"id": 10, "descricao": "Deploy no ambiente de produção", "tempo_execucao": 200, "criticidade": 5}
        ]
    })

@app.route('/api/tarefas/exemplo3', methods=['GET'])
def exemplo3():
    """
    API endpoint para fornecer um exemplo ainda mais complexo de lista de tarefas com tempos de execução, descrições e criticidade.
    Este exemplo inclui 14 tarefas para um cenário de maior carga computacional.

    :return: JSON contendo uma lista de 14 tarefas.
    """
    return jsonify({
        "tarefas": [
            {"id": 1, "descricao": "Compilar módulo A", "tempo_execucao": 45, "criticidade": 4},
            {"id": 2, "descricao": "Rodar testes unitários", "tempo_execucao": 80, "criticidade": 3},
            {"id": 3, "descricao": "Gerar relatório de cobertura", "tempo_execucao": 60, "criticidade": 2},
            {"id": 4, "descricao": "Deploy no ambiente de staging", "tempo_execucao": 150, "criticidade": 5},
            {"id": 5, "descricao": "Verificação de segurança", "tempo_execucao": 130, "criticidade": 5},
            {"id": 6, "descricao": "Compilar módulo B", "tempo_execucao": 55, "criticidade": 3},
            {"id": 7, "descricao": "Rodar testes de integração", "tempo_execucao": 95, "criticidade": 4},
            {"id": 8, "descricao": "Auditoria de dependências", "tempo_execucao": 65, "criticidade": 2},
            {"id": 9, "descricao": "Verificação de desempenho", "tempo_execucao": 110, "criticidade": 4},
            {"id": 10, "descricao": "Deploy no ambiente de produção", "tempo_execucao": 175, "criticidade": 5},
            {"id": 11, "descricao": "Backup de dados", "tempo_execucao": 90, "criticidade": 3},
            {"id": 12, "descricao": "Atualização de sistema", "tempo_execucao": 60, "criticidade": 4},
            {"id": 13, "descricao": "Verificação de logs", "tempo_execucao": 30, "criticidade": 2},
            {"id": 14, "descricao": "Análise de desempenho", "tempo_execucao": 85, "criticidade": 3}
        ]
    })

if __name__ == '__main__':
    app.run(debug=True)
