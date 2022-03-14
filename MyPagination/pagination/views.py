from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage
from django.views.generic import ListView

from pagination.models import SchoolInfo, StudentInfo


# Create your views here.
def school_list(request):
    school_list = SchoolInfo.objects.all()
    paginator = Paginator(school_list, 5)

    page_number = request.GET.get('page', None)

    try:
        page_obj = paginator.get_page(page_number)
        page_range = paginator.get_elided_page_range(number=page_number, on_each_side=2)
        context = {
            'page_obj': page_obj,
            'page_range': page_range
        }
        return render(request, 'list.html', context)
    except PageNotAnInteger:
        return redirect(to="/schools/?page=1", permanent=True)


class StudentList(ListView):
    model = StudentInfo
    template_name = 'list.html'
    object_list = StudentInfo.objects.all()
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(StudentList, self).get_context_data(**kwargs)
        page = self.kwargs.get(self.page_kwarg) or self.request.GET.get(self.page_kwarg) or 1
        try:
            self.page_number = int(page)
        except ValueError:
            self.page_number = 1    # 重定向
        finally:
            page_range = context['paginator'].get_elided_page_range(number=self.page_number, on_each_side=2)
            context['page_range'] = page_range  # 添加额外的键值对，传到模板中
        return context
