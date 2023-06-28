# courses.urls.py

from django.views import generic
from django.urls import path, include

from accounts.views import students
from courses.views import search, course


urlpatterns = [
    # course/
    path(
        "",
        include(
            (
                [
                    path(route="search/", view=search.search_view, name="search"),
                    path(route="", view=course.course_list_view, name="course_list"),
                    path(
                        route="detail/<slug>/",
                        view=course.course_detail_view,
                        name="course_detail",
                    ),
                ],
                "courses",
            ),
            namespace="courses",
        ),
    ),
    # course/<slug>/lessons/
    path(
        "<slug>/lesson/",
        include(
            (
                [
                    path(
                        route="<chapiter_slug>~<pk>",
                        view=course.lesson_detail_view,
                        name="chapiter_detail",
                    ),
                    path(
                        route="<chapiter_slug>~<pk>~<lesson_slug>/",
                        view=course.lesson_detail_view,
                        name="chapiter_lesson_detail",
                    ),
                ],
                "courses",
            ),
            namespace="lessons",
        ),
    ),
    # course/checkout/<slug>.<uuid>/
    path(
        "checkout/",
        include(
            (
                [
                    path(
                        route="<slug>/",
                        view=students.student_checkout_view,
                        name="checkout_course",
                    ),
                ],
                "courses",
            ),
            namespace="checkout",
        ),
    ),
    # course/<slug>/joinus/
    path(
        "joinus/",
        include(
            (
                [
                    path(
                        route="",
                        view=students.student_enrolled_course_view,
                        name="student_enrolled_course",
                    ),
                    path(
                        route="<slug>.<uuid>/",
                        view=students.student_course_detail_view,
                        name="student_course_detail",
                    ),
                ],
                "courses",
            ),
            namespace="student_enrolled",
        ),
    ),
]
