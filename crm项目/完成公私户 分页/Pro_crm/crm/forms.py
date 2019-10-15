import hashlib
from crm import models
from django import forms
from django.core.exceptions import ValidationError
from multiselectfield.forms.fields import MultiSelectFormField

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


class Customer_form(forms.ModelForm):

    class Meta:
        model = models.Customer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():

            if isinstance(field,MultiSelectFormField):
                continue
            field.widget.attrs['class'] = 'form-control'






        # exclude = ['last_consult_date']
        # widgets = {
        #     'qq': forms.EmailInput(attrs={'placeholder': 'QQ号码', 'autocomplete': 'off',
        #                                   'class':'form-control'}),
        #     'qq_name': forms.TextInput(attrs={'placeholder': 'QQ昵称', 'autocomplete': 'off',
        #                                       'class':'form-control'}),
        #     'name':forms.TextInput(attrs={'placeholder': '真实姓名', 'autocomplete': 'off',
        #                                   'class':'form-control'}),
        #     'phone':forms.TextInput(attrs={'placeholder': '手机号', 'autocomplete': 'off',
        #                                    'class':'form-control'}),
        #     'source':forms.Select(attrs={'placeholder': '来源', 'autocomplete': 'off',
        #                                     'class':'form-control'}),
        #     'introduce_from':forms.TextInput(attrs={'placeholder': '推荐您来的学员(选填)', 'autocomplete': 'off',
        #                                     'class':'form-control'}),
        #     'course':forms.SelectMultiple(attrs={'placeholder': '咨询课程', 'autocomplete': 'off',
        #                                     'class':'form-control'}),
        #     'class_type':forms.Select(attrs={'placeholder': '班级', 'autocomplete': 'off',
        #                                     'class':'form-control'}),
        #
        #     'status':forms.Select(attrs={'placeholder': '当前状态', 'autocomplete': 'off',
        #                                     'class':'form-control'}),
        #     'next_date':forms.DateInput(attrs={'placeholder': '预计再次跟进时间,格式yyyy-mm-dd', 'autocomplete': 'off',
        #                                     'class':'form-control'}),
        #     'consultant':forms.Select(attrs={'placeholder': '所属销售', 'autocomplete': 'off',
        #                                     'class':'form-control'}),
        #     'class_list':forms.SelectMultiple(attrs={'placeholder': '已报班级', 'autocomplete': 'off',
        #                                     'class':'form-control'}),
        #     'customer_note':forms.TextInput(attrs={'placeholder': '客户备注', 'autocomplete': 'off',
        #                                     'class':'form-control'}),
        #     'sex':forms.Select(attrs={'placeholder': '性别', 'autocomplete': 'off',
        #                                     'class':'form-control'})
        # }
