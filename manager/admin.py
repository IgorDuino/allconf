from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from manager.models import Category, Conference, Lecture


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title', 'description')
    list_display_links = ('indented_title', )


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'date')
    list_display_links = ('title', )


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    list_display_links = ('title', )
