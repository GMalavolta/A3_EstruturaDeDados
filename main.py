import gensim
from gensim import corpora
import networkx as nx

import nltk
from nltk.corpus import stopwords

import matplotlib.pyplot as plt

import archive

def Grafo1_Topicos():
    docTxt = []
    textoPrincipal = []
    topicos = []
    corpo = []
    frases = []
    corpoBow = []
    palavrasFiltradas = []

    diretorio = 'C:\\Users\\guilh\OneDrive\Área de Trabalho\Projeto faculdade_Estrutura de dados\BaseDadosResumos'


    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')
    stop_words = set(stopwords.words('portuguese'))

    docTxt = archive.arquivoDiretorio(diretorio)

    textoPrincipal = [archive.separarParagrafos(arquivo, diretorio)[1] for arquivo in docTxt]

    prePro = archive.preProcessamento(textoPrincipal, stop_words)

    dicionario = corpora.Dictionary(prePro)
    archive.corpoBags(dicionario, prePro, corpoBow)

    grafo = archive.criarGrafo(prePro, 30)# Gera o nó com palavras que se repetiram ao menos 30 vezes

    # Desenha o grafo usando Matplotlib
    posicao = nx.spring_layout(grafo, k=0.2)  # Define a disposição dos nós usando um algoritmo de layout
    rotulo = {node: node for node in grafo.nodes()}  # Rótulos dos nós

    arestas = [data['weight'] for u, v, data in grafo.edges(data=True)]

    nx.draw_networkx_nodes(grafo, posicao, node_size=1000, node_color='skyblue')
    nx.draw_networkx_edges(grafo, posicao, width=arestas, alpha=0.5)
    nx.draw_networkx_labels(grafo, posicao, rotulo, font_size=8)

    plt.title("Grafo")
    plt.show()

def Grafo2_Autores():
    docTxt = []

    diretorio = 'C:\\Users\\guilh\OneDrive\Área de Trabalho\Projeto faculdade_Estrutura de dados\BaseDadosResumos'

    docTxt = archive.arquivoDiretorio(diretorio)

    # Dicionário para rastrear os nós associados a cada autor
    autores_nos = {}

    # Cria o grafo
    grafo_coautoria = nx.Graph()

    for arquivo in docTxt:
        resumo = archive.separarParagrafos(arquivo, diretorio)[3]
        autores_resumo = [autor.strip().lower() for autor in resumo.split(',')]  # Converte para minúsculas

        # Adiciona arestas ao grafo com base nas colaborações
        for i in range(len(autores_resumo)):
            for j in range(i + 1, len(autores_resumo)):
                autor_i = autores_resumo[i]
                autor_j = autores_resumo[j]

                # Se o autor_i já estiver no dicionário, obtenha seu nó correspondente
                if autor_i in autores_nos:
                    no_i = autores_nos[autor_i]
                else:
                    no_i = len(autores_nos)
                    autores_nos[autor_i] = no_i
                    grafo_coautoria.add_node(no_i, label=autor_i)  # Adiciona nó com rótulo

                # Se o autor_j já estiver no dicionário, obtenha seu nó correspondente
                if autor_j in autores_nos:
                    no_j = autores_nos[autor_j]
                else:
                    no_j = len(autores_nos)
                    autores_nos[autor_j] = no_j
                    grafo_coautoria.add_node(no_j, label=autor_j)  # Adiciona nó com rótulo

                # Adicione uma aresta entre os nós correspondentes
                grafo_coautoria.add_edge(no_i, no_j)


    # é utilizado a biblioteca para calcular a centralidade dos nós
    centralidade = nx.degree_centrality(grafo_coautoria)

    # Identifique os pesquisadores mais influentes na rede(O mesmo é printado no terminal)
    pesquisadores_influentes = [autor for autor in autores_nos if centralidade.get(autores_nos[autor]) is not None]
    pesquisadores_influentes = sorted(pesquisadores_influentes, key=lambda autor: centralidade[autores_nos[autor]],reverse=True)
    print("Pesquisadores mais influentes:")
    print(pesquisadores_influentes[:5])  # Imprime os 5 pesquisadores mais influentes

    # Desenhe o grafo
    pos = nx.spring_layout(grafo_coautoria)
    labels = nx.get_node_attributes(grafo_coautoria, 'label')  # Obtém rótulos dos nós
    nx.draw_networkx_labels(grafo_coautoria, pos, labels, font_size=10)  # Adiciona rótulos ao desenho
    nx.draw(grafo_coautoria, pos, with_labels=False, font_weight='bold', node_size=1200, node_color='skyblue')
    plt.show()

while True:
    # Exibindo o menu
    print("\nMenu:")
    print("1. Grafo de tópicos")
    print("2. Grafo de coautoria")
    print("4. Sair")

    # Obtendo a escolha do usuário
    escolha = input("Escolha uma opção: ")

    # Chamando a função correspondente à escolha do usuário
    if escolha == '1':
        Grafo1_Topicos()
    elif escolha == '2':
        Grafo2_Autores()
    elif escolha == "4":
        break

    else:
        print("Opção inválida. Tente novamente.")
