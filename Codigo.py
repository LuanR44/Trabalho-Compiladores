import os

# Função para limpar a tela, compatível com Windows e Unix
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# Função para exibir o título do projeto com arte ASCII
def exibir_titulo():
    limpar_tela()
    print("""
    ╔════════════════════════════════════════════════╗
    ║          PROJETO DE COMPILADORES               ║
    ║   Analisador Léxico e Sintático de Linguagem   ║
    ║              Inspirada em Futebol              ║
    ╚════════════════════════════════════════════════╝
    """)

# Função para exibir o menu principal e retornar a opção escolhida pelo usuário
def exibir_menu():
    print("\nMenu Principal:\n")
    print("1. Inserir e analisar código")
    print("2. Integrantes")
    print("3. Sair")
    return input("\nEscolha uma opção: ")



# Função para exibir os integrantes do grupo
def exibir_integrantes():
    limpar_tela()
    print("""
    ╔════════════════════════════════════════════════╗
    ║             INTEGRANTES DO GRUPO               ║
    ╚════════════════════════════════════════════════╝
    """)
    print("1. João Pedro Moreno Ayres")
    print("2. Laura Lonardoni Paulino Schiavon")
    print("3. Luan Ribeiro Sancassani")
    print("4. Rahul Sbaraglini Couto")
    input("\nPressione Enter para voltar ao menu...")



# Inicializa a lista de erros para armazenar mensagens de erro de sintaxe
erros = []

# Função principal do analisador sintático, que verifica a estrutura geral do código
def analisador_sintatico(linhas_codigo):
    index = 0
    # Verifica se o programa começa com a palavra-chave "COMECAPARTIDA"
    if linhas_codigo[index] == "COMECAPARTIDA":
        index += 1  # Avança para o próximo índice
        index = analisar_corpo(linhas_codigo, index)  # Analisa o corpo do programa
        
        # Verifica se o programa termina com "FIMDEJOGO"
        if index < len(linhas_codigo) and linhas_codigo[index] == "FIMDEJOGO":
            if not erros:  # Só exibe "Sintaxe correta!" se não houver erros
                print("Sintaxe correta!")
        else:
            erros.append("Erro: FIMDEJOGO esperado no final do programa.")
    else:
        erros.append("Erro: COMECAPARTIDA esperado no início do programa.")

    # Exibe os erros acumulados, se houver
    if erros:
        print("Erros sintáticos:")
        for erro in erros:
            print(erro)


# Função que analisa o corpo do programa, processando cada linha até "FIMDEJOGO"
def analisar_corpo(linhas_codigo, index):
    while index < len(linhas_codigo) and linhas_codigo[index] != "FIMDEJOGO":
        linha = linhas_codigo[index].strip()  # Remove espaços em branco nas extremidades

        # Verifica se a linha é uma declaração de variável
        if linha.startswith("Escalacao"):
            index = analisar_declaracao_variavel(linha, index)
        # Verifica se a linha é uma atribuição de valor
        elif "=" in linha:
            index = analisar_atribuicao(linha, index)
        # Verifica se a linha é um comando de entrada/saída
        elif linha.startswith("RecebePasse") or linha.startswith("Placar"):
            index = analisar_comando_io(linha, index)
        # Se o comando não for reconhecido, adiciona um erro
        else:
            erros.append(f"Erro de sintaxe na linha {index + 1}: Comando desconhecido.")
            index += 1

    return index

# Função que analisa declarações de variáveis, esperando "Escalacao <tipo> <nome>;"
def analisar_declaracao_variavel(linha, index):
    partes = linha.split()
    # Verifica se a declaração segue o padrão: Escalacao golint/golreal nomeVariavel;
    if len(partes) == 3 and partes[0] == "Escalacao" and partes[1] in ["golint", "golreal"] and partes[2].endswith(";"):
        return index + 1
    else:
        erros.append(f"Erro na declaração de variável na linha {index + 1}.")
        return index + 1

# Função que analisa atribuições, verificando a presença do operador "=" e o ";" no final
def analisar_atribuicao(linha, index):
    if linha.endswith(";"):
        partes = linha.split("=")
        # Verifica se a atribuição está no formato esperado: variavel = valor;
        if len(partes) == 2 and partes[0].strip() and partes[1].strip():
            return index + 1
        else:
            erros.append(f"Erro de atribuição na linha {index + 1}.")
            return index + 1
    else:
        erros.append(f"Erro: Linha {index + 1} deve terminar com ';'.")
        return index + 1

# Função que analisa comandos de entrada/saída, como RecebePasse(variavel); e Placar(variavel);
def analisar_comando_io(linha, index):
    if linha.startswith("RecebePasse(") or linha.startswith("Placar("):
        # Verifica se o comando termina com ");"
        if linha.endswith(");"):
            return index + 1
        else:
            erros.append(f"Erro no comando de entrada/saída na linha {index + 1}.")
            return index + 1
    else:
        erros.append(f"Erro: Comando desconhecido na linha {index + 1}.")
        return index + 1

# Função principal que executa o programa com o menu e loop
def main():
    while True:
        exibir_titulo()
        opcao = exibir_menu()

        if opcao == "1":
            limpar_tela()
            print("\nInsira o código da linguagem linha por linha (pressione Enter em uma linha vazia para finalizar):")
            linhas_codigo = []
            while True:
                linha = input()
                if linha == "":
                    break
                linhas_codigo.append(linha.strip())

            # Limpa erros antigos antes de iniciar nova análise
            global erros
            erros = []

            # Executa o analisador sintático com o código fornecido pelo usuário
            limpar_tela()
            print("\nAnalisando o código...\n")
            analisador_sintatico(linhas_codigo)

            # Exibe uma pausa antes de retornar ao menu
            input("\nPressione Enter para voltar ao menu...")
        
        elif opcao == "2":
            exibir_integrantes()  # Chama a função para exibir os integrantes do grupo

        elif opcao == "3":
            limpar_tela()
            input("\nObrigado por utilizar! Pressione Enter para Sair...")
            limpar_tela()
            break

        else:
            print("Opção inválida. Tente novamente.")


# Executa o programa
main()
