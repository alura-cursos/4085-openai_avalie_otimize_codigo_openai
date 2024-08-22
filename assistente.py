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