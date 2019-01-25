from django.core.paginator import Paginator, Page
from django.http.response import JsonResponse
from django.db.models import Model
from django.forms.models import model_to_dict
from django.db.models import QuerySet


def _model_to_dict(model):
    if hasattr(model, 'to_dict'):
        return model.to_dict()
    else:
        return model_to_dict(model)


class RestJsonResponse(JsonResponse):
    def __init__(self, info=None, msg='', code='0', **kwargs):
        if isinstance(info, Model):
            info_dict = _model_to_dict(info)
        elif isinstance(info, QuerySet):
            info_dict = []
            for item in info:
                info_dict.append(_model_to_dict(item))
        elif isinstance(info, Page):
            info_dict = {
                'count': info.paginator.count,
                'content': list(map(lambda e: _model_to_dict(e) if isinstance(e, Model) else e, list(info))),
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
