from django.http import HttpResponseNotFound, Http404
from forms_v1.utils import get_model_or_404

# acts as a middleware to invalidate non existant form models
class CheckValidFormMixin(object):
    def dispatch(self, request, *args, **kwargs):
        model_type = self.kwargs.get('form_type')
        if model_type.startswith('form_'):
            model = get_model_or_404('forms_v1', model_type)
            model_serializer = model.get_default_serializer()
            return (super(CheckValidFormMixin, self)
                            .dispatch(
                                request, 
                                model=model, 
                                model_serializer=model_serializer, 
                                *args, 
                                **kwargs))
        raise Http404()