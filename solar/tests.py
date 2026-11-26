from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

from django.http import Http404
from django.test import RequestFactory, SimpleTestCase
from django.urls import reverse

from .forms import EnquiryForm
from .services import SERVICES
from .views import contact, home, service_detail


class EnquiryFormTests(SimpleTestCase):
    def test_only_name_and_phone_are_required(self):
        form = EnquiryForm(data={"name": "A Solar Customer", "phone": "+919999999999"})

        self.assertTrue(form.is_valid(), form.errors)

    def test_service_field_accepts_listed_services_and_rejects_unknown_values(self):
        form = EnquiryForm(
            data={
                "name": "A Solar Customer",
                "phone": "+919999999999",
                "service": "Solar Fencing",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

        form = EnquiryForm(
            data={
                "name": "A Solar Customer",
                "phone": "+919999999999",
                "service": "Unlisted service",
            }
        )
        self.assertTrue(form.has_error("service", "invalid_choice"))


class ServicePageTests(SimpleTestCase):
    def test_every_service_has_a_rendering_detail_page(self):
        request_factory = RequestFactory()

        for service in SERVICES:
            with self.subTest(service=service["slug"]):
                url = reverse("service_detail", args=[service["slug"]])
                response = service_detail(request_factory.get(url), service["slug"])

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, service["title"], html=True)
                self.assertContains(response, service["main_image_alt"])

    def test_unknown_service_slug_returns_not_found(self):
        with self.assertRaises(Http404):
            service_detail(RequestFactory().get("/services/not-a-service/"), "not-a-service")


class BoardProfileTests(SimpleTestCase):
    def test_leadership_cards_render_director_photos_with_accessible_names(self):
        response = home(RequestFactory().get("/"))

        self.assertContains(response, 'alt="Komeshwar Reddy Mettu"')
        self.assertContains(response, 'src="/static/images/profile/komeshwar.jpeg"')
        self.assertContains(response, 'alt="Mettu Ashwini Reddy"')
        self.assertContains(response, 'src="/static/images/profile/ashwini.jpeg"')


class ContactWhatsAppTests(SimpleTestCase):
    @patch("solar.views.EnquiryForm")
    def test_valid_enquiry_saves_and_redirects_to_whatsapp_with_encoded_details(self, form_class):
        form = form_class.return_value
        form.is_valid.return_value = True
        form.cleaned_data = {
            "name": "Solar Customer",
            "phone": "+91 99482 24123",
            "email": "customer@example.com",
            "service": "Solar Fencing",
            "message": "Need 5 kW solar & fencing",
        }

        response = contact(
            RequestFactory().post("/contact/", {"name": "Solar Customer"})
        )

        form.save.assert_called_once_with()
        self.assertEqual(response.status_code, 302)
        location = urlsplit(response["Location"])
        self.assertEqual(location.netloc, "wa.me")
        self.assertEqual(location.path, "/919963543433")
        message = parse_qs(location.query)["text"][0]
        self.assertIn("Phone: +91 99482 24123", message)
        self.assertIn("Service: Solar Fencing", message)
        self.assertIn("Need 5 kW solar & fencing", message)
