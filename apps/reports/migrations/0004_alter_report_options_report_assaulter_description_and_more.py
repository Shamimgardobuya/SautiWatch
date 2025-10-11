from django.db import migrations, models


def add_missing_fields(apps, schema_editor):
    Report = apps.get_model('reports', 'Report')

    # Check existing fields dynamically
    existing_field_names = [f.name for f in Report._meta.get_fields() if f.concrete]

    # Add 'assaulter_description' if missing
    if 'assaulter_description' not in existing_field_names:
        new_field = models.TextField(
            name='assaulter_description',
            blank=True,
            null=True,
        )
        schema_editor.add_field(Report, new_field)
        print("✅ Added 'assaulter_description' field")
    else:
        print("ℹ️ 'assaulter_description' already exists, skipping...")

    # Add 'assaulter_name' if missing
    if 'assaulter_name' not in existing_field_names:
        new_field = models.CharField(
            name='assaulter_name',
            max_length=255,
            blank=True,
            null=True,
        )
        schema_editor.add_field(Report, new_field)
        print("✅ Added 'assaulter_name' field")
    else:
        print("ℹ️ 'assaulter_name' already exists, skipping...")


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
