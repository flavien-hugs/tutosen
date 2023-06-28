# courses.views.course.py

from django.views import View
from django.views import generic
from django.urls import reverse
from django.shortcuts import render
from django.contrib.messages import views
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from comment import models, forms
from courses.models import Subject


class FeedbackListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 10
    model = models.Subject
    context_object_name = "course_list"
    template_name = "dashboard/courses/feedback/feedback_list.html"


feedback_list_view = FeedbackListView.as_view(
    extra_context={"page_title": "feedback for courses"}
)


class FeedbackDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Subject
    context_object_name = "comment"
    template_name = "dashboard/courses/feedback/feedback_detail.html"

    def get_context_data(self, **kwargs):
        kwargs["form"] = forms.CommentForm(instance=self.get_object())
        kwargs["page_title"] = f"Comment for '{self.object.title}'"
        return super(FeedbackDetailView, self).get_context_data(**kwargs)


feedback_detail_view = FeedbackDetailView.as_view()


def feedback_detail(
    request, link, slug, template="dashboard/courses/feedback/feedback_detail.html"
):

    course = get_object_or_404(Subject, instructor__link=link, slug=slug)

    # list of active parent comments
    feedbacks = course.get_comments().filter(parent__isnull=True)

    if request.method == "POST":
        # comment has been added
        form = forms.CommentForm(data=request.POST or None)

        if form.is_valid():
            parent_obj = None

            # get parent comment id from hidden input
            try:
                # id integer e.g. 15
                parent_id = int(request.POST.get("parent_id"))
            except:
                parent_id = None

            # if parent_id has been submitted get parent_obj id
            if parent_id:
                parent_obj = models.Comment.objects.get(id=parent_id)

                # if parent object exist
                if parent_obj:
                    # create replay comment object

                    replay_comment = form.save(commit=False)

                    # assign parent_obj to replay comment
                    replay_comment.parent = parent_obj
                    replay_comment.author = request.user

            # normal comment
            # create comment object but do not save to database
            new_comment = form.save(commit=False)

            # assign ship to the comment
            new_comment.course = course
            new_comment.author = request.user

            # save
            new_comment.save()
            return HttpResponseRedirect(course.get_comment_detail_url())
    else:
        form = forms.CommentForm()

    page_title = f"Comment for '{course.title}'"
    context = {
        "form": form,
        "comment": course,
        "feedbacks": feedbacks,
        "page_title": page_title,
    }

    return render(request, template, context)
