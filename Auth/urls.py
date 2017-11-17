from django.conf.urls import url
from . import controller


urlpatterns = [
        url(r'^login/google$', controller.google_redirect),
        url(r'^callback$', controller.google_authorize),
      	url(r'^login/facebook$', controller.facebook_redirect),
      	url(r'^facebook/callback', controller.facebook_authorize),
      	url(r'^login/twitter', controller.twitter_redirect),
      	url(r'^twitter/callback', controller.twitter_authorize),
      	url(r'^login/legacy', controller.legacy_login),
      	url(r'^signup', controller.signup),
      	url(r'^pagination', controller.pagination)

]
