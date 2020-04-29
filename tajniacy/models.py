from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Game(models.Model):
    data = models.DateField(auto_now_add=True) #pole z data automatycznie ustawiana przy dodawaniu
    status = models.CharField(max_length=20) #pole znakow o max dlugosci 20

class Word(models.Model):
    uses = models.IntegerField(default=0) #pole numeryczne z domyslna wartoscia 0
    word = models.CharField(max_length=100, unique=True) #pole znakow z max dlugoscia 100, z ochrona przed duplikacja (wymuszeniem unikatowosci)

    def __str__(self):  #to definiuje jak obiekt bedzie wygladal przy probie zamienienia na stringa. czyli print(word) zwroci word.word
        return self.word

class Card(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE) #FK, czyli trzyma tu identyfikator slowa. Czyli kazda karta przypina sie do jednego slowa
    visible = models.BooleanField(default=False) #Bool - wartosc logiczna prawda/falsz. Tu domyslnie zawze falsz (karty domyslnie sa zakryte)
    status = models.CharField(max_length=10) #status trzymam jako kombinacje 10 znakow. Popularne jest dla oszczednosci miejsca zakodowanie statusu na liczbach i pozniejsze dekodowanie (jesli mamy 10 mozliwych statusow to wystarcza 2 znaki na 0-9)
    game = models.ForeignKey(Game, on_delete=models.CASCADE) #Analogicznie, kazda karta jest podpieta do jednej konkretnej gry
    uncovered_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE) #kazda karta podpieta jest do jednego uzytkownika po odkryciu. Null true oznacza ze moze nie byc przypieta do nikogo (pole moze byc puste)


class Team(models.Model):
    name = models.CharField(max_length=30)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ManyToManyField(User, related_name="players") #zamiast pola FK mozymy miec MtM. To pozwala na relacje wielu uzytkownikow do wielu druzyn (druzyna jest tworzona per gre wiec pozwolilem aby jeden user byl w wielu teamach)
    leader = models.ForeignKey(User, on_delete=models.CASCADE, null=True)





