import random

from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from comment.forms import CommentForm
from courses import models, filters, mixins, forms


class CourseListView(
    mixins.CourseSearchMixin, mixins.CourseFilterMixin, generic.ListView
):
    paginate_by = 25
    queryset = models.Subject
    context_object_name = "object_course_list"
    template_name = "courses/course_list.html"

    def get_queryset(self):
        return models.Subject.objects.get_courses_published()[0:10]

    def head(self, *args, **kwargs):
        last_course = self.get_queryset().latest("created_at")
        response = HttpResponse(
            headers={
                "Last-Modified": last_course.created_at.strftime(
                    "%a, %d %b %Y %H:%M:%S GMT"
                )
            },
        )
        return response

    def get_context_data(self, **kwargs):
        filter = filters.CourseFilter(self.request.GET, queryset=self.get_queryset())
        kwargs["object_course_list"] = filter.qs
        return super(CourseListView, self).get_context_data(**kwargs)


course_list_view = CourseListView.as_view(
    extra_context={"page_title": "tous les cours"}
)


class CourseDetailView(generic.DetailView, generic.FormView):
    slug_field = "slug"
    slug_url_kwarg = "slug"
    model = models.Subject
    context_object_name = "course"
    template_name = "courses/course_detail.html"
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)

        button_context = ""
        button_text_enrolled = ""
        user = self.request.user
        course = get_object_or_404(self.model, slug=self.object.slug)

        if self.request.user.is_authenticated and user.type == "STUDENT":
            if "comment_form" not in context:
                context["comment_form"] = self.form_class(self.request)

        if self.request.user.is_authenticated:
            button_context = "you dont enrolled this course"
            button_text_enrolled = "disableClick"
        elif self.request.user.is_authenticated and user.type == "TEACHER":
            button_context = "you dont enrolled this course"
            button_text_enrolled = "disableClick"
        else:
            button_context = "Enroll the course"
            button_text_enrolled = button_text_enrolled

        context["similar_courses"] = sorted(
            self.model.objects.get_category_related(instance=course)[0:25],
            key=lambda x: random.random(),
        )

        context["checkout_form"] = forms.CheckoutCourseForm(
            initial={"course": self.object}
        )

        context["button_context"] = button_context
        context["button_text_enrolled"] = button_text_enrolled
        context["page_title"] = f"{self.object.title}"
        return context

    def get_success_url(self):
        self.object = self.get_object()
        return self.object.get_absolute_url()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class()

        if form.is_valid():
            print("comment form is returned")
            return self.form_valid(form)

    def form_valid(self, form):
        self.object = self.get_object()
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.course = self.object
        comment.course_id = self.object.id
        comment.save()
        return HttpResponseRedirect(self.get_success_url())


course_detail_view = CourseDetailView.as_view()


class LessonDetailView(generic.DetailView):
    model = models.Course
    context_object_name = "course"
    template_name = "courses/course_resume.html"

    def get_context_data(self, **kwargs):
        obj = self.get_object()

        subject = models.Subject.objects.get_courses_published().values("pk")
        courses = self.model.objects.filter(subject__pk__in=subject)
        course = courses.values("pk")
        lessons = models.CourseChapter.objects.filter(course__pk__in=course)

        kwargs["subject"] = subject
        kwargs["courses"] = courses
        kwargs["lessons"] = lessons
        kwargs["page_title"] = f"{obj.title}"
        return super(LessonDetailView, self).get_context_data(**kwargs)


lesson_detail_view = LessonDetailView.as_view()
