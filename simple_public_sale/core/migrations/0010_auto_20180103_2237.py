# Generated by Django 2.0 on 2018-01-03 22:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20180103_2236'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prenda',
            old_name='caracteristicasPrenda',
            new_name='caracteristicas',
        ),
    ]
