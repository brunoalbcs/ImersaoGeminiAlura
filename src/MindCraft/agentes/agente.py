import warnings  # Usado para ignorar warnings
from google import genai  # Necessário para o SDK da Google GenAI
from google.adk.agents import Agent  # Necessário para criar agentes
from google.adk.runners import Runner  # Necessário para executar agentes
from google.adk.sessions import InMemorySessionService  # Necessário para sessões em memória
from google.adk.tools import google_search  # Ferramenta usada nos agentes
from google.genai import types  # Usado para criar `Content` e `Part`

warnings.filterwarnings("ignore")

class Agente:
    def __init__(self):
        self.model = "gemini-2.0-flash"  # Modelo que será usado.

    def pesquisador(self, topico, data_de_hoje):
        buscador = Agent(
        name="agente_pesquisador",
        model=self.model,
        description="Agente que faz busca detalhada no google_search",
        tools=[google_search],
        instruction="""
        Você é um assistente de pesquisa. Sua tarefa é usar a ferramenta de busca do Google (google_search)
        para fazer uma busca detalhada com a maior riqueza de detalhes possível sobre o tema. Você deve
        pesquisar em fontes confiáveis (não precisa citá-las) pois o conteúdo da pesquisa será usado para
        ensinar pessoas sobre esse tema, então deve conter a maior riqueza de detalhes possível. Traga as
        informações mais relevantes possíveis para o público geral. Dê preferências a informações atuais
        e com a maior veracidade possível, ou seja, se um fato é mostrado em várias fontes diferentes, é
        mais provável que ele seja de maior interesse do público.
        """
        )
        entrada_do_agente_buscador = f"Tópico: {topico}\nData de hoje: {data_de_hoje}"
        lancamentos = self.call_agent(buscador, entrada_do_agente_buscador)
        return lancamentos

    def redator(self, conteudo_pesquisado, topico):
        agente_redator = Agent( # Nome da variável corrigido para evitar conflito com o nome da classe
            name="agente_redator",
            model=self.model,
            description="Agente que redige e organiza conteúdo em formato didático e informativo.",
            tools=[google_search],
            instruction=f"""
            Você é um redator de textos didáticos. Sua tarefa será estruturar o conteúdo fornecido sobre o tema '{topico}'
            de forma clara, lógica e envolvente para fins educacionais.
            O objetivo é transformar o conteúdo pesquisado em um material didático e científico de alta qualidade,
            informativo e que motive o aprendizado. Evite jargões excessivos e explique termos técnicos quando necessário.
            O texto final deve ser coeso e coerente.
            Conteúdo a ser trabalhado:
            {conteudo_pesquisado}.
            Caso seja necessário, faça mais pesquisas utilizando a ferramenta de busca do Google (google_search) e complemente
            sobre o tema, sempre de forma didática e com a maior riqueza de informações possível.
            """
        )
        entrada_do_agente_redator = f"Reescreva e estruture o seguinte conteúdo sobre '{topico}':\n{conteudo_pesquisado}"
        texto_redigido = self.call_agent(agente_redator, entrada_do_agente_redator)
        return texto_redigido

    # Função auxiliar que envia uma mensagem para um agente via Runner e retorna a resposta final
    def call_agent(self, agent: Agent, message_text: str) -> str:
        # Cria um serviço de sessão em memória
        session_service = InMemorySessionService()
        # Cria uma nova sessão (você pode personalizar os IDs conforme necessário)
        # Usando o nome do agente específico para a app_name na sessão
        session = session_service.create_session(app_name=agent.name, user_id="user1", session_id="session1")
        # Cria um Runner para o agente
        runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
        # Cria o conteúdo da mensagem de entrada
        content = types.Content(role="user", parts=[types.Part(text=message_text)])

        final_response = ""
        # Itera assincronamente pelos eventos retornados durante a execução do agente
        # Nota: A execução síncrona é mais simples para este exemplo.
        # Para execução assíncrona, você usaria 'async for event in await runner.run_async(...):'
        # Aqui estamos usando a forma síncrona que o SDK adk.runners.Runner parece implicar
        # com base na sua estrutura original.
        # Se o runner.run() for um gerador síncrono, o loop 'for' está correto.
        # Se for um gerador assíncrono, o código precisaria ser ajustado para um contexto 'async'.
        # Assumindo que `runner.run` é síncrono com base no seu código original.
        for chunk in runner.run(user_id="user1", session_id="session1", new_message=content):
            if chunk.is_final_response():
                for part in chunk.content.parts:
                    if part.text is not None:
                        final_response += part.text
                        final_response += "\n"
            # Você pode adicionar tratamento para 'tool_code' ou 'tool_response' aqui se necessário
            # elif chunk.type == EventType.TOOL_CODE:
            #     print(f"Tool Code: {chunk.content.parts}")
            # elif chunk.type == EventType.TOOL_RESPONSE:
            #     print(f"Tool Response: {chunk.content.parts}")

        return final_response.strip() # .strip() para remover nova linha extra no final
