# courses.filters.py

from django import forms

from courses.models import Subject

import django_filters
from distutils.util import strtobool


class CourseFilterPrice(django_filters.FilterSet):
    price = django_filters.NumberFilter()

    class Meta:
        model = Subject
        fields = ["price"]


class CourseFilter(django_filters.FilterSet):

    category = django_filters.ChoiceFilter(
        label="catégories de cours",
        choices=Subject.SUBJECT_CATEGORY,
        widget=forms.RadioSelect(
            attrs={
                "class": "custom-control-input",
            }
        ),
    )

    language = django_filters.ChoiceFilter(
        label="langues",
        choices=Subject.LANGUAGE_CHOICES,
        widget=forms.RadioSelect(
            attrs={
                "class": "custom-control-input",
            }
        ),
    )

    level = django_filters.ChoiceFilter(
        label="niveau d'étude",
        choices=Subject.SUBJECT_LEVEL,
        widget=forms.RadioSelect(
            attrs={
                "class": "custom-control-input",
            }
        ),
    )

    class Meta:
        model = Subject
        fields = ["category", "language", "level"]
