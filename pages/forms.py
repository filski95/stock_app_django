from django import forms


class StockEntryForm(forms.Form):
    stock_abbreviation = forms.CharField(
        label="Stock", help_text="Enter here the abbreviation of the stock used on Yahoo's website"
    )
