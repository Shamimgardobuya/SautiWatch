from django.db import migrations


def remove_contact_fields_safely(apps, schema_editor):
    table_name = 'reports_region'
    columns_to_drop = ['contact_phone', 'contact_email']
    connection = schema_editor.connection

    # Safely check and drop columns if they exist
    with connection.cursor() as cursor:
        existing_columns = [
            col.name for col in connection.introspection.get_table_description(cursor, table_name)
        ]
        for column in columns_to_drop:
            if column in existing_columns:
                cursor.execute(f'ALTER TABLE "{table_name}" DROP COLUMN "{column}" CASCADE;')


def delete_reportnote_model(apps, schema_editor):
    table_name = 'reports_reportnote'
    connection = schema_editor.connection

    # Safely drop the table if it exists
    with connection.cursor() as cursor:
        tables = connection.introspection.table_names()
        if table_name in tables:
            cursor.execute(f'DROP TABLE "{table_name}" CASCADE')


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(remove_contact_fields_safely),
        migrations.RunPython(delete_reportnote_model),
    ]
