# Generated by Django 5.1.4 on 2024-12-23 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sklad', '0005_alter_produkt_options_produkt_uzivatel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='produkt',
            options={},
        ),
        migrations.RemoveField(
            model_name='produkt',
            name='uzivatel',
        ),
    ]
