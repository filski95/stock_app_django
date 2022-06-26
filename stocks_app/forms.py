from django import forms


class RemoveStockWatchlist(forms.Form):
    remove_stock_from_your_watchlist = forms.CharField(
        max_length=5, help_text="Enter the stock ticker/abbreviation you would like to remove from your watchlist"
    )
