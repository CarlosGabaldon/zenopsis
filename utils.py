from django.conf import settings
import time
import urllib

class AuthUtil(object):
        
    @staticmethod
    def hash_query_string(username, version=1, time_sensitive=True):
        message = '%s#%s' % (username, version)
        qs = '&u=%s&v=%s' % (username, version)
        if time_sensitive:
            time_created = time.time()
            message += ('#%s' % time_created)
            qs += ('&t=%s' % time_created)
        hash = AuthUtil.generate_hash(message)
        qs = ('?auth=%s' % urllib.quote(hash)) + qs
        return qs
    
    @staticmethod
    def validate_query_string(request):
        auth = request.GET.get('auth')
        if auth:
            username = request.GET.get('u')
            version = request.GET.get('v')
            time_created = request.GET.get('t')
            message = '%s#%s' % (username, version)
            if time_created:
                message += ('#%s' % time_created)
            hash = AuthUtil.generate_hash(message)
            if hash == auth:
                if time_created:
                    if (time.time() - float(time_created) < 3601.0):
                        return True
                else:
                    return True         
        return False
            
    @staticmethod
    def generate_hash(message, key=settings.SECRET_KEY, base64_encode=True):
        import hashlib
        import hmac
        import base64
        # Use default md5 hash since Python 2.4 can't handle hashlib.sha1.
        digest = hmac.new(key, message).digest()
        if base64_encode:
            return base64.encodestring(digest).strip('\n')
        return digest        
