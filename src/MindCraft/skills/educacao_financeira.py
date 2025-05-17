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
    print("\nAntes de prosseguir, você deve responder um pequeno questionário de 5 questões.")
    formulario_respondido = form.comunicacao()

    agente = Agente()
    hoje = date.today().strftime("%Y-%m-%d")
    topico = "Educação Financeira Completa"
    print("(15%) Pesquisando conteúdo atualizado...")
    conteudo_pesquisado = agente.pesquisador(topico, hoje)
    print("(40%) Redigindo aula...")
    texto_redigido = agente.redator(conteudo_pesquisado, topico)

    modelo = "gemini-2.0-flash"
    nivel_usuario = "iniciante"  # Isso pode vir do formulário no futuro
    instrucoes = f"""
        Sua tarefa é sempre ensinar sobre '{topico}', adaptado ao nível do usuário, sem nunca fugir do tema.
        Você deve identificar o nível do usuário a partir do questionário enviado abaixo e personalizar a didática para ensiná-lo.
        Você deve se basear no seguinte material:\n{texto_redigido}\n
        Você pode fazer mais pesquisas utilizando a ferramenta de busca do Google (google_search), baseando-se sempre nas informações
        mais recentes para complementar o material. Você sempre fará uma pergunta ao usuário puxando gancho para ensinar um próximo tópico e sempre deve corrigi-lo
        caso algo que ele tenha dito esteja errado.
        Seu conteúdo deve cobrir todos os tópicos do material, sempre certificando que o usuário entendeu antes de passar para o próximo
        tópico.
        O objetivo é capacitar o usuário com conhecimento financeiro prático e aplicável.
    """
    client = genai.Client()
    chat_config = types.GenerateContentConfig(system_instruction=instrucoes)
    chat = client.chats.create(model=modelo, config=chat_config)

    print("(92%) Estruturando aula...")
    prompt = f"Ensine sobre: {topico}\nMaterial de base:\n{texto_redigido}\n\nQuestionário respondido para você conhecer mais sobre mim:\n{formulario_respondido}"
    while prompt.lower() != "encerrar":
        resposta = chat.send_message(prompt)
        print(f"\n🟢 {resposta.text}")
        prompt = input('Mensagem (ou digite "encerrar"): ')
