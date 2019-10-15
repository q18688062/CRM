from django.db import models


class Permission(models.Model):
    url = models.CharField('可访问的地址', max_length=100)
    url_name = models.CharField('地址标题', max_length=32)

    def __str__(self):
        return self.url_name


class Role(models.Model):
    name = models.CharField('职位名称', max_length=32)
    permissions = models.ManyToManyField('Permission', verbose_name='职位权限', blank=True)

    def __str__(self):
        return self.name


class User(models.Model):
    username = models.CharField('用户账号', max_length=32)
    password = models.CharField('用户密码', max_length=32)
    roles = models.ManyToManyField('Role', verbose_name='账号的职位', blank=True)

    def __str__(self):
        return self.username
