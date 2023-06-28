from django import forms

from courses.models import Subject


class CheckoutCourseForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Subject.objects.all(), widget=forms.HiddenInput
    )
