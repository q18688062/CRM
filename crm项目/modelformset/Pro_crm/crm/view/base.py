from django.views import View
from django.db.models import Q



class Baseview(View):

    def post(self, request, *args, **kwargs):
        operation = request.POST.get('operation')
        if hasattr(self, operation):
            ret = getattr(self, operation)()
            if ret:
                return ret
            return self.get(request, *args, **kwargs)



    def dispose(self, field_list):
        content = self.request.GET.get('content', '')
        q = Q()
        q.connector = 'OR'
        for field in field_list:
            q.children.append(Q(('{}__contains'.format(field), content)))
        return q