import os
import re  # Importa o módulo re para usar expressões regulares

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

# Inicializa as listas de erros para armazenar mensagens de erro léxico e sintático
erros_lexicos = []
erros = []

# Função de análise léxica que verifica cada linha em busca de tokens válidos ou erros léxicos
def analisador_lexico(linhas_codigo):
    tokens = []
    # Define os padrões de tokens usando expressões regulares
    token_specification = [
        ('COMENTARIO', r'//.*'),                   # Comentários
        ('NUM_REAL',   r'\d+\.\d+'),               # Números reais
        ('NUM_INT',    r'\d+'),                    # Números inteiros
        ('ID',         r'[A-Za-z_][A-Za-z0-9_]*'), # Identificadores
        ('OP_ARIT',    r'[+\-*/]'),                # Operadores aritméticos
        ('OP_ATRIB',   r'='),                      # Operador de atribuição
        ('ABRE_PAREN', r'\('),                     # Parênteses de abertura
        ('FECHA_PAREN', r'\)'),                    # Parênteses de fechamento
        ('SIMBOLO',    r'[;]'),                    # Símbolos especiais
        ('ESPACO',     r'\s+'),                    # Espaços em branco
        ('ERRO',       r'.'),                      # Qualquer outro caractere
    ]
    # Compila as expressões regulares
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    get_token = re.compile(tok_regex).match

    linha_num = 1
    for linha in linhas_codigo:
        posicao = 0
        mo = get_token(linha)
        while mo is not None:
            tipo = mo.lastgroup
            valor = mo.group(tipo)
            if tipo == 'ESPACO' or tipo == 'COMENTARIO':
                pass  # Ignora espaços em branco e comentários
            elif tipo == 'ERRO':
                erros_lexicos.append(f"Erro léxico na linha {linha_num}: Caractere inválido '{valor}'")
            else:
                tokens.append((tipo, valor, linha_num))
            posicao = mo.end()
            mo = get_token(linha, posicao)
        linha_num += 1
    return tokens

# Variáveis globais para o analisador sintático
token_atual = None
posicao_token = 0
tokens = []

# Função para avançar para o próximo token
def proximo_token():
    global posicao_token, token_atual
    if posicao_token < len(tokens):
        token_atual = tokens[posicao_token]
        posicao_token += 1
    else:
        token_atual = ('EOF', '', tokens[-1][2] if tokens else 0)  # Token de fim de arquivo

# Função principal do analisador sintático, que verifica a estrutura geral do código
def analisador_sintatico(token_list):
    global tokens, posicao_token, token_atual, erros
    tokens = token_list
    posicao_token = 0
    erros = []
    proximo_token()

    # Verifica se o programa começa com a palavra-chave "COMECAPARTIDA"
    if token_atual[1] == "COMECAPARTIDA":
        proximo_token()  # Avança para o próximo token
        analisar_corpo()
        # Verifica se o programa termina com "FIMDEJOGO"
        if token_atual[1] == "FIMDEJOGO":
            proximo_token()
            if token_atual[0] != 'EOF':
                erros.append(f"Erro: Tokens inesperados após 'FIMDEJOGO' na linha {token_atual[2]}.")
        else:
            erros.append(f"Erro: 'FIMDEJOGO' esperado na linha {token_atual[2]}.")
    else:
        erros.append(f"Erro: 'COMECAPARTIDA' esperado na linha {token_atual[2]}.")

    # Exibe os erros acumulados, se houver
    if erros_lexicos:
        print("Erros léxicos:")
        for erro in erros_lexicos:
            print(erro)

    if erros:
        if not erros_lexicos:
            print("Nenhum erro léxico encontrado.")
        print("\nErros sintáticos:")
        for erro in erros:
            print(erro)
    elif not erros_lexicos:
        print("Análise léxica e sintática concluída sem erros!")

# Função que analisa o corpo do programa
def analisar_corpo():
    while token_atual[1] != "FIMDEJOGO" and token_atual[0] != 'EOF':
        if token_atual[1] == "Escalacao":
            analisar_declaracao_variavel()
        elif token_atual[1] in ["RecebePasse", "Placar"]:
            analisar_comando_io()
        elif token_atual[0] == 'ID':
            analisar_atribuicao()
        else:
            erros.append(f"Erro de sintaxe na linha {token_atual[2]}: Comando desconhecido '{token_atual[1]}'.")
            proximo_token()

# Função que analisa declarações de variáveis
def analisar_declaracao_variavel():
    linha_atual = token_atual[2]
    proximo_token()
    if token_atual[1] in ["golint", "golreal"]:
        proximo_token()
        if token_atual[0] == 'ID':
            proximo_token()
            if token_atual[1] == ';':
                proximo_token()
            else:
                erros.append(f"Erro na linha {linha_atual}: ';' esperado após a declaração.")
                sincronizar(';')
        else:
            erros.append(f"Erro na linha {linha_atual}: Identificador esperado após o tipo.")
            sincronizar(';')
    else:
        erros.append(f"Erro na linha {linha_atual}: Tipo de variável inválido ou não especificado.")
        sincronizar(';')

# Função que analisa atribuições
def analisar_atribuicao():
    linha_atual = token_atual[2]
    if token_atual[0] == 'ID':
        proximo_token()
        if token_atual[0] == 'OP_ATRIB':
            proximo_token()
            analisar_expressao()
            if token_atual[1] == ';':
                proximo_token()
            else:
                erros.append(f"Erro na linha {linha_atual}: ';' esperado no final da atribuição.")
                sincronizar(';')
        else:
            erros.append(f"Erro na linha {linha_atual}: Operador '=' esperado.")
            sincronizar(';')
    else:
        erros.append(f"Erro na linha {linha_atual}: Identificador esperado no início da atribuição.")
        sincronizar(';')


# Função de sincronização com opção de consumir o símbolo
def sincronizar(simbolo, consumir=True):
    while token_atual[1] != simbolo and token_atual[0] != 'EOF' and token_atual[1] != 'FIMDEJOGO':
        proximo_token()
    if token_atual[1] == simbolo and consumir:
        proximo_token()


# Função que analisa expressões
def analisar_expressao():
    analisar_termo()
    while token_atual[0] == 'OP_ARIT' and token_atual[1] in ('+', '-'):
        proximo_token()
        analisar_termo()
    
    # Verifica se há um termo inesperado (indicando operador ausente)
    if token_atual[0] in ['NUM_INT', 'NUM_REAL', 'ID', 'ABRE_PAREN']:
        erros.append(f"Erro na linha {token_atual[2]}: Operador esperado antes de '{token_atual[1]}'.")
        sincronizar(';', consumir=False)  # Não consome o ';'
        return  # Interrompe a função após sincronizar

# Função que analisa termos
def analisar_termo():
    analisar_fator()
    while token_atual[0] == 'OP_ARIT' and token_atual[1] in ('*', '/'):
        proximo_token()
        analisar_fator()

    # Verifica se há um fator inesperado (indicando operador ausente)
    if token_atual[0] in ['NUM_INT', 'NUM_REAL', 'ID', 'ABRE_PAREN']:
        erros.append(f"Erro na linha {token_atual[2]}: Operador esperado antes de '{token_atual[1]}'.")
        sincronizar(';', consumir=False)  # Não consome o ';'
        return  # Interrompe a função após sincronizar

# Função que analisa fatores
def analisar_fator():
    if token_atual[0] in ('NUM_INT', 'NUM_REAL', 'ID'):
        proximo_token()
    elif token_atual[0] == 'ABRE_PAREN':
        proximo_token()
        analisar_expressao()
        if token_atual[0] == 'FECHA_PAREN':
            proximo_token()
        else:
            erros.append(f"Erro na linha {token_atual[2]}: ')' esperado.")
            sincronizar(';')
    else:
        erros.append(f"Erro na linha {token_atual[2]}: Valor ou expressão esperada.")
        sincronizar(';')


# Função que analisa comandos de entrada/saída
def analisar_comando_io():
    comando = token_atual[1]
    linha_atual = token_atual[2]
    proximo_token()
    if token_atual[0] == 'ABRE_PAREN':
        proximo_token()
        if token_atual[0] == 'ID':
            proximo_token()
            if token_atual[0] == 'FECHA_PAREN':
                proximo_token()
                if token_atual[1] == ';':
                    proximo_token()
                else:
                    erros.append(f"Erro na linha {linha_atual}: ';' esperado no final do comando '{comando}'.")
                    sincronizar(';')
            else:
                erros.append(f"Erro na linha {linha_atual}: ')' esperado após o identificador.")
                sincronizar(';')
        else:
            erros.append(f"Erro na linha {linha_atual}: Identificador esperado dentro de '{comando}('.")
            sincronizar(';')
    else:
        erros.append(f"Erro na linha {linha_atual}: '(' esperado após '{comando}'.")
        sincronizar(';')

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
                linhas_codigo.append(linha.rstrip())

            # Limpa erros antigos antes de iniciar nova análise
            global erros, erros_lexicos
            erros = []
            erros_lexicos = []

            # Executa o analisador léxico com o código fornecido pelo usuário
            token_list = analisador_lexico(linhas_codigo)

            limpar_tela()
            print("\nAnalisando o código...\n")
            # Executa o analisador sintático somente se não houver erros léxicos
            if not erros_lexicos:
                analisador_sintatico(token_list)
            else:
                print("Erros léxicos encontrados. A análise sintática não foi realizada.")
                for erro in erros_lexicos:
                    print(erro)

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
            limpar_tela()
            print("Opção inválida. Tente novamente.")
            input("\nPressione Enter para voltar ao menu...")

# Executa o programa
main()
