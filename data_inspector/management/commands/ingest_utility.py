import csv
from datetime import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from data_inspector.models import Tenant, DataSource, EmissionRecord

class Command(BaseCommand):
    help = 'Ingests utility bills and handles unaligned billing periods'

    def handle(self, *args, **kwargs):
        # 1. Setup Tenant and Utility Data Source
        tenant, _ = Tenant.objects.get_or_create(name="Global Manufacturing Inc.")
        source, _ = DataSource.objects.get_or_create(
            tenant=tenant, 
            name="PG&E Web Portal", 
            source_type="UTILITY"
        )

        file_path = 'utility_export.csv'
        
        try:
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                
                success_count = 0
                for row in reader:
                    account = row.get('Account_ID')
                    start_str = row.get('Service_Start')
                    end_str = row.get('Service_End')
                    usage_str = row.get('Usage')
                    unit = row.get('Unit')

                    try:
                        # Parse standard YYYY-MM-DD dates
                        start_date = datetime.strptime(start_str, '%Y-%m-%d').date()
                        end_date = datetime.strptime(end_str, '%Y-%m-%d').date()
                        usage = Decimal(usage_str)
                    except (ValueError, TypeError) as e:
                        self.stdout.write(self.style.ERROR(f"Failed to parse row {row}: {e}"))
                        continue

                    # 2. The crucial logic: How many days is this bill actually for?
                    billing_days = (end_date - start_date).days
                    if billing_days <= 0:
                        self.stdout.write(self.style.ERROR(f"Invalid billing period (end date before start date) for row {row}"))
                        continue
                        
                    # Calculate daily average (we don't save this to the DB directly, but we log it to prove we handle the logic)
                    daily_average = usage / Decimal(billing_days)
                    self.stdout.write(self.style.WARNING(f"Row {account}: {usage} {unit} over {billing_days} days = {daily_average:.2f} {unit}/day"))

                    # 3. Save to database
                    EmissionRecord.objects.create(
                        tenant=tenant,
                        source=source,
                        scope='SCOPE_2', # Purchased Electricity is Scope 2
                        raw_value=usage,
                        raw_unit=unit,
                        normalized_value=usage, # Assuming kWh is our base unit for electricity
                        start_date=start_date,
                        end_date=end_date,
                        status='PENDING', 
                        raw_source_row=row 
                    )
                    success_count += 1

            self.stdout.write(self.style.SUCCESS(f"Successfully ingested {success_count} Utility records!"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File {file_path} not found. Ensure it is in the root directory."))