
from django.http.response import JsonResponse
from django.db.models import Model
from django.forms.models import model_to_dict
from django.db.models import QuerySet

class RestJsonResponse(JsonResponse):
    def __init__(self, info=None, msg='', code='0', **kwargs):
        if isinstance(info, Model):
            dict = model_to_dict(info)
        elif isinstance(info, QuerySet):
            dict = []
            for item in info:
                dict.append(model_to_dict(item))
        else:
            dict = info
        super().__init__(data={
            'code':code,
            'msg': msg,
            'info': dict,
        },safe=False,**kwargs)