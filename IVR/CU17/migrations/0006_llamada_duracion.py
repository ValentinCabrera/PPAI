# Generated by Django 4.1.2 on 2023-06-26 06:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("CU17", "0005_llamada_fechainicio"),
    ]

    operations = [
        migrations.AddField(
            model_name="llamada",
            name="duracion",
            field=models.DecimalField(
                blank=True, decimal_places=1, max_digits=1, null=True
            ),
        ),
    ]
