from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpRequest
from httplib2 import Http
import oauth2 as oauth
from env import *
import requests
import urlparse
import datetime
import urllib
import tweepy
import bcrypt
import json
import os

# Create your views here.

class LegacyAuthentication():

    def legacy_login(self,request):
        if request.method == 'POST':     
            return HttpResponse('done')

    def signup(self, request):
        if request.method == 'POST':
            values = {}
            values['first_name'] = request.POST.get('firstName')
            values['last_name'] = request.POST.get('lastName')
            values['display_name'] = request.POST.get('displayName')
            values['email'] = request.POST.get('email')
            values['password'] = request.POST.get('password')
            values['is_banned'] = False
            values['is_active'] = True
            values['created_at'] = datetime.datetime.now()
            values['updated_at'] = datetime.datetime.now()
            print values


class GoogleSocialAuthentication():

    token_request_uri = 'https://accounts.google.com/o/oauth2/auth'
    access_token_uri = 'https://accounts.google.com/o/oauth2/token'
    redirect_uri = 'http://127.0.0.1:8000/auth/callback'
    scope =  'profile email https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/contacts'
    grant_type = 'authorization_code'
    response_type = 'code'

    def redirect(self):
        url = "{token_request_uri}?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}".format(token_request_uri=self.token_request_uri,response_type=self.response_type,client_id=GOOGLE_CLIENT_ID,redirect_uri=self.redirect_uri,scope=self.scope)
        return redirect(url)


    def authorize(self,request):
        parser = Http()
        params = urllib.urlencode({'code':request.GET['code'],'redirect_uri':self.redirect_uri,'client_id':GOOGLE_CLIENT_ID,'client_secret':GOOGLE_CLIENT_SECRET,'grant_type':self.grant_type})
        headers = {'Content-Type':'application/x-www-form-urlencoded'}
        resp, content = parser.request(self.access_token_uri,method='POST',body=params,headers=headers)
        return content



class FacebookSocialAuthentication():

    token_uri = 'https://www.facebook.com/dialog/oauth'
    token_request_uri = 'https://accounts.google.com/o/oauth2/auth'
    access_token_uri = 'https://graph.facebook.com/oauth/access_token'
    redirect_uri = 'http://127.0.0.1:8000/auth/facebook/callback'
    response_type = 'code'
    scope = 'email'

    def redirect(self):
        url = "{token_uri}?client_id={facebook_client_id}&app_id={facebook_app_id}&redirect_uri={redirect_uri}&response_type={response_type}&scope=email".format(token_uri=self.token_uri,facebook_client_id=FACEBOOK_APP_ID,facebook_app_id=FACEBOOK_APP_ID,redirect_uri=self.redirect_uri,response_type=self.response_type)
        return redirect(url)

    def authorize(self,request):
        consumer = oauth.Consumer(key=FACEBOOK_APP_ID, secret=FACEBOOK_APP_SECRET)
        client = oauth.Client(consumer)
        request_url = self.access_token_uri + '?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s' % (FACEBOOK_APP_ID, self.redirect_uri, FACEBOOK_APP_SECRET, request.GET['code'])
        resp, content = client.request(request_url, 'GET')
        access_token = json.loads(content)['access_token']
        request_url = 'https://graph.facebook.com/me?access_token=%s&fields=id,name,email,picture' % access_token
        resp, content = client.request(request_url, 'GET')
        return content

class TwitterSocialAuthentication():
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    authorize_url = 'https://api.twitter.com/oauth/authorize'
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    callback_url =  'http://127.0.0.1:8000/auth/twitter/callback'
    access_token = '769606826539167746-CIHk5DVCIurlTfnrsocxR9gSTfq3jHg'
    access_token_secret = 'xAOnWxJDS5xEGRp43gRd5bXjME2ZA11AgzHNurr4tbGXT'

    def redirect(self,request):
        auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth)
        print dir(api)
        print dir(api.auth)
        print api.auth.username
        # try:
        #     redirect_url = auth.get_authorization_url()
        #     print redirect_url
        # except tweepy.TweepError:
        #     print 'Error! Failed to get request token.'
        # request.session['request_token'] = auth.request_token
        # print request.session['request_token']
        # # verifier = request.GET.get('oauth_verifier')
        # verifier = raw_input('Verifier:')
        # print verifier
        # print "-------------------"
        # auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
        # token = request.session.get('request_token')
        # request.session.delete('request_token')
        # auth.request_token = token
        # try:
        #     auth.get_access_token(verifier)
        # except tweepy.TweepError:
        #     print 'Error! Failed to get access token.'
        
        # api = tweepy.API(auth)
        # print api      
            
        # request.session.set('request_token', auth.request_token)    
        # parser = Http()
        # params = urllib.urlencode({'oauth_callback':self.callback_url})
        # headers = {"oauth_consumer_key":TWITTER_API_KEY,"oauth_callback":self.callback_url}
        # content = parser.request(self.request_token_url, method='POST',body="",headers=headers)
        # print '++++++++++++++++++++++++'
        # print content
        # return content
        # print json.loads(content)
        return HttpResponse('kk')

    def authorize(self,request):
        pass             
    
