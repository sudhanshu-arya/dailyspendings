from django import forms

class formdata (forms.Form):
    info=forms.CharField()
    cost=forms.IntegerField()