import os
import requests
import json
from dotenv import load_dotenv

#cle_api
load_dotenv()
api_key = os.getenv('TMDB_API_KEY')

#creation d'une erreur exception
class NumberErrorUnder0(Exception):
    def __init__(self):
        self.message = "Ecrivez un nombre au dessus de 0 !"

class NumberErrorAboveMax(Exception):
    def __init__(self):
        self.message = "Nombre trop grand !"



#interaction avec l'utilisateur
name_film = input("entrez votre nom de film: ")

#parametre de la requete
params = {"api_key": api_key, "query": name_film, "language": "fr-FR"}
params_details = {"api_key": api_key, "language": "fr-FR"}

#requetes de l'api

response = requests.get("https://api.themoviedb.org/3/search/movie", params=params, timeout=10)


#reponse de l'api
if response.status_code == 200:
    film_listes = response.json()["results"]

    if not film_listes:
        print("film introuvable !")
    else:
        for i, film_l in enumerate(film_listes, start=1):
            date = film_l["release_date"].split("-")[0]
            print(f"{i}.{film_l['title']}({date})")

        while True:
            try:
                choose_film = int(input("entrer le numero du film pour avoir plus de details: "))
                if choose_film <= 0:
                    raise NumberErrorUnder0()

                if choose_film > len(film_listes):
                    raise NumberErrorAboveMax()

                break
            except ValueError:
                print("Entrez un nombre s'il vous plaît !")
            except NumberErrorUnder0 as e:
                print(e.message)
            except NumberErrorAboveMax as e:
                print(e.message)

        if 1 <= choose_film <= len(film_listes):
            id_film = film_listes[choose_film - 1]["id"]
            titre = film_listes[choose_film - 1]["title"]
            note = film_listes[choose_film - 1]["vote_average"]
            synops = film_listes[choose_film - 1]["overview"]
            date = film_listes[choose_film - 1]["release_date"]
            number_v = film_listes[choose_film - 1]["vote_count"]
            titre_original = film_listes[choose_film - 1]["original_title"]

            response_details = requests.get(f"https://api.themoviedb.org/3/movie/{id_film}", params=params_details)
            response_review = requests.get(f"https://api.themoviedb.org/3/movie/{id_film}/reviews", params=params_details)

            if response_details.status_code == 200:
                film_details = response_details.json()
                film_reviews = response_review.json()["results"][0:3]
                duree = film_details["runtime"]
                budget = film_details["budget"]
                revenue = film_details["revenue"]

                heure = duree // 60
                minutes = duree % 60
                duree_final = f"{heure}h{minutes:02d}m"

                benefice = revenue - budget

                def affiche_reviews():
                    for review in film_reviews:
                        print("")
                        print(f"{review['author']}: {review['content']}")


                if budget == 0 or revenue == 0:
                    print("Movie details:")
                    print("Titre:", titre)
                    print("Titre original:", titre_original)
                    print("Date:", date)
                    print("Durée:", duree_final)
                    print("Note:", note)
                    print(f"Nombre de vote: {number_v:,}".replace(",", " "))
                    print(f"Budget: Aucun")
                    print(f"Revenue: Aucun")
                    print(f"benefice: Aucun")
                    print("Synopsis:", synops)
                    affiche_reviews()

                else:
                    if benefice <= 0:
                        print("Movie details:")
                        print("Titre:", titre)
                        print("Titre original:", titre_original)
                        print("Date:", date)
                        print("Durée:", duree_final)
                        print("Note:", note)
                        print(f"Nombre de vote: {number_v:,}".replace(",", " "))
                        print(f"Budget: {budget:,}$".replace(",", " "))
                        print(f"Revenue: {revenue:,}$".replace(",", " "))
                        print(f"Perte: {benefice:,}$".replace(",", " "))
                        print("Synopsis:", synops)
                        affiche_reviews()

                    else:
                        print("Movie details:")
                        print("Titre:", titre)
                        print("Titre original:", titre_original)
                        print("Date:", date)
                        print("Durée:", duree_final)
                        print("Note:", note)
                        print(f"Nombre de vote: {number_v:,}".replace(",", " "))
                        print(f"Budget: {budget:,}$".replace(",", " "))
                        print(f"Revenue: {revenue:,}$".replace(",", " "))
                        print(f"benefice: {benefice:,}$".replace(",", " "))
                        print("Synopsis:", synops)
                        affiche_reviews()

            else:
                print("Erreur !")

        else:
            print("film introuvable !")
else:
    print("Erreur !")








