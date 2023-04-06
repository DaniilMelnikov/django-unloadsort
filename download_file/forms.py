from django import forms

class DomainForm(forms.Form):
    name = forms.CharField(max_length=512, widget=forms.TextInput(attrs={"class":"form-field", 'placeholder': 'Введите домен'}), label=False, required=True)
    limit = forms.IntegerField(widget=forms.TextInput(attrs={"class":"form-field", 'placeholder': 'Введите лимит'}), label=False, required=True)

class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'placeholder': 'Выберите csv файл', "class":"file-field", 'title': 'Выберите файл CSV'}), label=False, required=True)