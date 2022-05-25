from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from manager.models import Category, Conference, Lecture


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    fields = ('title', 'description', 'slug', 'parent', 'is_active')
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title', 'slug', 'is_active')
    list_editable = ('is_active', )
    list_display_links = ('indented_title', )


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'date', 'is_active')
    list_editable = ('is_active', )
    list_display_links = ('title', )


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active')
    list_editable = ('is_active', )
    list_display_links = ('title', )
