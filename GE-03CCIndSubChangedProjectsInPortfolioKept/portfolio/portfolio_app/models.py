from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.

class Portfolio(models.Model):
    title = models.CharField(max_length=200, default=timezone.now)
    contact_email = models.CharField(max_length=200, default=timezone.now)
    is_active = models.BooleanField(default=False)
    about = models.TextField(blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('portfolio-detail', args=[str(self.id)])


class Project(models.Model):
    title = models.CharField(max_length=200, default=timezone.now)
    description = models.TextField()
    #portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, default = None)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('project-detail', args=[str(self.id)])

class ProjectsInPortfolio(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class Meta:
    unique_together = ('portfolio', 'project')

class Student(models.Model):
    #List of choices for majors
    MAJOR =(
        ('CSCI-BS', 'BS in Computer Science'),
        ('CPEN-BS', 'BS in Computer Engineering'),
        ('BIGD-BI', 'BI in Game Design and Development'),
        ('BICS-BI', 'BI in Computer Science'),
        ('BISC-BI', 'BI in Computer Security'),
        ('CSCI-BA', 'BA in Computer Science'),
        ('DASE-BS', 'BS in Data Analytics and Systems Engineering')
        
    )#end of major

    name = models.CharField(max_length=200)
    email = models.CharField("UCCS Email", max_length=200)
    major = models.CharField(max_length=200, choices=MAJOR)#, blank = True)
    portfolio = models.OneToOneField(Portfolio, on_delete=models.CASCADE, null = True, default = None, blank = True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('student-detail', args=[str(self.id)])
