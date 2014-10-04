# -*- coding: utf-8 -*-
from member.models import User


def global_context(request):
    processor = {
        'request': request,
    }

    member_id = request.session.get('member_id', None)
    processor['user'] = User.get_by(member_id=member_id)

    return processor