from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .forms import CreateCategoryForm, UpdateCategoryForm,          \
    CreateSubcategoryForm
from .models import Category, Subcategory


def get_all_categories():
    category_list = []
    for cat in Category.objects.all().order_by("name"):
        category_list.append(
            {
                "id": cat.id,
                "name": cat.name
            }
        )
    
    return category_list


def create_category(request):
    if request.method != "POST":
        return JsonResponse(
            {
                "status": "error",
                "message": "Method not allowed"
            },
            status=405
        )
    
    form = CreateCategoryForm(
        request.POST,
        prefix="create_category"
    )
    if form.is_valid():
        category = form.save()
    
        return JsonResponse(
            {
                "status": "success",
                # "created_category_id": category.id,
                "categories": get_all_categories()
            }
        )
    
    return JsonResponse(
        {
            "status": "error",
            "errors": form.errors
        },
        status=400
    )


def update_category(request):
    if request.method != "POST":
        return JsonResponse(
            {
                "status": "error",
                "message": "Method not allowed"
            },
            status=405
        )

    form = UpdateCategoryForm(
        request.POST,
        prefix="update_category"
    )
    if not form.is_valid():
        return JsonResponse(
            {
                "status": "error",
                "errors": form.errors
            },
            status=400
        )

    category = form.cleaned_data["category_select"]
    new_name = form.cleaned_data["name"]

    if Category.objects.filter(name__iexact=new_name).exclude(id=category.id).exists():
        return JsonResponse(
            {
                "status": "error",
                "errors": {
                    "update_category-name": [
                        "A category with this name already exists"
                    ]
                }
            },
            status=400
        )

    category.name = new_name
    category.save()

    # all_categories = Category.objects.all().order_by("name")
    # category_list = [{"id": cat.id, "name": cat.name} for cat in all_categories]
    category_list = []
    for cat in Category.objects.all().order_by("name"):
        category_list.append(
            {
                "id": cat.id,
                "name": cat.name
            }
        )
    
    return JsonResponse(
        {
            "status": "success",
            "message": "Category renamed successfully!",
            "categories": category_list
        }
    )
    

def delete_category(request):
    if request.method != "POST":
        return JsonResponse(
            {
                "status": "error",
                "message": "Method not allowed"
            },
            status=405
        )
    
    print(request.POST)
    category_id = request.POST.get("update_category-category_select")
    print(f"Category ID: {category_id}")
    if not category_id:
        return JsonResponse(
            {
                "status": "error",
                "message": "Category missing ID!"
            },
            status=400
        )
    
    try:
        category = Category.objects.get(id=category_id)
        print(f"Category: {category}")
        category.delete()

    except Category.DoesNotExist:
        return JsonResponse(
            {
                "status": "error",
                "message": "Category not found or no longer exists!"
            },
            status=404
        )

    return JsonResponse(
        {
            "status": "success",
            "message": "Category deleted successfully!",
            "categories": get_all_categories()
        }
    )