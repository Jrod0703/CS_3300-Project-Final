from django.db import models
from django.urls import reverse
import math

class Golfer(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # mail should be unique
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('golfer-detail', args=[str(self.id)])

class Notebook(models.Model): #one to one golfer to notebook notebook to golfer
    golfer = models.OneToOneField(Golfer, on_delete=models.CASCADE)

    def average_score(self):#function to get avg takes all score total divide by the rounds
        total_score = sum(round.score for round in self.golfround_set.all())
        number_of_rounds = self.golfround_set.count()
        return total_score / number_of_rounds if number_of_rounds else 0

    def __str__(self):#lable note for golfer name
        return f"Notebook for {self.golfer.name}"
    
    def get_absolute_url(self):#get rounds detils 
        return reverse('notebook-detail', args=[str(self.id)])

class GolfRound(models.Model):
    notebook = models.ForeignKey(Notebook, on_delete=models.CASCADE)
    date = models.DateField()
    score = models.IntegerField()

    def __str__(self):
        return f"Golf round on {self.date}"
    
    def get_absolute_url(self):
        return reverse('golfround-detail', args=[str(self.id)])
