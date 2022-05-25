from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from users.models import ConferenceOrganizer, ConferenceModerator, Listener, Speaker


@admin.register(ConferenceOrganizer)
class ConferenceOrganizerAdmin(admin.ModelAdmin):
    list_display = ('user', 'conference')
    list_display_links = ('user', )


@admin.register(ConferenceModerator)
class ConferenceModeratorAdmin(admin.ModelAdmin):
    list_display = ('user', 'conference')
    list_display_links = ('user', )


@admin.register(Listener)
class ListenerAdmin(admin.ModelAdmin):
    list_display = ('user', 'conference')
    list_display_links = ('user', )


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('user', 'lecture')
    list_display_links = ('user', )
