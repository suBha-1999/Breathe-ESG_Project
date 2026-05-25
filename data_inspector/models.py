from django.db import models
from django.contrib.auth.models import User

class Tenant(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class DataSource(models.Model):
    SOURCE_TYPES = [
        ('SAP', 'SAP ERP'),
        ('UTILITY', 'Utility Portal'),
        ('TRAVEL', 'Corporate Travel API'),
    ]
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    source_type = models.CharField(max_length=50, choices=SOURCE_TYPES)
    
    def __str__(self):
        return f"{self.name} ({self.source_type})"

class EmissionRecord(models.Model):
    SCOPE_CHOICES = [
        ('SCOPE_1', 'Scope 1 (Direct)'),
        ('SCOPE_2', 'Scope 2 (Indirect - Owned)'),
        ('SCOPE_3', 'Scope 3 (Indirect - Value Chain)'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pending Analyst Review'),
        ('APPROVED', 'Approved for Audit'),
        ('FLAGGED', 'Suspicious / Error'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    source = models.ForeignKey(DataSource, on_delete=models.SET_NULL, null=True)
    scope = models.CharField(max_length=20, choices=SCOPE_CHOICES)
    
    raw_value = models.DecimalField(max_digits=15, decimal_places=4)
    raw_unit = models.CharField(max_length=50) 
    normalized_value = models.DecimalField(max_digits=15, decimal_places=4)
    
    start_date = models.DateField()
    end_date = models.DateField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    raw_source_row = models.JSONField(help_text="Store the exact incoming JSON/CSV row")

    def __str__(self):
        return f"{self.tenant.name} | {self.scope} | {self.normalized_value} MT CO2e"