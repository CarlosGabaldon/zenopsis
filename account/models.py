from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    first_name = models.CharField(maxlength=50)
    last_name = models.CharField(maxlength=50)
    email = models.CharField(maxlength=80)
    avatar = models.ImageField(upload_to='media/avatars', blank=True, null=True)
    country = models.CharField(maxlength=50, null=True)


    def _get_full_name(self):
        """Return the person's full name."""
        return u'%s %s' % (self.user.first_name, self.user.last_name)
    full_name = property(_get_full_name)
    

    def _get_avatar_filename(self):
        """Return the avatar's filename."""
        from os.path import split
        return u'%s' % split(self.avatar)[1]
    avatar_filename = property(_get_avatar_filename)
    
    def _get_full_country_name(self):
        """Return the full country name."""
        from gabaluu.form_choices import get_country_name
        return get_country_name(self.country)
    country_name = property(_get_full_country_name)
    
    @classmethod
    def remove_dups(cls, list):
        """ Returns a list with all duplicate items removed (maintains order) """
        uniqueList = []
        [uniqueList.append(item) for item in list if item not in uniqueList]
        return uniqueList;
    
    @classmethod
    def query(cls, query):
        """Run query against user profiles"""
        keywords = query.split(' ')
        keywords = filter(None, keywords)
        profiles = []
        if not keywords:
            return Profile.objects.all()
 
        for keyword in keywords:
            filtered_profiles = Profile.objects.filter(Q(user__username__icontains=keyword))
            if filtered_profiles:      
                profiles.extend(filtered_profiles)
                
        return Profile.remove_dups(profiles)    
     

