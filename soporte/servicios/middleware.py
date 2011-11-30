from django.http import HttpResponseRedirect
from django.conf import settings
import re






class EnforceLoginMiddleware(object):
    

    def __init__(self):
        self.login_url   = getattr(settings, 'LOGIN_URL', '/accounts/login/' )
        if hasattr(settings,'PUBLIC_URLS'):
            public_urls = [re.compile(url) for url in settings.PUBLIC_URLS]
        else:
            public_urls = [(re.compile("^%s$" % ( self.login_url[1:] )))]
        if getattr(settings, 'SERVE_STATIC_TO_PUBLIC', True ):
            root_urlconf = __import__(settings.ROOT_URLCONF)
            public_urls.extend([ re.compile(url.regex) 
                for url in root_urlconf.urls.urlpatterns 
                if url.__dict__.get('_callback_str') == 'django.views.static.serve' 
            ])
        self.public_urls = tuple(public_urls)

    def process_request(self, request):
       
        try:
            if request.user.is_anonymous():
                for url in self.public_urls:
                    if url.match(request.path[1:]):
                        return None
                return HttpResponseRedirect("%s?next=%s" % (self.login_url, request.path))
        except AttributeError:
            return HttpResponseRedirect("%s?next=%s" % (self.login_url, request.path))
