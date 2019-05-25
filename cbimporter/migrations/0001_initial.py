# Generated by Django 2.2.1 on 2019-05-25 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('total_value', models.DecimalField(decimal_places=2, max_digits=8)),
                ('high_date', models.DateTimeField()),
                ('high_value', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cb_id', models.CharField(max_length=36, unique=True)),
                ('currency', models.CharField(max_length=4)),
                ('quantity', models.DecimalField(decimal_places=16, max_digits=25)),
                ('available', models.DecimalField(decimal_places=16, max_digits=25)),
                ('hold', models.DecimalField(decimal_places=16, max_digits=25)),
                ('price', models.DecimalField(decimal_places=8, max_digits=16)),
                ('value', models.DecimalField(decimal_places=8, max_digits=16)),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbimporter.Portfolio')),
            ],
        ),
    ]
