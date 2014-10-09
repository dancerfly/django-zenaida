from django import forms
from zenaida.contrib.hints.models import Dismissed


class DismissHintForm(forms.ModelForm):
	"""
	A form that creates a Dismissed object. Requires a user object be passed
	as a keyword argument for the `save` method to work.

	"""

	key = forms.CharField(max_length=255, widget=forms.HiddenInput)

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user') if 'user' in kwargs else None
		return super(DismissHintForm, self).__init__(*args, **kwargs)

	def save(self, *args, **kwargs):
		if self.user is None:
			raise Exception("DismissHintForm must be called with a user to be saved.")
		obj = super(DismissHintForm, self).save(commit=False)
		obj.user = self.user
		return obj.save()

	class Meta:
		model = Dismissed
		exclude = ['user',]
