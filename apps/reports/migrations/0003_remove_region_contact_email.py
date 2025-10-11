from django.db import migrations

def remove_contact_email_field(apps, schema_editor):
    table_name = 'reports_region'
    column_name = 'contact_email'
    connection = schema_editor.connection

    try:
        # Get all existing columns for this table
        existing_columns = [
            col.name
            for col in connection.introspection.get_table_description(
                connection.cursor(),
                table_name
            )
        ]

        # Only drop the column if it exists
        if column_name in existing_columns:
            schema_editor.execute(f'ALTER TABLE {table_name} DROP COLUMN {column_name}')
            print(f" Removed column '{column_name}' from '{table_name}'")
        else:
            print(f"ℹColumn '{column_name}' not found in '{table_name}', skipping...")

    except Exception as e:
        print(f" Skipping removal of '{column_name}': {e}")

class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_remove_region_contact_phone_report_is_anonymous_and_more'),
    ]

    operations = [
        migrations.RunPython(remove_contact_email_field),
    ]
