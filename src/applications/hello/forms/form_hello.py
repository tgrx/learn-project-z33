from django import forms

from applications.hello.forms.fields import NameField


class HelloForm(forms.Form):
    name = NameField(required=True)
    age = forms.IntegerField(min_value=0, max_value=110, required=True)
