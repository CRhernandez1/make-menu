from django import forms
from .models import Establishment, Table, Manage

class EstablishmentCreateForm(forms.ModelForm):
    class Meta:
        model = Establishment
        fields = ['cif', 'name', 'legal_name', 'description', 'zip_code', 'city', 'address', 'phone']

class EstablishmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Establishment
        exclude = ['cif', 'opened']

class TableCreateForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['number', 'max_guests']

class TableUpdateForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['max_guests']

class ManageUpdateForm(forms.ModelForm):
    class Meta:
        model = Manage
        fields = ['role']