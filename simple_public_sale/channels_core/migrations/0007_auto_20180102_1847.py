# Generated by Django 2.0 on 2018-01-02 18:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('channels_core', '0006_auto_20180102_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupoevento',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]