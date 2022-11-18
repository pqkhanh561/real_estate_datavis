from django import forms
from .models import Bank

class InterestForm(forms.Form):
    # CHOICE
    TYPE_CHOICES = (
        ("1", "Dư nợ giảm dần (kỳ khoản giảm dần)"),
        ("2", "Dư nợ giảm dần (kỳ khoản cố định)"),
    )
    so_tien_vay = forms.DecimalField(label="Số tiền vay (VND)", max_digits=15, localize=True)
    ky_han = forms.IntegerField(label="Thời gian vay (tháng)")
    lai_suat = forms.DecimalField(decimal_places=2, label="Lãi suất % (năm)")
    loai_hinh = forms.ChoiceField(choices=TYPE_CHOICES, label="Loại hình")

    # Updating class for each form
    lai_suat.widget.attrs.update({'class': 'myclass'})
    ky_han.widget.attrs.update({'class': 'myclass'})
    so_tien_vay.widget.attrs.update({'class': 'myclass'})
    loai_hinh.widget.attrs.update({'class': 'loaihinhclass'})

class BankForm(forms.Form):

    initial = tuple(['Không có', 'Chọn ngân hàng'])
    CHOICE = tuple(Bank.objects.values_list('lai_suat','ten_ngan_hang'))
    CHOICES = (initial,) + CHOICE

    ten_ngan_hang = forms.ChoiceField(choices=CHOICES, required=False,
                                           label="Ngân hàng",
    )
    ten_ngan_hang.widget.attrs.update({'class': 'loaihinhclass', 'id': "mySelect",
                                       'onchange': 'show_laisuat()'
                                    })

