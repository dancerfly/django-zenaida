from django import forms
from zenaida.contrib.hints.models import Dismissed


class DismissHintForm(forms.ModelForm):
	"""
	A form that creates a Dismissed object.

	The object created by this form will need to have a user added to it
	before saving, like so:

	>>> form = DismissHintForm(request.POST)
	>>> obj = form.save(commit=False)
	>>> obj.user = request.user
	>>> obj.save()

	"""
	key = forms.CharField(max_length=255, widget=forms.HiddenInput)

	class Meta:
		model = Dismissed
		exclude = ['user',]
