# Generated by Django 4.1.3 on 2022-11-27 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_bedroom', models.IntegerField(null=True)),
                ('num_bathroom', models.IntegerField(null=True)),
                ('area', models.DecimalField(decimal_places=2, max_digits=19, null=True)),
                ('direction', models.TextField(null=True)),
                ('status', models.TextField(null=True)),
                ('license', models.TextField(null=True)),
                ('width', models.DecimalField(decimal_places=2, max_digits=19, null=True)),
                ('height', models.DecimalField(decimal_places=2, max_digits=19, null=True)),
                ('road_width', models.DecimalField(decimal_places=2, max_digits=19, null=True)),
                ('structure', models.TextField(null=True)),
                ('year', models.IntegerField(null=True)),
                ('front_width', models.DecimalField(decimal_places=2, max_digits=19, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Utility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('near_market', models.BooleanField(null=True)),
                ('near_school', models.BooleanField(null=True)),
                ('near_center', models.BooleanField(null=True)),
                ('good_design', models.BooleanField(null=True)),
                ('security', models.BooleanField(null=True)),
                ('near_front_road', models.BooleanField(null=True)),
                ('near_hospital', models.BooleanField(null=True)),
                ('near_park', models.BooleanField(null=True)),
                ('parking', models.BooleanField(null=True)),
                ('through_road', models.BooleanField(null=True)),
                ('fast_trade', models.BooleanField(null=True)),
                ('open_house', models.BooleanField(null=True)),
                ('two_small_roads', models.BooleanField(null=True)),
                ('two_roads', models.BooleanField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('code', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('address', models.TextField()),
                ('total_price', models.IntegerField()),
                ('unit_price', models.TextField(null=True)),
                ('property', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='search.property')),
                ('utility', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='search.utility')),
            ],
        ),
    ]
