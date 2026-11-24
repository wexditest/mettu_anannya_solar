from django import forms
from .models import Enquiry
class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ["name","phone","email","service","message"]
        widgets = {"message": forms.Textarea(attrs={"rows":4})}
