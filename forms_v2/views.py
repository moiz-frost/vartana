from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from forms_v2.models import FormDefinition, FormInstance
from forms_v2.serializers import FormDefinitionViewSerializer, FormInstanceViewSerializer
from forms_v1.utils import get_object_or_404


class FormDefinitionViewSet(
        mixins.RetrieveModelMixin, 
        mixins.ListModelMixin, 
        mixins.DestroyModelMixin, 
        viewsets.GenericViewSet):

    queryset = FormDefinition.objects.all()

    def list(self, request):
        queryset = FormDefinition.objects.all()
        serializer = FormDefinitionViewSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = FormDefinitionViewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(FormDefinition.objects.filter(pk=pk))
        serializer = FormDefinitionViewSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        queryset = get_object_or_404(FormDefinition.objects.filter(pk=pk))
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FormInstanceViewSet(
        mixins.RetrieveModelMixin, 
        mixins.ListModelMixin, 
        mixins.DestroyModelMixin, 
        viewsets.GenericViewSet):

    queryset = FormInstance.objects.all()

    def list(self, request):
        queryset = FormInstance.objects.all()
        serializer = FormInstanceViewSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = FormInstanceViewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(FormInstance.objects.filter(pk=pk))
        serializer = FormInstanceViewSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        queryset = get_object_or_404(FormInstance.objects.filter(pk=pk))
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)