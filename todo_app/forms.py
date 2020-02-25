from django import forms


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=75)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
