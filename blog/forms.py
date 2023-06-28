# blog.forms.py

from django import forms
from blog.models import Post
from django.contrib.admin import widgets

from django_summernote.widgets import SummernoteWidget


class CreatePostForm(forms.ModelForm):
    body = forms.CharField(label="Description", widget=SummernoteWidget())

    class Meta:
        model = Post
        fields = ["title", "subtitle", "body", "tags", "image", "published"]

    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update(
                {"class": "form-control shadow-none"}
            )
            self.fields["tags"].widget.attrs.update({"class": ""})
            self.fields["published"].widget.attrs.update(
                {"class": "custom-control-input shadow-none"}
            )
