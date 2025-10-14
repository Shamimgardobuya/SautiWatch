from django.db import migrations

def safe_add_assaulter_fields(apps, schema_editor):
    table_name = 'reports_report'
    connection = schema_editor.connection

    with connection.cursor() as cursor:
        cursor.execute(f'''
            ALTER TABLE "{table_name}"
            ADD COLUMN IF NOT EXISTS "assaulter_name" VARCHAR(255);
        ''')
        cursor.execute(f'''
            ALTER TABLE "{table_name}"
            ADD COLUMN IF NOT EXISTS "assaulter_description" TEXT;
        ''')

class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_remove_region_contact_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={
                'ordering': ['-created_at'],
                'permissions': [('can_view_reports', 'Can view confidential reports')],
            },
        ),
        migrations.RunPython(safe_add_assaulter_fields),
    ]
