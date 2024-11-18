from rest_framework import viewsets


from planetarium.models import (
    ShowTheme,
    PlanetariumDome,
    AstronomyShow,
    ShowSession,
    Reservation
)
from planetarium.serializers import (
    ShowThemeSerializer,
    PlanetariumDomeSerializer,
    AstronomyShowSerializer,
    AstronomyShowListSerializer,
    AstronomyShowRetrieveSerializer,
    ShowSessionSerializer,
    ShowSessionListSerializer,
    ShowSessionRetrieveSerializer,
    ReservationSerializer,
)


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.prefetch_related("show_themes")
    serializer_class = AstronomyShowSerializer

    @staticmethod
    def _params_to_ints(query_string):
        return [int(str_id) for str_id in query_string.split(",")]

    def get_queryset(self):
        queryset = self.queryset
        title = self.request.query_params.get("title")
        show_themes = self.request.query_params.get("show_themes")

        if title:
            queryset = queryset.filter(title__icontains=title)
        if show_themes:
            show_themes = self._params_to_ints(show_themes)
            queryset = queryset.filter(show_themes__id__in=show_themes)
        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return AstronomyShowListSerializer
        if self.action == "retrieve":
            return AstronomyShowRetrieveSerializer
        return AstronomyShowSerializer


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all().select_related(
        "astronomy_show", "planetarium_dome"
    )
    serializer_class = ShowSessionSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            return queryset.select_related("astronomy_show", "planetarium_dome")
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ShowSessionListSerializer
        if self.action == "retrieve":
            return ShowSessionRetrieveSerializer
        return ShowSessionSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
