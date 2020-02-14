from django.shortcuts import render
from .models import Level
from .models import World
from .models import Detail
from .models import Player
from django.http import Http404

def index(request):
    return render(request , 'game/index.html', {'levels' : Level.objects.all()})

def show(request , id):
    try:
        level = Level.objects.get(id=id)
        detail = Detail.objects.filter(id_level = id)
        # mettre les champs details1, details2, details3, details4, details5 à false si tous les champs sont à true + idlevel + 1
        player = Player.objects.get(id=1) 
        print(player.detail1)
    except Level.DoesNotExist:
        raise Http404(id)
    return render(request , 'game/level.html', { 'level' : level, 'detail' : detail})

def form_user(request):
    return render(request , 'game/form_user.html')

def add_user(request):
    #if request.is_ajax and request.POST:
    new_pseudo = request.POST.get('pseudo')
    players = Player.objects.all()
    for p in players:
        if new_pseudo == p.login:
            print("error")
            #ajouter message qui dit que le nom se trouve deja dans la bdd
            return render(request , 'game/form_user.html')
    #new_player = Player(login = new_pseudo)
    #new_player.save()
    # save ne marche pas car pas de valeur par défaut pour le level 1
    #appel de la vue 

    
