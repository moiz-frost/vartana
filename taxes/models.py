from django.db import models
from model_utils.models import TimeStampedModel


class Form(TimeStampedModel):

    alias = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        unique=True, # create db index as well
        help_text='[Optional] use this field to search this form for later'
    )

    description = models.CharField(
        max_length=1000, 
        blank=True, 
        null=True,
        help_text='[Optional] custom description'
    )

    class Meta:
        abstract = True

    def get_taxable_income_from_bracket(self, taxable_income, percentage):
        if taxable_income > 50000:
            taxable_income -= (taxable_income * (percentage / 100))
        elif taxable_income > 10000 and taxable_income < 50000:
            taxable_income -= 1000
        else:
            pass
        
        return taxable_income

class Form_1099(Form):

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
    total_taxable_income = models.IntegerField(help_text='Computed')

    class Meta:
        db_table = 'form_1099'

    def compute_total_taxable_income(self):
        revenue = self.total_income - self.total_business_expenses
        taxable_income = revenue - (2.1 * self.total_miles_driven)
        return self.get_taxable_income_from_bracket(taxable_income, 1)

    def save(self, *args, **kwargs):
        self.total_taxable_income = self.compute_total_taxable_income()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.pk

class Form_W2(Form):
    
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

    total_taxable_income = models.IntegerField(help_text='Computed')

    class Meta:
        db_table = 'form_W2'

    def save(self, *args, **kwargs):
        self.total_taxable_income = self.get_taxable_income_from_bracket(self.total_income, 2)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.pk

class Form_1040(Form):
    
    total_taxable_income = models.DecimalField(
        default=0.00, 
        max_digits=19, 
        decimal_places=2,
        help_text='Sum of taxable incomes across all Form 1099 ​and Form W-2'
    )
    
    total_taxes_paid = models.DecimalField(
        default=0.00, 
        max_digits=19, 
        decimal_places=2,
        help_text='Sum tax paid across all Form W-2'
    )

    total_tax_liability = models.DecimalField(
        default=0.00, 
        max_digits=19, 
        decimal_places=2,
        help_text='Computed'
    )

    tax_difference = models.DecimalField(
        default=0.00, 
        max_digits=19, 
        decimal_places=2,
        help_text='Total tax paid minus total tax liability'
    )

    class Meta:
        db_table = 'form_1040'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.pk
