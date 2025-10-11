from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_remove_region_contact_phone_report_is_anonymous_and_more'),
    ]

    operations = [
        # Replaced RunPython with ORM-based RemoveField
        migrations.RemoveField(
            model_name='region',
            name='contact_email',
        ),
    ]