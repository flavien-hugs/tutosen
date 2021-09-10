# accounts.views.students.py

from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from accounts.models import Student
from accounts.mixins import GetStudent
from courses import models, mixins, forms


class StudentDashboardDetailView(GetStudent, generic.DetailView):

    model = Student
    login_url = reverse_lazy('account_login')
    template_name = 'dashboard/student/student_dashboard.html'

    def get_context_data(self, **kwargs):
        kwargs['courses_list'] = models.Subject.objects.get_courses_published().filter(
            instructor=self.request.user)[0:5]
        return super(StudentDashboardDetailView, self).get_context_data(**kwargs)


student_detail_view = StudentDashboardDetailView.as_view(
    extra_context={'page_title': 'tableau de bord'}
)


class StudentEnrolledCourseView(generic.edit.FormView):
    course = None
    success_message = "You join course successfully !"
    form_class = forms.CheckoutCourseForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user.id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'checkout:checkout_course',
            kwargs={'slug': str(self.course.slug)}
        )


student_enrolled_course_view = StudentEnrolledCourseView.as_view()


class StudentEnrolledCheckoutView(generic.DetailView):
    model = models.Subject
    context_object_name = 'courses_list'
    template_name = 'courses/course_checkout.html'


student_checkout_view = StudentEnrolledCheckoutView.as_view()

		

class StudentCourseDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Subject
    context_object_name = 'courses_list'
    template_name = 'dashboard/student/student_dashboard.html'

    def get_queryset(self):
        queryset = super(StudentCourseDetailView, self).get_queryset()
        return queryset.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super(StudentCourseDetailView, self).get_context_data(**kwargs)
        course = self.get_object()
        if 'course_id' in self.kwargs:
            context['course'] = course.get(id=self.kwargs['course_id'])
        else:
            context['course'] = course
        return context


student_course_detail_view = StudentCourseDetailView.as_view()
