# courses.views.search.py

from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import ListView

from courses.models import Subject
from courses.mixins import CourseSearchMixin


class SearchView(CourseSearchMixin, ListView):
    model = Subject
    paginate_by = 80
    context_object_name = "object_course_list"
    template_name = 'courses/course_list.html'
    success_url = reverse_lazy('courses:search')

    def head(self, *args, **kwargs):
        last_course = self.get_queryset().latest('created_at')
        response = HttpResponse(
            headers={
                'Last-Modified': last_course.created_at.strftime('%a, %d %b %Y %H:%M:%S GMT')
            },
        )
        return response


search_view = SearchView.as_view()
