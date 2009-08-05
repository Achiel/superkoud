from django import forms
from models import Movietip
from django.forms import ModelForm


class MovieSaveForm(forms.Form): 
  title = forms.CharField( 
    label='Title', 
    widget=forms.TextInput(attrs={'size': 64}) 
  ) 

class MovietipSaveForm(forms.Form): 
	movie = forms.CharField( 
		label='Movie', 
		widget=forms.TextInput(attrs={'size': 64}),
		required=True
	) 
	description = forms.CharField( 
		label='Description', 
		required=False, 
		widget=forms.TextInput(attrs={'size': 64}) 
	)
	tags = forms.CharField(
		label='Tags', 
		required=False, 
		widget=forms.TextInput(attrs={'size': 64})
	)
	
class MoviewishSaveForm(forms.Form):
	movie = forms.CharField( 
		label='Moviewish', 
		widget=forms.TextInput(attrs={'size': 64}),
		required=True
	)
	
class MoviewishConvertForm(forms.Form):
	movie = forms.CharField(
		widget=forms.HiddenInput
	)
	# class Meta:
	# 	model = Movietip
	# 	exclude = ('user',)
  