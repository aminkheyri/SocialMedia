from django import forms


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=25, widget=forms.TextInput(
        attrs={'class': 'form-control', 'place-holder': 'User_Name'}
    ))
    password = forms.CharField(max_length=25, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'place-holder': 'Password'}
    ))


class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=25, widget=forms.TextInput(
        attrs={'class': 'form-control', 'place-holder': 'User_Name'}
    ))
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'place-holder': 'Email'}))
    password = forms.CharField(max_length=60, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'place-holder': 'Password'}
    ))