
from django.db import migrations, models

def add_missing_fields(apps, schema_editor):
    table_name = 'reports_report'
    connection = schema_editor.connection

    try:
        # Fetch existing columns in the table
        existing_columns = [
            col.name
            for col in connection.introspection.get_table_description(
                connection.cursor(),
                table_name
            )
        ]

        # Define the fields you want to ensure exist
        new_fields = {
            "assaulter_description": "TEXT",
            "assaulter_name": "VARCHAR(255)",
        }

        for column_name, column_type in new_fields.items():
            if column_name not in existing_columns:
                schema_editor.execute(
                    f'ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}'
                )
                print(f"✅ Added column '{column_name}' to '{table_name}'")
            else:
                print(f"ℹ️ Column '{column_name}' already exists in '{table_name}', skipping...")

    except Exception as e:
        print(f"⚠️ Error while adding columns: {e}")

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
        migrations.RunPython(add_missing_fields),
    ]
