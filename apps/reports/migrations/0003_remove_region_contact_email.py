from django.db import migrations, models


def remove_contact_email_field(apps, schema_editor):
    # Get the Region model from the historical apps registry
    Region = apps.get_model('reports', 'Region')

    # Check if the field exists
    existing_field_names = [f.name for f in Region._meta.get_fields() if f.concrete]

    if 'contact_email' in existing_field_names:
        field = Region._meta.get_field('contact_email')
        schema_editor.remove_field(Region, field)
        print("✅ Removed 'contact_email' field from Region")
    else:
        print("ℹ️ 'contact_email' field not found in Region, skipping...")


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_remove_region_contact_phone_report_is_anonymous_and_more'),
    ]

    operations = [
        migrations.RunPython(remove_contact_email_field),
    ]
