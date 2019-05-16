import test
import generateDB





def main():
    """
    1. Genère un fichier csv qui contient le type d'un grand nombre de tweets et leur date de publication
    2. Créer la base de donnée avec les Followers et leurs Tweets
    3. Calculer les pics d'activités des Followers
    :return: Une liste de jours de la semaine et d'heures
    """
    #generateCSV()
    createDB()
    calculatePeaks()