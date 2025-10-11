import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from difflib import get_close_matches
from apps.authorities.models import Authority  # adjust import if needed


class Command(BaseCommand):
    help = "Update Authority table with state phone numbers using fuzzy matching"

    def handle(self, *args, **options):
        file_path = os.path.join(settings.BASE_DIR, 'sauti_watch', 'police_stations_cellphones.xlsx')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        df = pd.read_excel(file_path)
        records = df.to_dict(orient='records')

        # get all authority names at once for faster matching
        all_authority_names = list(Authority.objects.values_list('name', flat=True))

        updated = 0
        not_found = []

        for record in records:
            state = str(record.get('State')).strip()
            phone = str(record.get('Cellphone Number')).strip() if record.get('Cellphone Number') else None

            if not state or not phone:
                continue

            # Find close matches (fuzzy search)
            matches = get_close_matches(state, all_authority_names, n=1, cutoff=0.6)

            if matches:
                match_name = matches[0]
                affected = Authority.objects.filter(name=match_name).update(state_phone_number=phone)
                updated += affected
            else:
                not_found.append(state)

        self.stdout.write(self.style.SUCCESS(f"✅ Updated {updated} police stations with phone numbers."))
        if not_found:
            self.stdout.write(self.style.WARNING(f"⚠️ No close match found for: {', '.join(set(not_found))}"))
