from django import forms
from .models import Review

class ProductFilterForm(forms.Form):
    product_search = forms.CharField(label="Product search", max_length=50, required=True)
    min_price = forms.DecimalField(decimal_places=2)
    max_price = forms.DecimalField(decimal_places=2)
    avg_rating = forms.DecimalField()


class ReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		fields = ['stars', 'review_text']