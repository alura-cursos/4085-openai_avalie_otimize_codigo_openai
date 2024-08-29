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