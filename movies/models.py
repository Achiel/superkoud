from django.db import models
from django.db.models.signals import post_save

# Create your models here.
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	following = models.ManyToManyField(User, symmetrical=False, related_name="following")
	joined = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return "User profile for %s" % user.username
		
class Movie(models.Model):
	title = models.TextField(unique=True)
	trailer = models.URLField()
	imdb = models.URLField()
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

# Signals:
def create_profile(sender, **kwargs):
	print "should create profile"

post_save.connect(create_profile, sender=User, created=True)
