from django import forms
from .models import Transaction, Category, Subcategory




class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            "transaction_type",
            "date",
            "amount",
            "category",
            "subcategory",
            "note"
        ]


class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            "name"
        ]

        # widgets = {
        #     "name": forms.Select(attrs={"class": "form-dropdown"})
        # }


class UpdateCategoryForm(forms.ModelForm):
    category_select = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="-- Select Category --"
    )

    class Meta:
        model = Category
        fields = [
            "name"
        ]



class CreateSubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = [
            "name",
            "category"
        ]