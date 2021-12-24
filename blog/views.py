# blog.views.py

from django.urls import reverse
from django.views import generic
from django.core import serializers
from django.contrib.messages import views
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_list_or_404
from django.views.decorators.clickjacking import xframe_options_exempt

from blog import models, forms, mixins
from pages.forms import NewslettersForm


class BlogPostListView(generic.ListView):
    paginate_by = 14
    queryset = models.Post.objects.filter(published=True)
    context_object_name = "post_list"
    template_name = "blog/blog_post_list.html"


blog_post_list_view = BlogPostListView.as_view(
    extra_context={"page_title": "blog"}
)


def ajax_post_view(request):
    dataset = get_list_or_404(models.Post, published=True)
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, content_type='application/json', safe=False)


ajax_post_view = ajax_post_view


class PostDetailView(generic.DetailView):
    model = models.Post
    context_object_name = "post"
    template_name = "blog/blog_post_detail.html"

    def get_context_data(self, **kwargs):
        kwargs['form'] = NewslettersForm()
        kwargs['page_title'] = f"{self.object.title}"
        return super().get_context_data(**kwargs)


blog_post_detail_view = PostDetailView.as_view()


def blog_tag(request, tag):
    posts = models.Post.objects.filter(tags__contains=tag).published()
    context = {"tag": tag, "posts": posts}
    return render(request, "blog/blog_post_tags.html", context)


class TeacherPostListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 10
    model = models.Post
    form_class = forms.CreatePostForm
    template_name = "dashboard/blog/post_list.html"

    def get_queryset(self):
        post = self.model.objects.filter(
            author=self.request.user
        )[:11]
        return post


post_list_view = TeacherPostListView.as_view(
    extra_context={"page_title": "your blog"}
)


@method_decorator(xframe_options_exempt, name='dispatch')
class TeacherPostCreateView(
    views.SuccessMessageMixin,
    mixins.PostEditMixin, generic.CreateView
):  
    success_message = "Post successfully created !"
    template_name = "dashboard/blog/post_create.html"


post_create_view = TeacherPostCreateView.as_view(
    extra_context={"page_title": "create new post"}
)


@method_decorator(xframe_options_exempt, name='dispatch')
class TeacherPostUpdateiew(
    views.SuccessMessageMixin,
    mixins.PostEditMixin, generic.UpdateView
):  
    success_message = "Post successfully updated !"
    template_name = "dashboard/blog/post_create.html"

    def get_context_data(self, **kwargs):
        kwargs['page_title'] = f'Update post "{self.object.title}"'
        return super().get_context_data(**kwargs)


post_update_view = TeacherPostUpdateiew.as_view()


class TeacherPostDeleteView(
    views.SuccessMessageMixin,
    mixins.PostEditMixin, generic.DeleteView
):
    def delete(self, request, *args, **kwargs):
        return super(TeacherPostDeleteView, self).delete(request, *args, **kwargs)


post_delete_view = TeacherPostDeleteView.as_view()
