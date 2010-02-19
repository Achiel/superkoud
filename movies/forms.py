from django import forms
from models import Movietip
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


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
  
class SKUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and password.
    """
    username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^\w+$',
        help_text = _("Required. 30 characters or fewer. Alphanumeric characters only (letters, digits and underscores)."),
        error_message = _("This value must contain only letters, numbers and underscores."))
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_("A user with that username already exists."))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        return password1

    def save(self, commit=True):
        user = super(SKUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class FollowForm(forms.Form):
	username = forms.CharField(
		widget=forms.HiddenInput,
		required=True
	)
