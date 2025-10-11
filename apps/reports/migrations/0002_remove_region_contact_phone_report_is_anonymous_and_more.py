from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        # Replaced RunPython with ORM-based RemoveField
        migrations.RemoveField(
            model_name='region',
            name='contact_phone',
        ),
        
        # Existing AddField operations remain valid
        migrations.AddField(
            model_name='report',
            name='is_anonymous',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='report',
            name='tracking_id',
            field=models.CharField(
                db_index=True,
                editable=False,
                max_length=20,
                null=True,
                unique=True,
            ),
        ),
        # migrations.DeleteModel(...)
    ]