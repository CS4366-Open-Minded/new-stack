"""
Definition of forms.
"""

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .models import STATE_CHOICES

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses bootstrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


class BootstrapRegistrationForm(forms.ModelForm):
    """Registration form which uses bootstrp CSS."""

    error_messages = {
        'username_exists:': _("The username %(username) already exists."),
        'email_exists':_("The email %(email) already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.CharField(label=_("User Name"),max_length=254, min_length=8, 
                               widget=forms.TextInput({
                                   'class':'form-control',
                                   'placeholder':'User name'}),
                               help_text=_("Enter a username."),
                )
    email = forms.EmailField(label=_("Email"),
                                     widget=forms.EmailInput({
                                         'class':'form-control',
                                         'placeholder':'Email'}),
                                     help_text=_("Enter a valid email address.")
                                     )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput({
                                     'class':'form-control',
                                     'placeholder':'Password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput({
                                     'class':'form-control',
                                     'placeholder':'Confirm Password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super(BootstrapRegistrationForm, self).__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        u = User.objects.filter(username=username)
        if u.count():
            raise forms.ValidationError(
                self.error_messages['username_exists'],
                code='username_exists',
                )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        u = User.objects.filter(email=email)
        if u.count():
            raise forms.ValidationError(
                self.error_messages['email_exists'],
                code='email_exists',
                )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user