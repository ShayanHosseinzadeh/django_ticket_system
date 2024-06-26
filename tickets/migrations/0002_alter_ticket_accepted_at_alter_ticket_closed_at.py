# Generated by Django 5.0.6 on 2024-05-24 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='accepted_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Accepted at'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='closed_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Closed at'),
        ),
    ]
