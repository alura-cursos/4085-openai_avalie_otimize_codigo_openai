from openai import OpenAI
from helper_models import MODELO_GPT
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

class Assistente:
  def avaliar_resultado(self, resultado_avaliado, pergunta):
        CHAVE_API_GEMINI = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=CHAVE_API_GEMINI)
        prompt_sistema = "Você é um avaliador de respostas da área de computação. Seu objetivo é verificar se códigos ou sugestões estão corretas e indicar, de forma estruturada, os erros e oportunidades de melhoria. Dê um parecer da qualidade da solução."
        llm = genai.GenerativeModel(
            model_name = 'gemini-1.5-pro',
            system_instruction = prompt_sistema
        )
        resposta = llm.generate_content(f"{resultado_avaliado} . Pergunta: {pergunta}")

        return resposta.text

  def __init__(self, nome, instrucoes):
    CHAVE_API = os.getenv("OPENAI_API_KEY")
    self.cliente = OpenAI(api_key=CHAVE_API)

    self.nome = nome
    self.instrucoes = instrucoes

    self.thread = None
    self.arquivo = None

    self._criar_agente()



  def perguntar(self, pergunta, caminho_arquivo = None, estou_continuando_conversa = False):
      self._criar_thread(pergunta=pergunta, caminho_arquivo=caminho_arquivo)

      if estou_continuando_conversa and self.thread:
        self.cliente.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=pergunta
        )

      run = self.cliente.beta.threads.runs.create_and_poll(
          thread_id=self.thread.id,
          assistant_id=self.agente.id
      )

      if run.status == "completed":
          respota_completa = []
          mensagens_resposta = self.cliente.beta.threads.messages.list(
              thread_id=self.thread.id
          )

          for uma_mensagem in mensagens_resposta.data[0].content:
              if hasattr(uma_mensagem, "text") and uma_mensagem.text:
                  respota_completa.append(uma_mensagem.text.value)
                  anotacoes = getattr(uma_mensagem.text, "annotations", None)

                  if anotacoes:
                      caminho_arquivo_resposta = getattr(anotacoes[0], "file_path", None)
                      if caminho_arquivo_resposta:
                          id_arquivo = getattr(caminho_arquivo_resposta, "file_id", None)
                          conteudo_binario = self.cliente.files.content(id_arquivo)
                          respota_completa.append(f"\n\nCódigo Gerado\n\n{conteudo_binario.text}")
      
      return "".join(respota_completa)

  def associar_arquivo(self, caminho_arquivo):
      if self.arquivo is None:
          self.arquivo = self.cliente.files.create(
              file=open(caminho_arquivo, "rb"),
              purpose="assistants"
          )

  def _criar_agente(self):
      self.agente = self.cliente.beta.assistants.create(
          name=self.nome,
          instructions=self.instrucoes,
          model=MODELO_GPT,
          tools=[
              {
                  "type":"code_interpreter"
              }
          ],
          tool_resources={
              "code_interpreter":{
                  "file_ids": []
              }
          }
      )

  def _criar_thread(self, pergunta, caminho_arquivo):
        if self.thread is None:
            self.associar_arquivo(caminho_arquivo)
            self.thread = self.cliente.beta.threads.create(
                messages=[
                    {
                        "role": "user",
                        "content": pergunta,
                        "attachments": [
                            {
                                "file_id": self.arquivo.id,
                                "tools": [{"type": "code_interpreter"}]
                            }
                        ]
                    }
                ]
            )
  
  def apagar_agente(self):
        if self.agente:
            self.cliente.beta.assistants.delete(self.agente.id)
            self.agente = None
            self._apagar_thread()
            self._apagar_arquivo()
    
  def _apagar_thread(self):
      if self.thread:
          self.cliente.beta.threads.delete(self.thread.id)
          self.thread = None

  def _apagar_arquivo(self):
      if self.arquivo:
          self.cliente.files.delete(self.arquivo.id)
          self.arquivo = None