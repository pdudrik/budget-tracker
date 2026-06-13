from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .forms import CreateCategoryForm, UpdateCategoryForm,          \
    CreateSubcategoryForm, UpdateSubcategoryForm
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


def get_all_subcategories(category):
    pass


########### CATEGORY ###########
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
        form.save()
    
        return JsonResponse(
            {
                "status": "success",
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
    
    category_id = request.POST.get("update_category-category_select")
    if not category_id:
        return JsonResponse(
            {
                "status": "error",
                "message": "Category missing ID!"
            },
            status=400
        )
    
    try:
        print(f"Category: {category}")
        category = Category.objects.get(id=category_id)
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


########### SUBCATEGORY ###########
def create_subcategory(request):
    if request.method != "POST":
        return JsonResponse(
            {
                "status": "error",
                "message": "Method not allowed"
            },
            status=405
        )
    
    form = CreateSubcategoryForm(
        request.POST,
        prefix="create_subcategory"
    )
    if form.is_valid():
        form.save()
        print(form) 
        return JsonResponse(
            {
                "status": "success",
                "subcategories": get_all_subcategories(1)
            }
        )
    
    return JsonResponse(
        {
            "status": "error",
            "errors": form.errors
        },
        status=400
    )


def update_subcategory(request):
    if request.method != "POST":
        return JsonResponse(
            {
                "status": "error",
                "message": "Method not allowed"
            },
            status=405
        )

    form = UpdateSubcategoryForm(
        request.POST,
        prefix="update_subcategory"
    )
    print(f"form: {form}\n\n\n")
    # print(f"category: {form.cleaned_data["category"]}")
    # print(f"subcategory_select: {form.cleaned_data["subcategory_select"]}")
    # print(f"target subcategory ID: {form.cleaned_data["id"]}")
    # print(f"new name: {form.cleaned_data["name"]}")

    if not form.is_valid():
        return JsonResponse(
            {
                "status": "error",
                "errors": form.errors
            },
            status=400
        )

    subcategory = form.cleaned_data["subcategory"]      # "subcategory" is prefix
    # subcategory = form.cleaned_data["subcategory_select"]
    # parent_category = form.cleaned_data["category"]
    new_name = form.cleaned_data["name"]

    print(f"Subcategory: {subcategory}")
    print(f"New name: {new_name}")

    print(f"subcategory \"{subcategory.name}\" will be renamed to \"{new_name}\"")

    if subcategory.name == new_name:
        return JsonResponse(
        {
            "status": "success",
            "message": "New category name is same!",
        }
    )

    if Subcategory.objects.filter(name__iexact=new_name).exclude(id=subcategory.id).exists():
        return JsonResponse(
            {
                "status": "error",
                "errors": {
                    "update_subcategory-name": [
                        "A subcategory with this name already exists!"
                    ]
                }
            },
            status=400
        )
    
    if Category.objects.filter(name__iexact=new_name).exists():
        return JsonResponse(
            {
                "status": "error",
                "errors": {
                    "update_category-name": [
                        "A category with this name already exists! Both category and subcategory can't have the same names."
                    ]
                }
            },
            status=400
        )
    

    subcategory.name = new_name
    subcategory.save()

    # category_list = []
    # for cat in Category.objects.all().order_by("name"):
    #     category_list.append(
    #         {
    #             "id": cat.id,
    #             "name": cat.name
    #         }
    #     )
    
    return JsonResponse(
        {
            "status": "success",
            "message": "Subcategory renamed successfully!",
            # "categories": category_list
            "categories": None
        }
    )
    

def delete_subcategory(request):
    pass
#     if request.method != "POST":
#         return JsonResponse(
#             {
#                 "status": "error",
#                 "message": "Method not allowed"
#             },
#             status=405
#         )
    
#     category_id = request.POST.get("update_category-category_select")
#     if not category_id:
#         return JsonResponse(
#             {
#                 "status": "error",
#                 "message": "Category missing ID!"
#             },
#             status=400
#         )
    
#     try:
#         print(f"Category: {category}")
#         category = Category.objects.get(id=category_id)
#         category.delete()

#     except Category.DoesNotExist:
#         return JsonResponse(
#             {
#                 "status": "error",
#                 "message": "Category not found or no longer exists!"
#             },
#             status=404
#         )

#     return JsonResponse(
#         {
#             "status": "success",
#             "message": "Category deleted successfully!",
#             "categories": get_all_categories()
#         }
#     )