from django import forms
from .models import Join

#This is for regular django forms in views.py
class EmailForm(forms.Form):
	email = forms.EmailField()


#This is for model forms in views.py
class JoinForm(forms.ModelForm):
	class Meta:
		model  = Join
		fields = ['email',]