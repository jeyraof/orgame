# -*- coding: utf-8 -*-
def global_context(request):
    processor = {
        'request': request,
    }

    return processor