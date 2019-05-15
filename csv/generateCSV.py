# coding=utf-8
import csv


def generateCsv():
    """
    On doit recuperer les tweets un par un.
    On parcours l ensemble des tweets un par un.
    Pour chacun d entre eux, on détermine si c est un tweet ou un retweet.
    On stocke cette information et la date du tweet dans un fichier .csv qui aura donc le format suivant :
        <date_tweet>,<type_tweet>
    N.B. : le type d'un tweet est : T (pour tweet) ou RT (pour retweet)
    :return:
    """

    fname = "data.csv"
    file = open(fname, "wb")

    try:
        writer = csv.writer(file)

#        for <chaque tweet>
#            if tweet[n].startwith("RT"):
#                type = "RT"
#            else type = "T"


        writer.writerow(("type", "<DATE>"))

    finally: file.close()