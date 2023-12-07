# Generated by Django 4.2.6 on 2023-12-07 19:32

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("CU17", "0005_remove_opcionllamada_seleccionada_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="AAuditar",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("CU17.estado",),
        ),
        migrations.CreateModel(
            name="ConObservacion",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("CU17.estado",),
        ),
        migrations.CreateModel(
            name="Correcta",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("CU17.estado",),
        ),
        migrations.CreateModel(
            name="Descartada",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("CU17.estado",),
        ),
    ]