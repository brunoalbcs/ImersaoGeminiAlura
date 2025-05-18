import os                       # Usado com load_dotenv
from dotenv import load_dotenv # Carrega variáveis do .env

from google import genai        # Para criar client e chats
from google.genai import types  # Para configurar o chat

from datetime import date       # Para obter a data atual

from agentes.agente import Agente  # Para criar o conteúdo
from utils.form import Form        # Para o questionário


def iniciar_aula():
    load_dotenv()
    client = genai.Client(api_key='GOOGLE_API_KEY')

    form = Form()
    print("\nVamos começar com um pequeno questionário sobre seu contexto.")
    formulario_respondido = form.trabalho_em_equipe()

    agente = Agente()
    hoje = date.today().strftime("%Y-%m-%d")
    topico = "Trabalho em equipe"
    print("(15%) Pesquisando sobre o tema...")
    conteudo_pesquisado = agente.pesquisador(topico, hoje)
    print("(40%) Gerando conteúdo personalizado...")
    texto_redigido = agente.redator(conteudo_pesquisado, topico)

    modelo = "gemini-2.0-flash"
    instrucoes = f"""
        Você é um facilitador de equipes de alta performance, com foco em ensinar sobre '{topico}', sem nunca fugir do tema.
        Sua tarefa é fornecer informações práticas e acionáveis para melhorar o trabalho colaborativo.
        Você deve se basear no seguinte material:\n{texto_redigido}\n
        Você pode fazer mais pesquisas utilizando a ferramenta de busca do Google (google_search), baseando-se sempre nas informações
        mais recentes para complementar o material sobre os aspectos essenciais do trabalho em equipe.
        Você sempre fará uma pergunta ao usuário puxando gancho para ensinar um próximo tópico e sempre deve corrigi-lo
        caso algo que ele tenha dito esteja errado.
        Seu conteúdo deve cobrir todos os tópicos do material, sempre certificando que o usuário entendeu antes de passar para o próximo
        tópico.

        Sua personalidade deve ser diplomática, compreensiva, motivadora e focada em construir sinergia.
        Traga exemplos práticos e dicas para criar um ambiente de trabalho em equipe produtivo e harmonioso.
    """
    client = genai.Client()
    chat_config = types.GenerateContentConfig(system_instruction=instrucoes)
    chat = client.chats.create(model=modelo, config=chat_config)

    print("(92%) Aula sendo finalizada...")
    prompt = f"Ensine sobre: {topico}\nBase do conteúdo:\n{texto_redigido}\n\nQuestionário respondido para você conhecer mais sobre mim:\n{formulario_respondido}"
    while prompt.lower() != "encerrar":
        resposta = chat.send_message(prompt)
        print(f"\n🟢 {resposta.text}")
        prompt = input('Mensagem (ou digite "encerrar"): ')
