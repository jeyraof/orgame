# -*- coding: utf-8 -*-
from member.models import User


def global_context(request):
    member_id = request.session.get('member_id', None)
    user = User.get_by(member_id=member_id)
    if user:
        request.user = user

    processor = {
        'user': user,
        'request': request,
    }

    return processor