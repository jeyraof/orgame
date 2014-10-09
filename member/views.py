from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from orgame.settings import FACEBOOK_CLIENT_ID, FACEBOOK_CLIENT_SECRET, SECRET_KEY
from .models import SocialOAuth
import urllib2
import json


def sign_in(request):
    if request.user.is_authenticated():
        return redirect('orgame.views.main')
    return render(request, 'member/sign_in.html')


def sign_out(request):
    logout(request=request)
    return redirect('orgame.views.main')


def oauth_facebook(request):
    """
    Dynamic redirect to facebook OAuth link
    """
    url = 'https://www.facebook.com/dialog/oauth?client_id={app_id}&redirect_uri={redirect_uri}'
    url = url.format(app_id=FACEBOOK_CLIENT_ID,
                     redirect_uri=request.build_absolute_uri(reverse('member.views.oauth_facebook_auth')))
    return redirect(url)


def oauth_facebook_auth(request):
    """
    Facebook OAuth Processor
    """
    code = request.GET.get('code', '')

    def get_access_token(c):
        u = 'https://graph.facebook.com/oauth/access_token?'
        u += 'client_id={app_id}&redirect_uri={redirect_uri}&client_secret={app_secret}&code={code_parameter}'
        u = u.format(app_id=FACEBOOK_CLIENT_ID,
                     redirect_uri=request.build_absolute_uri(reverse('member.views.oauth_facebook_auth')),
                     app_secret=FACEBOOK_CLIENT_SECRET,
                     code_parameter=c)
        f = urllib2.urlopen(u)
        resp = f.read()
        if not 'access_token' in resp:
            return None, None

        data = resp.split('&')
        token_tuple = data[0]
        expires_tuple = data[1]

        return token_tuple.split('=')[1], expires_tuple.split('=')[1]

    access_token, expired_at = get_access_token(code)

    if not access_token:
        return redirect('member.views.sign_in')

    def get_user_profile(token):
        u = 'https://graph.facebook.com/me?access_token={access_token}'.format(access_token=token)
        f = urllib2.urlopen(u)
        resp = f.read()
        return json.loads(resp)

    user_profile = get_user_profile(access_token)
    social_user = list(SocialOAuth.objects.filter(provider=SocialOAuth.FACEBOOK, uid=user_profile.get('id', 0)))
    if social_user:
        social_user = social_user[0]
    else:
        social_user = SocialOAuth.join(provider=SocialOAuth.FACEBOOK,
                                       uid=user_profile.get('id', 0),
                                       profile=user_profile)

    login_user = authenticate(username=social_user.user.username,
                              password=make_password(social_user.user.username, salt=SECRET_KEY))

    if login_user is not None:
        login(request=request, user=login_user)
        return redirect('orgame.views.main')

    else:
        return redirect('member.views.sign_in')
