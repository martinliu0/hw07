from django import forms

class ProductFilterForm(forms.Form):
    product_search = forms.CharField(label="Product search", max_length=50, required=True)
    min_price = forms.DecimalField(decimal_places=2)
    max_price = forms.DecimalField(decimal_places=2)