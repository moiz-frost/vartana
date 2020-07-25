from django.db import models
from model_utils.models import TimeStampedModel
from rest_framework import serializers

class FormDefinition(TimeStampedModel):
    
    name = models.CharField(
        max_length=100, 
        help_text='[Unique] Form Name'
    )

    alias = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text='[Optional] use this field to search this form for later'
    )

    description = models.CharField(
        max_length=1000, 
        blank=True, 
        null=True,
        help_text='[Optional] custom description'
    )

    # form_fields = models.ManyToManyField('FormFieldDefinition', through='FormDefinitionFields')

    class Meta:
        db_table = 'form_definition'
        constraints = [
            models.UniqueConstraint(fields=['name'], name='name constraint')
        ]
"""
class FormFieldDataType(TimeStampedModel):
    
    FIELD_DATA_TYPES = (
        ('integer', 'integer'),
        ('string', 'string'),
        ('decimal', 'decimal'),
        ('enum', 'enum'),
        ('computed', 'computed')
    )

    type = models.CharField(max_length=20, choices=FIELD_DATA_TYPES)
    
    description = models.CharField(
        max_length=1000, 
        blank=True, 
        null=True,
        help_text='[Optional] custom description'
    )

    class Meta:
        db_table = 'form_field_data_type'
"""

class FormFieldDefinition(TimeStampedModel):

    FIELD_DATA_TYPES = (
        ('integer', 'integer'),
        ('string', 'string'),
        ('decimal', 'decimal'),
        ('enum', 'enum'),
        ('computed', 'computed')
    )
    
    name = models.CharField(
        max_length=100, 
        help_text='Field Name'
    )

    reference_name = models.CharField(
        max_length=100,
        blank=True, 
        null=True, 
        help_text='Field Name'
    )

    display_order = models.IntegerField(help_text='Display order number')

    # form = models.ForeignKey(FormDefinition, on_delete=models.CASCADE)
    # data_type = models.ForeignKey(FormFieldDataType, on_delete=models.SET_NULL, null=True)
    data_type = models.CharField(max_length=20, choices=FIELD_DATA_TYPES)
    form_definition = models.ForeignKey(FormDefinition, related_name='form_fields_definitions', on_delete=models.CASCADE)

    description = models.CharField(
        max_length=1000, 
        blank=True, 
        null=True,
        help_text='[Optional] custom description'
    )

    class Meta:
        db_table = 'form_field_definition'
        constraints = [
            models.UniqueConstraint(fields=['reference_name', 'id'], name='reference_name and pk'),
            models.UniqueConstraint(fields=['display_order', 'form_definition'], name='display_order and form_definition')
        ]
"""
class FormDefinitionFields(TimeStampedModel):
    form_definition = models.ForeignKey(FormDefinition, on_delete=models.CASCADE)
    form_field_definition = models.ForeignKey(FormFieldDefinition, on_delete=models.CASCADE)

    class Meta:
        db_table = "form_definition_fields"
"""

class FormInstance(TimeStampedModel):

    form_definition = models.ForeignKey(FormDefinition, on_delete=models.CASCADE)

    description = models.CharField(
        max_length=1000, 
        blank=True, 
        null=True,
        help_text='[Optional] custom description'
    )

    # form_field_values = models.ManyToManyField('FormFieldValue', through='FormInstaceFieldValue')

    class Meta:
        db_table = 'form_instance'

# class FormInstaceFieldValue(TimeStampedModel):
#     form_instance = models.ForeignKey(FormInstance, on_delete=models.CASCADE)
#     form_field_value = models.ForeignKey('FormFieldValue', on_delete=models.CASCADE)

#     class Meta:
#         db_table = "form_instance_field_value"

class FormFieldValue(TimeStampedModel):

    value = models.CharField(
        blank=True, 
        null=True,
        max_length=500, 
        help_text='FieldValue'
    )

    reference_name = models.CharField(
        max_length=100,
        blank=True, 
        null=True, 
        help_text='Field Name'
    )

    form_field_definition = models.ForeignKey(FormFieldDefinition, on_delete=models.CASCADE)

    form_instance = models.ForeignKey(FormInstance, related_name='form_instance_fields', on_delete=models.CASCADE)

    description = models.CharField(
        max_length=1000, 
        blank=True, 
        null=True,
        help_text='[Optional] custom description'
    )

    class Meta:
        db_table = 'form_field_value'