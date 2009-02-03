from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.core.exceptions import ObjectDoesNotExist
from gabaluu.account.models import Profile
from gabaluu.account.forms import ProfileForm, UserForm
from gabaluu.synopsis.models import Synopsis
from gabaluu.form_choices import get_country_name
import captcha

def signup(request, template_name='registration/register.html'):
    
    captcha_form = captcha.displayhtml("6LfitQAAAAAAAPuPkbRUUbT6mjhFbTGaS_nwKjkl")
    
    if request.method == 'POST':
        
        recaptcha_challenge_field = request.POST["recaptcha_challenge_field"]
        recaptcha_response_field = request.POST["recaptcha_response_field"]
        private_key = "6LfitQAAAAAAAGlpZA4DyouLEWRkfqLwBawQAxrq"
        remoteip = request.META['REMOTE_ADDR']
        
        captcha_response = captcha.submit(recaptcha_challenge_field=recaptcha_challenge_field,
                                          recaptcha_response_field=recaptcha_response_field,
                                          private_key=private_key,
                                          remoteip=remoteip)
        
        if captcha_response.is_valid:
            new_data = request.POST
            form = UserForm(data=new_data)

            if form.is_valid():
                new_user = form.save()
                profile = Profile(user=new_user,
                                  first_name=new_data['first_name'],
                                  last_name=new_data['last_name'],
                                  email=new_data['email'],
                                  country='us')
                profile.save()
                login(request, authenticate(username=new_data['username'],
                                        password=new_data['password2']))
                # Why doesn't this work? AttributeError: 'User' object has no attribute 'backend'
                #login(request, new_user)
                return HttpResponseRedirect("/accounts/profile/")
                
        else:
            form = UserForm(request.POST)
            captcha_error = "<span style='color:red'>Incorrect captcha, please try again!</span>"
            
    else:
        form = UserForm()
        captcha_error = ""

    return render_to_response(template_name, 
                            dict(form=form, 
                                 captcha_form=captcha_form,
                                 captcha_error=captcha_error),
                            context_instance=RequestContext(request))

@login_required
def profile(request, template_name='accounts/settings.html'):
    """
    Allows a user to view and edit their profile.

    Context::
        form
            The the profile form.


    Template::
        accounts/settings.html

    """
    # Settings.py: AUTH_PROFILE_MODULE = "account.profile"
    try:
        profile = request.user.get_profile()
    except ObjectDoesNotExist:
        # User not already in our account_profile table, 
        # probably a superuser created by Django's syncdb. 
        profile = Profile(user=request.user,
                          first_name=request.user.first_name,
                          last_name=request.user.last_name,
                          email=request.user.email)

    if request.method == 'POST':
        new_data = request.POST.copy()
        #Merge dictionaries so is_valid() can see request.FILES['avatar'].
        new_data.update(request.FILES)
        form = ProfileForm(data=new_data)
        if form.is_valid():            
            form.save(profile)
    else:
        form = ProfileForm(data=profile.__dict__)
    return render_to_response(template_name,
                              dict(form=form, profile=profile),
                              context_instance=RequestContext(request))

def user_profile_posted(request, username, template_name='accounts/profile.html'):
    return user_profile(request, username, "posted", template_name)

def user_profile_voted(request, username, template_name='accounts/profile.html'):
    return user_profile(request, username, "voted", template_name)

def user_profile_commented(request, username, template_name='accounts/profile.html'):
    return user_profile(request, username, "commented", template_name)
    
def user_profile(request, username, list, template_name='accounts/profile.html'):
     """
     User profile page.

     Context::
         user name.

     Template::
         accounts/profile.html

     """
     user = User.objects.get(username=username)
     profile =  user.get_profile()
 
     user_posted_synopsis_list = []
     user_voted_synopsis_list = []
     user_commented_synopsis_list = []
     if list == "voted":
         user_voted_synopsis_list = Synopsis.user_voted_synopsis_list(user=user)
     elif list == "commented":
         user_commented_synopsis_list = Synopsis.user_commented_synopsis_list(user=user)
     else:
        user_posted_synopsis_list = Synopsis.user_posted_synopsis_list(user=user)

     return render_to_response(template_name, 
                             dict(profile=profile,
                                  country=profile.country_name,
                                  username=username,
                                  list=list,
                                  user_posted_synopsis_list=user_posted_synopsis_list,
                                  user_voted_synopsis_list=user_voted_synopsis_list,
                                  user_commented_synopsis_list=user_commented_synopsis_list),
                             context_instance=RequestContext(request))




def members(request, template_name='accounts/members.html'):
     """
     Member list page.

     Context::
         None

     Template::
         accounts/members.html

     """
     profile_list = Profile.objects.all()
     return render_to_response(template_name, 
                             dict(profile_list=profile_list),
                             context_instance=RequestContext(request))

def auth(request):
    auth = request.GET.get('auth')
    app_name = request.GET.get('app')
    username = request.GET.get('u')
    if auth and app_name and username:
        if app_name == 'zenopsis':
            from gabaluu.utils import AuthUtil
            import urllib
            hash = AuthUtil.generate_hash('%s#%s' % (app_name, username))
            if hash == urllib.unquote(auth):
                # Set auth cookie???
                return HttpResponseRedirect('/accounts/profile')
            else:
                qs = '?auth=%s&app=%s&u=%s' % (urllib.quote(hash), app_name, username)
                return_url = 'http://zenopsis.com' + request.path
                return HttpResponseRedirect('https://gabaluu.com/accounts/auth/?return=%s%s' % (return_url, qs))
    else:
        raise Http404
