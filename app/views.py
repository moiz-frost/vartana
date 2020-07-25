from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from app.utils import get_model_or_404, get_object_or_404
from app.mixin import CheckValidFormMixin

class FormViewSet(
        CheckValidFormMixin, 
        mixins.RetrieveModelMixin, 
        mixins.ListModelMixin, 
        mixins.DestroyModelMixin, 
        viewsets.GenericViewSet):

    def get_queryset(self):
        model_name = self.kwargs['form_type']
        model = get_model_or_404(model_name)
        return model.objects.all()
    
    def get_serializer_class(self):
        model_name = self.kwargs['form_type']
        model = get_model_or_404(model_name)
        serializer_class = model.get_serializer()
        return serializer_class

    def list(self, request, form_type, model, model_serializer):
        queryset = model.objects.all()
        serializer = model_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, form_type, model, model_serializer):
        serializer = model_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, form_type, model, model_serializer, pk=None):
        form_object = get_object_or_404(model.objects.filter(pk=pk))
        serializer = model_serializer(form_object)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, form_type, model, model_serializer, pk=None):
        form_object = get_object_or_404(model.objects.filter(pk=pk))
        form_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)