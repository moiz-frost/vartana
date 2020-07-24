from django.http import HttpResponseNotFound
from app.utils import get_model_or_404

# acts as a middleware to invalidate non existant form models
class CheckValidFormMixin(object):
    def dispatch(self, request, *args, **kwargs):
        model_type = self.kwargs.get('form_type')
        model = get_model_or_404(model_type)
        return super(CheckValidFormMixin, self).dispatch(request, model=model, *args, **kwargs)