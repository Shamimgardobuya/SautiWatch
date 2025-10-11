from django.db import migrations, models


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
        
        # Replaced RunPython with ORM-based AddField operations
        migrations.AddField(
            model_name='report',
            name='assaulter_description',
            field=models.TextField(null=True, blank=True), # Adjusted to use Django models.TextField
        ),
        migrations.AddField(
            model_name='report',
            name='assaulter_name',
            field=models.CharField(max_length=255, null=True, blank=True), # Adjusted to use Django models.CharField
        ),
    ]