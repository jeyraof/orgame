# -*- coding: utf-8 -*-
from member.models import Profile
from series.models import Series
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View


def main(request):
    return render(request, 'index.html')


def handler404(request):
    return render(request, '404.html')


class SearchView(View):
    def get(self, request):
        opt = {
            'is_search_page': True,
            'search_type': request.GET.get('type', 'Series')
        }

        search_keyword = request.GET.get('q', None)
        if search_keyword:
            profile = Profile.objects.filter(Q(nickname__contains=search_keyword)).exclude(email='')
            opt['profile'] = profile
            opt['profile_count'] = profile.count()

            series = Series.objects.filter(Q(name__contains=search_keyword))
            opt['series'] = series
            opt['series_count'] = series.count()

        return render(request, 'search.html', opt)