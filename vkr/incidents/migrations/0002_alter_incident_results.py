# Generated by Django 5.0.4 on 2024-04-26 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='results',
            field=models.JSONField(null=True, verbose_name='Результаты'),
        ),
    ]