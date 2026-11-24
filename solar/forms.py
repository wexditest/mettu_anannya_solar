from django import forms
from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    service = forms.ChoiceField(
        label="Service interested in (optional)",
        choices=(
            ("", "Choose a service"),
            ("Solar Power Systems - On-grid", "Solar Power Systems - On-grid"),
            ("Solar Power Systems - Off-grid", "Solar Power Systems - Off-grid"),
            ("Solar Power Systems - Hybrid", "Solar Power Systems - Hybrid"),
            ("Solar Fencing", "Solar Fencing"),
            ("Solar Water Heaters", "Solar Water Heaters"),
            ("Solar Street Lights", "Solar Street Lights"),
            ("Backup Inverters", "Backup Inverters"),
            ("Battery & Inverter Solutions", "Battery & Inverter Solutions"),
            ("Annual Maintenance (AMC)", "Annual Maintenance (AMC)"),
        ),
        required=False,
        widget=forms.Select(attrs={"autocomplete": "off"}),
    )

    class Meta:
        model = Enquiry
        fields = ["name", "phone", "email", "service", "message"]
        labels = {
            "name": "Full name",
            "phone": "Phone number",
            "email": "Email address (optional)",
            "service": "Service interested in (optional)",
            "message": "Tell us about your requirement (optional)",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"autocomplete": "name", "placeholder": "Your full name"}
            ),
            "phone": forms.TextInput(
                attrs={
                    "type": "tel",
                    "autocomplete": "tel",
                    "placeholder": "Your phone number",
                }
            ),
            "email": forms.EmailInput(
                attrs={"autocomplete": "email", "placeholder": "name@example.com"}
            ),
            "message": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Share any details that will help us assist you.",
                }
            ),
        }
