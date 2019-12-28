from django import forms
from .models import User , Branch , Tag , Item


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 20}))

    class Meta:
        model = User
        fields = ['first_name' , 'middle_name' , 'last_name' , 'username' , 'password' , 'email' , 'phone' , 'role' , 'branch' , 'address' ,'photo' , 'is_staff' , 'is_active']


class BranchForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))

    class Meta:
        model = Branch
        fields = ['name' , 'description']

class TagForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))

    class Meta:
        model = Tag
        fields = ['name' , 'description']

class ItemForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 5,"cols": 20}))
    tags = forms.CheckboxSelectMultiple()

    class Meta:
        model = Item
        fields = ['name' , 'branch' , 'price' , 'description' , 'photo','total_count', 'tags']