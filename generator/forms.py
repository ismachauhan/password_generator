from django import forms

class PasswordForm(forms.Form):
    password_text = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
