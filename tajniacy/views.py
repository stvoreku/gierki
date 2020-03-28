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
            items = Word.objects.all()
            random_words = random.sample(items, 2)
            for a in random_words:
                newCard = Card(word = a, game = game, status='None')
            return JsonResponse({'gamelink':'ohanagierki.herokuapp.com/{}/'.format(game.id)})

class GameView(TemplateView):
    template_name = 'game.html'

    def get_context_data(self, **kwargs):
        game = Game.objects.get(pk=int(self.kwargs['pk']))
        context = super(GameView, self).get_context_data(**kwargs)
        context['game'] = game
        teams = Team.objects.filter(game=game)
        context['team1'] = teams[0]
        context['team2'] = teams[1]
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
                return JsonResponse({'success': team.name})
            if 'game_status' in request.POST:
                game = Game.objects.get(pk=int(self.kwargs['pk']))
                game.status = request.POST.get('game_status')
                return JsonResponse({'success': int(self.kwargs['pk'])})

class GameUpdate(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return JsonResponse({'ping': 'pong'})
