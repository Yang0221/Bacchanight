from django.shortcuts import render
from .models import Level
from .models import World
from .models import Detail
from .models import Player
from django.http import Http404
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

def index(request):
    return render(request , 'game/index.html', {'levels' : Level.objects.all()})

#TODO : récupérer player dans la variable globale --> details + level en fonction + champs détail1 ... details5
# a appeler a chaque affichage d'un level
def show(request , id):
    try:
        level = Level.objects.get(id=id)
        detail = Detail.objects.filter(id_level = id)
        player = Player.objects.filter(id=request.session['player_id'])
        print(player)
    except Level.DoesNotExist:
        raise Http404(id)
    return render(request , 'game/level.html', { 'level' : level, 'detail' : detail, 'player' : player})

def form_user(request):
    return render(request , 'game/form_user.html')

def add_user(request):
    first_level = 1
    if request.POST:
        new_pseudo = request.POST.get('pseudo')
        players = Player.objects.all()
        for p in players:
            if new_pseudo == p.login:
                print("error")
                #ajouter message qui dit que le nom se trouve deja dans la bdd
                return render(request , 'game/form_user.html', {'error' : "Ce pseudo est déjà utilisé."})
        level = Level.objects.get(id=first_level)
        new_player = Player(login = new_pseudo, id_level = level)
        new_player.save()
        request.session['player_id'] = new_player.id
        return HttpResponseRedirect('level/' + str(first_level))

    
