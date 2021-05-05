# accounts.mixins.py

from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import get_user_model

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

    @property
    def success_message(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_message)
        return super().form_valid(form)
