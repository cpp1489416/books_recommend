from django.core.paginator import Paginator, Page
from django.http.response import JsonResponse
from django.db.models import Model
from django.forms.models import model_to_dict
from django.db.models import QuerySet


class RestJsonResponse(JsonResponse):
    def __init__(self, info=None, msg='', code='0', **kwargs):
        if isinstance(info, Model):
            info_dict = info.to_dict()
        elif isinstance(info, QuerySet):
            info_dict = []
            for item in info:
                info_dict.append(info.to_dict())
        elif isinstance(info, Page):
            info_dict = {
                'count': info.paginator.count,
                'content': list(map(lambda e: e.to_dict() if isinstance(e, Model) else e, list(info))),
            }
        else:
            info_dict = info
        super().__init__(data={
            'code': code,
            'msg': msg,
            'info': info_dict,
        }, safe=False, **kwargs)


def get_page_info(page):
    pass
