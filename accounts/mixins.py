# accounts.mixins.py

from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class GetUserObject(object):

    def get_object(self):

        current_user = CustomUser.objects.get(
            first_name=self.request.user.first_name,
            uuid=self.request.user.uuid
        )

        current_user.last_accessed = timezone.now()
        current_user.save()

        return current_user
