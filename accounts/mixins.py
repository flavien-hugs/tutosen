# accounts.mixins.py

from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse

CustomUser = get_user_model()


class GetUserObject:

    def get_object(self):

        current_user = CustomUser.objects.get(
            first_name=self.request.user.first_name,
            uuid=self.request.user.uuid
        )
        current_user.last_accessed = timezone.now()
        current_user.save()

        return current_user

    def get_queryset(self):
        current_user = CustomUser.objects.filter(uuid=self.request.uuid)
        return current_user

    @property
    def success_message(self):
        return NotImplemented

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class InstructorSearchMixin:
    
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        q = self.request.GET.get('q', None)
        if q:
            lookups = (
                Q(statut__icontains=q)|
                Q(brief_desc__icontains=q)|
                Q(country__icontains=q)|
                Q(state__icontains=q)
            )
            resultat = queryset.filter(lookups).distinct()
            return resultat
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', None)
        if query:
            context['page_title'] = 'Recherche pour "{0}"'.format(query)
        return context


class AjaxResponseMixin:
    def post(self, request, **kwargs):
        if request.is_ajax() and request.method == "POST":
            form = self.form_class(data=request.POST, instance=request.user)
            if form.is_valid():
                self.object = form.save()
                message = self.success_message
                return JsonResponse({"success": True, "message": message})
            else:
                return JsonResponse({"error": form.errors})
        return HttpResponse("success submit !")
