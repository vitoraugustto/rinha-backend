from django import forms
from django.contrib import admin
from django.db import models

from .models import (
    Fighter,
    Occupation,
    Trait,
)


class TraitAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

    search_fields = (
        "name",
        "description",
    )


class OccupationAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

    search_fields = (
        "name",
        "description",
    )


class FighterAdmin(admin.ModelAdmin):
    list_display = ("name", "biography", "age", "height", "weight")
    search_fields = ("name", "biography")

    autocomplete_fields = (
        "occupation",
        "traits",
    )

    fieldsets = (
        ("Identity", {"fields": ("name", "biography")}),
        ("Biological Stats", {"fields": ("age", "height", "weight")}),
        ("Profile", {"fields": ("occupation", "traits")}),
    )

    formfield_overrides = {
        models.TextField: {
            "widget": forms.Textarea(
                attrs={"class": "vTextField", "rows": 5, "style": "resize: none;"}
            )
        },
    }


admin.site.register(Trait, TraitAdmin)
admin.site.register(Fighter, FighterAdmin)
admin.site.register(Occupation, OccupationAdmin)
