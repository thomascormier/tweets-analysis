# -*- coding: utf-8 -*
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')

#on va faire le principe inverse d'un tokenizer dans le sens que l'on ne va pas supprimer des mots pour ne garder que les
#mots clefs intéressants, mais l'on va relever que les mots clefs intéressant à partir du banque de mots prédéfinis
#afin de donnée un poid d'intérêt au tweets
#Dans notre cas nous travaillons avec agricool nous allons donc chercher des mots clefs en lien avec l'agriculture

def getTokens(str):

    keyWords = {"agriculture":10}
    words = word_tokenize(str)

    for w in words:
        if w not in keyWords:
            wordsFiltered.append(w)
