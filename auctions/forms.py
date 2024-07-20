from django import forms
from .models import ListingInformation


class ListingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-3'
            visible.field.widget.attrs['placeholder'] = visible.field.label


    class Meta:
        labels = {
            "title":"Title",
            "description":"Description",
            "bidCurrentPrice":"Initial Bid",
            "image":"Item Image",
            "category":"Category"
        }
        model = ListingInformation
        fields = ['title', 'description', 'bidCurrentPrice', 'image', 'category']
