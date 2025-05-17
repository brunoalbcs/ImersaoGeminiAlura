# class que vai fazer todo o formulário e retornar a resposta em formato de texto.
class Form():
    def __init__(self):
        self.respostas = {}

    def _validar_escala(self, resposta):
        resposta = resposta.lower()
        if resposta in ['1', '2', '3', '4', '5', 'a', 'b', 'c', 'd', 'e']:
            return True
        return False

    def _converter_escala(self, resposta, opcoes):
        resposta = resposta.lower()
        if resposta.isdigit() and 1 <= int(resposta) <= 5:
            indice = int(resposta) - 1
            return opcoes[indice]
        elif resposta in ['a', 'b', 'c', 'd', 'e']:
            indice = ord(resposta) - ord('a')
            return opcoes[indice]
        return None

    def comunicacao(self):
        self.respostas['Comunicação'] = {}
        perguntas = [
            ('Você se considera uma pessoa que se expressa de forma clara e objetiva?',
             ['Sim, sempre tento ser direto(a) e evitar ambiguidades.',
              'Geralmente sim, mas às vezes tenho dificuldade em ser conciso(a).',
              'Às vezes sim, depende do assunto e da pessoa com quem estou falando.',
              'Não me considero muito claro(a) e objetivo(a) na comunicação.',
              'Prefiro uma comunicação mais indireta e atenta às nuances.']),
            ('Como você costuma lidar com conversas difíceis ou com pessoas que têm opiniões muito diferentes das suas?',
             ['Mantenho a calma, ouço atentamente e tento encontrar pontos em comum.',
              'Evito o confronto direto e tento mudar de assunto.',
              'Defendo meu ponto de vista com firmeza, mesmo que gere debate.',
              'Sinto-me desconfortável e tento encerrar a conversa o mais rápido possível.',
              'Busco entender a perspectiva do outro, mesmo que não concorde.']),
            ('Você se considera um bom ouvinte? O que você faz para garantir que entendeu a mensagem do outro?',
             ['Sim, presto atenção, faço perguntas e resumo o que ouvi para confirmar.',
              'Geralmente sim, mas às vezes me distraio ou interrompo sem querer.',
              'Acredito que ouço bem, mas nem sempre verifico se entendi corretamente.',
              'Tenho dificuldade em manter a atenção por muito tempo durante a escuta.',
              'Priorizo expressar minhas próprias ideias e nem sempre foco em ouvir ativamente.']),
            ('Em que situações você sente mais dificuldade em se comunicar?',
             ['Ao falar em público ou apresentar minhas ideias para um grupo grande.',
              'Ao expressar sentimentos ou emoções de forma clara.',
              'Ao dar ou receber feedback negativo.',
              'Ao comunicar-me com pessoas muito diferentes de mim (cultura, idade, etc.).',
              'Não sinto grandes dificuldades em nenhuma situação específica.']),
            ('Em uma escala de 1 a 5, como você avalia sua habilidade de transmitir suas ideias de forma eficaz para diferentes tipos de pessoas?',
             ['1 - Tenho muita dificuldade em fazer com que as pessoas entendam minhas ideias.',
              '2 - Às vezes consigo, mas nem sempre minha mensagem é clara para todos.',
              '3 - Geralmente consigo transmitir minhas ideias de forma compreensível.',
              '4 - Adapto minha comunicação para diferentes públicos e sou bem compreendido(a).',
              '5 - Sou um(a) comunicador(a) nato(a) e minhas ideias sempre são bem recebidas.'])
        ]

        for i, (pergunta, opcoes) in enumerate(perguntas):
            while True:
                print(f"\n{pergunta}\n")
                for j, opcao in enumerate(opcoes):
                    letra = chr(ord('a') + j)
                    print(f"{letra}) {opcao}")
                resposta = input("\nSua resposta: ").lower()

                if i == 4: # Pergunta de escala
                    if self._validar_escala(resposta):
                        self.respostas['Comunicação'][f'Pergunta {i+1}'] = {
                            'pergunta': pergunta,
                            'resposta': self._converter_escala(resposta, opcoes)
                        }
                        break
                    else:
                        print("OPÇÃO INVÁLIDA! Digite um número de 1 a 5 ou uma letra de 'a' a 'e'.")
                elif resposta in [chr(ord('a') + k) for k in range(len(opcoes))]:
                    self.respostas['Comunicação'][f'Pergunta {i+1}'] = {
                        'pergunta': pergunta,
                        'resposta': opcoes[ord(resposta) - ord('a')]
                    }
                    break
                else:
                    print("OPÇÃO INVÁLIDA! Digite apenas uma letra correspondente à opção.")

        return self.exibir_respostas()

    def educacao_financeira(self):
        self.respostas['Educação Financeira'] = {}
        perguntas = [
            ('Como você costuma controlar seus gastos mensais?',
             ['Anoto todos os meus gastos detalhadamente.',
              'Tenho um orçamento fixo e tento segui-lo.',
              'Acompanho meus gastos de forma geral, sem muitos detalhes.',
              'Não costumo controlar meus gastos de forma sistemática.',
              'Outro método (especifique).']),
            ('Você possui alguma reserva de emergência? Se sim, qual o valor aproximado em relação aos seus gastos mensais?',
             ['Sim, o equivalente a mais de 6 meses dos meus gastos.',
              'Sim, o equivalente a cerca de 3 a 6 meses dos meus gastos.',
              'Sim, o equivalente a menos de 3 meses dos meus gastos.',
              'Não possuo reserva de emergência no momento.',
              'Estou começando a construir uma reserva de emergência.']),
            ('Você investe seu dinheiro atualmente? Se sim, em quais tipos de investimentos?',
             ['Sim, em diversos tipos de investimentos (renda fixa e variável).',
              'Sim, principalmente em renda fixa (poupança, CDB, etc.).',
              'Sim, principalmente em renda variável (ações, fundos imobiliários, etc.).',
              'Não invisto meu dinheiro atualmente.',
              'Estou começando a aprender sobre investimentos.']),
            ('Qual sua principal dificuldade em relação ao planejamento financeiro?',
             ['Dificuldade em controlar gastos impulsivos.',
              'Falta de conhecimento sobre como planejar e investir.',
              'Renda instável que dificulta o planejamento.',
              'Falta de tempo para me dedicar ao planejamento financeiro.',
              'Não sinto grandes dificuldades com meu planejamento financeiro.']),
            ('Em uma escala de 1 a 5 (sendo 1 muito baixo e 5 muito alto), como você avalia seu conhecimento sobre juros compostos?',
             ['1 - Nunca ouvi falar ou não entendo o conceito.',
              '2 - Já ouvi falar, mas não sei como funciona na prática.',
              '3 - Tenho uma ideia básica de como funciona.',
              '4 - Entendo bem como funciona e considero seus efeitos.',
              '5 - Tenho um conhecimento avançado sobre juros compostos e seu impacto.'])
        ]

        for i, (pergunta, opcoes) in enumerate(perguntas):
            while True:
                print(f"\n{pergunta}\n")
                for j, opcao in enumerate(opcoes):
                    letra = chr(ord('a') + j)
                    print(f"{letra}) {opcao}")
                resposta = input("\nSua resposta: ").lower()

                if i == 4: # Pergunta de escala
                    if self._validar_escala(resposta):
                        self.respostas['Educação Financeira'][f'Pergunta {i+1}'] = {
                            'pergunta': pergunta,
                            'resposta': self._converter_escala(resposta, opcoes)
                        }
                        break
                    else:
                        print("OPÇÃO INVÁLIDA! Digite um número de 1 a 5 ou uma letra de a a e.")
                elif resposta in [chr(ord('a') + k) for k in range(len(opcoes))]:
                    self.respostas['Educação Financeira'][f'Pergunta {i+1}'] = {
                        'pergunta': pergunta,
                        'resposta': opcoes[ord(resposta) - ord('a')]
                    }
                    break
                elif resposta == 'e' and i == 0: # Outro método na primeira pergunta
                    outro = input("Especifique seu método: ")
                    self.respostas['Educação Financeira'][f'Pergunta {i+1}'] = {
                        'pergunta': pergunta,
                        'resposta': f"{opcoes[4]} {outro}"
                    }
                    break
                else:
                    print("OPÇÃO INVÁLIDA! Digite apenas uma letra correspondente à opção.")

        return self.exibir_respostas()

    def proatividade_produtividade(self):
        self.respostas['Proatividade e Produtividade'] = {}
        perguntas = [
            ('Quando você tem uma ideia para melhorar algo no seu dia a dia ou trabalho, qual sua primeira atitude?',
             ['Coloco a ideia em prática imediatamente, se possível.',
              'Anoto a ideia e planejo como implementá-la.',
              'Compartilho a ideia com outras pessoas para obter feedback.',
              'Penso sobre a ideia, mas geralmente não a coloco em prática.',
              'Espero que alguém mais tome a iniciativa.']),
            ('Como você costuma priorizar suas tarefas quando tem muitas coisas para fazer?',
             ['Priorizo as tarefas com prazos mais urgentes e importantes.',
              'Faço primeiro as tarefas mais fáceis para ganhar motivação.',
              'Sigo uma lista de tarefas pré-definida, sem muita flexibilidade.',
              'Acabo fazendo um pouco de tudo, sem uma prioridade clara.',
              'Peço ajuda para definir as prioridades.']),
            ('Você utiliza alguma ferramenta ou método para organizar suas atividades e aumentar sua produtividade? Qual?',
             ['Sim, utilizo aplicativos de gerenciamento de tarefas (Trello, Asana, etc.).',
              'Sim, utilizo agendas físicas ou digitais para planejar meu dia.',
              'Sim, utilizo técnicas específicas (Pomodoro, GTD, etc.).',
              'Não utilizo nenhuma ferramenta ou método específico.',
              'Utilizo métodos informais, como listas de papel.']),
            ('Como você lida com distrações quando precisa se concentrar em uma tarefa importante?',
             ['Busco um ambiente silencioso e desligo notificações.',
              'Faço pausas regulares para evitar o esgotamento mental.',
              'Tenho dificuldade em evitar distrações e isso afeta minha produtividade.',
              'Priorizo terminar a tarefa o mais rápido possível, ignorando as distrações.',
              'Utilizo aplicativos ou ferramentas para bloquear distrações.']),
            ('Em uma escala de 1 a 5, como você avalia sua capacidade de iniciar tarefas sem precisar de muita motivação externa?',
             ['1 - Quase sempre preciso de um impulso externo para começar.',
              '2 - Geralmente preciso de um pouco de motivação para iniciar.',
              '3 - Consigo iniciar a maioria das tarefas sem muita dificuldade.',
              '4 - Tenho facilidade em iniciar tarefas, mesmo as mais desafiadoras.',
              '5 - Sou altamente proativo e raramente preciso de motivação externa.'])
        ]

        for i, (pergunta, opcoes) in enumerate(perguntas):
            while True:
                print(f"\n{pergunta}\n")
                for j, opcao in enumerate(opcoes):
                    letra = chr(ord('a') + j)
                    print(f"{letra}) {opcao}")
                resposta = input("\nSua resposta: ").lower()

                if i == 4: # Pergunta de escala
                    if self._validar_escala(resposta):
                        self.respostas['Proatividade e Produtividade'][f'Pergunta {i+1}'] = {
                            'pergunta': pergunta,
                            'resposta': self._converter_escala(resposta, opcoes)
                        }
                        break
                    else:
                        print("OPÇÃO INVÁLIDA! Digite um número de 1 a 5 ou uma letra de a a e.")
                elif resposta in [chr(ord('a') + k) for k in range(len(opcoes))]:
                    self.respostas['Proatividade e Produtividade'][f'Pergunta {i+1}'] = {
                        'pergunta': pergunta,
                        'resposta': opcoes[ord(resposta) - ord('a')]
                    }
                    break
                elif resposta == 'a' and i == 2: # Especificar ferramenta
                    ferramenta = input("Qual aplicativo você utiliza? ")
                    self.respostas['Proatividade e Produtividade'][f'Pergunta {i+1}'] = {
                        'pergunta': pergunta,
                        'resposta': f"{opcoes[0]} {ferramenta}"
                    }
                    break
                elif resposta == 'b' and i == 2: # Especificar agenda
                    agenda = input("Qual tipo de agenda você utiliza? ")
                    self.respostas['Proatividade e Produtividade'][f'Pergunta {i+1}'] = {
                        'pergunta': pergunta,
                        'resposta': f"{opcoes[1]} {agenda}"
                    }
                    break
                elif resposta == 'c' and i == 2: # Especificar técnica
                    tecnica = input("Qual técnica você utiliza? ")
                    self.respostas['Proatividade e Produtividade'][f'Pergunta {i+1}'] = {
                        'pergunta': pergunta,
                        'resposta': f"{opcoes[2]} {tecnica}"
                    }
                    break
                elif resposta == 'e' and i == 2: # Especificar método informal
                    metodo = input("Qual método informal você utiliza? ")
                    self.respostas['Proatividade e Produtividade'][f'Pergunta {i+1}'] = {
                        'pergunta': pergunta,
                        'resposta': f"{opcoes[4]} {metodo}"
                    }
                    break
                else:
                    print("OPÇÃO INVÁLIDA! Digite apenas uma letra correspondente à opção.")

        return self.exibir_respostas()

    def resolucao_de_problemas(self):
        self.respostas['Resolução de Problemas'] = {}
        perguntas = [
            ('Qual sua primeira reação ao se deparar com um problema complexo?',
             ['Sinto-me desafiado(a) e motivado(a) a encontrar uma solução.',
              'Sinto-me um pouco ansioso(a), mas procuro abordá-lo de forma lógica.',
              'Fico frustrado(a) e tento evitar ou adiar a resolução.',
              'Peço ajuda imediatamente, pois me sinto incapaz de resolver sozinho(a).',
              'Analiso o problema com calma para entender suas diferentes partes.']),
            ('Como você costuma abordar a busca por soluções para um problema?',
             ['Pesquiso informações e busco diferentes perspectivas.',
              'Faço um brainstorming individual para gerar ideias.',
              'Discuto o problema com outras pessoas para obter sugestões.',
              'Sigo minha intuição e tento a primeira solução que me vem à mente.',
              'Tento aplicar soluções que já funcionaram em problemas semelhantes.']),
            ('Você costuma analisar as causas de um problema antes de tentar solucioná-lo? Como você faz isso?',
             ['Sim, investigo as possíveis causas através de perguntas e análise de dados.',
              'Geralmente sim, mas de forma mais intuitiva e menos estruturada.',
              'Tento resolver o problema o mais rápido possível, sem focar muito nas causas.',
              'Acredito que já sei a causa e foco em encontrar a solução.',
              'Peço ajuda para identificar as causas do problema.']),
            ('Como você lida com a frustração quando as primeiras tentativas de solucionar um problema não funcionam?',
             ['Persisto e tento diferentes abordagens até encontrar uma solução.',
              'Faço uma pausa para clarear a mente e tento novamente depois.',
              'Sinto-me desmotivado(a) e tenho vontade de desistir.',
              'Peço ajuda de outras pessoas para encontrar novas ideias.',
              'Analiso o que não funcionou para aprender com os erros e tentar algo diferente.']),
            ('Em uma escala de 1 a 5, como você avalia sua capacidade de encontrar soluções criativas e eficazes para problemas?',
             ['1 - Geralmente tenho dificuldade em encontrar boas soluções para problemas.',
              '2 - Consigo encontrar soluções, mas nem sempre são as mais criativas ou eficazes.',
              '3 - Sou capaz de encontrar soluções funcionais para a maioria dos problemas.',
              '4 - Costumo encontrar soluções criativas e eficazes, mesmo para problemas complexos.',
              '5 - Sou um(a) excelente solucionador(a) de problemas e minhas soluções são inovadoras.'])
        ]

        for i, (pergunta, opcoes) in enumerate(perguntas):
            while True:
                print(f"\n{pergunta}\n")
                for j, opcao in enumerate(opcoes):
                    letra = chr(ord('a') + j)
                    print(f"{letra}) {opcao}")
                resposta = input("\nSua resposta: ").lower()

                if i == 4: # Pergunta de escala
                    if self._validar_escala(resposta):
                        self.respostas['Resolução de Problemas'][f'Pergunta {i+1}'] = {
                            'pergunta': pergunta,
                            'resposta': self._converter_escala(resposta, opcoes)
                        }
                        break
                    else:
                        print("OPÇÃO INVÁLIDA! Digite um número de 1 a 5 ou uma letra de a a e.")
                elif resposta in [chr(ord('a') + k) for k in range(len(opcoes))]:
                    self.respostas['Resolução de Problemas'][f'Pergunta {i+1}'] = {
                        'pergunta': pergunta,
                        'resposta': opcoes[ord(resposta) - ord('a')]
                    }
                    break
                elif resposta == 'a' and i == 2: # Especificar como analisa as causas
                    como = input("Como você faz essa investigação? ")
                    self.respostas['Resolução de Problemas'][f'Pergunta {i+1}'] = {
                        'pergunta': pergunta,
                        'resposta': f"{opcoes[0]} {como}"
                    }
                    break
                elif resposta == 'e' and i == 2: # Especificar ajuda para identificar causas
                    ajuda_como = input("Quem te ajuda a identificar as causas? ")
                    self.respostas['Resolução de Problemas'][f'Pergunta {i+1}'] = {
                        'pergunta': pergunta,
                        'resposta': f"{opcoes[4]} {ajuda_como}"
                    }
                    break
                else:
                    print("OPÇÃO INVÁLIDA! Digite apenas uma letra correspondente à opção.")

        return self.exibir_respostas()

    def trabalho_em_equipe(self):
        self.respostas['Trabalho em Equipe'] = {}
        perguntas = [
            ('Em um projeto em grupo, qual o papel que você geralmente assume?',
             ['Líder, tomando a iniciativa e coordenando as atividades.',
              'Executor, focando em realizar as tarefas designadas de forma eficiente.',
              'Mediador, buscando o consenso e a harmonia entre os membros.',
              'Observador, preferindo acompanhar o trabalho dos outros antes de agir.',
              'Contribuidor criativo, trazendo novas ideias e perspectivas.']),
            ('Como você lida com opiniões diferentes das suas em um ambiente de equipe?',
             ['Defendo meu ponto de vista com argumentos sólidos.',
              'Escuto atentamente as outras opiniões e tento encontrar um meio-termo.',
              'Aceito a opinião da maioria para evitar conflitos.',
              'Sinto-me desconfortável e prefiro não expressar minha opinião.',
              'Analiso os diferentes pontos de vista para chegar à melhor solução em conjunto.']),
            ('O que você considera mais importante para o sucesso de um trabalho em equipe?',
             ['Uma liderança forte e clara.',
              'Uma comunicação aberta e honesta entre os membros.',
              'A divisão clara de tarefas e responsabilidades.',
              'O respeito e a colaboração entre os membros.',
              'Metas bem definidas e um plano de ação claro.']),
            ('Como você reage quando um membro da equipe não está cumprindo suas responsabilidades?',
             ['Abordo a pessoa diretamente e tento entender a situação.',
              'Comunico a situação ao líder da equipe ou responsável.',
              'Tento compensar a falta do colega para não prejudicar o projeto.',
              'Fico frustrado(a), mas não costumo fazer nada a respeito.',
              'Discuto a situação com os outros membros da equipe para encontrar uma solução.']),
            ('Em uma escala de 1 a 5, como você avalia sua capacidade de colaborar e contribuir em um time?',
             ['1 - Prefiro trabalhar sozinho(a) e tenho dificuldade em colaborar.',
              '2 - Colaboro quando necessário, mas não é minha preferência.',
              '3 - Contribuo ativamente e me sinto confortável trabalhando em equipe.',
              '4 - Sou um(a) colaborador(a) eficaz e busco sempre o melhor para o time.',
              '5 - Sou um(a) excelente jogador(a) de equipe e inspiro a colaboração.'])
        ]

        for i, (pergunta, opcoes) in enumerate(perguntas):
            while True:
                print(f"\n{pergunta}\n")
                for j, opcao in enumerate(opcoes):
                    letra = chr(ord('a') + j)
                    print(f"{letra}) {opcao}")
                resposta = input("\nSua resposta: ").lower()

                if i == 4: # Pergunta de escala
                    if self._validar_escala(resposta):
                        self.respostas['Trabalho em Equipe'][f'Pergunta {i+1}'] = {
                            'pergunta': pergunta,
                            'resposta': self._converter_escala(resposta, opcoes)
                        }
                        break
                    else:
                        print("OPÇÃO INVÁLIDA! Digite um número de 1 a 5 ou uma letra de a a e.")
                elif resposta in [chr(ord('a') + k) for k in range(len(opcoes))]:
                    self.respostas['Trabalho em Equipe'][f'Pergunta {i+1}'] = {
                        'pergunta': pergunta,
                        'resposta': opcoes[ord(resposta) - ord('a')]
                    }
                    break
                else:
                    print("OPÇÃO INVÁLIDA! Digite apenas uma letra correspondente à opção.")

        return self.exibir_respostas()

    def exibir_respostas(self):
        texto_resposta = "Conhecendo o usuário:\n\n"
        for skill, perguntas in self.respostas.items():
            texto_resposta += f"### {skill} ###\n\n"
            for pergunta_num, resposta_dict in perguntas.items():
                texto_resposta += f"Pergunta: {resposta_dict['pergunta']}\n"
                texto_resposta += f"Resposta: {resposta_dict['resposta']}\n\n"
        return texto_resposta

