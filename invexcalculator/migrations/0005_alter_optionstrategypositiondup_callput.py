# Generated by Django 4.1.7 on 2023-04-12 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invexcalculator', '0004_optionstrategydup_current_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='optionstrategypositiondup',
            name='callput',
            field=models.CharField(blank=True, choices=[('call', 'Call'), ('put', 'Put'), ('stock', 'Stock')], max_length=10),
        ),
    ]
