# Generated by Django 4.2.4 on 2023-08-15 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_casa_dispositivos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casa',
            name='areaCuadrada',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]