from django import forms
from .models import Contact
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update({
            'required': '',
            'name': 'full_name',
            'id': 'name',
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'نام و نام خانوادگی',
        }),
        self.fields['email'].widget.attrs.update({
            'name': 'email',
            'id': 'email',
            'type': 'email',
            'class': 'form-control',
            'placeholder': 'test@test.com',
        }),
        self.fields['relationship'].widget.attrs.update({
            'name': 'relationship',
            'id': 'relationship',
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'همکار , عمو',
        }),
        self.fields['phone_number'].widget.attrs.update({

            'name': 'phone_number',
            'id': 'subject',
            'type': 'number',
            'class': 'form-control',
            'placeholder': '09123456789',
        }),
        self.fields['address'].widget.attrs.update({

            'name': 'address',
            'id': 'message',
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'آدرس',
            'cols': 30,
            'rows': 4,
        }),
        self.fields['image'].widget.attrs.update({
            'label':'delete'
        }),


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(), label='رمز قدیمی')
    new_password1 = forms.CharField(widget=forms.PasswordInput(), label='رمز جدید')
    new_password2 = forms.CharField(widget=forms.PasswordInput(), label='تایید رمز')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user",None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        myuser = User.objects.get(id=self.user.id)
        old_password = self.cleaned_data.get("old_password")

        if not myuser.check_password(old_password):
            raise forms.ValidationError('لطفا رمز قدیمی خود را به درستی وارد کنید')
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password2 != password1:
            raise forms.ValidationError('لطفا رمز خود را به درستی تایید کنید!')
        return password2


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


    # def clean(self, *args , **kwargs):
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')
    #
    #     if username or password:
    #         user = authenticate(username=username, password=password)
    #         if not user:
    #             raise forms.ValidationError("این کاربر وجود ندارد !")
    #
    #         if not user.check_password(password):
    #             raise forms.ValidationError("این رمز اشتباه است !")
    #
    #         if not user.is_active():
    #             raise forms.ValidationError("این کاربر غیر فعال است !")
    #
    #         return




class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True, )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

    def clean(self):
       email = self.cleaned_data.get('email')
       username = self.cleaned_data.get('username')
       if User.objects.filter(email=email).exists():
            raise forms.ValidationError('این ایمیل تکراری است!')
       if User.objects.filter(username=username).exists():
           raise forms.ValidationError('این نام کاربری تکراری است !')
       return self.cleaned_data
