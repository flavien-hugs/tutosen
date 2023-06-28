# courses.mixins.py

from django.db.models import Q

from courses import filters


class CourseSearchMixin(object):
    def get_queryset(self, **kwargs):
        queryset = super(CourseSearchMixin, self).get_queryset(**kwargs)
        query = self.request.GET.get("q", None)
        if query:
            lookups = (
                Q(title__icontains=query)
                | Q(language__icontains=query)
                | Q(category__icontains=query)
                | Q(level__icontains=query)
                | Q(resume__icontains=query)
                | Q(description__icontains=query)
            )
            return queryset.filter(lookups).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        query = self.request.GET.get("q", None)
        if query:
            kwargs["page_title"] = f'Recherche pour "{query}"'
        return super(CourseSearchMixin, self).get_context_data(**kwargs)


class CourseFilterMixin(object):
    def get_context_data(self, **kwargs):

        filter_course = filters.CourseFilter(
            self.request.GET, queryset=self.get_queryset()
        )

        kwargs["filter_course"] = filter_course
        return super(CourseFilterMixin, self).get_context_data(**kwargs)
