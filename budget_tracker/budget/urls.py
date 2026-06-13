from django.urls import path
from budget import views, endpoints


app_name = "budget"


urlpatterns = [
    path("", views.home, name="dashboard"),
    path("transactions/", views.TransationView.as_view(), name="transactions"),
    path("transactions/add", views.AddTransactionView.as_view(), name="add_transaction"),
    path("transactions/<int:pk>/update/", views.UpdateTransactionView.as_view(), name="update_transaction"),
    path("transactions/<int:pk>/delete/", views.DeleteTransactionView.as_view(), name="delete_transaction"),
    path("settings/", views.SettingsView.as_view(), name="settings"),
    path("settings/api/category/create/", endpoints.create_category, name="api_create_category"),
    path("settings/api/category/update/", endpoints.update_category, name="api_update_category"),
    path("settings/api/category/delete/", endpoints.delete_category, name="api_delete_category"),
    path("settings/api/subcategory/create/", endpoints.create_subcategory, name="api_create_subcategory"),
    path("settings/api/subcategory/update/", endpoints.update_subcategory, name="api_update_subcategory"),
    path("settings/api/subcategory/delete/", endpoints.delete_subcategory, name="api_delete_subcategory"),
]
