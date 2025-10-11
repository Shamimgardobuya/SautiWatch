import os
import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand
from apps.authorities.models import Authority  # adjust if your model path differs


class Command(BaseCommand):
    help = "Import police station or authority data from an Excel file."

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Path to the Excel file (defaults to apps/authority.xlsx)',
        )

    def handle(self, *args, **options):
        file_path = options['file'] or os.path.join(settings.BASE_DIR, 'sauti_watch','authority.xlsx')

        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        self.stdout.write(self.style.NOTICE(f"Loading data from: {file_path}"))

        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error reading Excel: {e}"))
            return

        required_columns = ['properties/name', 'geometry/coordinates/0', 'geometry/coordinates/1']
        if not all(col in df.columns for col in required_columns):
            self.stderr.write(self.style.ERROR(f"Missing one of the required columns: {required_columns}"))
            return

        model_instances = [
            Authority(
                name=row['properties/name'],
                latitude=row['geometry/coordinates/1'], 
                longitude=row['geometry/coordinates/0'], 
            )
            for _, row in df.iterrows()
        ]

        created = Authority.objects.bulk_create(model_instances, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f"✅ Successfully imported {len(model_instances)} authority records."))
