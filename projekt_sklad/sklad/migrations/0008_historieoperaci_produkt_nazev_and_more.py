# Generated by Django 5.1.4 on 2025-01-06 20:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sklad', '0007_produkt_uzivatel'),
    ]

    operations = [
        migrations.AddField(
            model_name='historieoperaci',
            name='produkt_nazev',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='historieoperaci',
            name='produkt',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sklad.produkt'),
        ),
    ]
