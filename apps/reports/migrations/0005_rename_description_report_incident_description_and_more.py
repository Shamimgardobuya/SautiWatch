
from django.db import migrations, models

def safe_rename_and_add_image(apps, schema_editor):
    connection = schema_editor.connection
    table_name = 'reports_report'

    try:
        existing_columns = [
            col.name
            for col in connection.introspection.get_table_description(
                connection.cursor(),
                table_name
            )
        ]

        # Rename only if 'description' exists
        if 'description' in existing_columns:
            schema_editor.execute(
                f'ALTER TABLE {table_name} RENAME COLUMN description TO incident_description'
            )
            print("✅ Renamed 'description' → 'incident_description'")
        else:
            print("ℹ️ Column 'description' not found, skipping rename")

        # Add 'image' field only if missing
        if 'image' not in existing_columns:
            schema_editor.execute(
                f"ALTER TABLE {table_name} ADD COLUMN image VARCHAR(100)"
            )
            print("✅ Added 'image' column")
        else:
            print("ℹ️ Column 'image' already exists, skipping add")

    except Exception as e:
        print(f"⚠️ Error during migration: {e}")

class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_alter_report_options_report_assaulter_description_and_more'),
    ]

    operations = [
        migrations.RunPython(safe_rename_and_add_image),
    ]
