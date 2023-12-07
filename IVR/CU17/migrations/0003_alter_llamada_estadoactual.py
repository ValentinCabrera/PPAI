# Generated by Django 4.2.6 on 2023-12-06 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("CU17", "0002_alter_cambioestado_llamada_alter_llamada_duracion"),
    ]

    operations = [
        migrations.AlterField(
            model_name="llamada",
            name="estadoActual",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="llamada",
                related_query_name="estado",
                to="CU17.estado",
            ),
        ),
    ]