from django.shortcuts import render
from .models import Level
from .models import World
from .models import Detail
from .models import Player
from .models import Clue
from django.http import Http404
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import json

BOSS_LEVEL_ID = 36
Boss_content = [
{'text' : 'Tu es sur le point de me retrouver. Je suis dans une ville que tu as sûrement reconnu à travers ces photos. Sais-tu où suis-je?', "responses" : ['Lyon', 'Bordeaux', 'Strasbourg' ,'Toulouse'], 'good_response' : 'Bordeaux', 'images' : ['w1level5.jpg', 'w4level2.jpg']},
{'text' : 'Tu as trouvé que je suis à Bordeaux. Dans l endroit où je suis, tu retrouveras un élément qui est dans ces deux tableaux à la fois', "responses" : ['Drapeau', 'Cheval', 'Eglise' ,'Voiture'], 'good_response' : 'Eglise', 'images' : ['w6level3.jpg', 'w6level4.jpg']},
{'text' : 'Tu y es presque ! Avec tout ce que tu sais sur l endroit où je suis, je suis sûre que tu peux trouver le tableau qui me contient', 'images' : [ 'choix1.jpg', 'choix2.jpg' , 'choix3.jpg', 'choix4.jpg'], 'good_response' : '3' },
{'text' : 'Et voilà, tu as retrouvé ma cachette! J espere que tu vois le point commum entre ces tableaux! Je suis comme eux', "responses" : ['Petit garçon', 'Animal', 'Marchand' ,'Oiseau'], 'good_response' : 'Petit garçon', 'images' : ['w2level3.jpg', 'w3level1.jpg']},
{'text' : 'Oh mais dans cet endroit, il y en a beaucoup comme moi ! C est plus simple si tu sais ce que je porte. Tu verras en commun avec ces tableaux!', "responses" : ['Chemise blanche', 'Chapeau', 'Pantalon orange' ,'Jupe'], 'good_response' : 'Chapeau', 'images' : ['w3level4.jpg', 'w6level5.jpg']},
{'text' : ['Presque mais ce n est pas moi, jouer n est pas ce qui m interesse le plus', 'Je préfère observer et parler de sujets intéressant avec une grande personne' , 'Je suis le petit garçon avec un manteau, pas loin de la porte de l eglise et en train de parler à la dame.'], 'position_x': 65, 'position_y': 87, 'width': 7, 'height':9, 'image' : 'choix3.jpg'},
]

# Affiche la page d'accueil
def index(request):
    return render(request , 'game/index.html')

# Affiche un niveau
def show(request):
    try:
        player = Player.objects.get(id = request.session['player_id'])
        level = player.id_level
        detail = Detail.objects.filter(id_level = level.id)
        i = 0
        for d in detail:
            d.clue = Clue.objects.get(id = d.id).content

    except Level.DoesNotExist or Player.DoesNotExist or Detail.DoesNotExist:
        return HttpResponseRedirect('/')
    return render(request , 'game/level.html', { 'level' : level, 'detail' : detail, 'player' : player })

# Affiche le formulaire pour commencer une partie (form_user.html avec bouton commencer)
def form_user_start(request):
    return render(request , 'game/form_user.html', {'start' :  'add_user' })

# Affiche le formulaire pour reprednre une partie (form_user.html avec bouton continuer)
def form_user_continue(request):
    return render(request , 'game/form_user.html', {'continue' :  'recover_user' })

# Passage au niveau suivant
def next_level(request):
    if request.session['player_id'] :
        player = Player.objects.get(id = request.session['player_id'])
        player_level = player.id_level
        id = (player_level.id)+1
        if id == BOSS_LEVEL_ID :
            player.id_level = BOSS_LEVEL_ID
            player.save()
            return HttpResponseRedirect('boss')
        next_level = Level.objects.get(id = id )
        player.id_level = next_level
        print(player.currentClick)
        if player.currentClick > 15 :
            player.nb_stars = player.nb_stars + 1
        elif player.currentClick <= 15 and player.currentClick > 10 :
            player.nb_stars = player.nb_stars + 3
        elif player.currentClick <= 10 and player.currentClick > 5 :
            player.nb_stars = player.nb_stars + 6
        elif player.currentClick == 5 :
            player.nb_stars = player.nb_stars + 10
        player.totalClick = player.totalClick + player.currentClick
        player.currentClick = 0
        player.detail1 = False
        player.detail2 = False
        player.detail3 = False
        player.detail4 = False
        player.detail5 = False

        player.save()
        return HttpResponseRedirect('level')
    return render(request , 'game/index.html')

# Cree un nouveau joueur
def add_user(request):
    first_level = 1
    if request.POST:
        new_pseudo = request.POST.get('pseudo')
        players = Player.objects.all()
        for p in players:
            if new_pseudo == p.login:
                return render(request , 'game/form_user.html', {'error' : "Ce pseudo est déjà utilisé.", 'start' :  'add_user'})
        level = Level.objects.get(id=first_level)
        new_player = Player(login = new_pseudo, id_level = level, nb_stars  = 3)
        new_player.save()
        request.session['player_id'] = new_player.id
        return HttpResponseRedirect('level')

# Recupere la partie d'un joueur
def recover_user(request):
    if request.POST:
        user_pseudo = request.POST.get('pseudo')
        players = Player.objects.all()
        for p in players:
            if user_pseudo == p.login:
                request.session['player_id'] = p.id
                level = Level.objects.get(name = p.id_level)
                return HttpResponseRedirect('level')
        return render(request , 'game/form_user.html', {'error' : "Aucune partie ne correspond à ce joueur.", 'continue' :  'recover_user' })

# Enregistre un ddétail trouvé dans la BDD
def check_detail(request):
    if request.is_ajax and request.POST:
        num = request.POST.get('num')
        player = Player.objects.get(id = request.session['player_id'])
        if num == '1' :
            player.detail1 = True
        elif num == '2' :
            player.detail2 = True
        elif num == '3' :
            player.detail3 = True
        elif num == '4' :
            player.detail4 = True
        elif num == '5' :
            player.detail5 = True
        player.save()
        return HttpResponse(json.dumps("ok"), content_type="application/json")
    else:
        raise Http404
# Enregistre  un nouveau clic dans la BDD
def new_click(request):
    if request.is_ajax and request.POST:
        player = Player.objects.get(id = request.session['player_id'])
        player.currentClick = player.currentClick + 1;
        player.save()
        return HttpResponse(json.dumps("ok"), content_type="application/json")
    else:
        raise Http404

# Décremente le compteur à l'achat d'une étoile
def buy_clue(request):
    if request.is_ajax and request.POST:
        player = Player.objects.get(id = request.session['player_id'])
        player.nb_stars = player.nb_stars - 3;
        player.save()
        return HttpResponse(json.dumps("ok"), content_type="application/json")
    else:
        raise Http404

def boss(request):
    try:
        player = Player.objects.get(id = request.session['player_id'])
        error = ""
        #if player.id_level != BOSS_LEVEL_ID :
        #    raise Http404
        step = 0
        if request.POST:
            step = int(request.POST.get('step'))
            if request.POST.get('response') == Boss_content[step]['good_response'] :
                player.nb_stars = player.nb_stars + 5
                step = step + 1
            else :
                player.nb_stars = player.nb_stars - 3
                error = "Mauvaise réponse, réessaie !"
            player.save()
    except Player.DoesNotExist:
        raise Http404

    if step == 0 or step == 1 or step == 3 or step == 4:
        return render(request , 'game/boss.html', {'basic' : 'true', 'player' : player, 'title' : 'boss', 'step' : step, 'text' : Boss_content[step]['text'], 'responses' : Boss_content[step]['responses'], 'images' : Boss_content[step]['images'], 'error' : error})
    if step == 2 :
        return render(request , 'game/boss.html', {'middle' : 'true', 'player' : player, 'title' : 'boss', 'step' : step, 'text' : Boss_content[step]['text'], 'images' : Boss_content[step]['images'], 'error' : error})
    return render(request , 'game/boss.html', {'middle' : 'true', 'player' : player, 'title' : 'boss', 'step' : step, 'text' : Boss_content[step]['text'], 'position_x' : Boss_content[step]['position_x'], 'position_y' : Boss_content[step]['position_y'], 'height' : Boss_content[step]['height'], 'width' : Boss_content[step]['width'], 'image' : Boss_content[step]['image']})
