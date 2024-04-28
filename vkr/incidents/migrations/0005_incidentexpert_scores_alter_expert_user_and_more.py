# Generated by Django 5.0.4 on 2024-04-27 19:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0004_alter_critery_options_alter_incidentbasis_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='incidentexpert',
            name='scores',
            field=models.JSONField(blank=True, null=True, verbose_name='Оценки'),
        ),
        migrations.AlterField(
            model_name='expert',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='incident',
            name='creator_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authored_incidents', to='incidents.expert', verbose_name='Инициатор'),
        ),
        migrations.AlterField(
            model_name='incident',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='incidents.status', verbose_name='Статус'),
        ),
    ]