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
    print("\nAntes de começar, responda um breve questionário.")
    formulario_respondido = form.comunicacao()

    agente = Agente()
    hoje = date.today().strftime("%Y-%m-%d")
    topico = "Proatividade e Produtividade. Como planejar rotina, imprevistos e se livrar da procrastinação."
    print("(15%) Realizando pesquisa...")
    conteudo_pesquisado = agente.pesquisador(topico, hoje)
    print("(40%) Preparando conteúdo...")
    texto_redigido = agente.redator(conteudo_pesquisado, topico)

    modelo = "gemini-2.0-flash"
    instrucoes = f"""
        Você é um coach de alta performance, combinando as expertises do "Mestre da Ação", "Especialista em Hábitos", "Arquiteto do Tempo" e "Mestre da Adaptação".
        Sua tarefa é sempre ensinar sobre '{topico}', com foco em acabar com a procrastinação e otimizar o desempenho pessoal, sem nunca fugir do tema.
        Você deve se basear no seguinte material:\n{texto_redigido}\n
        Você pode fazer mais pesquisas utilizando a ferramenta de busca do Google (google_search), baseando-se sempre nas informações
        mais recentes para complementar o material sobre os pilares de Ação, Hábitos, Planejamento e Adaptação.
        Você sempre fará uma pergunta ao usuário puxando gancho para ensinar um próximo tópico e sempre deve corrigi-lo
        caso algo que ele tenha dito esteja errado.
        Seu conteúdo deve cobrir todos os tópicos do material, sempre certificando que o usuário entendeu antes de passar para o próximo
        tópico.

        Sua personalidade deve ser motivadora, prática, metódica, organizada, calma e flexível. Forneça ferramentas e exercícios práticos.
        O objetivo é capacitar o usuário a ser mais produtivo e proativo.
    """
    client = genai.Client()
    chat_config = types.GenerateContentConfig(system_instruction=instrucoes)
    chat = client.chats.create(model=modelo, config=chat_config)

    print("(92%) Quase lá...")
    prompt = f"Ensine sobre: {topico}\nMaterial base:\n{texto_redigido}\n\nQuestionário respondido para você conhecer mais sobre mim:\n{formulario_respondido}"
    while prompt.lower() != "encerrar":
        resposta = chat.send_message(prompt)
        print(f"\n🟢 {resposta.text}")
        prompt = input('Mensagem (ou digite "encerrar"): ')
