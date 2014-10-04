from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from orgame.settings import FACEBOOK_CLIENT_ID, FACEBOOK_CLIENT_SECRET
from .models import SocialOAuth
import urllib2
import json


def sign_in(request):
    RequestContext(request=request)
    if request.user.is_authenticated is True:
        return redirect('orgame.views.main')
    return render(request, 'sign_in.html')


def sign_out(request):
    if 'member_id' in request.session:
        del request.session['member_id']

    return redirect('orgame.views.main')


def oauth_facebook(request):
    url = 'https://www.facebook.com/dialog/oauth?client_id={app_id}&redirect_uri={redirect_uri}'
    url = url.format(app_id=FACEBOOK_CLIENT_ID,
                     redirect_uri=request.build_absolute_uri(reverse('member.views.oauth_facebook_auth')))
    return redirect(url)


def oauth_facebook_auth(request):
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

    def get_user_id(token):
        u = 'https://graph.facebook.com/me?access_token={access_token}'.format(access_token=token)
        f = urllib2.urlopen(u)
        resp = f.read()
        data = json.loads(resp)
        return data.get('id', None)

    user_id = get_user_id(access_token)
    social_user = list(SocialOAuth.objects.filter(provider=SocialOAuth.FACEBOOK, uid=user_id))
    if social_user:
        social_user = social_user[0]
    else:
        social_user = SocialOAuth.join(provider=SocialOAuth.FACEBOOK, uid=user_id)

    social_user.user.sign_in(request=request)
    if not request.session.get('member_id', None) == social_user.user.id:
        return redirect('member.views.sign_in')

    return redirect('orgame.views.main')