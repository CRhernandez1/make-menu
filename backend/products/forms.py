from django import forms
from .models import Product, Ingredient, Category, Component


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category']


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category']


class IngredientCreateForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'ingredient_type', 'description', 'available']


class IngredientUpdateForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'ingredient_type', 'description']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class ComponentCreateForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ['quantity', 'unity', 'removable']