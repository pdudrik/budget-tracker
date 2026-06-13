from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView,      \
    UpdateView, View, TemplateView
from .models import Transaction, Subcategory
from .forms import TransactionForm, CreateCategoryForm,                 \
    UpdateCategoryForm, CreateSubcategoryForm, UpdateSubcategoryForm,   \
    UpdateSubcategoryParentForm, DeleteSubcategoryForm

# Create your views here.
def home(request):
    return render(request, "home.html")


class TransationView(ListView):
    model = Transaction
    template_name = "transactions.html"
    context_object_name = "records"
    ordering = ["-date"]            # newest first
    paginate_by = 25


class AddTransactionView(CreateView):
    model = Transaction
    template_name = "add_transactions.html"
    success_url = reverse_lazy("budget:transactions")
    form_class = TransactionForm


class UpdateTransactionView(UpdateView):
    model = Transaction
    template_name = "add_transactions.html"
    success_url = reverse_lazy("budget:transactions")
    form_class = TransactionForm


class DeleteTransactionView(DeleteView):
    model = Transaction
    success_url = reverse_lazy("budget:transactions")

    def get(self, request, *args, **kwargs):
        return redirect(self.success_url)
    

class SettingsView(TemplateView):
    template_name = "settings.html"
    success_url = reverse_lazy("budget:settings")

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        subcategories = Subcategory.objects.all().values("id", "name", "category_id")

        context["create_category_form"] = CreateCategoryForm(prefix="create_category")
        context["update_category_form"] = UpdateCategoryForm(prefix="update_category")
        context["create_subcategory_form"] = CreateSubcategoryForm(prefix="create_subcategory")
        context["update_subcategory_form"] = UpdateSubcategoryForm(prefix="update_subcategory")
        context["update_subcategory_parent_form"] = UpdateSubcategoryParentForm(prefix="update_subcategory_parent")
        context["delete_subcategory_form"] = DeleteSubcategoryForm(prefix="delete_subcategory")
        context["data_json"] = {
            "subcategories": list(subcategories)
        }
        return self.render_to_response(context)