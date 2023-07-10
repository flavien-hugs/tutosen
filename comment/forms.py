# comment.forms.py

from django import forms

from comment.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        """
        Save the request with the form so it
        can be accessed in clean_*()
        """
        super(CommentForm, self).__init__(*args, **kwargs)

        self.request = kwargs.pop('request', None)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control shadow-none'
            # if self.fields['rate']:
            #     self.fields['rate'].widget.attrs['class'] = 'custom-select mb-2'