from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from planetarium.models import (
    AstronomyShow,
    ShowTheme
)
from planetarium.serializers import (
    AstronomyShowListSerializer,
    AstronomyShowDetailSerializer
)


ASTRONOMY_SHOW_URL = reverse("planetarium:astronomyshow-list")


def detail_url(astronomy_show_id):
    return reverse("planetarium:astronomyshow-detail", args=(astronomy_show_id,))


def sample_astronomy_show(**params) -> AstronomyShow:
    default_astronomy_show = {
        "title": "The Big Bang",
        "description": "An astronomy show about the beginning of space.",
    }
    default_astronomy_show.update(params)
    return AstronomyShow.objects.create(**default_astronomy_show)


class UnauthenticatedAstronomyShowApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(ASTRONOMY_SHOW_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAstronomyShowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test_user@example.com", password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_astronomy_shows_list(self):
        sample_astronomy_show()

        astronomy_show_with_show_themes = sample_astronomy_show()
        show_theme_1 = ShowTheme.objects.create(name="Planets and their features")
        show_theme_2 = ShowTheme.objects.create(name="Life in space")
        astronomy_show_with_show_themes.show_themes.add(show_theme_1, show_theme_2)

        res = self.client.get(ASTRONOMY_SHOW_URL)
        astronomy_shows = AstronomyShow.objects.all()
        serializer = AstronomyShowListSerializer(astronomy_shows, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_astronomy_shows_by_show_themes(self):
        astronomy_show_without_show_themes = sample_astronomy_show()
        astronomy_show_with_show_theme_1 = sample_astronomy_show(title="Show 1")
        astronomy_show_with_show_theme_2 = sample_astronomy_show(title="Show 2")

        show_theme_1 = ShowTheme.objects.create(name="Planets and their features")
        show_theme_2 = ShowTheme.objects.create(name="Life in space")

        astronomy_show_with_show_theme_1.show_themes.add(show_theme_1)
        astronomy_show_with_show_theme_2.show_themes.add(show_theme_2)

        res = self.client.get(
            ASTRONOMY_SHOW_URL,
            {"show_themes": f"{show_theme_1.id},{show_theme_2.id}"}
        )

        serializer_without_show_themes = AstronomyShowListSerializer(astronomy_show_without_show_themes)
        serializer_astronomy_show_show_theme_1 = AstronomyShowListSerializer(astronomy_show_with_show_theme_1)
        serializer_astronomy_show_show_theme_2 = AstronomyShowListSerializer(astronomy_show_with_show_theme_2)

        self.assertIn(serializer_astronomy_show_show_theme_1.data, res.data)
        self.assertIn(serializer_astronomy_show_show_theme_2.data, res.data)
        self.assertNotIn(serializer_without_show_themes.data, res.data)

    def test_retrieve_astronomy_show_detail(self):
        astronomy_show = sample_astronomy_show()
        astronomy_show.show_themes.add(ShowTheme.objects.create(name="Space missions"))

        url = detail_url(astronomy_show.id)

        res = self.client.get(url)

        serializer = AstronomyShowDetailSerializer(astronomy_show)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_astronomy_show_forbidden(self):
        payload = {
            "title": "Spacecraft adventures",
            "description": "Journeys to the edge of the Solar System (Voyagers, New Horizons).",
        }

        res = self.client.post(ASTRONOMY_SHOW_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminAstronomyShowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test_admin@example.com", password="testpassword", is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_astronomy_show(self):
        payload = {
            "title": "Spacecraft adventures",
            "description": "Journeys to the edge of the Solar System (Voyagers, New Horizons).",
        }

        res = self.client.post(ASTRONOMY_SHOW_URL, payload)

        astronomy_show = AstronomyShow.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        for key in payload:
            self.assertEqual(payload[key], getattr(astronomy_show, key))

    def test_create_astronomy_show_with_show_themes(self):
        show_theme_1 = ShowTheme.objects.create(name="Planets and their features")
        show_theme_2 = ShowTheme.objects.create(name="Life in space")

        payload = {
            "title": "Spacecraft adventures",
            "description": "Journeys to the edge of the Solar System (Voyagers, New Horizons).",
            "show_themes": [show_theme_1.id, show_theme_2.id],
        }

        res = self.client.post(ASTRONOMY_SHOW_URL, payload)

        astronomy_show = AstronomyShow.objects.get(id=res.data["id"])
        show_themes = astronomy_show.show_themes.all()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn(show_theme_1, show_themes)
        self.assertIn(show_theme_2, show_themes)
        self.assertEqual(show_themes.count(), 2)

    def test_delete_astronomy_show_allowed(self):
        astronomy_show = sample_astronomy_show()
        url = detail_url(astronomy_show.id)

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
