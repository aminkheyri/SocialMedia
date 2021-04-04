from django import forms

message = {
    'required': 'این فیلد اجباری است',
    'invalid': 'لطفا یک ایمیل معتبر وارد کنید',
    'max_length': 'تعداد کاراکتر ها نباید بیشتر از 50 تا باشد'
}


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=25, widget=forms.TextInput(
        attrs={'class': 'form-control', 'place-holder': 'User_Name'}
    ))
    password = forms.CharField(max_length=25, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'place-holder': 'Password'}
    ))


class UserRegistrationForm(forms.Form):
    username = forms.CharField(error_messages=message, max_length=25, widget=forms.TextInput(
        attrs={'class': 'form-control', 'place-holder': 'User_Name'}
    ))
    email = forms.EmailField(error_messages=message, max_length=50, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'place-holder': 'Email'}))
    password = forms.CharField(error_messages=message, max_length=60, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'place-holder': 'Password'}
    ))