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
                                'placeholder': '再次输入您的密码',
                                'autocomplete': 'off'}))

    class Meta:
        model = models.UserProfile
        fields ='__all__'
        exclude = ['is_active']
        widgets = {
            # 'memo': forms.TextInput(attrs={'placeholder': '备注信息'})
        }
        widgets = {
            'username': forms.EmailInput(attrs={'placeholder': '您的邮箱名', 'autocomplete': 'off'}),
            'mobile': forms.TextInput(attrs={'placeholder': '您的手机号码', 'autocomplete': 'off'}),
            'name': forms.TextInput(attrs={'placeholder': '您的真实姓名', 'autocomplete': 'off'})
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args,**kwargs)
    #     for field in self.fields.values():
    #         field.widget.attrs['autocomplete'] = 'off'
    #         field.widget.attrs['class'] = 'form-control'

    def clean(self):
        self._validate_unique = True
        password =self.cleaned_data.get('password','')
        re_password = self.cleaned_data.get('re_password','')
        if password == re_password:
            md5 = hashlib.md5()
            md5.update(password.encode('utf-8'))
            self.cleaned_data['password'] = md5.hexdigest()
            return self.cleaned_data
        else:
            self.add_error('password', '两次密码输入不一致')
            raise ValidationError('密码输入不一致')


class BSModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():

            if isinstance(field, (MultiSelectFormField,forms.BooleanField)):
                continue
            field.widget.attrs['class'] = 'form-control'


class Customer_form(BSModelForm):

    class Meta:
        model = models.Customer
        fields = '__all__'



class Record_form(BSModelForm):

    class Meta:
        model = models.ConsultRecord
        fields = '__all__'


    def __init__(self, request, customer_id, *args, **kwargs):
        super().__init__(*args,**kwargs)
        if customer_id and customer_id != '0':
            self.fields['customer'].choices = [(i.pk,str(i)) for i in models.Customer.objects.filter(pk=customer_id)]
        else:
            self.fields['customer'].choices = [(i.pk, str(i)) for i in request.obj.customers.all()]

        self.fields['consultant'].choices = [(request.obj.pk,request.obj.name)]



class Enrollment_form(BSModelForm):

    class Meta:
        model = models.Enrollment
        fields = '__all__'


    def __init__(self, request, customer_id, *args, **kwargs):
        super().__init__(*args,**kwargs)
        if customer_id and customer_id != '0':
            self.fields['customer'].choices = [(i.pk,str(i)) for i in models.Customer.objects.filter(pk=customer_id)]
            self.fields['enrolment_class'].choices = [(i.pk, str(i)) for i in
                                                      models.Customer.objects.get(pk=customer_id).class_list.all()]

        else:
            self.fields['customer'].choices = [(i.pk, str(i)) for i in request.obj.customers.all()]