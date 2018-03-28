"""
Definition of forms.
"""

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
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


class BootstrapRegistrationForm(UserCreationForm):
    """Registration form which uses bootstrp CSS."""        
    class Meta(UserCreationForm.Meta):
            model = User
            fields = UserCreationForm.Meta.fields + ('email', 'password1', 'password2')
            field_classes = {'username': UsernameField}

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'email_exists':_("The entered email already exists."),
    }

    username = forms.CharField(label=_("User Name"),max_length=254, min_length=7, 
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
        min_length=8,
        strip=False,
        widget=forms.PasswordInput({
                                     'class':'form-control',
                                     'placeholder':'Password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        min_length=8,
        strip=False,
        widget=forms.PasswordInput({
                                     'class':'form-control',
                                     'placeholder':'Confirm Password'}),
        help_text=_("Enter the same password as before, for verification."),
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).count():
            raise forms.ValidationError(
                self.error_messages['email_exists'],
                code='email_exists',
                )
        return email

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
        #user = super(UserCreationForm, self).save(commit=False)
        #user.set_password(self.cleaned_data["password1"])
        #if commit:
        #    user.save()

        # Create user
        user = User.objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'], password=self.cleaned_data['password1'])
        
        # Make user inactive
        user.is_active = False
        user.save()

        return user