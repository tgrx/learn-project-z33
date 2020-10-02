from django import forms


class HelloForm(forms.Form):
    name = forms.CharField(min_length=3, max_length=1000, required=True)
    age = forms.IntegerField(min_value=0, max_value=110, required=True)

    def clean_name(self):
        name = self.cleaned_data["name"]
        if not name.startswith("a"):
            raise forms.ValidationError("name must starts with 'a'")

        return name
