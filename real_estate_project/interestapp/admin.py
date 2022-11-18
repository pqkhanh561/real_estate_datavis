from django.contrib import admin
from .models import Bank

class BankAdmin(admin.ModelAdmin):
    list_display = ["ten_ngan_hang", "lai_suat"]
    list_filter = ['ten_ngan_hang', "lai_suat"]
    search_fields = ['ten_ngan_hang']

admin.site.register(Bank, BankAdmin)