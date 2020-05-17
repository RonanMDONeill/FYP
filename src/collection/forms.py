from django import forms

# Allow a user to create a collection
class CreateNewColl(forms.Form):
	name = forms.CharField(label='Name', max_length=200)
