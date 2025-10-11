from django.db import migrations, models


def remove_contact_phone_field(apps, schema_editor):
    table_name = 'reports_region'
    column_name = 'contact_phone'
    connection = schema_editor.connection

    # Check if column exists before trying to drop it
    with connection.cursor() as cursor:
        existing_columns = [
            col.name for col in connection.introspection.get_table_description(cursor, table_name)
        ]
        if column_name in existing_columns:
            cursor.execute(f'ALTER TABLE "{table_name}" DROP COLUMN "{column_name}"')


def delete_reportnote_model(apps, schema_editor):
    table_name = 'reports_reportnote'
    connection = schema_editor.connection

    # Check if table exists before dropping it
    with connection.cursor() as cursor:
        tables = connection.introspection.table_names()
        if table_name in tables:
            cursor.execute(f'DROP TABLE "{table_name}" CASCADE')


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(remove_contact_phone_field),
        migrations.AddField(
            model_name='report',
            name='is_anonymous',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='report',
            name='tracking_id',
            field=models.CharField(
                db_index=True, editable=False, max_length=20, null=True, unique=True
            ),
        ),
        migrations.AlterField(
            model_name='region',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.RunPython(delete_reportnote_model),
    ]
