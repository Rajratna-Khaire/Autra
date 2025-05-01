from django import forms
from .models import Trade

class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = ['stock_symbol', 'action', 'quantity', 'price', 'sl', 'target', 'trade_type']

        # Optional: Customize field widgets
        widgets = {
            'stock_symbol': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Stock Symbol'}),
            'action': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'sl': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stop Loss'}),
            'target': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Target Price'}),
            'trade_type': forms.Select(attrs={'class': 'form-control'}),
        }
