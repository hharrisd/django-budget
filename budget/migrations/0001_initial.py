# Generated by Django 4.2.5 on 2023-11-07 16:20

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('frequency', models.CharField(choices=[('Monthly', 'Monthly'), ('Bimonthly', 'Bimonthly'), ('Quarterly', 'Quarterly'), ('Biannually', 'Biannually'), ('Annually', 'Annually')], default='Monthly', max_length=20)),
                ('concept', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('frequency', models.CharField(choices=[('Monthly', 'Monthly'), ('Bimonthly', 'Bimonthly'), ('Quarterly', 'Quarterly'), ('Biannually', 'Biannually'), ('Annually', 'Annually')], default='Monthly', max_length=20)),
                ('concept', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_essential', models.BooleanField()),
                ('transaction_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='budget.itemcategory')),
            ],
        ),
    ]
