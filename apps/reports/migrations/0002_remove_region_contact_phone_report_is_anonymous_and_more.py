from django.db import migrations, models, connection


def remove_contact_phone_if_exists(apps, schema_editor):
    table_name = 'reports_region'
    column_name = 'contact_phone'

    with connection.cursor() as cursor:
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [col[1] for col in cursor.fetchall()]
        if column_name in columns:
            cursor.execute(f'ALTER TABLE {table_name} DROP COLUMN {column_name};')
            print(f"Dropped column '{column_name}' from '{table_name}'.")
        else:
            print(f"Skipped removing '{column_name}' — column does not exist in '{table_name}'.")


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(remove_contact_phone_if_exists),
        migrations.AddField(
            model_name='report',
            name='is_anonymous',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='report',
            name='tracking_id',
            field=models.CharField(
                db_index=True,
                editable=False,
                max_length=20,
                null=True,
                unique=True,
            ),
        ),
        # migrations.DeleteModel(
        #     name='ReportNote',
        # ),
    ]
