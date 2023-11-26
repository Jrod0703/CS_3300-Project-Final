from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User  # import the User model

class Golfer(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    # linked Golfer model to User with a One-to-One field

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        # Assuming you want to use the related User's username
        return self.user.username
    
    def get_absolute_url(self):
        return reverse('golfer-detail', args=[str(self.id)])

class Notebook(models.Model): 
    golfer = models.OneToOneField(Golfer, on_delete=models.CASCADE)

    # new (explore from class) files for image and videos of their golf swing or golf card.
    image = models.ImageField(upload_to='notebooks/images/', blank=True, null=True)
    video = models.FileField(upload_to='notebooks/videos/', blank=True, null=True)
    

    def average_score(self): 
        # function to get avg takes all score total divide by the rounds
        total_score = sum(round.score for round in self.golfround_set.all())
        number_of_rounds = self.golfround_set.count()
        return total_score / number_of_rounds if number_of_rounds else 0

    def __str__(self):
        # label note for golfer name (now using user's username)
        return f"Notebook for {self.golfer.user.username}"
    
    def get_absolute_url(self):
        # get rounds details 
        return reverse('notebook-detail', args=[str(self.id)])

class GolfRound(models.Model):
    notebook = models.ForeignKey(Notebook, on_delete=models.CASCADE)
    date = models.DateField()
    score = models.IntegerField()

    def __str__(self):
        return f"Golf round on {self.date}"
    
    def get_absolute_url(self):
        return reverse('golfround-detail', args=[str(self.id)])
