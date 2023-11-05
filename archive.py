import os

import networkx as nx
from nltk import word_tokenize, sent_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords


# Armazena os arquivos .txt em um array
def arquivoDiretorio(diretorio):
    arquivos = [arquivo for arquivo in os.listdir(diretorio) if arquivo.endswith('.txt')]
    return arquivos


# Separa os paragrafos de um arquivo
def separarParagrafos(arquivo, diretorio):
    local = diretorio + "\\" + arquivo
    try:
        with open(local, 'r') as arqV:
            texto = arqV.read()
        paragrafos = texto.split('\n')
    except FileNotFoundError:
        return "O arquivo não foi encontrado."
    return paragrafos


def preProcessamento(textoPrincipal, stop_words):
    preProcessamento_sentencas = []
    for texto in textoPrincipal:
        sentencas = sent_tokenize(texto)  # Tokenização em frases
        lematizar = WordNetLemmatizer()
        for sentenca in sentencas:
            palavras = word_tokenize(sentenca.lower())  # Tokenização em palavras e conversão para minúsculas
            palavras = [lematizar.lemmatize(palavra) for palavra in palavras if
                        palavra.isalpha() and len(palavra) > 2]  # Lematização e remoção de pontuações
            palavras = [palavra for palavra in palavras if
                        palavra not in stopwords.words('portuguese')]  # Remoção de stopwords
            preProcessamento_sentencas.append(palavras)
    return preProcessamento_sentencas


# Grupo de palavras
def corpoBags(dicionario, corpo, corpoBow):
    corpoBow = [dicionario.doc2bow(text) for text in corpo]
    return corpoBow


# Pega os tópicos do modelo LDA
def pegarTopicosLDA(topicos, modeloLDA):
    for topic_id, palavras in modeloLDA.print_topics(60, 30):
        topic_words = palavras.split("+")
        topicos = [palavra.split("*")[1].strip() for palavra in topic_words]
    return topicos


def criarGrafo(prePro, x):
    grafo = nx.Graph()
    contador = {}

    for sentenca in prePro:
        for palavra in sentenca:
            if palavra not in contador:
                contador[palavra] = 0
            contador[palavra] += 1

    for sentenca in prePro:
        palavras = [palavra for palavra in sentenca if contador[palavra] >= x]

        for i in range(len(palavras)):
            for j in range(i + 1, len(palavras)):
                if grafo.has_edge(palavras[i], palavras[j]):
                    grafo[palavras[i]][palavras[j]]['weight'] += 1
                elif palavras[i] != palavras[j]:
                    grafo.add_edge(palavras[i], palavras[j], weight=1)

    for palavra, count in contador.items():
        if count >= x:
            grafo.nodes[palavra]['count'] = count
            print(f"{palavra}: {count}")
    return grafo

