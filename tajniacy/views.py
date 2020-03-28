from django.shortcuts import render
from django.views.generic import TemplateView, View
from .models import Game
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
            game = Game(status='active')
            game.save()
            return JsonResponse({'gameid':str(game.id)})

class GameView(TemplateView):
    template_name = 'game.html'