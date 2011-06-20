from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from dungeon.forms import *
from dungeon.models import *
from django.shortcuts import get_object_or_404
from random import randint
from dungeon.lexicon import *
from dungeon.rooms import *

def main_page(request):
    
    try:
        user = request.user
        players = Player.objects.filter(user=user.id)
    except Player.DoesNotExist:
        players = Null
    
    if request.GET and request.GET['deleted'] == "true":
        message = "%s deleted successfully" % request.GET['playername']
    else:
        message = False
        
    
    variables = RequestContext(request, {
        'players': players,
        'message': message
    })
    return render_to_response('main_page.html', variables)

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
    

def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response(
        'registration/register.html',
        variables
    )

def create_player(request):
    user = request.user
    if request.method == 'POST':
        form = NewPlayerForm(request.POST)
        if form.is_valid():
            constitution = randint(1, 100)
            health = 100 + constitution
            player = Player(player_name=form.cleaned_data['player_name'], 
                            user=request.user,
                            inventory=" ",
                            location="Entrance",
                            last_location="Entrance",
                            luck=randint(1, 100),
                            strength=randint(1, 100),
                            constitution=constitution,
                            speed=randint(1, 100),
                            health=health,
                            alive=True,
                            achievements=" " )
            player.save()
            
            return HttpResponseRedirect('/players/%s/%s/?new=true' % (user.username, player.player_name))
    else:
        form = NewPlayerForm()
    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response(
        'players/create_player.html',
        variables
    )

def player(request, username, player_name):
    user = get_object_or_404(User, username=username)
    try:
        players = Player.objects.filter(user=user).filter(player_name=player_name)
        player = players[0]
    except Player.DoesNotExist:
        raise Http404
    
    if request.method == "POST":
        playername = player.player_name
        player.delete()
        return HttpResponseRedirect('/?deleted=true&playername=%s' % playername)    
    
    if request.GET and request.GET['new'] == "true":
        new = True
    else:
        new = False
    
    total_health = 100 + player.constitution
        
    
    variables = RequestContext(request, {
        'new': new,
        'player': player,
        'total_health': total_health
    })
    
    return render_to_response(
        'players/player.html',
        variables
    )
    
def play(request, username, player_name):

    user = get_object_or_404(User, username=username)
    try:
        players = Player.objects.filter(user=user).filter(player_name=player_name)
        player = players[0]
    except Player.DoesNotExist:
        raise Http404
        
    lexicon = Lexicon()
    
    room = rooms(player, player.location)
    
    if room.nouns:
        for noun in room.nouns:
            if noun in lexicon.nouns:
                pass
            else:        
                lexicon.nouns.append(noun)
                
    text = room.enter()
    
    if request.method == "POST":
        form = GameForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            try: 
                sentence = lexicon.parse_sentence(prompt)
                text = room.actions(sentence)
                if player.location != player.last_location:
                    room = rooms(player, player.location)
                    text = room.enter()
                    player.last_location = player.location
            except ParseError:
                text = "I didn't understand that - say again?"
    else:
        form = GameForm() 
    
    player.save()
    
    variables = RequestContext(request, {
        'text': text,
        'player': player,
        'form': form,
    })
    
    return render_to_response(
        'play.html',
        variables
    )
    
    