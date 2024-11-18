from rest_framework import serializers

from planetarium.models import (
    ShowTheme,
    PlanetariumDome,
    AstronomyShow,
    ShowSession,
    Ticket, Reservation
)


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ("id", "name")


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ("id", "name", "rows", "seats_in_row", "capacity")


class AstronomyShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "show_theme")


class AstronomyShowListSerializer(AstronomyShowSerializer):
    show_themes = serializers.SlugRelatedField(
            many=True,
            read_only=True,
            slug_field="name"
    )


class AstronomyShowRetrieveSerializer(AstronomyShowSerializer):
    show_themes = ShowThemeSerializer(many=True, read_only=True)


class ShowSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowSession
        fields = "__all__"


class ShowSessionListSerializer(ShowSessionSerializer):
    astronomy_show_title = serializers.CharField(
        source="astronomy_show.title"
    )
    planetarium_dome_name = serializers.CharField(
        source="planetarium_dome.name"
    )
    planetarium_dome_capacity = serializers.IntegerField(
        source="planetarium_dome.capacity"
    )

    class Meta:
        model = ShowSession
        fields = (
            "id",
            "show_time",
            "astronomy_show_title",
            "planetarium_dome_name",
            "planetarium_dome_capacity"
        )


class ShowSessionRetrieveSerializer(ShowSessionSerializer):
    astronomy_show = AstronomyShowListSerializer(many=False, read_only=True)
    planetarium_dome = PlanetariumDomeSerializer(many=False, read_only=True)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "show_session")


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Reservation
        fields = ("id", "tickets", "created_at")
