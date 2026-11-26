from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from django.utils.http import urlencode
from .forms import EnquiryForm
from .services import SERVICES, SERVICES_BY_SLUG

WHATSAPP_NUMBER = "919963543433"


def home(request):
    return render(
        request,
        "solar/home.html",
        {"form": EnquiryForm(), "services": SERVICES},
    )


def service_detail(request, slug):
    service = SERVICES_BY_SLUG.get(slug)
    if service is None:
        raise Http404("Service not found")
    return render(request, "solar/service_detail.html", {"service": service})


def contact(request):
    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            cleaned_data = form.cleaned_data
            message = "\n".join(
                (
                    "New enquiry from the Mettu Anannya Solar website",
                    "",
                    f"Name: {cleaned_data['name']}",
                    f"Phone: {cleaned_data['phone']}",
                    f"Email: {cleaned_data.get('email') or 'Not provided'}",
                    f"Service: {cleaned_data.get('service') or 'Not selected'}",
                    f"Message: {cleaned_data.get('message') or 'Not provided'}",
                )
            )
            whatsapp_url = (
                f"https://wa.me/{WHATSAPP_NUMBER}?"
                f"{urlencode({'text': message})}"
            )
            return redirect(whatsapp_url)
        messages.error(request, "Please check the form and try again.")
        return render(
            request,
            "solar/home.html",
            {"form": form, "services": SERVICES},
        )
    return redirect("home")
