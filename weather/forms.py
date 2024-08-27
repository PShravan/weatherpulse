from django import forms


class LocationSearchForm(forms.Form):
    location = forms.CharField(
        max_length=100, required=True, help_text="Enter location name"
    )
