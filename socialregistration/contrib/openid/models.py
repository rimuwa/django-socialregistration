from django.conf import settings
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth import authenticate

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class OpenIDProfile(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL)
    site = models.ForeignKey(Site, default=Site.objects.get_current)
    identity = models.TextField(unique=True)

    def __unicode__(self):
        try:
            return 'OpenID profile for %s, via provider %s' % (self.user, self.identity)
        except models.ObjectDoesNotExist:
            return 'OpenID profile for None, via provider None'

    def authenticate(self):
        return authenticate(identity=self.identity)

class OpenIDStore(models.Model):
    site = models.ForeignKey(Site, default=Site.objects.get_current)
    server_url = models.CharField(max_length=255)
    handle = models.CharField(max_length=255)
    secret = models.TextField()
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.TextField()

    def __unicode__(self):
        return u'OpenID Store %s for %s' % (self.server_url, self.site)

class OpenIDNonce(models.Model):
    server_url = models.CharField(max_length=255)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'OpenID Nonce for %s' % self.server_url
