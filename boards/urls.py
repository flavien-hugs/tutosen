# boards.urls.py

from django.views import generic
from django.urls import path, include
from django.views.decorators.http import require_POST

from blog import views as blog_views
from accounts.views import teachers, students
from boards.views import subject, course, chapter, feedback


urlpatterns = [
    # me/u/0/<link>/boards/
    path(
        "u/<link>/dashboard/",
        include(
            (
                [
                    # teacher url dashboard
                    path(
                        route="t/",
                        view=teachers.teacher_detail_view,
                        name="teacher_detail",
                    ),
                    path(
                        route="t/settings/",
                        view=teachers.teacher_update_view,
                        name="teacher_update",
                    ),
                    path(
                        route="t/boards/delete/",
                        view=teachers.teacher_delete_view,
                        name="teacher_delete",
                    ),
                    # student url dashboard
                    path(
                        route="s/",
                        view=students.student_detail_view,
                        name="student_detail",
                    ),
                    path(
                        route="privacy-policy/",
                        view=generic.TemplateView.as_view(
                            template_name="dashboard/teacher/partials/_partial_profile_privacy.html",
                            extra_context={"page_title": "confidentialité du profil"},
                        ),
                        name="teacher_profil_privacy_url",
                    ),
                    path(
                        route="notifications/",
                        view=generic.TemplateView.as_view(
                            template_name="dashboard/teacher/partials/_partial_notification.html",
                            extra_context={"page_title": "notifications"},
                        ),
                        name="teacher_notification_url",
                    ),
                ],
                "boards",
            ),
            namespace="boards",
        ),
    ),
    # /me/u/0/<link>/dashboard/t/subjects/
    path(
        "u/0/<link>/dashboard/t/subjects/",
        include(
            (
                [
                    path(
                        route="",
                        view=subject.subject_list_view,
                        name="list_subject_url",
                    ),
                    path(
                        route="create/",
                        view=subject.subject_create_view,
                        name="create_subject_url",
                    ),
                    path(
                        route="<slug>/update/",
                        view=subject.subject_update_view,
                        name="update_subject_url",
                    ),
                    path(
                        route="<slug>/delete/",
                        view=subject.subject_delete_view,
                        name="delete_subject_url",
                    ),
                ],
                "boards",
            ),
            namespace="subject",
        ),
    ),
    # /me/u/0/<link>/dashboard/t/course/feedback/
    path(
        "u/0/<link>/dashboard/t/course/feedback/",
        include(
            (
                [
                    path(
                        route="",
                        view=feedback.feedback_list_view,
                        name="list_feedback_url",
                    ),
                    path(
                        route="<slug>/",
                        view=feedback.feedback_detail,
                        name="detail_feedback_url",
                    ),
                ],
                "boards",
            ),
            namespace="feedback",
        ),
    ),
    # /me/u/0/<link>/dashboard/t/blog/
    path(
        "u/0/<link>/dashboard/t/blog/",
        include(
            (
                [
                    path(route="", view=blog_views.post_list_view, name="post_url"),
                    path(
                        route="add/",
                        view=blog_views.post_create_view,
                        name="create_post_url",
                    ),
                    path(
                        route="<slug>/update/",
                        view=blog_views.post_update_view,
                        name="update_post_url",
                    ),
                    path(
                        route="<slug>/delete/",
                        view=blog_views.post_delete_view,
                        name="delete_post_url",
                    ),
                ],
                "boards",
            ),
            namespace="blogs",
        ),
    ),
    # /me/u/0/<link>/dashboard/t/subject/<slug>/
    path(
        "u/0/<link>/dashboard/t/subject/<slug>/",
        include(
            (
                [
                    path(
                        route="chapiters/",
                        view=course.course_list_view,
                        name="list_course_url",
                    ),
                    path(
                        route="chapiter/create/",
                        view=course.course_create_view,
                        name="create_course_url",
                    ),
                    path(
                        route="chapiter/<pk>/update/",
                        view=course.course_update_view,
                        name="update_course_url",
                    ),
                    path(
                        route="chapiter/<pk>/delete/",
                        view=course.course_delete_view,
                        name="delete_course_url",
                    ),
                ],
                "boards",
            ),
            namespace="course",
        ),
    ),
    # /me/u/0/<link>/dashboard/t/subject/<slug>/chapiter/<pk>/
    path(
        "u/0/<link>/dashboard/t/subject/<slug>/chapiter/<pk>/",
        include(
            (
                [
                    path(
                        "lessons/", chapter.chapter_list_view, name="chapter_list_url"
                    ),
                    path(
                        route="lesson/create/",
                        view=chapter.chapter_create_view,
                        name="chapter_create_url",
                    ),
                    path(
                        route="lesson/<lesson_pk>/update/",
                        view=chapter.chapter_update_view,
                        name="chapter_update_url",
                    ),
                ],
                "boards",
            ),
            namespace="course_chapter",
        ),
    ),
]
