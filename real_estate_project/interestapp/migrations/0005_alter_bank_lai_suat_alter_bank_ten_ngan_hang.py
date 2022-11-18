# Generated by Django 4.1.3 on 2022-11-16 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("interestapp", "0004_alter_bank_ten_ngan_hang"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bank",
            name="lai_suat",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=15,
                verbose_name="Lãi suất mua nhà % (năm) ",
            ),
        ),
        migrations.AlterField(
            model_name="bank",
            name="ten_ngan_hang",
            field=models.CharField(max_length=120, verbose_name="Tên ngân hàng"),
        ),
    ]
