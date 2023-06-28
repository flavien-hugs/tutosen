# courses.forms.py

from django import forms
from django.forms.models import formset_factory, inlineformset_factory

from courses import models

from django_summernote.widgets import SummernoteWidget


class SubjectForm(forms.ModelForm):
    class Meta:
        model = models.Subject
        fields = [
            "language",
            "title",
            "subtitle",
            "price",
            "sale_price",
            "category",
            "level",
            "description",
            "resume",
            "image",
            "free",
            "published",
        ]

        widgets = {"description": SummernoteWidget(), "resume": SummernoteWidget()}

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control shadow-none"
            self.fields["free"].widget.attrs["class"] = "custom-control-input"
            self.fields["published"].widget.attrs["class"] = "custom-control-input"


class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ["title", "description"]

        widgets = {"description": SummernoteWidget()}

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control shadow-none"


CourseFormSet = inlineformset_factory(
    models.Subject,
    models.Course,
    form=CourseForm,
    fk_name="subject",
    extra=1,
    can_delete=False,
)


class LessonForm(forms.ModelForm):
    class Meta:
        model = models.CourseChapter
        fields = ["title", "chapter_desc", "movie", "document", "access"]
        localized_fields = ("created_at",)
        widgets = {"chapter_desc": SummernoteWidget()}

    def __init__(self, *args, **kwargs):
        super(LessonForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control shadow-none"
            self.fields["access"].widget.attrs["class"] = "custom-control-label"


LessonFormSet = inlineformset_factory(
    models.Course,
    models.CourseChapter,
    form=LessonForm,
    extra=1,
    fk_name="course",
    can_delete=False,
)
