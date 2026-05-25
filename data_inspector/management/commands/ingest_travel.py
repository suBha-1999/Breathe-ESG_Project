import csv
from datetime import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from data_inspector.models import Tenant, DataSource, EmissionRecord

class Command(BaseCommand):
    help = 'Ingests corporate travel data, calculating distance from IATA codes and applying cabin-specific emission factors'

    # Mock database for airport distances (in km) to prove the architectural concept
    MOCK_DISTANCE_DB = {
        ('SFO', 'JFK'): Decimal('4150.0'),
        ('LHR', 'CDG'): Decimal('344.0'),
    }

    # Mock emission factors (kg CO2e per km)
    # Business class takes up more physical space on the plane, so its footprint is higher
    EMISSION_FACTORS = {
        'Economy': Decimal('0.15'),
        'Business': Decimal('0.30'),
    }

    def get_distance(self, origin, dest):
        # Check both directions (A to B, or B to A)
        if (origin, dest) in self.MOCK_DISTANCE_DB:
            return self.MOCK_DISTANCE_DB[(origin, dest)]
        elif (dest, origin) in self.MOCK_DISTANCE_DB:
            return self.MOCK_DISTANCE_DB[(dest, origin)]
        return None

    def handle(self, *args, **kwargs):
        # 1. Setup Tenant and Travel Data Source
        tenant, _ = Tenant.objects.get_or_create(name="Global Manufacturing Inc.")
        source, _ = DataSource.objects.get_or_create(
            tenant=tenant, 
            name="Navan Expense API Export", 
            source_type="TRAVEL"
        )

        file_path = 'travel_export.csv'
        
        try:
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                
                success_count = 0
                for row in reader:
                    date_str = row.get('Travel_Date')
                    origin = row.get('Origin_IATA')
                    dest = row.get('Dest_IATA')
                    cabin = row.get('Cabin_Class')

                    try:
                        travel_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    except ValueError:
                        self.stdout.write(self.style.ERROR(f"Invalid date format in row: {row}"))
                        continue

                    # 2. Detective Work: Calculate Distance
                    distance = self.get_distance(origin, dest)
                    if not distance:
                        self.stdout.write(self.style.ERROR(f"Distance lookup failed for {origin} to {dest}. Flagging row."))
                        status = 'FLAGGED'
                        emissions = Decimal('0.0') # We can't calculate it yet
                    else:
                        # 3. Apply the correct emission factor based on cabin class
                        factor = self.EMISSION_FACTORS.get(cabin, Decimal('0.15')) # Default to economy if missing
                        emissions = distance * factor
                        status = 'PENDING'
                        self.stdout.write(self.style.WARNING(f"Row {origin}->{dest} ({cabin}): {distance} km * {factor} factor = {emissions:.2f} kg CO2e"))

                    # 4. Save to database
                    EmissionRecord.objects.create(
                        tenant=tenant,
                        source=source,
                        scope='SCOPE_3', # Business travel is Scope 3
                        raw_value=distance if distance else Decimal('0.0'),
                        raw_unit='km',
                        normalized_value=emissions,
                        start_date=travel_date,
                        end_date=travel_date, # Flight is a discrete event
                        status=status, 
                        raw_source_row=row 
                    )
                    success_count += 1

            self.stdout.write(self.style.SUCCESS(f"Successfully ingested {success_count} Travel records!"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File {file_path} not found."))