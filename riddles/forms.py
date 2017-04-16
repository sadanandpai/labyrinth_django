from django import forms

class SigninForm(forms.Form):
    username = forms.CharField(min_length=6, max_length=15)
    password = forms.CharField(min_length=6, max_length=15)


class SignupForm(forms.Form):
    signup_username = forms.CharField(min_length=6, max_length=15)
    signup_password = forms.CharField(min_length=6, max_length=15)
    mobile = forms.CharField(min_length=10, max_length=12)
    email = forms.EmailField(min_length=6, max_length=50)

class AnswerForm(forms.Form):
    answer = forms.CharField(max_length=50)
