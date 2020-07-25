from rest_framework import serializers
from forms_v2.models import FormDefinition, FormFieldDefinition, FormInstance, FormFieldValue
from forms_v1.utils import get_object_or_404


class FormFieldDefinitionViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormFieldDefinition
        fields = ['id', 'name', 'reference_name', 'display_order', 'data_type', 'description']


class FormDefinitionViewSerializer(serializers.ModelSerializer):
    form_fields_definitions = FormFieldDefinitionViewSerializer(many=True)
    
    class Meta:
        model = FormDefinition
        fields = ['id', 'name', 'alias', 'description', 'form_fields_definitions']

    def create(self, validated_data):
        form_fields_definitions = validated_data.pop('form_fields_definitions')
        form_definition = FormDefinition.objects.create(**validated_data)

        form_field_model_objects = []
        for form_field in form_fields_definitions:
            form_field_model_objects.append(FormFieldDefinition(form_definition=form_definition, **form_field))

        FormFieldDefinition.objects.bulk_create(form_field_model_objects)
        return form_definition


class FormFieldValueViewSerializer(serializers.ModelSerializer):
    # form_field_definition = FormFieldDefinitionViewSerializer(many=True)
    form_field_definition = serializers.PrimaryKeyRelatedField(queryset=FormFieldDefinition.objects.all())

    class Meta:
        model = FormFieldValue
        fields = ['id', 'value', 'reference_name', 'form_field_definition']

class FormInstanceViewSerializer(serializers.ModelSerializer):
    form_instance_fields = FormFieldValueViewSerializer(many=True)

    class Meta:
        model = FormInstance
        fields = ['id', 'description', 'form_definition', 'form_instance_fields']

    def validate(self, data):
        qs = FormFieldDefinition.objects.filter(form_definition=data['form_definition'].id)
        if len(data['form_instance_fields']) != qs.count():
            raise serializers.ValidationError("form_instance_fields length mismatch")
        return data

    def create(self, validated_data):
        form_instance_fields = validated_data.pop('form_instance_fields')
        form_instance = FormInstance.objects.create(**validated_data)

        form_instance_fields_model_objects = []
        for form_field in form_instance_fields:
            print("form_field", form_field)
            form_instance_fields_model_objects.append(FormFieldValue(form_instance=form_instance, **form_field))

        FormFieldValue.objects.bulk_create(form_instance_fields_model_objects)
        return form_instance