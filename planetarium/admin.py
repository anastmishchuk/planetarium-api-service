from django.contrib import admin

from .models import (
    AstronomyShow,
    ShowTheme,
    PlanetariumDome,
    ShowSession,
    Reservation,
    Ticket
)


class TicketInLine(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    inlines = (TicketInLine,)


admin.site.register(ShowTheme)
admin.site.register(PlanetariumDome)
admin.site.register(AstronomyShow)
admin.site.register(ShowSession)
