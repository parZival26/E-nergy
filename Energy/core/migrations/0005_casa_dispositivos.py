# Generated by Django 4.2.4 on 2023-08-15 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_dispositivos_consumowperh_dispositivos_horasactivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='casa',
            name='dispositivos',
            field=models.ManyToManyField(related_name='dispositivos', to='core.dispositivos'),
        ),
    ]
