from rest_framework import serializers
from .models import EmissionRecord, DataSource, Tenant

class EmissionRecordSerializer(serializers.ModelSerializer):
    # We want to see the readable names of the source and tenant, not just their ID numbers
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)
    source_name = serializers.CharField(source='source.name', read_only=True)
    source_type = serializers.CharField(source='source.source_type', read_only=True)

    class Meta:
        model = EmissionRecord
        fields = [
            'id', 'tenant_name', 'source_name', 'source_type', 'scope', 
            'raw_value', 'raw_unit', 'normalized_value', 
            'start_date', 'end_date', 'status', 'created_at', 'raw_source_row'
        ]