# courses.forms.py

from django import forms
from django.forms.models import inlineformset_factory

from courses.models import Course, CourseChapter


class CourseChapterForm(forms.ModelForm):
    
    class Meta:
        model = CourseChapter
        exclude = ()


course_chapter_formset = inlineformset_factory(
    Course, CourseChapter, form=CourseChapterForm,
    fields=['chapter_title', 'chapter_order', 'chapter_desc'],
    extra=1, field_classes='form-control', can_delete=True
)
