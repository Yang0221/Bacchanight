from django.shortcuts import render
from .models import Level
from .models import World
from .models import Detail
from .models import Player
from django.http import Http404
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

#Page d"accueil à revoir
####################TO DO ##############################################################
def index(request):
    return render(request , 'game/index.html', {'levels' : Level.objects.all()})

# Affiche un niveau
def show(request):
    try:
        player = Player.objects.get(id = request.session['player_id'])
        level = player.id_level
        detail = Detail.objects.filter(id_level = level.id)
    except Level.DoesNotExist or Player.DoesNotExist or Detail.DoesNotExist:
        return HttpResponseRedirect('/')
    return render(request , 'game/level.html', { 'level' : level, 'detail' : detail, 'player' : player})

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
        next_level = Level.objects.get(id = (player_level.id)+1 )
        player.id_level = next_level
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
                return render(request , 'game/form_user.html', {'error' : "Ce pseudo est déjà utilisé."})
        level = Level.objects.get(id=first_level)
        new_player = Player(login = new_pseudo, id_level = level)
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
        return render(request , 'game/form_user.html', {'error' : "Aucune partie ne correspond à ce joueur."})

# Enregistre un ddétail trouvé dans la BDD
# Marche pas pour le momement (liée au AJAX qui marche pas)
def check_detail(request):
    if request.is_ajax and request.POST:
        num = request.POST.get('num')
        player = Player.objects.get(id = request.session['player_id'])
        print("ok")
        if num == 1 :
            player.detail1 = True
        elif num == 2 :
            player.detail2 = True
        elif num == 3 :
            player.detail3 = True
        elif num == 4 :
            player.detail4 = True
        elif num == 5 :
            player.detail5 = True
        player.save()
        return HttpResponse(json.dumps("ok"), content_type="application/json")
    else:
        raise Http404
