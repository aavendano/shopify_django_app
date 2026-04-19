from unittest.mock import patch

from django.test import SimpleTestCase
from django.urls import reverse

from session.models import Session
from session.views import SessionDetailView


class SessionDetailViewTests(SimpleTestCase):
    def test_detail_page_renders_session_fields(self):
        session = Session(
            id="sess-1",
            shop="demo-shop.myshopify.com",
            state="active",
            isonline=True,
            scope="read_products",
            accesstoken="abcd1234secret9876",
            accountowner=True,
        )

        with patch.object(SessionDetailView, "get_object", return_value=session):
            response = self.client.get(reverse("session:detail", kwargs={"pk": session.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "demo-shop.myshopify.com")
        self.assertContains(response, "abcd...9876")
        self.assertContains(response, "Session Detail")
