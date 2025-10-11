from django.db import migrations

def safe_remove_contact_email_field(apps, schema_editor):
    table_name = 'reports_region'
    column_name = 'contact_email'
    connection = schema_editor.connection

    # Drop column safely using PostgreSQL's IF EXISTS
    with connection.cursor() as cursor:
        cursor.execute(f'ALTER TABLE "{table_name}" DROP COLUMN IF EXISTS "{column_name}" CASCADE;')

class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_remove_region_contact_phone_report_is_anonymous_and_more'),
    ]

    operations = [
        migrations.RunPython(safe_remove_contact_email_field),
    ]
