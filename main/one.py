from django.http.response import JsonResponse
from django.db.models import Model
from django.forms.models import model_to_dict
from django.db.models import QuerySet


class RestJsonResponse(JsonResponse):
    def __init__(self, info=None, msg='', code='0', **kwargs):
        if isinstance(info, Model):
            info_dict = model_to_dict(info)
        elif isinstance(info, QuerySet):
            info_dict = []
            for item in info:
                info_dict.append(model_to_dict(item))
        else:
            info_dict = info
        super().__init__(data={
            'code': code,
            'msg': msg,
            'info': info_dict,
        }, safe=False, **kwargs)
