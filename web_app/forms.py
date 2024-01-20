from django import forms
from web_app.models import Visitor,Picture

class LoginForm(forms.Form):
    user = forms.CharField(max_length=30)
    password = forms.CharField(max_length=20,widget=forms.PasswordInput())

    def clean_user(self):
        user = self.cleaned_data['user']
        self.db_data = Visitor.objects.filter(user=user)

        if self.db_data:    #檢查資料庫儲存帳號是否存在
            return user
        return False

    def clean_password(self):
        password = self.cleaned_data['password']
        if self.db_data:
            if self.db_data[0].password == password:  #檢查資料庫儲存密碼是否存在
                return password
            return False
        return False

class RegiesterForm(LoginForm):
    name = forms.CharField(max_length=30)
    email = forms.CharField(max_length=30)

    def clean_user(self):
        user = self.cleaned_data['user']
        db_user = Visitor.objects.filter(user=user)

        if db_user:    #檢查資料庫儲存帳號是否存在
            return False
        return user

    def clean_password(self):
        password = self.cleaned_data['password']
        # db_password = Visitor.objects.filter(password=password)

        # if db_password:  #檢查資料庫儲存密碼是否存在
        #     return False
        return password

class ResetPasswordForm(forms.Form):
    password = forms.CharField(max_length=20,widget=forms.PasswordInput())
    again = forms.CharField(max_length=20,widget=forms.PasswordInput())

class PictureForm(forms.Form):
    filename = forms.CharField(max_length=30)
    picture = forms.ImageField(allow_empty_file=False)










