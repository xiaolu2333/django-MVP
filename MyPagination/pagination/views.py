from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger

from pagination.models import SchoolInfo, StudentInfo


# Create your views here.
def school_list(request):
    contact_list = SchoolInfo.objects.all()
    paginator = Paginator(contact_list, 5)

    page_number = request.GET.get('page', None)

    try:
        page_obj = paginator.get_page(page_number)
        page_range = paginator.get_elided_page_range(number=page_number, on_each_side=2)
        context = {
            'page_obj': page_obj,
            'page_range': page_range
        }
        return render(request, 'list.html', context)
    except PageNotAnInteger as e:
        return redirect(to="/schools/?page=1", permanent=True)


def student_list(request):
    contact_list = StudentInfo.objects.all()
    paginator = Paginator(contact_list, 25)

    page_number = request.GET.get('page', None)

    try:
        page_obj = paginator.get_page(page_number)
        page_range = paginator.get_elided_page_range(number=page_number, on_each_side=2)
        context = {
            'page_obj': page_obj,
            'page_range': page_range
        }
        return render(request, 'list.html', context)
    except PageNotAnInteger as e:
        return redirect(to="/students/?page=1", permanent=True)