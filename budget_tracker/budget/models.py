from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Category name"
    )
    
    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name="Subcategory name",
        unique=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="subcategories",
        null=True
    )

    class Meta:
        ordering = ["category", "name"]
        verbose_name_plural = "Subcategories"
        unique_together = ("name", "category")      # prevents having same category and subcategory name
    
    def __str__(self):
        return f"{self.category.name} -> {self.name}"


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ("income", "Income"),
        ("expense", "Expense"),
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES
        )
    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2
        )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="category",
        null=True
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.SET_NULL,
        related_name="subcategory",
        null=True
    )
    date = models.DateField()
    note = models.TextField(blank=True)


