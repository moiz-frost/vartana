from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from app.mixin import CheckValidFormMixin

class FormViewSet(CheckValidFormMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

    def list(self, request, form_type=None, model=None):
        return Response(status=status.HTTP_200_OK)

    def create(self, request, form_type=None, model=None):
        return Response(status=status.HTTP_200_OK)

    def retrieve(self, request, form_type=None, model=None, pk=None):
        return Response(status=status.HTTP_200_OK)
        # bundle = get_object_or_404(Bundle.objects.filter(pk=pk).filter(app__creator_id = request.user.id))
        # serializer = AdminBundleSerializer(bundle)
        # return Response(serializer.data, status=status.HTTP_200_OK)