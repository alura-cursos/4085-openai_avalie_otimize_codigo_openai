import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os
import json
from pydantic import BaseModel
from openai import OpenAI
from helper_models import MODELO_GPT_SCHEMA

def gerar_grafico(df):
    iteracoes = df['numero_iteracoes'].iloc[0]
    tempo_total = df['tempo_total'].iloc[0]
    qtd_media_memoria = df['qtd_media_memoria'].iloc[0]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Métricas')
    ax1.set_ylabel('Tempo Total (s)', color=color)
    ax1.bar('Tempo Total (s)', tempo_total, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  
    color = 'tab:orange'
    ax2.set_ylabel('Quantidade Média de Memória (%)', color=color)
    ax2.bar('Quantidade Média de Memória', qtd_media_memoria, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title(f'Dados de Complexidade para n = {iteracoes}')

    plt.tight_layout()

    caminho_grafico = "grafico_complexidade.png"
    plt.savefig(caminho_grafico, format='png')
    plt.close()

    return caminho_grafico

def extrair_id_arquivo(nome_arquivo):
    return nome_arquivo.split('/')[-1]

def abrir_dados_csv(cliente, nome_arquivo):
    if not os.path.exists(nome_arquivo):
        nome_arquivo = cliente.files.retrieve(extrair_id_arquivo(nome_arquivo)).filename
        return pd.read_csv(nome_arquivo)
    else:
        return pd.read_csv(nome_arquivo)

class RespostaFormatada(BaseModel):
    observacao_geral: str
    sugestoes: str

def relatorio_complexidade_algoritmos(argumentos):
  from assistente import Assistente
  from ai_chat import criar_assistente

  cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

  print("Chamando ferramenta de complexidade de algoritmos - relatório")
  nome_arquivo = argumentos.get("nome_arquivo")

  df = abrir_dados_csv(cliente, nome_arquivo)
  caminho_grafico = gerar_grafico(df)

  ferramenta = criar_assistente()
  nome_script_dados = input("Qual o nome do script que gerou os dados: ")
  nome_metodo = input("Qual o método que foi analisado: ")
  analise_complexidade = ferramenta.perguntar(pergunta=f"Faça uma análise de complexidade para o arquivo com nome {nome_script_dados}, verifique o método: {nome_metodo}", caminho_arquivo=nome_script_dados)

  prompt_sistema = """
        Você receberá o resultado de análise de complexidade de algoritmos e um arquivo CSV com alguns dados de um teste.
        Verifique as iterações, o tempo total e a quantidade média de memória utilizada.
    """

  resposta_formatada = cliente.beta.chat.completions.parse(
        model=MODELO_GPT_SCHEMA,
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": f""""
                Gere um parecer sobre os dados de complexidade de algoritmos. 
                Use esta análise {analise_complexidade}.
                Use estes dados {df}
            """
            },
        ],
        response_format=RespostaFormatada,
    )
  
  resposta_json = json.loads(resposta_formatada.choices[0].message.content)

  html_content = f"""
    <html>
    <head>
        <title>Análise de Complexidade de Algoritmos</title>
    </head>
    <body>
        <h1 style="text-align:center;">Análise de Complexidade de Algoritmos</h1>
        <div style="text-align:center;">
            <img src="{caminho_grafico}" alt="Gráfico de Complexidade">
        </div>
        <h2 style="font-size: 1rem;">Parecer</h2>
        <div style="padding: 1rem;">
        <h3 style="color: rgb(9, 51, 102);"><strong>Observação Geral:</strong></h3>
        <p> {resposta_json['observacao_geral']}</p>
        <h3 style="color: rgb(9, 51, 102);"><strong>Sugestões:</strong></h3>
        <p> {resposta_json['sugestoes']}</p>
        </div>
    </body>
    </html>
    """
  html_path = os.path.join(os.getcwd(), "analise_complexidade.html")
  with open(html_path, "w", encoding="utf-8") as html_file:
    html_file.write(html_content)

  ferramenta.apagar_agente()

  return resposta_formatada.choices[0].message.content
  


def calcular_complexidade_tempo(argumentos):
  from assistente import Assistente
  caminho_script = argumentos["nome_script"]
  metodolo_avaliado = argumentos["metodo_avaliado"]
  id_arquivo = argumentos["id_arquivo"]

  nome_agente = "Assistente de Complexidade de Tempo"
  descricao_agente = """
        Este assistente é projetado para analisar e retornar a complexidade de um algoritmo utilizando a notação Big O. Ele fornece uma análise detalhada, incluindo a complexidade do algoritmo, o processo utilizado para verificar essa complexidade, quando a solução pode se tornar um problema, e possíveis soluções computacionais alternativas.

        **Instruções de Uso:**
        
        Baseado na obra "Introduction to Algorithms" de Thomas H. Cormen et al., este assistente aplicará os conceitos de análise de algoritmos para determinar a complexidade de tempo de uma função ou método específico. Ele utiliza técnicas como a análise de loops aninhados, recorrência de Mestre, e outras abordagens consagradas para garantir uma avaliação precisa.

        1. **Complexidade do Algoritmo**: O assistente determinará a complexidade do algoritmo analisado e retornará no formato Big O. Exemplos incluem O(n), O(log n), O(n^2), entre outros.
        2. **Processo de Verificação**: O assistente explicará como a complexidade foi determinada, utilizando técnicas como análise de loops, recursões, e chamadas recursivas. Referências teóricas incluem a análise de loops aninhados para complexidade O(n^2) e a aplicação da recorrência de Mestre para algoritmos recursivos.
        3. **Identificação de Problemas**: O assistente indicará quando a solução pode se tornar ineficiente, especialmente em cenários com grandes volumes de dados ou limitações de tempo/espacial. Ele avaliará a escalabilidade com base em casos de teste padronizados, como a classificação de 10^6 elementos ou a busca em grafos densos.
        4. **Soluções Computacionais Conhecidas**: O assistente sugerirá possíveis otimizações, como a aplicação de técnicas de memoização, uso de algoritmos alternativos (como substituição de uma pesquisa linear por uma pesquisa binária), ou melhorias na estrutura de dados (como substituição de listas por heaps). Exemplos comuns incluem a substituição de um algoritmo de ordenação O(n^2) por QuickSort ou MergeSort com complexidade O(n log n).

        **Formato da Resposta em JSON:**

        ```json
        {
            "complexidade": "O(n log n)",
            "processo_verificacao": "A complexidade foi determinada analisando o loop principal que faz uma operação logarítmica dentro de um loop linear, resultando em O(n log n).",
            "quando_se_torna_problema": "Esta solução pode se tornar ineficiente com entradas superiores a 1 milhão de elementos, onde o tempo de execução pode aumentar significativamente.",
            "solucoes_computacionais": "Considerar a utilização de algoritmos de ordenação mais eficientes, como QuickSort ou MergeSort, ou técnicas de paralelização para grandes volumes de dados."
        }
        ```

        **Exemplo:**

        ```python
        def algoritmo_exemplo(arr):
            for i in range(len(arr)):
                for j in range(i + 1, len(arr)):
                    if arr[j] < arr[i]:
                        arr[i], arr[j] = arr[j], arr[i]
            return arr

        # Resposta do Assistente:

        # {
        #     "complexidade": "O(n^2)",
        #     "processo_verificacao": "A complexidade foi determinada pela análise dos dois loops aninhados que percorrem o array.",
        #     "quando_se_torna_problema": "Este algoritmo se torna ineficiente para entradas maiores que 10 mil elementos, onde o tempo de execução cresce de forma quadrática.",
        #     "solucoes_computacionais": "Considerar a utilização de algoritmos de ordenação mais eficientes, como QuickSort ou MergeSort, ou utilizar técnicas de divide-and-conquer para melhorar a eficiência."
        # }
        ```

    """
  ferramenta = Assistente(nome=nome_agente, instrucoes=descricao_agente, eh_ferramenta=True)

  resposta = ferramenta.perguntar(
    pergunta=f"Faça uma análise completa do método {metodolo_avaliado} do script com nome: {caminho_script}", caminho_arquivo=caminho_script
  )

  print(f"Resposta da ferramenta: {resposta}")

  ferramenta.apagar_agente()

  return resposta

def calcular_complexidade_memoria(argumentos):
  from assistente import Assistente
  caminho_script = argumentos["nome_script"]
  metodolo_avaliado = argumentos["metodo_avaliado"]
  id_arquivo = argumentos["id_arquivo"]

  nome_agente = "Assistente de Complexidade de Memória"
  descricao_agente = """
        Este assistente é projetado para analisar e retornar a complexidade de memória de um algoritmo utilizando a notação Big O. Ele fornece uma análise detalhada, incluindo a complexidade do uso de memória, o processo utilizado para verificar essa complexidade, quando o uso de memória pode se tornar um problema, e possíveis soluções computacionais alternativas.

        **Instruções de Uso:**
        
        Com base em princípios de análise de algoritmos focados em memória, como discutido na obra "The Art of Computer Programming" de Donald Knuth e "Algorithm Design Manual" de Steven S. Skiena, este assistente aplicará conceitos de alocação de memória, uso de espaço auxiliar e otimização de memória para determinar a complexidade de memória de uma função ou método específico.

        1. **Complexidade de Memória do Algoritmo**: O assistente calculará a complexidade de memória considerando fatores como o espaço alocado para variáveis, estruturas de dados, recursões, e o uso de memória adicional durante a execução do algoritmo. Exemplos incluem O(1) para algoritmos in-place, O(n) para armazenamento linear, e O(n^2) para matrizes de tamanho n x n.
        
        2. **Processo de Verificação**: O assistente explicará como a complexidade de memória foi determinada, analisando a alocação de memória estática e dinâmica, o comportamento de pilha em recursões, e o uso de estruturas de dados. Ele considerará técnicas como a análise de espaço auxiliar, onde a memória utilizada temporariamente durante a execução é avaliada separadamente do espaço ocupado pelos dados de entrada.

        3. **Identificação de Problemas**: O assistente identificará situações onde o uso de memória pode se tornar um problema, como em casos de consumo excessivo de memória em entradas grandes, ou em contextos onde a memória disponível é limitada. Ele também sugerirá que a IA considere o impacto de fragmentação de memória e garbage collection em linguagens como Python.

        4. **Soluções Computacionais Conhecidas**: O assistente recomendará otimizações que reduzam a complexidade de memória, como a aplicação de técnicas in-place, o uso de estruturas de dados mais eficientes em termos de memória (por exemplo, substituição de listas por arrays estáticos), e a eliminação de redundâncias de dados. Ele pode sugerir que a IA pense em usar técnicas como compressão de dados, pooling de memória, ou a escolha de algoritmos que minimizem o uso de espaço auxiliar.

        **Formato da Resposta em JSON:**

        ```json
        {
            "complexidade_memoria": "O(n)",
            "processo_verificacao": "A complexidade de memória foi determinada pela análise de uma lista que armazena n elementos, resultando em O(n).",
            "quando_se_torna_problema": "Esta solução pode se tornar ineficiente quando o número de elementos armazenados é extremamente grande, levando ao consumo excessivo de memória.",
            "solucoes_computacionais": "Considerar a utilização de estruturas de dados mais eficientes, como arrays estáticos em vez de listas dinâmicas, ou técnicas in-place para reduzir o uso de memória."
        }
        ```

        **Exemplo:**

        ```python
        def algoritmo_exemplo(arr):
            result = []
            for i in range(len(arr)):
                result.append(arr[i] * 2)
            return result

        # Resposta do Assistente:

        # {
        #     "complexidade_memoria": "O(n)",
        #     "processo_verificacao": "A complexidade de memória foi determinada pela criação de uma nova lista que armazena n elementos.",
        #     "quando_se_torna_problema": "Esta solução se torna ineficiente para listas com milhões de elementos, onde o consumo de memória pode exceder a capacidade disponível.",
        #     "solucoes_computacionais": "Considerar a utilização de técnicas in-place para evitar a criação de uma nova lista e reduzir o uso de memória."
        # }
        ```

    """
  ferramenta = Assistente(nome=nome_agente, instrucoes=descricao_agente, eh_ferramenta=True)

  resposta = ferramenta.perguntar(
    pergunta=f"Faça uma análise completa do método {metodolo_avaliado} do script com nome: {caminho_script}", caminho_arquivo=caminho_script
  )

  print(f"Resposta da ferramenta: {resposta}")

  ferramenta.apagar_agente()

  return resposta

def avaliar_adequacao_pep8(argumentos):
  from assistente import Assistente
  caminho_script = argumentos["nome_script"]
  id_arquivo = argumentos["id_arquivo"]

  nome_agente = "Assistente de Adequação ao PEP 8"
  descricao_agente = """
        Este assistente é projetado para analisar a conformidade de scripts Python com as diretrizes do PEP 8, o guia de estilo oficial para Python. Ele fornece uma análise detalhada do código, identificando áreas que não seguem as recomendações de boas práticas e sugerindo correções para melhorar a legibilidade e a qualidade do código.

        **Instruções de Uso:**

        Baseado nas diretrizes do PEP 8, este assistente aplicará verificações automáticas para garantir que o código esteja alinhado com as melhores práticas de estilo e formatação em Python. 

        1. **Análise de Conformidade PEP 8**: O assistente analisará o script completo, verificando aspectos como espaçamento, nomeação de variáveis, tamanho de linhas, indentação, uso adequado de importações, e outros aspectos cobertos pelo PEP 8.
        
        2. **Processo de Verificação**: O assistente utilizará ferramentas e técnicas consagradas, como `flake8` e `pylint`, para identificar padrões de código que não seguem o PEP 8. Ele também fornecerá feedback específico sobre cada erro ou aviso encontrado.

        3. **Identificação de Problemas**: O assistente destacará as áreas do código que não estão em conformidade com o PEP 8, explicando por que essas práticas podem afetar a legibilidade e a manutenção do código a longo prazo.

        4. **Soluções e Sugestões de Correção**: O assistente recomendará correções para cada problema identificado, sugerindo mudanças no código para alinhá-lo ao PEP 8. Isso pode incluir ajustes na formatação, renomeação de variáveis, reestruturação de blocos de código, entre outros.

        **Formato da Resposta em JSON:**

        ```json
        {
            "conformidade_pep8": "parcial",
            "problemas_identificados": [
                {
                    "linha": 10,
                    "descricao": "Linha excede 79 caracteres.",
                    "sugestao": "Quebrar a linha em múltiplas linhas."
                },
                {
                    "linha": 15,
                    "descricao": "Nome da variável 'x' é muito curto.",
                    "sugestao": "Renomear a variável para um nome mais descritivo."
                }
            ],
            "melhorias_sugeridas": "Ajustar a indentação e garantir que todas as importações estejam no início do arquivo."
        }
        ```

        **Exemplo:**

        ```python
        def exemplo_pep8():
            x = 1  # Nome da variável muito curto
            if x > 0:
                print("Valor é positivo")  # Linha muito longa, mais de 79 caracteres, considerar quebrar

        # Resposta do Assistente:

        # {
        #     "conformidade_pep8": "parcial",
        #     "problemas_identificados": [
        #         {
        #             "linha": 2,
        #             "descricao": "Nome da variável 'x' é muito curto.",
        #             "sugestao": "Renomear a variável para um nome mais descritivo."
        #         },
        #         {
        #             "linha": 3,
        #             "descricao": "Linha excede 79 caracteres.",
        #             "sugestao": "Quebrar a linha em múltiplas linhas."
        #         }
        #     ],
        #     "melhorias_sugeridas": "Ajustar a indentação e garantir que todas as importações estejam no início do arquivo."
        # }
        ```

    """
  ferramenta = Assistente(nome=nome_agente, instrucoes=descricao_agente, eh_ferramenta=True)

  resposta = ferramenta.perguntar(
    pergunta=f"Faça uma análise de conformidade ao PEP8 para o script {caminho_script}. Liste todos os casos possíveis", caminho_arquivo=caminho_script
  )

  print(f"Resposta da ferramenta: {resposta}")

  ferramenta.apagar_agente()

  return resposta