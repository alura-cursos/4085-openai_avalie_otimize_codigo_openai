from ai_tools_logic import calcular_complexidade_tempo, calcular_complexidade_memoria

minhas_ferramentas = [
  {
    "type":"code_interpreter"
  },
  {
    "type": "function",
      "function": {
        "name": "calcular_complexidade_tempo",
        "description": "Utilize esta ferramenta para analisar a complexidade de algoritmos em scripts Python, com foco na avaliação do tempo de execução. A ferramenta requer o caminho do script e o nome do método a ser analisado. Ela irá medir e reportar a eficiência temporal do algoritmo, auxiliando na identificação de possíveis otimizações.",
        "parameters": {
          "type": "object",
          "properties": {
            "nome_script": {
              "type": "string",
              "description": "Nome do script informado pelo usuário. Não utilize o id. Exemplo: script.py"
            },
            "metodo_avaliado": {
              "type": "string",
              "description": "Nome do método que deve ser análisado. Exemplo: busca()"
            },
            "id_arquivo": {
              "type": "string",
              "description": "Id do Script associado na OpenAI. Exemplo: file-v7X0bimuK8b3R9T242gfD2iY"
            }
          },
          "required": ["nome_script", "metodo_avaliado", "id_arquivo"]
        }
      }
  },
  {
    "type": "function",
    "function": {
        "name": "calcular_complexidade_memoria",
        "description": "Utilize esta ferramenta para analisar a complexidade de memória de algoritmos em scripts Python. A ferramenta requer o caminho do script, o nome do método a ser analisado e o ID do arquivo associado. Ela irá medir e reportar a eficiência de uso de memória do algoritmo, identificando possíveis otimizações e destacando áreas onde o uso de memória pode se tornar um problema.",
        "parameters": {
            "type": "object",
            "properties": {
                "nome_script": {
                    "type": "string",
                    "description": "Nome do script informado pelo usuário, incluindo a extensão. Exemplo: script.py ao invés de file-v7X0bimuK8b3R9T242gfD2iY."
                },
                "metodo_avaliado": {
                    "type": "string",
                    "description": "Nome do método que deve ser analisado. Exemplo: busca()."
                },
                "id_arquivo": {
                    "type": "string",
                    "description": "ID do script associado na OpenAI. Exemplo: file-v7X0bimuK8b3R9T242gfD2iY."
                }
            },
            "required": ["nome_script", "metodo_avaliado", "id_arquivo"]
        }
    }
  }
]

mapa_ferramenta = {
  "calcular_complexidade_tempo": calcular_complexidade_tempo,
  "calcular_complexidade_memoria" : calcular_complexidade_memoria
}