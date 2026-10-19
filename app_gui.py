import flet as ft
import os
import requests
from dotenv import load_dotenv
from flet import IconButton
from flet.controls import page
import json


if os.path.exists("liste_favoris.json"):
    try:
        with open("liste_favoris.json", "r") as file:
            liste_favoris = json.load(file)
    except json.JSONDecodeError:
        liste_favoris = {}

def sauvegarde_favoris():
    with open("liste_favoris.json", "w") as file:
        json.dump(liste_favoris, file)



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


def favoris(zone_contenu, ligne_txt, page: ft.Page):
    zone_favoris = ft.GridView(runs_count=5, spacing=30, run_spacing=30, child_aspect_ratio=0.67)

    for id_film, infos in liste_favoris.items():
        if infos['poster_path']:
            image = f"https://image.tmdb.org/t/p/w500{infos['poster_path']}"
        else:
            image = "https://ih1.redbubble.net/image.4905811472.8675/bg,f8f8f8-flat,750x,075,f-pad,750x1000,f8f8f8.jpg"

        carte = ft.Container(border_radius=10, clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            content=ft.Stack(controls=[ft.Image(src=image, fit=ft.BoxFit.COVER),
                ft.Container(left=8, top=8, padding=ft.Padding.symmetric(horizontal=6, vertical=3), border_radius=8, bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
                    content=ft.Row(spacing=3, tight=True,
                        controls=[ft.Icon(ft.Icons.STAR, color=ft.Colors.AMBER, size=14), ft.Text(str(round(infos["vote_average"], 1)), size=12)])),
                ft.Container(right=6, top=6, border_radius=20, bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
                    content=ft.IconButton(icon=ft.Icons.FAVORITE, icon_color=ft.Colors.RED_400, icon_size=18, padding=4, tooltip="Retirer des favoris",
                        on_click=lambda e, i=id_film, d=infos: add_favorite(d["title"], i, d["poster_path"], d["vote_average"], e))),
                ft.Container(left=0, right=0, bottom=0, padding=8, bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
                    content=ft.Text(infos["title"], size=13, weight=ft.FontWeight.BOLD, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS))]),
            on_click=lambda e, i=id_film: informations_film(int(i), zone_contenu, ligne_txt, page, page_favoris))

        zone_favoris.controls.append(carte)

    zone_contenu.content = zone_favoris
    page_favoris = zone_favoris
    page.update()




def add_favorite(nom_film, id_film, poster, note, e):
    if str(id_film) in liste_favoris:
        del liste_favoris[str(id_film)]
        e.control.icon = ft.Icons.FAVORITE_BORDER
    else:
        liste_favoris[str(id_film)] = {"title": nom_film, "poster_path": poster, "vote_average": note}
        e.control.icon = ft.Icons.FAVORITE

    sauvegarde_favoris()
    e.control.update()





def Films_Tiles(nom_film, zone_contenu, ligne_txt, page: ft.Page):
    liste_films = requetes_api(nom_film)

    zone_titre_films = ft.GridView(runs_count=5, spacing=30, run_spacing=30, child_aspect_ratio=0.67)

    if not liste_films:
        message_erreur = ft.Container(expand=True,alignment=ft.Alignment(0, 0),
            content=ft.Row(alignment=ft.MainAxisAlignment.CENTER,tight=True,spacing=10,
                controls=[ft.Icon(ft.Icons.ERROR_OUTLINED, size=30, color=ft.Colors.RED_400),ft.Text("Film introuvable", size=24)]))
        zone_contenu.content = message_erreur
        ligne_txt.controls = ft.Text("", size=20)
        page.update()
    else:
        for film in liste_films:
            if str(film["id"]) in liste_favoris and not film["poster_path"]:
                carte = ft.Container(border_radius=10, clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                                     content=ft.Stack(controls=[ft.Image(
                                         src=f"https://ih1.redbubble.net/image.4905811472.8675/bg,f8f8f8-flat,750x,075,f-pad,750x1000,f8f8f8.jpg",
                                         fit=ft.BoxFit.COVER),
                                         ft.Container(left=8, top=8,
                                                      padding=ft.Padding.symmetric(horizontal=6,
                                                                                   vertical=3),
                                                      border_radius=8,
                                                      bgcolor=ft.Colors.with_opacity(0.7,
                                                                                     ft.Colors.BLACK),
                                                      content=ft.Row(spacing=3, tight=True,
                                                                     controls=[
                                                                         ft.Icon(ft.Icons.STAR,
                                                                                 color=ft.Colors.AMBER,
                                                                                 size=14),
                                                                         ft.Text(str(round(film[
                                                                                               "vote_average"],
                                                                                           1)),
                                                                                 size=12)])),
                                         ft.Container(right=6, top=6, border_radius=20,
                                                      bgcolor=ft.Colors.with_opacity(0.7,
                                                                                     ft.Colors.BLACK),
                                                      content=ft.IconButton(
                                                          icon=ft.Icons.FAVORITE,
                                                          icon_color=ft.Colors.RED_400,
                                                          icon_size=18, padding=4,
                                                          tooltip="Ajouter aux favoris",
                                                          on_click=lambda e, f=film: add_favorite(f["title"], f["id"],
                                                                                                  f["poster_path"],
                                                                                                  f["vote_average"],
                                                                                                  e))),
                                         ft.Container(left=0, right=0, bottom=0, padding=8,
                                                      bgcolor=ft.Colors.with_opacity(0.7,
                                                                                     ft.Colors.BLACK),
                                                      content=ft.Text(film["title"], size=13,
                                                                      weight=ft.FontWeight.BOLD,
                                                                      max_lines=2,
                                                                      overflow=ft.TextOverflow.ELLIPSIS))]),
                                     on_click=lambda e, f=film: informations_film(f["id"], zone_contenu, ligne_txt,
                                                                                  page, page_recherche),
                                     )

                zone_titre_films.controls.append(carte)

            elif str(film["id"]) in liste_favoris:
                carte = ft.Container(border_radius=10, clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                                     content=ft.Stack(controls=[
                                         ft.Image(src=f"https://image.tmdb.org/t/p/w500{film['poster_path']}",
                                                  fit=ft.BoxFit.COVER),
                                         ft.Container(left=8, top=8,
                                                      padding=ft.Padding.symmetric(horizontal=6, vertical=3),
                                                      border_radius=8,
                                                      bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
                                                      content=ft.Row(spacing=3, tight=True,
                                                                     controls=[
                                                                         ft.Icon(ft.Icons.STAR, color=ft.Colors.AMBER,
                                                                                 size=14),
                                                                         ft.Text(str(round(film["vote_average"], 1)),
                                                                                 size=12)])),
                                         ft.Container(right=6, top=6, border_radius=20,
                                                      bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
                                                      content=ft.IconButton(icon=ft.Icons.FAVORITE,
                                                                            icon_color=ft.Colors.RED_400, icon_size=18,
                                                                            padding=4, tooltip="Ajouter aux favoris",
                                                                            on_click=lambda e, f=film: add_favorite(
                                                                                f["title"], f["id"], f["poster_path"],
                                                                                f["vote_average"], e))),
                                         ft.Container(left=0, right=0, bottom=0, padding=8,
                                                      bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
                                                      content=ft.Text(film["title"], size=13, weight=ft.FontWeight.BOLD,
                                                                      max_lines=2,
                                                                      overflow=ft.TextOverflow.ELLIPSIS))]),
                                     on_click=lambda e, f=film: informations_film(f["id"], zone_contenu, ligne_txt,
                                                                                  page,
                                                                                  page_recherche))
                zone_titre_films.controls.append(carte)


            elif not film["poster_path"]:
                carte = ft.Container(border_radius=10, clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                                     content=ft.Stack(controls=[ft.Image(
                                         src=f"https://ih1.redbubble.net/image.4905811472.8675/bg,f8f8f8-flat,750x,075,f-pad,750x1000,f8f8f8.jpg",
                                         fit=ft.BoxFit.COVER),
                                                                ft.Container(left=8, top=8,
                                                                             padding=ft.Padding.symmetric(horizontal=6,
                                                                                                          vertical=3),
                                                                             border_radius=8,
                                                                             bgcolor=ft.Colors.with_opacity(0.7,
                                                                                                            ft.Colors.BLACK),
                                                                             content=ft.Row(spacing=3, tight=True,
                                                                                            controls=[
                                                                                                ft.Icon(ft.Icons.STAR,
                                                                                                        color=ft.Colors.AMBER,
                                                                                                        size=14),
                                                                                                ft.Text(str(round(film[
                                                                                                                      "vote_average"],
                                                                                                                  1)),
                                                                                                        size=12)])),
                                                                ft.Container(right=6, top=6, border_radius=20,
                                                                             bgcolor=ft.Colors.with_opacity(0.7,
                                                                                                            ft.Colors.BLACK),
                                                                             content=ft.IconButton(
                                                                                 icon=ft.Icons.FAVORITE_BORDER,
                                                                                 icon_color=ft.Colors.RED_400,
                                                                                 icon_size=18, padding=4,
                                                                                 tooltip="Ajouter aux favoris", on_click=lambda e, f=film: add_favorite(f["title"], f["id"], f["poster_path"], f["vote_average"], e))),
                                                                ft.Container(left=0, right=0, bottom=0, padding=8,
                                                                             bgcolor=ft.Colors.with_opacity(0.7,
                                                                                                            ft.Colors.BLACK),
                                                                             content=ft.Text(film["title"], size=13,
                                                                                             weight=ft.FontWeight.BOLD,
                                                                                             max_lines=2,
                                                                                             overflow=ft.TextOverflow.ELLIPSIS))]),
                                     on_click=lambda e, f=film: informations_film(f["id"], zone_contenu, ligne_txt,
                                                                                  page, page_recherche),
                                     )

                zone_titre_films.controls.append(carte)

            else:
                carte = ft.Container(border_radius=10, clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                                     content=ft.Stack(controls=[
                                         ft.Image(src=f"https://image.tmdb.org/t/p/w500{film['poster_path']}",
                                                  fit=ft.BoxFit.COVER),
                                         ft.Container(left=8, top=8, padding=ft.Padding.symmetric(horizontal=6, vertical=3),
                                                      border_radius=8, bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
                                                      content=ft.Row(spacing=3, tight=True,
                                                                     controls=[ft.Icon(ft.Icons.STAR, color=ft.Colors.AMBER,
                                                                                       size=14),
                                                                               ft.Text(str(round(film["vote_average"], 1)),
                                                                                       size=12)])),
                                         ft.Container(right=6, top=6, border_radius=20,
                                                      bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
                                                      content=ft.IconButton(icon=ft.Icons.FAVORITE_BORDER,
                                                                            icon_color=ft.Colors.RED_400, icon_size=18,
                                                                            padding=4, tooltip="Ajouter aux favoris", on_click=lambda e, f=film: add_favorite(f["title"], f["id"], f["poster_path"], f["vote_average"], e))),
                                         ft.Container(left=0, right=0, bottom=0, padding=8,
                                                      bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
                                                      content=ft.Text(film["title"], size=13, weight=ft.FontWeight.BOLD,
                                                                      max_lines=2, overflow=ft.TextOverflow.ELLIPSIS))]),
                                     on_click=lambda e, f=film: informations_film(f["id"], zone_contenu, ligne_txt, page,
                                                                                  page_recherche))
                zone_titre_films.controls.append(carte)

        zone_contenu.content = zone_titre_films

        page_recherche = zone_titre_films

        ligne_txt.controls = ft.Text("Films Rerchercher:", size=20)

        page.update()





def informations_film(id_film, zone_contenue, ligne_txt, page: ft.Page, page_recherche=None):
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

    if not response["poster_path"]:
        zone_infos_film = ft.Container(expand=True, padding=20, content=ft.Column(scroll=ft.ScrollMode.AUTO,
                                         controls=[ft.Row(vertical_alignment=ft.CrossAxisAlignment.START,spacing=30,
                                            controls=[ft.Column(width=300,controls=[ft.Image(src=f"https://ih1.redbubble.net/image.4905811472.8675/bg,f8f8f8-flat,750x,075,f-pad,750x1000,f8f8f8.jpg",width=300,border_radius=10)]),
                                                    ft.Column(expand=True,spacing=12,controls=[
                                                        ft.Text(title,size=36,weight=ft.FontWeight.BOLD),
                                                        ft.Text(spans=[ft.TextSpan("Titre original : ",style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                                        ft.TextSpan(title_original)]),
                                                        ft.Text(spans=[ft.TextSpan("Durée : ",style=ft.TextStyle(weight=ft.FontWeight.BOLD)),ft.TextSpan(duree_final)]),
                                                        ft.Text(spans=[ft.TextSpan("Date : ",style=ft.TextStyle(weight=ft.FontWeight.BOLD)),ft.TextSpan(date)]),
                                                        ft.Row(spacing=4,tight=True,controls=[ft.Icon(ft.Icons.STAR,color=ft.Colors.AMBER,size=18),
                                                        ft.Text(f"{round(note, 1)}/10 ({number_v} votes)")]),
                                                        ft.Text(spans=[ft.TextSpan("Genre : ",style=ft.TextStyle(weight=ft.FontWeight.BOLD)),ft.TextSpan(genres)]),
                                                        ft.Text(spans=[ft.TextSpan("Budget : ",style=ft.TextStyle(weight=ft.FontWeight.BOLD)),ft.TextSpan(f"{budget:,} $".replace(","," "))]),
                                                        ft.Text(spans=[ft.TextSpan("Revenus : ", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),ft.TextSpan( f"{revenue:,} $".replace( ",", " "))]),
                                                        ft.Text("Synopsis :",size=18,weight=ft.FontWeight.BOLD),ft.Text(synops)])])]))

        zone_contenue.content = zone_infos_film
        page.update()

    else:
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

    def back(e):
        zone_contenue.content = page_recherche
        ligne_txt.controls = ft.Text("Films Rerchercher:", size=20)

    button_back = ft.Button(icon=ft.Icons.ARROW_BACK, on_click=back, tooltip="Retour a la page précédent")

    ligne_txt.controls = button_back

    page.update()








def page_accueil(page: ft.Page):

    def menu(e):
        page.clean()
        page_accueil(page)

    def delete_bar(e):
        barre_recherche.value = ""

    icon_menu = ft.IconButton(icon=ft.Icons.HOME, on_click=menu, icon_size=22, tooltip="Retour au menu")

    button_delete_bar = ft.IconButton(icon=ft.Icons.CLOSE, on_click=delete_bar, icon_size=18, tooltip="Supprimer le texte")

    barre_recherche = ft.SearchBar(bar_hint_text="Recherche un film", width=600, bar_leading=ft.Icon(ft.Icons.SEARCH), on_submit=lambda e: Films_Tiles(barre_recherche.value, zone_contenu, ligne_txt, page), bar_trailing=[button_delete_bar])

    logo = ft.Image(src="https://cdn-icons-png.flaticon.com/512/4096/4096441.png", width=50, height=50)
    titre_SM = ft.Text("SearchMovies", size=36, weight=ft.FontWeight.BOLD)

    retour_menu = ft.Container(content=ft.Row(controls=[logo, titre_SM]), on_click=menu)

    b_favoris = IconButton(icon=ft.Icons.FAVORITE, icon_size=22, tooltip="Voir tes favoris", on_click=lambda e: favoris(zone_contenu, ligne_txt, page))


    the_header = ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[retour_menu, ft.Row(controls=[icon_menu, b_favoris, barre_recherche])])

    txt_trending = ft.Text("Films Trending:", size=20)


    grille = ft.GridView(expand=True, runs_count=5, spacing=30, run_spacing=30, child_aspect_ratio=0.7)

    response_trend = requests.get("https://api.themoviedb.org/3/trending/movie/day", params=params_details)

    films_trending = response_trend.json()["results"]

    for film in films_trending:
        if str(film["id"]) in liste_favoris and not film["poster_path"]:
            carte = ft.Container(border_radius=10, clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                                 content=ft.Stack(controls=[ft.Image(
                                     src=f"https://ih1.redbubble.net/image.4905811472.8675/bg,f8f8f8-flat,750x,075,f-pad,750x1000,f8f8f8.jpg",
                                     fit=ft.BoxFit.COVER),
                                     ft.Container(left=8, top=8,
                                                  padding=ft.Padding.symmetric(horizontal=6,
                                                                               vertical=3),
                                                  border_radius=8,
                                                  bgcolor=ft.Colors.with_opacity(0.7,
                                                                                 ft.Colors.BLACK),
                                                  content=ft.Row(spacing=3, tight=True,
                                                                 controls=[ft.Icon(ft.Icons.STAR,
                                                                                   color=ft.Colors.AMBER,
                                                                                   size=14),
                                                                           ft.Text(str(round(
                                                                               film[
                                                                                   "vote_average"],
                                                                               1)), size=12)])),
                                     ft.Container(right=6, top=6, border_radius=20,
                                                  bgcolor=ft.Colors.with_opacity(0.7,
                                                                                 ft.Colors.BLACK),
                                                  content=ft.IconButton(
                                                      icon=ft.Icons.FAVORITE,
                                                      icon_color=ft.Colors.RED_400, icon_size=18,
                                                      padding=4, tooltip="Ajouter aux favoris",
                                                      on_click=lambda e, f=film: add_favorite(f["title"], f["id"],
                                                                                              f["poster_path"],
                                                                                              f["vote_average"], e))),
                                     ft.Container(left=0, right=0, bottom=0, padding=8,
                                                  bgcolor=ft.Colors.with_opacity(0.7,
                                                                                 ft.Colors.BLACK),
                                                  content=ft.Text(film["title"], size=13,
                                                                  weight=ft.FontWeight.BOLD,
                                                                  max_lines=2,
                                                                  overflow=ft.TextOverflow.ELLIPSIS))]),
                                 on_click=lambda e, f=film: informations_film(f["id"], zone_contenu, ligne_txt, page,
                                                                              page_menu),
                                 )
            grille.controls.append(carte)

        elif str(film["id"]) in liste_favoris:
            carte = ft.Container(border_radius=10, clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                                 content=ft.Stack(controls=[
                                     ft.Image(src=f"https://image.tmdb.org/t/p/w500{film['poster_path']}",
                                              fit=ft.BoxFit.COVER),
                                     ft.Container(left=8, top=8, padding=ft.Padding.symmetric(horizontal=6, vertical=3),
                                                  border_radius=8, bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
                                                  content=ft.Row(spacing=3, tight=True,
                                                                 controls=[
                                                                     ft.Icon(ft.Icons.STAR, color=ft.Colors.AMBER,
                                                                             size=14),
                                                                     ft.Text(str(round(film["vote_average"], 1)),
                                                                             size=12)])),
                                     ft.Container(right=6, top=6, border_radius=20,
                                                  bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
                                                  content=ft.IconButton(icon=ft.Icons.FAVORITE,
                                                                        icon_color=ft.Colors.RED_400, icon_size=18,
                                                                        padding=4, tooltip="Ajouter aux favoris",
                                                                        on_click=lambda e, f=film: add_favorite(
                                                                            f["title"], f["id"], f["poster_path"],
                                                                            f["vote_average"], e))),
                                     ft.Container(left=0, right=0, bottom=0, padding=8,
                                                  bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
                                                  content=ft.Text(film["title"], size=13, weight=ft.FontWeight.BOLD,
                                                                  max_lines=2, overflow=ft.TextOverflow.ELLIPSIS))]),
                                 on_click=lambda e, f=film: informations_film(f["id"], zone_contenu, ligne_txt, page,
                                                                              page_menu))

            grille.controls.append(carte)



        elif not film["poster_path"]:
            carte = ft.Container(border_radius=10, clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                                 content=ft.Stack(controls=[ft.Image(
                                     src=f"https://ih1.redbubble.net/image.4905811472.8675/bg,f8f8f8-flat,750x,075,f-pad,750x1000,f8f8f8.jpg",
                                     fit=ft.BoxFit.COVER),
                                                            ft.Container(left=8, top=8,
                                                                         padding=ft.Padding.symmetric(horizontal=6,
                                                                                                      vertical=3),
                                                                         border_radius=8,
                                                                         bgcolor=ft.Colors.with_opacity(0.7,
                                                                                                        ft.Colors.BLACK),
                                                                         content=ft.Row(spacing=3, tight=True,
                                                                                        controls=[ft.Icon(ft.Icons.STAR,
                                                                                                          color=ft.Colors.AMBER,
                                                                                                          size=14),
                                                                                                  ft.Text(str(round(
                                                                                                      film[
                                                                                                          "vote_average"],
                                                                                                      1)), size=12)])),
                                                            ft.Container(right=6, top=6, border_radius=20,
                                                                         bgcolor=ft.Colors.with_opacity(0.7,
                                                                                                        ft.Colors.BLACK),
                                                                         content=ft.IconButton(
                                                                             icon=ft.Icons.FAVORITE_BORDER,
                                                                             icon_color=ft.Colors.RED_400, icon_size=18,
                                                                             padding=4, tooltip="Ajouter aux favoris", on_click=lambda e, f=film: add_favorite(f["title"], f["id"], f["poster_path"], f["vote_average"], e))),
                                                            ft.Container(left=0, right=0, bottom=0, padding=8,
                                                                         bgcolor=ft.Colors.with_opacity(0.7,
                                                                                                        ft.Colors.BLACK),
                                                                         content=ft.Text(film["title"], size=13,
                                                                                         weight=ft.FontWeight.BOLD,
                                                                                         max_lines=2,
                                                                                         overflow=ft.TextOverflow.ELLIPSIS))]),
                                 on_click=lambda e, f=film: informations_film(f["id"], zone_contenu, ligne_txt, page,
                                                                              page_menu),
                                 )
            grille.controls.append(carte)

        else:
            carte = ft.Container(border_radius=10, clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                                 content=ft.Stack(controls=[
                                     ft.Image(src=f"https://image.tmdb.org/t/p/w500{film['poster_path']}",
                                              fit=ft.BoxFit.COVER),
                                     ft.Container(left=8, top=8, padding=ft.Padding.symmetric(horizontal=6, vertical=3),
                                                  border_radius=8, bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
                                                  content=ft.Row(spacing=3, tight=True,
                                                                 controls=[
                                                                     ft.Icon(ft.Icons.STAR, color=ft.Colors.AMBER, size=14),
                                                                     ft.Text(str(round(film["vote_average"], 1)),
                                                                             size=12)])),
                                     ft.Container(right=6, top=6, border_radius=20,
                                                  bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
                                                  content=ft.IconButton(icon=ft.Icons.FAVORITE_BORDER,
                                                                        icon_color=ft.Colors.RED_400, icon_size=18,
                                                                        padding=4, tooltip="Ajouter aux favoris", on_click=lambda e, f=film: add_favorite(f["title"], f["id"], f["poster_path"], f["vote_average"], e))),
                                     ft.Container(left=0, right=0, bottom=0, padding=8,
                                                  bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
                                                  content=ft.Text(film["title"], size=13, weight=ft.FontWeight.BOLD,
                                                                  max_lines=2, overflow=ft.TextOverflow.ELLIPSIS))]),
                                 on_click=lambda e, f=film: informations_film(f["id"], zone_contenu, ligne_txt, page,
                                                                              page_menu))

            grille.controls.append(carte)

    zone_contenu = ft.Container(content=grille, expand=True)
    page_menu = grille

    ligne_txt = ft.Row(controls=[txt_trending])

    page.add(the_header, ligne_txt, zone_contenu)





def main(page: ft.Page):
    page.title = "Search Movies"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 1000
    page.window.height = 800

    page_accueil(page)


ft.run(main)