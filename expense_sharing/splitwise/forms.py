# forms.py

from django import forms
from .models import *

class UserForm(forms.ModelForm):
    class MEta:
        fields = ['name' 'email', 'mobile_number', 'expense_share_amount']
    

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['total_expense', 'paid_by', 'expense_type', 'users_share']
        widgets = {
            'users_share': forms.CheckboxSelectMultiple,  # Use CheckboxSelectMultiple for multiple user selection
        }
