from django.utils.safestring import mark_safe
from django.http.request import QueryDict

class paginator:
    def __init__(self, page, all_count, params=None, per_page=10, max_show=11):
        try:
            page = int(page)
            if page <= 0:
                page = 1
        except Exception:
            page = 1

        total, rem = divmod(len(all_count), per_page)
        if rem:
            total += 1
        start_data = (page-1) * per_page
        end_data = page * per_page

        half_show = max_show // 2
        if total <= max_show:
            start_page = 1
            end_page = total
        else:
            if page - half_show < 0:
                start_page = 1
                end_page = max_show
            elif page + half_show > total:
                start_page = total - max_show + 1
                end_page = total

            else:
                start_page = page - half_show
                end_page = page + half_show

        self.page = page
        self.start_data = start_data
        self.end_data = end_data
        self.start_page = start_page
        self.end_page = end_page
        self.total = total
        self.params = params
        if not self.params:
            self.params = QueryDict(mutable=True)



    def page_html(self):
        get_list = []
        if self.page == 1:
            get_list.append('<li class="disabled"><a href="#" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>')
        else:
            self.params['page'] = self.page-1
            get_list.append('<li><a href="?{}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(self.params.urlencode()))
        for i in range(self.start_page, self.end_page+1):
            self.params['page'] = i
            if i == self.page:
                get_list.append('<li class="active"><a href="?{}">{}</a></li>'.format(self.params.urlencode(), i))
            else:
                get_list.append('<li><a href="?{}">{}</a></li>'.format(self.params.urlencode(), i))

        if self.page == self.total:
            get_list.append('<li class="disabled"><a href="#" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>')
        else:
            self.params['page'] = self.page+1
            get_list.append('<li><a href="?{}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'.format(self.params.urlencode()))

        return mark_safe(''.join(get_list))








