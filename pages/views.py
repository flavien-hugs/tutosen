from django.conf import settings
from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect

from pages import models, forms


def index(request, template="pages/ps-newsletters.html"):
    if request.method == "POST":
        post_data = request.POST.copy()
        email = post_data.get("email", None)
        newsletters = models.Newsletters()
        newsletters.email = email
        newsletters.save()

        # send a confirmation mail
        subject = "NewsLetter Subscription"
        message = f"""
            Hello {email}, Thanks for subscribing us.
            You will get notification of latest articles posted on our website.
            Please do not reply on this email.
        """

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [
            email,
        ]
        send_mail(subject, message, email_from, recipient_list)
        result = JsonResponse({"msg": "Thanks. Subscribed Successfully !"})
        return result

    return render(request, template)


class ContactView(generic.View):
    form_class = forms.ContactForm
    success_url = reverse_lazy("pages:contact")
    template_name = "pages/ps-contact.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        ctx = {"form": form, "page_title": "nous-contacter"}
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "Votre message a été envoyé avec succes !"
            )
            return HttpResponseRedirect(self.success_url)

        ctx = {"form": form}
        return render(request, self.template_name, ctx)


contact_view = ContactView.as_view()


def aboutUsDetail(request, template="pages/ps-page.html"):
    about_content = get_object_or_404(models.AboutUs, pk=1)
    page_title = "qui nous-sommes ?"
    page_heading = "Vous voulez en savoir plus sur nous ?"
    context = {
        "page_title": page_title,
        "page_heading": page_heading,
        "content": about_content,
    }
    return render(request, template, context)


page_aboutus_view = aboutUsDetail


def pageCGUDetail(request, template="pages/ps-page.html"):
    cgu_content = get_object_or_404(models.PageCGU, pk=1)
    page_title = "Foire aux questions"
    page_heading = "Questions fréquemment posées"
    context = {
        "page_title": page_title,
        "page_heading": page_heading,
        "content": cgu_content,
    }
    return render(request, template, context)


page_cgu_detail = pageCGUDetail


def pageSupportetail(request, template="pages/ps-page.html"):
    support_content = get_object_or_404(models.PageSupport, pk=1)
    page_title = "Condition Générale d'Utilisation"
    page_heading = "Politique de confidentialité et données personnelles"
    context = {
        "page_title": page_title,
        "page_heading": page_heading,
        "content": support_content,
    }
    return render(request, template, context)


page_support_detail = pageSupportetail
