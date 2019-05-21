from django import forms

class inputform (forms.Form):
    info=forms.CharField()
    cost=forms.IntegerField()