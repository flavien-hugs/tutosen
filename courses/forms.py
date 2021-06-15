# courses.forms.py

from django.forms.models import inlineformset_factory

from courses.models import Course, CourseChapter


course_chapter_formset = inlineformset_factory(
    Course, CourseChapter,
    fields=['chapter_title', 'chapter_desc'],
    extra=2, field_classes='form-control',
    error_message='Veuillez renseigner ces champs SVP !'
)
