from openai import OpenAI
from helper_models import MODELO_GPT
from dotenv import load_dotenv
import os

load_dotenv()

class Assistente:
  def __init__(self, nome, instrucoes):
    CHAVE_API = os.getenv("OPENAI_API_KEY")
    self.cliente = OpenAI(api_key=CHAVE_API)

    self.nome = nome
    self.instrucoes = instrucoes

    self.thread = None
    self.arquivo = None

    self._ciar_agente()

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