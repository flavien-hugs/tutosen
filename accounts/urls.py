# accounts.urls.py

from django.urls import path, include

from accounts.views import teachers


urlpatterns = [
    path(
        "",
        include(
            (
                [
                    path(
                        route="find/instructor/",
                        view=teachers.teacher_list_view,
                        name="teacher_list_view",
                    ),
                    path(
                        route="instructor/p/<link>/",
                        view=teachers.teacher_profile_detail_view,
                        name="teacher_detail_view",
                    ),
                    path(
                        route="instructor/p/<link>/course/",
                        view=teachers.teacher_course_view,
                        name="teacher_course_url",
                    ),
                    path(
                        route="instructor/p/<link>/blog/",
                        view=teachers.teacher_blog_view,
                        name="teacher_blog_url",
                    ),
                    path(
                        route="check_validate_data",
                        view=teachers.check_validate_data,
                        name="check_validate_data",
                    ),
                ],
                "accounts",
            ),
            namespace="accounts",
        ),
    ),
]
