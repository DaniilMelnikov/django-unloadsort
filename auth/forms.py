from django import forms

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=1024, widget=forms.TextInput(attrs={"class":"field", 'placeholder': 'Введите ваше имя'}), label=False, required=True)
    last_name = forms.CharField(max_length=1024, widget=forms.TextInput(attrs={"class":"field", 'placeholder': 'Введите вашу фамилию'}), label=False, required=True)
    email = forms.EmailField(max_length=1024, widget=forms.EmailInput(attrs={"class":"field", 'placeholder': 'Введите ваш Email'}), label=False, required=True)
    password = forms.CharField(max_length=1024, widget=forms.PasswordInput(attrs={"class":"field", 'placeholder': 'Введите ваш пароль'}), label=False, required=True)

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=1024, widget=forms.EmailInput(attrs={"class":"field", 'placeholder': 'Введите ваш Email'}), label=False, required=True)
    password = forms.CharField(max_length=1024, widget=forms.PasswordInput(attrs={"class":"field", 'placeholder': 'Введите ваш пароль'}), label=False, required=True)

class KeyXmlProxyForms(forms.Form):
    email = forms.EmailField(max_length=1024, widget=forms.EmailInput(attrs={"class":"form-field", 'placeholder': 'Введите ваш Email'}), label=False, required=True)
    key = forms.CharField(max_length=1024, widget=forms.TextInput(attrs={"class":"form-field", 'placeholder': 'Введите ваш ключ из xmlproxy'}), label=False, required=True)