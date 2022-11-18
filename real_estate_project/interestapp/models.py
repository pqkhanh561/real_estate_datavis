from django.db import models

class Bank(models.Model):
    ten_ngan_hang = models.CharField('Tên ngân hàng', max_length=120)
    lai_suat = models.DecimalField('Lãi suất mua nhà % (năm) ', decimal_places=2, max_digits=15)

    def __str__(self):
        return f"{self.ten_ngan_hang}"

    class Meta:
        ordering = ("ten_ngan_hang", "lai_suat")


