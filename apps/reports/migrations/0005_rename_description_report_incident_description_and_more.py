from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_alter_report_options_report_assaulter_description_and_more'),
    ]

    operations = [
        # Replaced custom RENAME COLUMN SQL with ORM-based RenameField
        migrations.RenameField(
            model_name='report',
            old_name='description',
            new_name='incident_description',
        ),
        
        # Replaced custom ADD COLUMN SQL with ORM-based AddField
        migrations.AddField(
            model_name='report',
            name='image',
            field=models.CharField(max_length=100, null=True, blank=True), # Using CharField to match VARCHAR(100)
        ),
    ]