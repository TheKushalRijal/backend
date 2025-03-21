from django import forms

class StoreSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label="Search")
