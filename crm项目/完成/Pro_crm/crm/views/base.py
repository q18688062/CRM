from django.views import View
from django.db.models import Q
from crm.models import source_type

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
        # if content:
        #     for i in source_type:
        #         print(i)
        #         if content in i[1]:
        #             print(content)
        #             content = i[0]
        #             break
        q = Q()
        q.connector = 'OR'
        for field in field_list:
            q.children.append(Q(('{}__contains'.format(field), content)))
        return q