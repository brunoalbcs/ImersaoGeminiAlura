# from diretorio.arquivo import NomeDaClasse
# from agentes.agente import Agent  # não precisa importar isso aqui
import skills.comunicacao
import skills.educacao_financeira
import skills.proatividade_produtividade
import skills.resolucao_de_problemas
import skills.trabalho_em_equipe

if __name__ == "__main__":
    
    tema = 0
    while tema not in [1,2,3,4,5]:
        tema = int(input('SELECIONE O TEMA DE ESTUDO:' \
        '\n1. Comunicação' \
        '\n2. Educação Financeira' \
        '\n3. Proatividade e Produtividade' \
        '\n4. Resolução de Problemas' \
        '\n5. Trabalho em Equipe\n'))
        if tema not in [1,2,3,4,5]:
            print("\nOPÇÃO INVÁLIDA! DIGITE APENAS UM NÚMERO DE 1 A 5")

    match tema:
        case 1:
            skills.comunicacao.iniciar_aula()
        case 2:
            skills.educacao_financeira.iniciar_aula()
        case 3:
            skills.proatividade_produtividade.iniciar_aula()
        case 4:
            skills.resolucao_de_problemas.iniciar_aula()
        case 5:
            skills.trabalho_em_equipe.iniciar_aula()
        case _:
            print("Erro no match case linha 30.")

