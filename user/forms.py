from django import forms


class UserRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput)
    dob = forms.DateField(required=False, label="Date Of Birth")


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class verifyForm(forms.Form):
    verify_code = forms.CharField(required=True)
