import os
from dotenv import load_dotenv

# Importações do Google ADK e GenAI
from google import genai
from google.adk.tools import google_search
from google.genai import types # Para criar conteúdos (Content e Part)
from datetime import date

from agentes.agente import Agente
from utils.form import Form

def iniciar_aula():
    '''
    Ao iniciar a aula, deverá ser criado um chat com o agente
    do tema e as informações pesquisadas e redigidas. Esse chat ficará rodando em loop sempre
    pedindo inputs do usuário ao final. Devo definir uma condição de parada no loop (que
    poderá ser informada ao usuário ou eu adiciono algo na interface que vai parar o loop).
    '''
    
    # Instanciar o client com a GOOGLE_API_KEY como variável de ambiente
    load_dotenv()
    client = genai.Client(api_key='GOOGLE_API_KEY')

    # Formulário Inicial
    form = Form()
    print("\nAntes de prosseguir, você deve responder um pequeno questionário de 5 questões, \nescolhendo a alternativa que mais se encaixa com a sua realidade. Vamos lá!")
    formulario_respondido = form.comunicacao()

    # Criando o texto base do conteúdo
    agente = Agente()
    hoje = date.today().strftime("%Y-%m-%d") # data_de_hoje ainda é necessária para o pesquisador
    topico = "Técnicas de comunicação"
    print("(15%) Fazendo pesquisas recentes sobre o tema...")
    conteudo_pesquisado = agente.pesquisador(topico, hoje)
    print("(40%) Montando sua aula...")
    texto_redigido = agente.redator(conteudo_pesquisado, topico)
    
    # Configurações do chat
    modelo = "gemini-2.0-flash"
    instrucoes = f"""
            Você é um especialista em comunicação multifacetado, combinando as habilidades do "Orador Eficaz" e do "Mestre das Relações".
            Sua tarefa é sempre ensinar sobre '{topico}', sem nunca fugir do tema.
            Você deve se basear no seguinte material:\n{texto_redigido}\n
            Você pode fazer mais pesquisas utilizando a ferramenta de busca do Google (google_search), baseando-se sempre nas informações
            mais recentes. Você sempre fará uma pergunta ao usuário puxando gancho para ensinar um próximo tópico e sempre deve corrigi-lo
            caso algo que ele tenha dito esteja errado.
            Seu conteúdo deve cobrir todos os tópicos do material, sempre certificando que o usuário entendeu antes de passar para o próximo
            tópico.

            Sua personalidade deve ser carismática, persuasiva, diplomática, compreensiva e didática.
            O objetivo é capacitar o usuário a se comunicar de forma mais clara, confiante e a construir relacionamentos saudáveis e produtivos.
            """
    client = genai.Client()
    chat_config = types.GenerateContentConfig(system_instruction = instrucoes)

    # Criando o chat
    chat = client.chats.create(model=modelo, config=chat_config)

    # Loop de iteração com o usuário
    print("(92%) Estruturando conteúdos...")
    prompt = f"Ensine sobre: {topico}\nMaterial de base: \n{texto_redigido}\n\nQuestionário respondido sobre seu aluno para que você o conheça um pouco:\n{formulario_respondido}"
    while prompt.lower() != "encerrar":
        resposta = chat.send_message(prompt)
        print(f'\n🔴 {resposta.text}')
        prompt = input('Mensagem (ou digite "encerrar"): ')
    
