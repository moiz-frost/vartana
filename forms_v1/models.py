from django.db import models
from django.db.models import Sum
from model_utils.models import TimeStampedModel
from rest_framework import serializers

from decimal import Decimal

class FormMeta(TimeStampedModel):

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

    class Meta:
        db_table = 'form_meta'
        constraints = [
            models.UniqueConstraint(fields=['alias', 'id'], name='alias and pk')
        ]
        # abstract = True

    @classmethod
    def get_default_serializer(cls):
        class BaseSerializer(serializers.ModelSerializer):
            class Meta:
                model = cls
                fields = '__all__'

        return BaseSerializer

    def get_taxable_income_from_bracket(self, taxable_income, percentage):
        if taxable_income > 50000:
            taxable_income -= (taxable_income * (percentage / 100))
        elif taxable_income > 10000 and taxable_income < 50000:
            taxable_income -= 1000
        else:
            pass
        
        return taxable_income

class Form_1099(FormMeta):

    total_income = models.DecimalField(
        default=0.00, 
        max_digits=19, 
        decimal_places=2,
        help_text='Total income earned in $ amount rounded up to two decimal places'
    )
    total_business_expenses = models.DecimalField(
        default=0.00, 
        max_digits=19, 
        decimal_places=2,
        help_text='Total business expenses in $ amount rounded up to two decimal places'
    )
    total_miles_driven = models.IntegerField(help_text='Total miles driven rounded to the nearest integer')
    total_taxable_income = models.IntegerField(null=True, help_text='Computed')

    class Meta:
        db_table = 'form_1099'
    
    def compute_total_taxable_income(self):
        revenue = self.total_income - self.total_business_expenses
        taxable_income = revenue - Decimal(2.1 * self.total_miles_driven)
        taxable_income = int(round(taxable_income))
        return self.get_taxable_income_from_bracket(taxable_income, 1)

    def save(self, *args, **kwargs):
        self.total_taxable_income = self.compute_total_taxable_income()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.pk

class Form_W2(FormMeta):
    
    total_income = models.DecimalField(
        default=0.00, 
        max_digits=19, 
        decimal_places=2,
        help_text='Total income earned in $ amount rounded up to two decimal places'
    )
    
    total_taxes_paid = models.DecimalField(
        default=0.00, 
        max_digits=19, 
        decimal_places=2,
        help_text='Total taxes paid in $ amount accurate rounded up to two decimal places'
    )

    total_taxable_income = models.IntegerField(null=True, help_text='Computed')

    class Meta:
        db_table = 'form_W2'

    def save(self, *args, **kwargs):
        self.total_taxable_income = self.get_taxable_income_from_bracket(self.total_income, 2)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.pk

class Tax_Form_1040(FormMeta):
    
    total_taxable_income = models.DecimalField(
        default=0.00, 
        max_digits=19, 
        decimal_places=2,
        null=True,
        help_text='Sum of taxable incomes across all Form 1099 ​and Form W-2'
    )
    
    total_taxes_paid = models.DecimalField(
        default=0.00, 
        max_digits=19, 
        decimal_places=2,
        null=True,
        help_text='Sum tax paid across all Form W-2'
    )

    total_tax_liability = models.DecimalField(
        default=0.00, 
        max_digits=19, 
        decimal_places=2,
        null=True,
        help_text='Computed'
    )

    tax_difference = models.DecimalField(
        default=0.00, 
        max_digits=19, 
        decimal_places=2,
        null=True,
        help_text='Total tax paid minus total tax liability'
    )

    class Meta:
        db_table = 'tax_form_1040'

    def compute_total_taxable_income(self):
        return Form_1099.objects.aggregate(Sum('total_income'))['total_income__sum'] or 0.0

    def compute_total_taxes_paid(self):
        return Form_W2.objects.aggregate(Sum('total_taxes_paid'))['total_taxes_paid__sum'] or 0.0

    def compute_total_tax_liability(self):
        total_taxable_income = self.total_taxable_income
        if total_taxable_income < 100000 and total_taxable_income > 0:
            total_taxable_income = total_taxable_income * Decimal(0.2)
        else:
            total_taxable_income = total_taxable_income * Decimal(0.28)
            
        return total_taxable_income

    def compute_tax_difference(self):
        return Decimal(self.total_taxes_paid) - self.total_tax_liability

    def save(self, *args, **kwargs):
        self.total_taxable_income = self.compute_total_taxable_income()
        self.total_taxes_paid = self.compute_total_taxes_paid()
        self.total_tax_liability = self.compute_total_tax_liability()
        self.tax_difference = self.compute_tax_difference()

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.pk
