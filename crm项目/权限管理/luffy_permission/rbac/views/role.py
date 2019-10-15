from rbac import models
from django.db.models import Q
from django.shortcuts import reverse, redirect, render
from rbac.form import RoleForm, MenuForm


def role_list(request):
    all_role = models.Role.objects.all()
    return render(request, 'rbac/role_list.html', {'all_role': all_role})



def role_change(request, pk=None):
    obj = models.Role.objects.filter(pk=pk).first()
    form_obj = RoleForm(instance=obj)
    if request.method == 'POST':
        form_obj = RoleForm(instance=obj, data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('role_list'))
    return render(request, 'rbac/form.html', {'form_obj': form_obj})


def menu_list(request):
    all_menu = models.Menu.objects.all()
    mid = request.GET.get('mid')
    if not mid:
        all_permission = models.Permission.objects.all()
    else:
        all_permission = models.Permission.objects.filter(Q(menu_id=mid) | Q(parent__menu_id=mid))

    permission_dict = {}

    for i in all_permission.values('id', 'url_name', 'url', 'name', 'menu_id', 'menu__title', 'parent_id'):
        menu_id = i.get('menu_id')
        if menu_id:
            permission_dict[i['id']] = i
            i['children'] = []

    for i in all_permission.values('id', 'url_name', 'url', 'name', 'menu_id', 'menu__title', 'parent_id'):
        parent_id = i.get('parent_id')
        if parent_id:
            permission_dict[parent_id]['children'].append(i)




    return render(request, 'rbac/menu_list.html', {'all_menu': all_menu, 'all_permission': permission_dict.values(),
                                                   'mid': mid})


def menu_change(request, pk=None):
    obj = models.Menu.objects.filter(pk=pk).first()
    form_obj = MenuForm(instance=obj)
    if request.method == 'POST':
        form_obj = MenuForm(instance=obj, data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('menu_list'))
    return render(request, 'rbac/form.html', {'form_obj': form_obj})