import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('TMDB_API_KEY')

name_film = input("entrez votre nom de film: ")


params = {"api_key": api_key, "query": name_film, "language": "fr-FR"}

params_details = {"api_key": api_key, "language": "fr-FR"}

response = requests.get("https://api.themoviedb.org/3/search/movie", params=params)


if response.status_code == 200:
    film = response.json()["results"]
    if not film:
        print("film introuvable !")

    else:
        id_film = film[0]["id"]
        titre = film[0]["title"]
        note = film[0]["vote_average"]
        synops = film[0]["overview"]
        date = film[0]["release_date"]
        number_v = film[0]["vote_count"]
        titre_original = film[0]["original_title"]

        response_details = requests.get(f"https://api.themoviedb.org/3/movie/{id_film}", params=params_details)

        if response_details.status_code == 200:
            film_details = response_details.json()
            duree = film_details["runtime"]
            budget = film_details["budget"]
            revenue = film_details["revenue"]

            heure = duree // 60
            minutes = duree % 60
            duree_final = f"{heure}h{minutes:02d}m"

            benefice = revenue - budget

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
        else:
            print("erreur")
else:
    print("erreur")