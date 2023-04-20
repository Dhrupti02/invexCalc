# Generated by Django 4.1.7 on 2023-03-28 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OptionStrategyDup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.IntegerField(blank=True, default=None, null=True)),
                ('ticker', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('parent_id', models.IntegerField(blank=True, default=0, null=True)),
                ('is_active', models.CharField(blank=True, choices=[('non active', 'Non Active'), ('active', 'Active'), ('expired', 'Expired')], max_length=30)),
                ('current_stock_price', models.FloatField(blank=True)),
                ('risk_free_rate', models.FloatField(blank=True)),
                ('days_from_today', models.FloatField(blank=True)),
                ('days_from_today_date', models.DateField(blank=True, default=None, null=True)),
                ('start_date', models.CharField(blank=True, max_length=20, null=True)),
                ('default_interval', models.IntegerField(blank=True)),
                ('calculation', models.JSONField(blank=True, default=None, null=True)),
                ('cash', models.FloatField(blank=True, default=0)),
                ('extra_cash', models.FloatField(blank=True, default=0)),
                ('cash_in_hand', models.FloatField(blank=True, default=0)),
                ('calc_itc', models.FloatField(blank=True, default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'option_strategy_dup',
            },
        ),
        migrations.CreateModel(
            name='OptionStrategyPositionDup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_strategy_id', models.IntegerField(null=True)),
                ('row_id', models.CharField(blank=True, max_length=10, null=True)),
                ('buysell', models.CharField(blank=True, max_length=10)),
                ('contract', models.IntegerField(blank=True)),
                ('callput', models.CharField(blank=True, max_length=10)),
                ('strike', models.FloatField(blank=True)),
                ('expiry_date', models.DateField(blank=True, default=None, null=True)),
                ('volatility', models.FloatField(blank=True)),
                ('premium', models.FloatField(blank=True, default=None, null=True)),
                ('debit_credit', models.FloatField(blank=True, default=None, null=True)),
                ('initial_trade_cost', models.FloatField(blank=True, default=None, null=True)),
                ('cash_required', models.FloatField(blank=True, default=None, null=True)),
                ('initial_cash_req', models.FloatField(blank=True, default=None, null=True)),
                ('graphcal', models.JSONField(blank=True, default=None, null=True)),
            ],
            options={
                'db_table': 'option_strategy_position_dup',
            },
        ),
        migrations.CreateModel(
            name='OptionStrategySpreadDup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_strategy_id', models.IntegerField()),
                ('position_id_first', models.CharField(max_length=10)),
                ('position_id_second', models.CharField(max_length=10)),
                ('cash_required', models.FloatField(default=None, null=True)),
                ('initial_cash_required', models.FloatField(default=None, null=True)),
                ('spread_data', models.TextField(default=None, null=True)),
            ],
            options={
                'db_table': 'option_strategy_spread_dup',
            },
        ),
    ]
