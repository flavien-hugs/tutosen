# blog.mixins.py

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from blog import models, forms


class PostMixin(LoginRequiredMixin, object):
    def get_queryset(self):
        queryset = super(PostMixin, self).get_queryset()
        return queryset.filter(author=self.request.user)


class PostEditMixin(PostMixin):
    model = models.Post
    form_class = forms.CreatePostForm

    def get_success_url(self):
        author = self.request.user
        return reverse("blogs:post_url", args=[author.link])

    def form_valid(self, form, *args, **kwargs):
        author = self.request.user
        post = form.save(commit=False)
        image = form.cleaned_data['image']
        post.author = author
        post.image = image
        post.save()
        return super().form_valid(form)
