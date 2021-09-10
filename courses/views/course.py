# courses.views.course.py

import random

from django.urls import reverse_lazy
from django.views import generic as mxs
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from courses import models, mixins, forms


class CourseListView(mixins.CourseSearchMixin, mxs.ListView):
    paginate_by = 20
    model = models.Subject
    context_object_name = "object_course_list"
    template_name = 'courses/course_list.html'

    def get_queryset(self):
        return models.Subject.objects.get_courses_published()

    def head(self, *args, **kwargs):
        last_course = self.get_queryset().latest('created_at')
        response = HttpResponse(
            headers={
                'Last-Modified': last_course.created_at.strftime('%a, %d %b %Y %H:%M:%S GMT')
            },
        )
        return response


course_list_view = CourseListView.as_view(
    extra_context={'page_title': 'tous les cours'}
)


class CourseDetailView(mxs.DetailView):
    slug_field = "slug"
    slug_url_kwarg = "slug"
    model = models.Subject
    context_object_name = 'course'
    template_name = 'courses/course_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        
        button_context = ""
        button_text_enrolled = ""
        user = self.request.user
        course = get_object_or_404(self.model, slug=self.object.slug)

        if (
            user.is_authenticated
            and context.get('course') in user.course_created.all()
        ):  
            button_context = "you dont enrolled this course"
            button_text_enrolled = "disableClick"
        elif (
            user.is_authenticated and user.type == "TEACHER"
        ):
            button_context = "you dont enrolled this course"
            button_text_enrolled = "disableClick"
        else:
            button_context = "Enroll the course"
            button_text_enrolled = button_text_enrolled

        context['similar_courses'] = sorted(
            self.model.objects.get_category_related(instance=course)[0:25],
            key=lambda x:random.random()
        )
        
        context['checkout_form'] = forms.CheckoutCourseForm(initial={'course': self.object})

        context['button_context'] = button_context
        context['button_text_enrolled'] = button_text_enrolled
        context['page_title'] = f'{self.object.title}'
        return context


course_detail_view = CourseDetailView.as_view()


class LessonDetailView(mxs.DetailView):
    model = models.Course
    context_object_name = 'course'
    template_name = 'courses/course_resume.html'

    def get_context_data(self, **kwargs):
        obj = self.get_object()

        subject = models.Subject.objects.get_courses_published().values('pk')
        courses = self.model.objects.filter(subject__pk__in=subject)
        course = courses.values('pk')
        lessons = models.CourseChapter.objects.filter(course__pk__in=course)
        
        kwargs['subject'] = subject
        kwargs['courses'] = courses
        kwargs['lessons'] = lessons
        kwargs['page_title'] = f'{obj.title}'
        return super(LessonDetailView, self).get_context_data(**kwargs)


lesson_detail_view = LessonDetailView.as_view()
