#on va faire le principe inverse d'un tokenizer dans le sens que l'on ne va pas supprimer des mots pour ne garder que les
#mots clefs intéressants, mais l'on va relever que les mots clefs intéressant à partir du banque de mots prédéfinis
#afin de donnée un poid d'intérêt au tweets
#Dans notre cas nous travaillons avec agricool nous allons donc chercher des mots clefs en lien avec l'agriculture

def getWeight(content):

    keyWords = {"agriculture":10,"Si":12,"en":4}
    weight = 0
    for w in content.split():
        if w in keyWords:
            weight+=keyWords[w]
    return weight
