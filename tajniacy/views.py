from django.shortcuts import render
from django.views.generic import TemplateView, View
from .models import Game, Team, Word, Card
from django.contrib.auth.models import User
from django.http import JsonResponse
import random
# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'


    def get_context_data(self, **kwargs):

        context = super(HomeView, self).get_context_data(**kwargs)
        context['games_list'] = Game.objects.all()

        return context

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            game = Game(status='new')
            game.save()
            team_1 = Team(name = 'red', game = game)
            team_2 = Team(name = 'blue', game = game)
            team_1.save()
            team_2.save()
            random_index = random.sample(list(Word.objects.values_list('id', flat=True)), 2)
            for a in random_index:
                word = Word.objects.get(pk=int(a))
                newCard = Card(word = word, game = game, status='None')
                newCard.save()
            return JsonResponse({'gamelink':'{}/'.format(game.id)})

class GameView(TemplateView):
    template_name = 'game.html'

    def get_context_data(self, **kwargs):
        game = Game.objects.get(pk=int(self.kwargs['pk']))
        context = super(GameView, self).get_context_data(**kwargs)
        context['game'] = game
        context['team1'] = Team.objects.get(game=game, name='red')
        context['team2'] = Team.objects.get(game=game, name='blue')
        context['users'] = User.objects.all()
        context['cards'] = Card.objects.filter(game=game)
        return context
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if 'add_player' in request.POST:
                team = request.POST.get('team')
                player = request.POST.get('add_player')
                team = Team.objects.get(pk=int(team))
                team.player.add(User.objects.get(username=player))
                return JsonResponse({'success': team.name})
            if 'add_leader' in request.POST:
                team = request.POST.get('team')
                player = request.POST.get('add_leader')
                team = Team.objects.get(pk=int(team))
                team.leader = User.objects.get(username=player)
                team.save()
                return JsonResponse({'success': team.name})
            if 'game_status' in request.POST:
                game = Game.objects.get(pk=int(self.kwargs['pk']))
                game.status = request.POST.get('game_status')
                return JsonResponse({'success': int(self.kwargs['pk'])})

class GameUpdate(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            if 'game_number' in request.POST:
                gameid = request.post.get('game_number')
                Cards = Card.objects.filter(game = Game.objects.get(pk=int(gameid)))
                return JsonResponse({'cards': gameid})
