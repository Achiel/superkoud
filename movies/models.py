from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Movie(models.Model):
	title = models.TextField(unique=True)
	def __str__(self):
		return self.title
	
class Movietip(models.Model): 
	user = models.ForeignKey(User)
	movie = models.ForeignKey(Movie)
	description = models.TextField(unique=False)
	def __str__(self): 
	    return self.movie.title + " " + self.description
	
class Tag(models.Model): 
	name = models.CharField(max_length=64, unique=True) 
	movietips = models.ManyToManyField(Movietip)
	def __str__(self): 
	    return self.name

class Moviewish(models.Model):
	user = models.ForeignKey(User)
	movie = models.ForeignKey(Movie)
	def __str__(self): 
	    return self.movie.title