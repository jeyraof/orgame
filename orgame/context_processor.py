# -*- coding: utf-8 -*-
def global_context(request):
    search_keyword = request.GET.get('q', '')

    processor = {
        'request': request,
        'user': request.user,
        'search_keyword': search_keyword,
    }

    return processor