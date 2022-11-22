from django import forms
from .models import House


class HouseFilterInfo(forms.Form):
    GEEKS_CHOICES = (
        (1, "One"),
        (2, "Two"),
        (3, "Three"),
        (4, "Four"),
        (5, "Five"),
    )
    start_price = forms.DecimalField(required=False)
    end_price = forms.DecimalField(required=False)

    start_area = forms.DecimalField(required=False)
    end_area = forms.DecimalField(required=False)

    num_bed = forms.ChoiceField(choices=GEEKS_CHOICES, required=False)
    num_bath = forms.ChoiceField(choices=GEEKS_CHOICES, required=False)


    start_price.widget.attrs.update({'class': 'loaihinhclass'})
    end_price.widget.attrs.update({'class': 'loaihinhclass'})

    start_area.widget.attrs.update({'class': 'loaihinhclass'})
    end_area.widget.attrs.update({'class': 'loaihinhclass'})

    num_bed.widget.attrs.update({'class': 'loaihinhclass'})
    num_bath.widget.attrs.update({'class': 'loaihinhclass'})