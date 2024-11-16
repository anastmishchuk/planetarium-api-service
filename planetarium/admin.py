from django.contrib import admin

from .models import (
    AstronomyShow,
    ShowTheme,
    PlanetariumDome,
    ShowSession
)


admin.site.register(AstronomyShow)
admin.site.register(ShowTheme)
admin.site.register(PlanetariumDome)
admin.site.register(ShowSession)
