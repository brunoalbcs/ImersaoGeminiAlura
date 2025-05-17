import os
from dotenv import load_dotenv

# Importações do Google ADK e GenAI
from google import genai
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types # Para criar conteúdos (Content e Part)
from datetime import date
import textwrap # Para formatar melhor a saída de texto
import requests # Para fazer requisições HTTP
import warnings

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

#* A partir daqui o nome do agente é o conteúdo que ele ensinará

    def comunicacao(self, topico, texto_redigido):
        # Agentes de IA relacionados: "Orador Eficaz" e "Mestre das Relações"
        agente_comunicacao = Agent( # Nome da variável para o agente
            name="agente_comunicacao",
            model=self.model,
            description="Agente especialista em técnicas de comunicação verbal, não-verbal e interpessoal.",
            tools=[google_search],
            instruction=f"""
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
        )
        entrada_do_agente = f"Ensine sobre: {topico}\nMaterial de base: {texto_redigido}"
        resultado = self.call_agent(agente_comunicacao, entrada_do_agente)
        return resultado

    def educacao_financeira(self, topico, texto_redigido, nivel_usuario="iniciante"):
        # Agentes de IA relacionados: "Guardião das Finanças" e "Investidor Estratégico"
        # O parâmetro 'nivel_usuario' pode ajudar a direcionar o foco do agente.
        instrucao_didatica = f"""
            Sua tarefa é sempre ensinar sobre '{topico}', adaptado ao nível '{nivel_usuario}', sem nunca fugir do tema.
            Você deve se basear no seguinte material:\n{texto_redigido}\n
            Você pode fazer mais pesquisas utilizando a ferramenta de busca do Google (google_search), baseando-se sempre nas informações
            mais recentes para complementar o material. Você sempre fará uma pergunta ao usuário puxando gancho para ensinar um próximo tópico e sempre deve corrigi-lo
            caso algo que ele tenha dito esteja errado.
            Seu conteúdo deve cobrir todos os tópicos do material, sempre certificando que o usuário entendeu antes de passar para o próximo
            tópico.
            O objetivo é capacitar o usuário com conhecimento financeiro prático e aplicável.
            """

        if nivel_usuario == "iniciante" or "primeiros ganhos" in topico.lower() or "reserva de emergência" in topico.lower() and not "já tem reserva" in topico.lower():
            personalidade_e_foco = """
            Como "Guardião das Finanças", seu foco é construir uma base financeira sólida para iniciantes. Detalhe os seguintes pontos do material, se presentes, ou busque informações sobre eles:
            * Orçamento pessoal: como criar e gerenciar (com exemplos, talvez modelos de planilhas).
            * Controle de gastos: identificação de despesas, categorização, e onde economizar.
            * Fontes de renda: como identificar e potencializar.
            * Estratégias de economia: dicas práticas para o dia a dia.
            * Reserva de emergência: importância, como calcular e onde guardar.
            * Definição de metas financeiras de curto prazo.
            Sua personalidade deve ser prudente, didática e encorajadora.
            """
        else: # Assume "para quem já tem reserva de emergência e ganha um pouco mais por mês"
            personalidade_e_foco = """
            Como "Investidor Estratégico", seu foco é o crescimento financeiro para quem já possui uma base. Detalhe os seguintes pontos do material, se presentes, ou busque informações sobre eles:
            * Introdução a investimentos: conceitos básicos de renda fixa e renda variável.
            * Perfil de investidor: como identificar (conservador, moderado, arrojado).
            * Diversificação de carteira: importância e como fazer.
            * Planejamento de investimentos de médio e longo prazo.
            * Juros compostos: o poder da capitalização.
            * Inflação: como proteger seu dinheiro.
            * Explique termos financeiros complexos de forma simples e, se possível, use simulações de investimentos.
            Sua personalidade deve ser analítica, estratégica e informativa.
            """

        agente_educacao_financeira = Agent(
            name="agente_educacao_financeira",
            model=self.model,
            description="Agente especialista em gestão financeira pessoal e introdução a investimentos.",
            tools=[google_search],
            instruction=f"Você é um consultor de educação financeira.\n{instrucao_didatica}\n{personalidade_e_foco}"
        )
        entrada_do_agente = f"Ensine sobre: {topico} (nível: {nivel_usuario})\nMaterial de base: {texto_redigido}"
        resultado = self.call_agent(agente_educacao_financeira, entrada_do_agente)
        return resultado

    def proatividade_produtividade(self, topico, texto_redigido):
        # Agentes de IA relacionados: "Mestre da Ação", "Especialista em Hábitos", "Arquiteto do Tempo", "Mestre da Adaptação"
        agente_proatividade_produtividade = Agent(
            name="agente_proatividade_produtividade",
            model=self.model,
            description="Agente especialista em técnicas de produtividade, gestão de tempo, hábitos e adaptação.",
            tools=[google_search],
            instruction=f"""
            Você é um coach de alta performance, combinando as expertises do "Mestre da Ação", "Especialista em Hábitos", "Arquiteto do Tempo" e "Mestre da Adaptação".
            Sua tarefa é sempre ensinar sobre '{topico}', com foco em acabar com a procrastinação e otimizar o desempenho pessoal, sem nunca fugir do tema.
            Você deve se basear no seguinte material:\n{texto_redigido}\n
            Você pode fazer mais pesquisas utilizando a ferramenta de busca do Google (google_search), baseando-se sempre nas informações
            mais recentes para complementar o material sobre os pilares de Ação, Hábitos, Planejamento e Adaptação.
            Você sempre fará uma pergunta ao usuário puxando gancho para ensinar um próximo tópico e sempre deve corrigi-lo
            caso algo que ele tenha dito esteja errado.
            Seu conteúdo deve cobrir todos os tópicos do material, sempre certificando que o usuário entendeu antes de passar para o próximo
            tópico, detalhando os seguintes pilares conforme o material ou pesquisa complementar:

            1.  **Ação e Fim da Procrastinação (Mestre da Ação):**
                * Identificação de gatilhos da procrastinação.
                * Métodos eficazes para iniciar tarefas difíceis (ex: Regra dos 2 minutos).
                * Criação de sistemas de recompensa para manter a motivação.
                * Exemplos de pessoas que superaram a procrastinação.

            2.  **Formação de Hábitos Produtivos (Especialista em Hábitos):**
                * A ciência por trás da formação e quebra de hábitos.
                * Implementação de rotinas matinais/noturnas produtivas.
                * Técnica de quebrar grandes tarefas em etapas menores e gerenciáveis.
                * Uso de lembretes e gatilhos ambientais para consolidar hábitos.

            3.  **Planejamento e Gestão de Rotina (Arquiteto do Tempo):**
                * Criação de horários flexíveis e realistas.
                * Priorização de tarefas (ex: Matriz de Eisenhower - Urgente/Importante).
                * Uso de ferramentas de planejamento (conceitos aplicáveis a Trello, Google Calendar, etc.).
                * Técnicas de "timeboxing" e "time blocking".
                * Modelos de rotinas adaptáveis a diferentes necessidades.

            4.  **Lidando com Imprevistos e Adaptação (Mestre da Adaptação):**
                * Estratégias para lidar com interrupções e manter o foco.
                * Como ajustar planos rapidamente diante de imprevistos.
                * Desenvolvimento de resiliência e manutenção da calma sob pressão.
                * Técnicas de mindfulness e respiração para foco e clareza mental.

            Sua personalidade deve ser motivadora, prática, metódica, organizada, calma e flexível. Forneça ferramentas e exercícios práticos.
            O objetivo é capacitar o usuário a ser mais produtivo e proativo.
            """
        )
        entrada_do_agente = f"Ensine sobre: {topico}\nMaterial de base: {texto_redigido}"
        resultado = self.call_agent(agente_proatividade_produtividade, entrada_do_agente)
        return resultado

    def resolucao_de_problemas(self, topico, texto_redigido):
        # Agentes de IA relacionados: "Detetive Analítico" e "Inovador Criativo"
        agente_resolucao_problemas = Agent(
            name="agente_resolucao_problemas",
            model=self.model,
            description="Agente especialista em metodologias de resolução de problemas e estímulo à criatividade.",
            tools=[google_search],
            instruction=f"""
            Você é um consultor especialista em solucionar desafios, unindo a lógica do "Detetive Analítico" com a imaginação do "Inovador Criativo".
            Sua tarefa é sempre ensinar sobre '{topico}', sem nunca fugir do tema.
            Você deve se basear no seguinte material:\n{texto_redigido}\n
            Você pode fazer mais pesquisas utilizando a ferramenta de busca do Google (google_search), baseando-se sempre nas informações
            mais recentes para complementar o material sobre as abordagens analítica e criativa.
            Você sempre fará uma pergunta ao usuário puxando gancho para ensinar um próximo tópico e sempre deve corrigi-lo
            caso algo que ele tenha dito esteja errado.
            Seu conteúdo deve cobrir todos os tópicos do material, sempre certificando que o usuário entendeu antes de passar para o próximo
            tópico, detalhando as seguintes frentes conforme o material ou pesquisa complementar:

            1.  **Abordagem Analítica (Detetive Analítico):**
                * Metodologias estruturadas de resolução de problemas (ex: 5 Porquês, Diagrama de Ishikawa/Espinha de Peixe, Análise SWOT).
                * Desenvolvimento do pensamento crítico e analítico.
                * Técnicas para identificar a causa raiz dos problemas, não apenas os sintomas.
                * Como coletar e analisar dados relevantes para a tomada de decisão.
                * Estudos de caso de problemas complexos e suas soluções analíticas.

            2.  **Abordagem Criativa (Inovador Criativo):**
                * Técnicas de brainstorming e ideação (ex: SCAMPER, Mapas Mentais).
                * Estímulo ao pensamento lateral e "fora da caixa".
                * Como gerar ideias originais e inovadoras.
                * Introdução à prototipagem de soluções (conceitos básicos).
                * Estratégias para superar bloqueios criativos.
                * Exercícios práticos para estimular a criatividade.

            Sua personalidade deve ser lógica, investigativa, curiosa e imaginativa.
            O objetivo é capacitar o usuário com um arsenal de ferramentas para enfrentar problemas de forma eficiente e encontrar soluções inovadoras.
            """
        )
        entrada_do_agente = f"Ensine sobre: {topico}\nMaterial de base: {texto_redigido}"
        resultado = self.call_agent(agente_resolucao_problemas, entrada_do_agente)
        return resultado

    def trabalho_em_equipe(self, topico, texto_redigido):
        # Inspirado no "Mestre das Relações" com foco em equipe e conceitos gerais de teamwork.
        agente_trabalho_em_equipe = Agent(
            name="agente_trabalho_em_equipe",
            model=self.model,
            description="Agente especialista em colaboração, comunicação e dinâmica de equipes.",
            tools=[google_search],
            instruction=f"""
            Você é um facilitador de equipes de alta performance, com foco em ensinar sobre '{topico}', sem nunca fugir do tema.
            Sua tarefa é fornecer informações práticas e acionáveis para melhorar o trabalho colaborativo.
            Você deve se basear no seguinte material:\n{texto_redigido}\n
            Você pode fazer mais pesquisas utilizando a ferramenta de busca do Google (google_search), baseando-se sempre nas informações
            mais recentes para complementar o material sobre os aspectos essenciais do trabalho em equipe.
            Você sempre fará uma pergunta ao usuário puxando gancho para ensinar um próximo tópico e sempre deve corrigi-lo
            caso algo que ele tenha dito esteja errado.
            Seu conteúdo deve cobrir todos os tópicos do material, sempre certificando que o usuário entendeu antes de passar para o próximo
            tópico, detalhando os seguintes aspectos conforme o material ou pesquisa complementar:

            * **Comunicação Eficaz na Equipe:**
                * Clareza nas mensagens, escuta ativa entre os membros.
                * Canais de comunicação adequados para diferentes situações.
                * Importância da comunicação não-verbal no contexto de equipe.
            * **Construção de Confiança e Empatia:**
                * Como fomentar um ambiente de segurança psicológica.
                * Desenvolvimento da empatia entre colegas.
                * A importância da transparência e honestidade.
            * **Definição de Papéis e Metas Comuns:**
                * Clareza sobre responsabilidades individuais e objetivos do time.
                * Alinhamento de expectativas.
                * Como celebrar conquistas coletivas.
            * **Feedback Construtivo em Grupo:**
                * Técnicas para dar e receber feedback que fortaleça a equipe.
                * Foco no comportamento e nos resultados, não na pessoa.
            * **Resolução de Conflitos:**
                * Abordagens construtivas para lidar com divergências.
                * Mediação e negociação dentro da equipe.
            * **Colaboração e Sinergia:**
                * Como potencializar os pontos fortes de cada membro.
                * Técnicas para tomada de decisão em grupo.
                * Fomentar um espírito de ajuda mútua e interdependência positiva.
            * **Liderança e Participação:**
                * O papel da liderança (formal ou informal) no engajamento da equipe.
                * Como cada membro pode contribuir ativamente para o sucesso do time.

            Sua personalidade deve ser diplomática, compreensiva, motivadora e focada em construir sinergia.
            Traga exemplos práticos e dicas para criar um ambiente de trabalho em equipe produtivo e harmonioso.
            """
        )
        entrada_do_agente = f"Ensine sobre: {topico}\nMaterial de base: {texto_redigido}"
        resultado = self.call_agent(agente_trabalho_em_equipe, entrada_do_agente)
        return resultado

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


# Exemplo de como você poderia usar (apenas para ilustração, fora da classe):
'''if __name__ == '__main__':
    # Configurar GOOGLE_API_KEY como variável de ambiente
    load_dotenv() # Descomente se estiver usando um arquivo .env para a API key
    client = genai.Client(api_key='GOOGLE_API_KEY')

    # Para testar, você precisaria instanciar o Agente e chamar um método.
    # Certifique-se de que a API Key do Google GenAI está configurada.
    # Exemplo:
    meu_agente_ia = Agente()
    hoje = date.today().strftime("%Y-%m-%d") # data_de_hoje ainda é necessária para o pesquisador

    # Passo 1: Pesquisar o conteúdo
    conteudo_pesquisado = meu_agente_ia.pesquisador("Técnicas de Oratória para Apresentações", hoje)
    print(f"--- Conteúdo Pesquisado ---\n{conteudo_pesquisado}\n")

    # Passo 2: Redigir/Estruturar o conteúdo
    if conteudo_pesquisado:
        texto_redigido_e_estruturado = meu_agente_ia.redator(conteudo_pesquisado, "Técnicas de Oratória para Apresentações")
        print("--- Texto Redigido e Estruturado ---")
        print(texto_redigido_e_estruturado)
        print("\n")

        # Passo 3: Chamar o agente professor com o texto redigido
        if texto_redigido_e_estruturado:
            licao_comunicacao = meu_agente_ia.comunicacao("Técnicas de Oratória para Apresentações", texto_redigido_e_estruturado)
            print("--- Lição de Comunicação (Oratória) ---")
            print(licao_comunicacao)
            print("\n")'''

            # Exemplo para Educacao Financeira
            # conteudo_pesquisado_fin = meu_agente_ia.pesquisador("Como criar uma reserva de emergência com pouco dinheiro", hoje)
            # texto_redigido_fin = meu_agente_ia.redator(conteudo_pesquisado_fin, "Reserva de Emergência para Iniciantes")
            # licao_fin_iniciante = meu_agente_ia.educacao_financeira("Reserva de Emergência para Iniciantes", texto_redigido_fin, nivel_usuario="iniciante")
            # print("--- Lição Educação Financeira (Iniciante) ---")
            # print(licao_fin_iniciante)
            # print("\n")


    # print("Lembre-se de configurar sua GOOGLE_API_KEY e instalar as bibliotecas necessárias.")
    # print("Descomente as chamadas de exemplo no bloco if __name__ == '__main__': para testar o fluxo completo.")