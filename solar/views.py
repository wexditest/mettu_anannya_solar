from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EnquiryForm
def home(request):
    return render(request, "solar/home.html", {"form": EnquiryForm()})
def contact(request):
    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Our team will contact you shortly.")
        else:
            messages.error(request, "Please check the form and try again.")
    return redirect("home")
