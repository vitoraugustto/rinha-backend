from django import forms
from django.contrib import admin
from django.db import models

from .models import (
    Arena,
    Match,
    MatchResult,
    Round,
)


class ArenaAdmin(admin.ModelAdmin):
    list_display = ("location", "description")
    search_fields = ("location", "description")

    formfield_overrides = {
        models.TextField: {
            "widget": forms.Textarea(
                attrs={"class": "vTextField", "rows": 5, "style": "resize: none;"}
            )
        },
    }

    fieldsets = (("ARENA INFORMATION", {"fields": ("location", "description")}),)


class RoundInline(admin.TabularInline):
    model = Round
    fields = ("winner", "description")
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class MatchAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "arena",
        "get_fighters",
        "max_number_of_rounds",
        "created_at",
    )
    list_filter = ("arena", "created_at")
    autocomplete_fields = ("fighters",)
    inlines = [RoundInline]

    fieldsets = (("MATCH INFORMATION", {"fields": ("title", "arena", "fighters")}),)

    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return []
        return super().get_inline_instances(request, obj)

    def get_fighters(self, obj):
        return ", ".join([str(fighter) for fighter in obj.fighters.all()])

    get_fighters.short_description = "Fighters"


class RoundAdmin(admin.ModelAdmin):
    list_display = ("match", "round_number", "winner", "description")
    list_filter = ("match__arena", "winner")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    fieldsets = (
        (
            "ROUND INFORMATION",
            {"fields": ("match", "round_number", "winner", "description")},
        ),
    )


class MatchResultAdmin(admin.ModelAdmin):
    list_display = ("match", "outcome", "winner")
    list_filter = ("outcome", "winner")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    fieldsets = (
        (
            "MATCH RESULT INFORMATION",
            {"fields": ("match", "outcome", "winner", "description")},
        ),
    )


admin.site.register(Arena, ArenaAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Round, RoundAdmin)
admin.site.register(MatchResult, MatchResultAdmin)
