from assistente import Assistente

def criar_assistente():
  nome_assistente = "Avaliador de Código"
  instrucoes_assistente = """
    Você receberá um script em Python que resolve um problema computacional.
    Seu objetivo é avaliar a complexidade de algoritmo desta solução e dar um parecer ao final do processo.
    
    # Para isso:
    
    1. Faça uma leitura do Script, analisando seu propósito e associando ao pedido do usuário
    2. Faça uma análise da complexidade do algoritmo implementado, considerando o pior caso
    3. Faça uma análise da eficiência do algoritmo, considerando o uso de memória e processamento
    4. Dê um parecer final sobre a solução, indicando se é adequada para o problema proposto
    5. Caso identifique oportunidades de melhoria, sugira alterações ou otimizações
    """
  
  return Assistente(nome=nome_assistente, instrucoes=instrucoes_assistente)

def chat(pergunta, caminho_arquivo):
  professor = criar_assistente()

  while pergunta != "fim":
    resposta = professor.perguntar(pergunta=pergunta, caminho_arquivo=caminho_arquivo, estou_continuando_conversa =True)
    
    print(f"\n\nResposta: {resposta}")

    resposta_avaliada = professor.avaliar_resultado(resposta, pergunta)

    print(f"\n\nAvaliação: {resposta_avaliada}")

    pergunta = input("\nDigite a sua nova pergunta, ou digite 'fim' para encerrar: ")
  
  professor.apagar_agente()

def main():
  caminho_arquivo = input("Digite o nome do arquivo que vocë deseja analisar: ")
  pergunta_inicial = input("Digite a sua dúvida: ")

  chat(pergunta=pergunta_inicial, caminho_arquivo=caminho_arquivo)

if __name__ == "__main__":
  main()