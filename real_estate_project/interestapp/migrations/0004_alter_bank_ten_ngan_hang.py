# Generated by Django 4.1.3 on 2022-11-16 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("interestapp", "0003_alter_bank_lai_suat_alter_bank_ten_ngan_hang"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bank",
            name="ten_ngan_hang",
            field=models.CharField(
                help_text="Tên ngân hàng", max_length=120, verbose_name="Tên ngân hàng"
            ),
        ),
    ]
