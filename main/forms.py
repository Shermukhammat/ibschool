from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'login__input',
            'placeholder': 'Foydalanuvchi nomi',
            'required': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'login__input',
            'placeholder': 'Parol',
            'required': True,
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove auto-focus and auto-complete
        self.fields['username'].widget.attrs.update({
            'autocomplete': 'username',
        })
        self.fields['password'].widget.attrs.update({
            'autocomplete': 'current-password',
        })

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, 
                username=username, 
                password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Foydalanuvchi nomi yoki parol noto'g'ri.",
                    code='invalid_login',
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data