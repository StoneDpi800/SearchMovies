import flet as ft
import os
import requests
import json
from dotenv import load_dotenv
from flet.controls import page

#cle_api
load_dotenv()
api_key = os.getenv('TMDB_API_KEY')

params_details = {"api_key": api_key, "language": "fr-FR"}

def requetes_api(nom_film):
    params = {"api_key": api_key, "query": nom_film, "language": "fr-FR"}
    response = requests.get("https://api.themoviedb.org/3/search/movie", params=params)
    return response.json()["results"]

def requetes_api_details(id_film):
    response_d = requests.get(f"https://api.themoviedb.org/3/movie/{id_film}", params=params_details)
    return response_d.json()

def Films_Tiles(nom_film, page: ft.Page):
    liste_films = requetes_api(nom_film)

    title_films = []
    for film in liste_films:
        title_films.append(film["title"])

    page.clean()

    for film in title_films:
        page.add(ft.Text(f"{film}"))

    page.update()


def informations_film(id_film, zone_contenue, page: ft.Page):
    response = requetes_api_details(id_film)

    title = response["title"]
    title_original = response["original_title"]
    date = response["release_date"]
    note = response["vote_average"]
    number_v = response["vote_count"]
    synops = response["overview"]
    duree = response["runtime"]
    budget = response["budget"]
    revenue = response["revenue"]
    genres = "-".join(g["name"] for g in response["genres"])

    heure = duree // 60
    minutes = duree % 60
    duree_final = f"{heure}h{minutes:02d}m"

    zone_infos_film = ft.Container(expand=True, padding=20, content=ft.Column(scroll=ft.ScrollMode.AUTO,
            controls=[ft.Row(vertical_alignment=ft.CrossAxisAlignment.START, spacing=30,
                    controls=[ft.Column(width=300, controls=[ft.Image(src=f"https://image.tmdb.org/t/p/w500{response['poster_path']}", width=300, border_radius=10)]),
                        ft.Column(expand=True, spacing=12,
                            controls=[ft.Text(title, size=36, weight=ft.FontWeight.BOLD), ft.Text(spans=[ft.TextSpan("Titre original : ", style=ft.TextStyle(weight=ft.FontWeight.BOLD)), ft.TextSpan(title_original)]),
                                ft.Text(spans=[ft.TextSpan("Durée : ", style=ft.TextStyle(weight=ft.FontWeight.BOLD)), ft.TextSpan(duree_final)]), ft.Text(spans=[ft.TextSpan("Date : ", style=ft.TextStyle(weight=ft.FontWeight.BOLD)), ft.TextSpan(date)]),
                                ft.Row(spacing=4, tight=True,
                                    controls=[ft.Icon(ft.Icons.STAR, color=ft.Colors.AMBER, size=18), ft.Text(f"{round(note, 1)}/10 ({number_v} votes)")]),
                                ft.Text(spans=[ft.TextSpan("Genre : ", style=ft.TextStyle(weight=ft.FontWeight.BOLD)), ft.TextSpan(genres)]),
                                ft.Text(spans=[ft.TextSpan("Budget : ", style=ft.TextStyle(weight=ft.FontWeight.BOLD)), ft.TextSpan(f"{budget:,} $".replace(",", " "))]),
                                ft.Text(spans=[ft.TextSpan("Revenus : ", style=ft.TextStyle(weight=ft.FontWeight.BOLD)), ft.TextSpan(f"{revenue:,} $".replace(",", " "))]),
                                      ft.Text("Synopsis :", size=18, weight=ft.FontWeight.BOLD), ft.Text(synops)])])]))

    zone_contenue.content = zone_infos_film
    page.update()




def page_accueil(page: ft.Page):

    def menu(e):
        page.clean()
        page_accueil(page)

    icon_menu = ft.Button(icon=ft.Icons.HOME, on_click=menu)

    barre_recherche = ft.SearchBar(bar_hint_text="Recherche un film", width=600, bar_leading=ft.Icon(ft.Icons.SEARCH), on_submit=lambda e: Films_Tiles(barre_recherche.value, page))

    logo = ft.Image(src="https://cdn-icons-png.flaticon.com/512/4096/4096441.png", width=50, height=50)
    titre_SM = ft.Text("SearchMovies", size=36, weight=ft.FontWeight.BOLD)

    retour_menu = ft.Container(content=ft.Row(controls=[logo, titre_SM]), on_click=menu)


    the_header = ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[ft.Row(controls=[retour_menu, icon_menu]), barre_recherche])


    grille = ft.GridView(expand=True, runs_count=5, spacing=10, run_spacing=10, child_aspect_ratio=0.7)

    response_trend = requests.get("https://api.themoviedb.org/3/trending/movie/day", params=params_details)

    films_trending = response_trend.json()["results"]

    for film in films_trending:
        if not film["poster_path"]:
            continue

        carte = ft.Container(border_radius=10, clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            content=ft.Stack(controls=[ft.Image(src=f"https://image.tmdb.org/t/p/w500{film['poster_path']}",fit=ft.BoxFit.COVER),
                    ft.Container(left=8, top=8, padding=ft.Padding.symmetric(horizontal=6, vertical=3), border_radius=8, bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
                        content=ft.Row(spacing=3, tight=True,
                            controls=[ft.Icon(ft.Icons.STAR, color=ft.Colors.AMBER, size=14), ft.Text(str(round(film["vote_average"], 1)), size=12)])),
                    ft.Container(left=0, right=0, bottom=0, padding=8, bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
                        content=ft.Text(film["title"], size=13, weight=ft.FontWeight.BOLD, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS))]), on_click=lambda e, f=film: informations_film(f["id"], zone_contenu, page))

        grille.controls.append(carte)

    zone_contenu = ft.Container(content=grille, expand=True)

    page.add(the_header, zone_contenu)

def main(page: ft.Page):
    page.title = "Search Movies"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 1000
    page.window.height = 800

    page_accueil(page)


ft.run(main)