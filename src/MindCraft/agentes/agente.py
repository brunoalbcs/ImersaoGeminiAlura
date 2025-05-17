import os
from dotenv import load_dotenv
import warnings
import datetime # Adicionado para uso no agente pesquisador

# Importações do Google ADK e GenAI
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google import genai
from google.adk.tools import Google Search

# Constante para o modelo a ser usado pelos agentes
MODEL_ID = "gemini-2.0-flash"

class Agente:
    def __init__(self):
        self.model = MODEL_ID

    def