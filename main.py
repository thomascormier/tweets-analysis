import generateCSV
import generateDB


def main():
    """
    1. Créer la base de donnée vide et les tables follower et tweet
    2. Récupérer les données des tables dans des CSV
    3. Insérer les data des CSV dans la base de données mySQL


    2. Genère un fichier csv qui contient le type d'un grand nombre de tweets et leur date de publication
    3. Calculer les pics d'activités des Followers
    :return: Une liste de jours de la semaine et d'heures
    """


    createCSVFollower()
    # On va créer un fichier CSV qui contient l'ensemble des followers de l'entreprise
    createCSVTweet()
    # On crée ensuite un fichier CSV qui contient tous les tweets de ces followers au cours du dernier mois
    createTables()
    # Lors du premier lancement du programme, on va remplir créer la structure de la base de données (notamment les tables)
    calculatePeaks()
    # On va calculer les pics d'activités des followers sur Twitter