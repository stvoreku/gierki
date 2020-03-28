from django.shortcuts import render
from django.views.generic import TemplateView, View
from .models import Game, Team
from django.http import JsonResponse
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
            return JsonResponse({'gamelink':'ohanagierki.herokuapp.com/{}/'.format(game.id)})

class GameView(TemplateView):
    template_name = 'game.html'

    def get_context_data(self, **kwargs):
        game = Game.objects.get(pk=int(self.kwargs['pk']))
        context = super(GameView, self).get_context_data(**kwargs)
        context['game'] = game
        context['teams'] = Team.objects.filter(game=game)
        return context
    def get(self, request, *args, **kwargs):
        if request.is_ajax():

            return JsonResponse({'':'ohanagierki.herokuapp.com/{}/'.format(game.id)})