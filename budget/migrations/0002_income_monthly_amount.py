# Generated by Django 4.2.5 on 2023-11-08 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='income',
            name='monthly_amount',
            field=models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=10, null=True),
        ),
    ]
