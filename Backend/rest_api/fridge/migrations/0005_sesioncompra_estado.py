# Generated by Django 5.0 on 2024-10-28 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fridge', '0004_sesioncompra_productocompra'),
    ]

    operations = [
        migrations.AddField(
            model_name='sesioncompra',
            name='estado',
            field=models.BooleanField(default=True),
        ),
    ]
