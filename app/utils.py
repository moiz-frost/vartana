import traceback

from django.http import Http404
from django.apps import apps

def get_model_or_404(name):
    try:
        return apps.get_model(app_label='app', model_name=name)
    except Exception as e:
        print('Not Found: {model}'.format(model=name))
        # print(traceback.format_stack())
        raise Http404('Not Found: {model}'.format(model=name))