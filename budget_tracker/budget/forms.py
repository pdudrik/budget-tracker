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


########### CATEGORY ###########
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


########### SUBCATEGORY ###########
class SubcategoryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name
    

class CreateSubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = [
            "name",
            "category"
        ]


# class UpdateSubcategoryForm(forms.ModelForm):
#     subcategory_select = SubcategoryChoiceField(
#         queryset=Subcategory.objects.all(),
#         empty_label="-- Select subcategory --"
#     )

#     class Meta:
#         model = Subcategory
#         fields = [
#             "name",
#             "category"
#         ]


class UpdateSubcategoryForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="-- Select category --",
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )

    subcategory = SubcategoryChoiceField(
        queryset=Subcategory.objects.all(),
        empty_label="-- Select subcategory --",
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )

    name = forms.CharField(
        max_length=100,
        label="New subcategory name",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Type new name here'
                }
        )
    )