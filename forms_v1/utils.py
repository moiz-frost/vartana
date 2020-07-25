import traceback

from django.http import Http404
from django.apps import apps
from django.shortcuts import _get_queryset

def get_model_or_404(app_label, model_name):
    try:
        return apps.get_model(app_label=app_label, model_name=model_name)
    except Exception as e:
        print('Not Found: {model}'.format(model=name))
        # print(traceback.format_stack())
        raise Http404('Not Found: {model}'.format(model=name))

def get_object_or_404(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        print('Not Found: {query}, {args}, {kwargs}'.format(query=queryset.query, args=args, kwargs=kwargs))
        # print(traceback.format_stack())
        raise Http404('Not Found: {model}'.format(model=queryset.model))