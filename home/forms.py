from django import forms


from django import forms
from .models import Merchant, Paybill

class PaymentForm(forms.Form):
    amount = forms.DecimalField(max_digits=8, decimal_places=2)
    description = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=10)
# class MerchantForm(forms.ModelForm):
#     class Meta:
#         model = Merchant
#         # fields = ['name', 'phone', 'email', 'address']
#         # widgets = {
#         #     'name': forms.TextInput(attrs={'class': 'form-control'}),
#         #     'phone': forms.TextInput(attrs={'class': 'form-control'}),
#         #     'email': forms.TextInput(attrs={'class': 'form-control'}),
#         #     'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#         # }

# class PaybillForm(forms.ModelForm):
#     class Meta:
#         model = Paybill
#         fields = ['number', 'description']
#         widgets = {
#             'number': forms.TextInput(attrs={'class': 'form-control'}),
#             'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#         }
