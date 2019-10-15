from django.db import models


class Menu(models.Model):
    title = models.CharField('标题', max_length=50)
    icon = models.CharField('图标', max_length=32)
    weight = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class Permission(models.Model):
    url = models.CharField('可访问的地址', max_length=100)
    name = models.CharField('别名', max_length=50, unique=True)
    url_name = models.CharField('地址标题', max_length=32)
    menu = models.ForeignKey('Menu', blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True)

    def __str__(self):
        return self.url_name


class Role(models.Model):
    name = models.CharField('职位名称', max_length=32)
    permissions = models.ManyToManyField('Permission', verbose_name='职位权限', blank=True)

    def __str__(self):
        return self.name


class User(models.Model):
    roles = models.ManyToManyField(Role, verbose_name='账号的职位', blank=True)

    class Meta:
        abstract = True
