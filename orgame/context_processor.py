# -*- coding: utf-8 -*-
def global_context(request):
    processor = {
        'request': request,
        'user': request.user,
    }

    return processor