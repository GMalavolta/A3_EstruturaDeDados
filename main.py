import gensim
from gensim import corpora
import networkx as nx

import nltk
from nltk.corpus import stopwords

import matplotlib.pyplot as plt

import archive


def main():
    docTxt = []
    textoPrincipal = []
    topicos = []
    corpo = []
    frases = []
    corpoBow = []
    palavrasFiltradas = []

    diretorio = 'C:\\Users\\natha\OneDrive\Área de Trabalho\BaseDadosResumos'

    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')
    stop_words = set(stopwords.words('portuguese'))

    docTxt = archive.arquivoDiretorio(diretorio)

    textoPrincipal = [archive.separarParagrafos(arquivo, diretorio)[1] for arquivo in docTxt]

    prePro = archive.preProcessamento(textoPrincipal, stop_words)

    dicionario = corpora.Dictionary(prePro)
    archive.corpoBags(dicionario, prePro, corpoBow)

    # Modelo LDA
    modeloLDA = gensim.models.LdaModel(corpoBow, num_topics=1, id2word=dicionario, passes=10)
    archive.pegarTopicosLDA(topicos, modeloLDA)

    grafo = archive.criarGrafo(prePro, 50)

    # Desenha o grafo usando Matplotlib
    posicao = nx.spring_layout(grafo, k=0.2)  # Define a disposição dos nós usando um algoritmo de layout
    rotulo = {node: node for node in grafo.nodes()}  # Rótulos dos nós

    arestas = [data['weight'] for u, v, data in grafo.edges(data=True)]

    nx.draw_networkx_nodes(grafo, posicao, node_size=1000, node_color='skyblue')
    nx.draw_networkx_edges(grafo, posicao, width=arestas, alpha=0.5)
    nx.draw_networkx_labels(grafo, posicao, rotulo, font_size=8)

    plt.title("Grafo")
    plt.show()


main()
