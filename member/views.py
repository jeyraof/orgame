from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from hashlib import md5
from member.models import Profile, SocialOAuth
from orgame.settings import FACEBOOK_CLIENT_ID, FACEBOOK_CLIENT_SECRET, SECRET_KEY
import urllib2
import json


def sign_in(request):
    if request.user.is_authenticated():
        return redirect('main')
    return render(request, 'member/sign_in.html')


def sign_out(request):
    logout(request=request)
    return redirect('main')


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
        return redirect('signin')

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
                              password=md5(social_user.user.username + SECRET_KEY).hexdigest())

    if login_user is not None:
        login(request=request, user=login_user)
        return redirect('main')

    else:
        return redirect('signin')


class SettingsView(View):
    def get(self, request):
        opt = {}
        if request.user.profile.is_newbie:
            opt['is_newbie'] = True
        return render(request, 'member/settings.html', opt)

    def post(self, request):
        opt = {}

        data = request.POST

        nickname = data.get('nickname', None)
        if not request.user.profile.nickname == nickname:
            nickname_valid, nickname_msg = request.user.profile.validate_nickname(nickname=nickname)
            if nickname_valid:
                request.user.profile.nickname = nickname
            opt['nickname_msg'] = nickname_msg

        email = data.get('email', None)
        if not request.user.profile.email == email:
            email_valid, email_msg = request.user.profile.validate_email(email=email)
            if email_valid:
                request.user.profile.email = email
            opt['email_msg'] = email_msg

        request.user.profile.save()

        return render(request, 'member/settings.html', opt)


class UserView(View):
    def get(self, request, nickname=None):
        if not nickname:
            if request.user.profile.is_newbie:
                return redirect('settings')

            opt = {
                'is_mine': True,
                'owner': request.user,
            }

        else:
            profile = get_object_or_404(Profile, nickname=nickname)
            is_mine = False
            if request.user.is_authenticated():
                is_mine = profile.id == request.user.profile.id

            opt = {
                'is_mine': is_mine,
                'owner': profile.user,
            }

        return render(request, 'member/collection.html', opt)
