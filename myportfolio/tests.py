from django.test import TestCase
from unittest.mock import patch

from .models import ContactMessage


class ContactViewTests(TestCase):

    @patch("myportfolio.views.requests.post")
    def test_contact_accepts_digit_only_phone(self, mock_post):
        mock_post.return_value.status_code = 200

        response = self.client.post(
            "/contact/",
            {
                "name": "Ali",
                "phone": "919434864",
                "email": "ali@example.com",
                "message": "Salom",
            },
        )

        self.assertEqual(response.status_code, 302)
        message = ContactMessage.objects.latest("id")
        self.assertEqual(message.phone, "919434864")
        self.assertTrue(mock_post.called)
        self.assertIn("📞 Phone: 919434864", mock_post.call_args.kwargs["json"]["text"])

    @patch("myportfolio.views.requests.post")
    def test_contact_accepts_twelve_digit_phone(self, mock_post):
        mock_post.return_value.status_code = 200

        response = self.client.post(
            "/contact/",
            {
                "name": "Ali",
                "phone": "998919434864",
                "email": "ali@example.com",
                "message": "Salom",
            },
        )

        self.assertEqual(response.status_code, 302)
        message = ContactMessage.objects.latest("id")
        self.assertEqual(message.phone, "998919434864")
        self.assertTrue(mock_post.called)
        self.assertIn("📞 Phone: 998919434864", mock_post.call_args.kwargs["json"]["text"])

    @patch("myportfolio.views.requests.post")
    def test_contact_ajax_returns_json(self, mock_post):
        mock_post.return_value.status_code = 200

        response = self.client.post(
            "/contact/",
            {
                "name": "Ali",
                "phone": "919434864",
                "email": "ali@example.com",
                "message": "Salom",
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
            HTTP_ACCEPT="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertJSONEqual(
            response.content.decode(),
            {"success": True, "message": "Xabaringiz yuborildi ✅", "telegram_sent": True},
        )

    def test_contact_rejects_wrong_length_phone(self):
        response = self.client.post(
            "/contact/",
            {
                "name": "Ali",
                "phone": "12345678",
                "email": "ali@example.com",
                "message": "Salom",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertContains(response, "9 yoki 12 xonali raqam")

    def test_contact_rejects_formatted_phone(self):
        response = self.client.post(
            "/contact/",
            {
                "name": "Ali",
                "phone": "+998 91 943 48 64",
                "email": "ali@example.com",
                "message": "Salom",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertContains(response, "9 yoki 12 xonali raqam")
