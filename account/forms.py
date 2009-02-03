from django import newforms as forms
from django.conf import settings
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from gabaluu.form_choices import COUNTRIES
from gabaluu.account.models import Profile

# ProfileForm.is_valid() calls PictureField.clean() but value is always None???
class PictureField(forms.Field):
    def clean(self, value):
        if not value:
            raise forms.ValidationError("PictureField.clean: value is None.")
        ct = value['content-type']
        main, sub = ct.split('/')
        if not(main.lower() == 'image' and sub.lower() in ('png', 'jpeg', 'gif', 'x-png')):
            raise forms.ValidationError("A valid image must be JPG/JPEG, GIF, or PNG.")
        return value

class RegForm(forms.Form):
    first_name = forms.CharField(label=_('First Name'), max_length=30, required=True)
    last_name = forms.CharField(label=_('Last Name'), max_length=30, required=True)
    email = forms.EmailField(label=_('Email Address'), max_length=30, required=True)

class UserForm(RegForm):
    def __init__(self, data=None):
        super(RegForm, self).__init__(data=data)

    username = forms.CharField(label=_('Username'), max_length=30, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, label=_('Password1'), max_length=60, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, label=_('Password2'), max_length=60, required=True)

    def clean_username(self):
        un = self.data['username']
        try:
            User.objects.get(username=un)
        except User.DoesNotExist:
            return
        raise forms.ValidationError("The username '%s' is already taken." % un)

    def clean_password2(self):
        p2 = self.data['password2']
        if self.data['password1'] != p2:
            raise forms.ValidationError("Passwords must match.")
        else:
            return p2

    def save(self):
        # Use Django's auth_user table strictly for authentication.
        # Save email in our own account_profile table.
        u = User.objects.create_user(self.data['username'],
                                 '',
                                 self.data['password2'])
        u.save()
        return u

class ProfileForm(RegForm):
    """
    
    The basic account profile form.
      
    """
    def __init__(self, data=None):
        super(ProfileForm, self).__init__(data=data)

    #avatar = PictureField(widget=forms.FileInput, required=False, label=_('Photo'))
    avatar = forms.Field(widget=forms.FileInput, required=False, label=_('Photo'))
    country = forms.ChoiceField(label=_('Country'), widget=forms.Select(), choices=COUNTRIES,
                                required=False)

    def clean_avatar(self):        
        if 'avatar' in self.data:
            ct = self.data['avatar']['content-type']
            main, sub = ct.split('/')
            if not(main.lower() == 'image' and sub.lower() in ('png', 'jpeg', 'gif', 'x-png')):
                raise forms.ValidationError("A valid image must be JPG/JPEG, GIF, or PNG.")

    def save(self, profile):
        profile.first_name = self.data['first_name']
        profile.last_name = self.data['last_name']
        profile.email = self.data['email']
        profile.country = self.data['country']
        if 'avatar' in self.data:
            image = self.data['avatar']
            import os
            from os.path import splitext, exists
            fn = 'avatar' + splitext(image['filename'])[1].lower()
            user_fn = '_'.join([profile.user.username, fn])
            if profile.avatar and exists(profile.avatar):
                os.remove(profile.avatar)
            profile.avatar = image
            profile.save_avatar_file(user_fn, image['content'])

        profile.save()




        
