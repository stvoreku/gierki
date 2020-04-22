from django.shortcuts import render
from django.views.generic import TemplateView, View
from .models import Game, Team, Word, Card
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
import random
# Create your views here.

class HomeView(TemplateView, LoginRequiredMixin):
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
            random_index = random.sample(list(Word.objects.values_list('id', flat=True)), 25)
            cards_list = []
            for a in random_index[0:9]:
                word = Word.objects.get(pk=int(a))
                newCard = Card(word = word, game = game, status='blue')
                cards_list.append(newCard)
                #newCard.save()
            for a in random_index[9:17]:
                word = Word.objects.get(pk=int(a))
                newCard = Card(word = word, game = game, status='red')
                #newCard.save()
                cards_list.append(newCard)
            for a in random_index[17:24]:
                word = Word.objects.get(pk=int(a))
                newCard = Card(word = word, game = game, status='none')
                #newCard.save()
                cards_list.append(newCard)
            word = Word.objects.get(pk=int(random_index[24]))
            newCard = Card(word=word, game=game, status='death')
            cards_list.append(newCard)
            random.shuffle(cards_list)
            for card in cards_list:
                card.save()
            return JsonResponse({'gamelink':'{}/'.format(game.id)})

class GameView(LoginRequiredMixin, TemplateView):
    template_name = 'game.html'

    def get_context_data(self, **kwargs):
        game = Game.objects.get(pk=int(self.kwargs['pk']))
        context = super(GameView, self).get_context_data(**kwargs)
        context['game'] = game
        context['team1'] = Team.objects.get(game=game, name='red')
        context['team2'] = Team.objects.get(game=game, name='blue')
        context['users'] = User.objects.all()
        context['cards'] = Card.objects.filter(game=game).order_by('id')
        return context
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if 'add_player' in request.POST: #dodawania gracza
                team = request.POST.get('team')
                player = request.POST.get('add_player')
                team = Team.objects.get(pk=int(team))
                team.player.add(User.objects.get(username=player))
                return JsonResponse({'success': team.name})
            if 'add_leader' in request.POST: #dodawnie lidera
                team = request.POST.get('team')
                player = request.POST.get('add_leader')
                team = Team.objects.get(pk=int(team))
                team.leader = User.objects.get(username=player)
                team.save()
                return JsonResponse({'success': team.name})
            if 'game_status' in request.POST:
                game = Game.objects.get(pk=int(self.kwargs['pk']))
                game.status = request.POST.get('game_status')
                game.save()
                return JsonResponse({'success': int(self.kwargs['pk'])})
            if 'card_tap' in request.POST:
                card = Card.objects.get(pk=int(request.POST.get('card_tap')))
                card.visible = True;
                card.uncovered_by = request.user
                card.save()
                return JsonResponse({'success': int(self.kwargs['pk'])})

class GameUpdate(View):
    #TODO list graczy poszczególnych drużyn
    #TODO refactor na ogólną klasę GameUpdate (uuuu!)
    def get(self, request, *args, **kwargs):
        if request.is_ajax():




            if 'game_number' in request.GET:
                gameid = request.GET.get('game_number')
                game = Game.objects.get(pk=int(gameid))
                # Pozyskiwanie listy graczy
                teams = Team.objects.filter(game=game)
                teams_list = {}
                for team in teams:
                    teams_list[team.name] = {'leader': team.leader, 'players': list(team.player.all().id)}

                # Pozyskiwanie informacji o kartach

                Cards = Card.objects.filter(game = game).order_by('id')
                card_list = []
                current_user = request.user #np bryla



                if game.status == 'active':
                    if Team.objects.filter(game=game, leader=current_user).count() > 0:
                        for card in Cards:
                            card_list.append({'id': card.id, 'word': card.word.word, 'status': card.status, 'visible': card.visible})
                    else:
                        for card in Cards:
                            if card.visible == True:
                                card_list.append({'id':card.id, 'word': card.word.word, 'visible': card.visible, 'status':card.status, 'uncovered_by': card.uncovered_by.username})
                            else:
                                card_list.append({'id':card.id, 'word': card.word.word, 'visible': card.visible})
                elif game.status == 'new':
                    for card in Cards:
                            card_list.append({'id':card.id, 'word': card.word.word})
                return JsonResponse({'cards': card_list, 'teams': teams_list})
