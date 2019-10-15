import hashlib
from crm import models
from django import forms
from django.core.exceptions import ValidationError


class RegForm(forms.ModelForm):
    password = forms.CharField(min_length=6,
                              widget=forms.PasswordInput(attrs={
                                'placeholder': '您的密码',
                                'autocomplete': 'off'}))
    re_password = forms.CharField(min_length=6,
                              widget=forms.PasswordInput(attrs={
                                'placeholder': '您的密码',
                                'autocomplete': 'off'}))

    class Meta:
        model = models.UserProfile
        fields ='__all__'
        exclude = ['is_alive']
        widget = {
            'username': forms.EmailInput(attrs={'placeholder': '您的邮箱名', 'autocomplete': 'off'}),
            'mobile': forms.TextInput(attrs={'placeholder': '您的手机号码', 'autocomplete': 'off'}),
            'name':forms.TextInput(attrs={'placeholder': '您的真实姓名', 'autocomplete': 'off'})

        }
    def clean(self):
        self._validate_unique = True
        password =self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password == re_password:
            md5 = hashlib.md5()
            md5.update(password.encode('utf-8'))
            self.cleaned_data['password'] = md5.hexdigest()
            return self.cleaned_data
        else:
            self.add_error('password', '两次密码输入不一致')
            raise ValidationError('密码输入不一致')


class Logform(forms.Form):
    username = forms.CharField(min_length=6,widget=forms.TextInput(attrs={'placeholder': '您的用户名',
                                                             'class': "input__field input__field--hideo",
                                                             'id': 'login-username',
                                                             'autocomplete': 'off',
                                                             }))
    password = forms.CharField(min_length=6,widget=forms.PasswordInput(attrs={'placeholder': '您的密码',
                                                                              'class': "input__field input__field--hideo",
                                                             'id': 'login-username','autocomplete': 'off'}))



