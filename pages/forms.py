# pages.forms.py


from django import forms

from pages.models import Contact, Newsletters
from django_summernote.widgets import SummernoteWidget


class ContactForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Contact
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'reason',
            'message',
        ]

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control shadow-none'


class NewslettersForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Newsletters
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(NewslettersForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control shadow-none'
