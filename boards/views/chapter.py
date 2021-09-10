# courses.views.module.py

from django.urls import reverse
from django.views import generic
from django.db import transaction
from django.contrib.messages import views

from boards import forms
from courses import models
from accounts import mixins


class ChapterListView(generic.DetailView):
    paginate_by = 20
    model = models.Course
    context_object_name = 'lesson'
    template_name = 'dashboard/courses/manage/chapter/chapter_list.html'

    def get_queryset(self):
        course_lesson = self.model.objects.filter(
            subject__instructor=self.request.user
        )
        return course_lesson

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'chapiter "{self.object.title}" lessons'
        context['empty_subject_label'] = "Adding new lessons"
        context['empty_subject_content'] =  "Ce chapitre n'a aucune leçon"
        return context


chapter_list_view = ChapterListView.as_view()


class ChapterCreateView(views.SuccessMessageMixin, generic.CreateView):  
    
    model = models.Course
    form_class = forms.LessonFormSet
    success_message = "Lesson successfully created !"
    template_name = 'dashboard/courses/manage/chapter/chapter_form.html'

    def get_context_data(self, **kwargs):
        context = super(ChapterCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = self.form_class(
                self.request.POST, self.request.FILES,
                instance=self.get_object()
            )
        else:
            context['formset'] = self.form_class()
        context['lesson'] = self.get_object()
        context['page_title'] = f'Add new lesson this chapiter "{self.get_object()}"'
        return context

    def form_valid(self, formset):
        formset = self.form_class(
            self.request.POST, self.request.FILES,
            instance=self.get_object()
        )
        with transaction.atomic():
            formset.instance.instructor = self.request.user
            if formset.is_valid():
                formset.instance = self.get_object()
                formset.save()
        return super(ChapterCreateView, self).form_valid(formset)

    def get_success_url(self):
        obj = self.get_object()
        return reverse(
            'course_chapter:chapter_list_url',
            kwargs={
                'username': str(obj.subject.instructor.get_first_name()),
                'slug': str(obj.subject.slug),
                'pk': str(obj.id)
            }
        )


chapter_create_view = ChapterCreateView.as_view()


class ChapterUpdateView(views.SuccessMessageMixin, generic.UpdateView):
    model = models.Course
    form_class = forms.LessonFormSet
    success_message = "Lesson successfully updated !"
    template_name = 'dashboard/courses/manage/chapter/chapter_form.html'

    def form_valid(self, formset):
        formset = self.form_class(
            self.request.POST, self.request.FILES,
            instance=self.get_object()
        )
        with transaction.atomic():
            formset.instance.instructor = self.request.user
            self.object = formset.save()
            if formset.is_valid():
                formset.instance = self.get_object()
                formset.save()
        return super(ChapterUpdateView, self).form_valid(formset)

    def get_context_data(self, **kwargs):
        context = super(ChapterUpdateView, self).get_context_data(**kwargs)
        obj = self.get_object()
        context['lesson'] = obj
        context['formset'] = self.form_class(instance=obj)
        context['page_title'] = f'Update chapiter "{obj}" lessons'
        return context

    def get_success_url(self):
        obj = self.get_object()
        return reverse(
            'course_chapter:chapter_list_url',
            kwargs={
                'username': str(obj.subject.instructor.get_first_name()),
                'slug': str(obj.subject.slug),
                'pk': str(obj.id)
            }
        )


chapter_update_view = ChapterUpdateView.as_view()
