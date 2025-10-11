from django.db import migrations, models


def safe_rename_and_add_image(apps, schema_editor):
    Report = apps.get_model('reports', 'Report')
    table_name = Report._meta.db_table

    # Get existing columns for the table
    existing_columns = [f.name for f in Report._meta.get_fields() if f.concrete]

    # Rename 'description' → 'incident_description' if it exists
    if 'description' in existing_columns:
        old_field = Report._meta.get_field('description')
        new_field = models.TextField(
            name='incident_description',
            null=old_field.null,
            blank=old_field.blank,
        )
        schema_editor.alter_field(Report, old_field, new_field)
        print("✅ Renamed 'description' → 'incident_description'")
    else:
        print("ℹ️ Column 'description' not found, skipping rename")

    # Add 'image' field if missing
    if 'image' not in existing_columns:
        new_image_field = models.ImageField(
            name='image',
            upload_to='reports/',
            blank=True,
            null=True,
        )
        schema_editor.add_field(Report, new_image_field)
        print("✅ Added 'image' field")
    else:
        print("ℹ️ Column 'image' already exists, skipping add")


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_alter_report_options_report_assaulter_description_and_more'),
    ]

    operations = [
        migrations.RunPython(safe_rename_and_add_image),
    ]
