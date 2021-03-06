from django import forms
from .models import Profile

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
        attrs={'class': 'form-control', 'place-holder': 'User_Name'}))
    email = forms.EmailField(error_messages=message, max_length=50, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'place-holder': 'Email'}))
    password = forms.CharField(error_messages=message, max_length=60, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'place-holder': 'Password'}))


class EditProfileForm(forms.ModelForm):
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(
        attrs={'class': 'form-control col-md-2', 'place-holder': 'Email'}))
    first_name = forms.CharField(error_messages=message, max_length=25, widget=forms.TextInput(
        attrs={'class': 'form-control col-md-2', 'place-holder': 'first_name'}))
    last_name = forms.CharField(error_messages=message, max_length=25, widget=forms.TextInput(
        attrs={'class': 'form-control col-md-2', 'place-holder': 'last_name'}))

    class Meta:
        model = Profile
        fields = ('bio', 'age', 'phone')


class PhoneLoginForm(forms.Form):
    phone = forms.IntegerField()

    def clean_phone(self):
        phone = Profile.objects.filter(phone=self.cleaned_data['phone'])
        if not phone.exists():
            raise forms.ValidationError('this phone number does not exists')
        return self.cleaned_data['phone']


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()