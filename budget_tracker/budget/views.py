from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView,  \
    UpdateView, View, TemplateView
from .models import Transaction
from .forms import TransactionForm, CreateCategoryForm,             \
    UpdateCategoryForm


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
        context["create_category_form"] = CreateCategoryForm(prefix="create_category")
        context["update_category_form"] = UpdateCategoryForm(prefix="update_category")
        # context["subcategory_form"] = SubcategoryForm(prefix="subcategory")

        return self.render_to_response(context)

    # def post(self, request, *args, **kwargs):
        # create_category_form = CreateCategoryForm(request.POST, prefix="create_category")
        # update_category_form = UpdateCategoryForm(request.POST, prefix="update_category")
        # form = None

        # if "submit_category" in request.POST:
        #     form = CreateCategoryForm(request.POST, prefix="create_category")
        #     if form.is_valid():
        #         form.save()
        #         return redirect(self.success_url)
            
            
            
        # if "submit_subcategory" in request.POST:
        #     if subcategory_form.is_valid():
        #         subcategory_form.save()
        #         return redirect(self.success_url)
        
        # return render( 
        #     request,
        #     self.template_name,
        #     {
        #         "create_category_form": form,
        #         # "subcategory_form": subcategory_form
        #     }
        # )