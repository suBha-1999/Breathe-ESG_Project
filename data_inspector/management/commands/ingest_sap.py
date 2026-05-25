import csv
from datetime import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from data_inspector.models import Tenant, DataSource, EmissionRecord

class Command(BaseCommand):
    help = 'Ingests messy SAP CSV exports, handling German headers and European formats'

    def clean_european_number(self, value_str):
        """Converts '1.200,50' to '1200.50'"""
        # Remove periods used as thousand separators, then replace comma with a dot
        clean_str = value_str.replace('.', '').replace(',', '.')
        return Decimal(clean_str)

    def handle(self, *args, **kwargs):
        # 1. Setup a dummy Tenant and Data Source for this ingestion
        tenant, _ = Tenant.objects.get_or_create(name="Global Manufacturing Inc.")
        source, _ = DataSource.objects.get_or_create(
            tenant=tenant, 
            name="Legacy SAP ECC", 
            source_type="SAP"
        )

        file_path = 'sap_export.csv'
        
        try:
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file, delimiter=';')
                
                success_count = 0
                for row in reader:
                    # 2. Map German Headers to Python Variables
                    plant_code = row.get('WERKS')
                    material = row.get('MATNR')
                    quantity_str = row.get('MENGE')
                    unit = row.get('MEINS')
                    date_str = row.get('ERDAT')

                    # 3. Clean the messy data
                    try:
                        # Parse DD.MM.YYYY
                        parsed_date = datetime.strptime(date_str, '%d.%m.%Y').date()
                        # Clean European Decimals
                        clean_quantity = self.clean_european_number(quantity_str)
                    except ValueError as e:
                        self.stdout.write(self.style.ERROR(f"Failed to parse row {row}: {e}"))
                        continue

                    # 4. Save to our normalized single source of truth
                    EmissionRecord.objects.create(
                        tenant=tenant,
                        source=source,
                        scope='SCOPE_1', # Fuel falls under Scope 1
                        raw_value=clean_quantity,
                        raw_unit=unit,
                        # For the prototype, we'll store the raw value as normalized until we build a conversion table
                        normalized_value=clean_quantity, 
                        start_date=parsed_date,
                        end_date=parsed_date, # SAP fuel lines are discrete events, so start = end
                        status='PENDING', # Needs analyst review
                        raw_source_row=row # Audit trail
                    )
                    success_count += 1

            self.stdout.write(self.style.SUCCESS(f"Successfully ingested {success_count} SAP records!"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File {file_path} not found. Please ensure it is in the root directory."))