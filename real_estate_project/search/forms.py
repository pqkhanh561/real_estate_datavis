from django import forms
from .models import House


class HouseFilterInfo(forms.Form):
    NUM_CHOICES = (
        (None, "Chọn"),
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )
    start_price = forms.DecimalField(required=False)
    end_price = forms.DecimalField(required=False)

    start_area = forms.DecimalField(required=False)
    end_area = forms.DecimalField(required=False)

    num_bed = forms.ChoiceField(choices=NUM_CHOICES, required=False)
    num_bath = forms.ChoiceField(choices=NUM_CHOICES, required=False)

    compare_no1 = forms.CharField(required=False)
    compare_no2 = forms.CharField(required=False)


    start_price.widget.attrs.update({'class': 'loaihinhclass'})
    end_price.widget.attrs.update({'class': 'loaihinhclass'})

    start_area.widget.attrs.update({'class': 'loaihinhclass'})
    end_area.widget.attrs.update({'class': 'loaihinhclass'})

    num_bed.widget.attrs.update({'class': 'loaihinhclass'})
    num_bath.widget.attrs.update({'class': 'loaihinhclass'})