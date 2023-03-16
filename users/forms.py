from django import forms
from allauth.account.forms import SignupForm
from .models import User

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']



class MyCustomSignupForm(SignupForm, forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput())
    # confirm_password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(MyCustomSignupForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['email', ]

    def clean(self):
        clean_data = super(MyCustomSignupForm, self).clean()
        password = clean_data.get("password")
        confirm_password = clean_data.get("confirm_password")
    
        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm password does not match"
            )
