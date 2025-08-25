from django import forms
from django.contrib import admin
from django.db import models

from .models import (
    Fighter,
    Trait,
)


class TraitAdmin(admin.ModelAdmin):
    list_display = ("__str__", "description")


class FighterAdmin(admin.ModelAdmin):
    list_display = ("__str__", "description", "age", "height", "weight")
    filter_horizontal = ("traits",)

    fieldsets = (
        ("Basic Information", {"fields": ("name", "description", "age")}),
        ("Attributes", {"fields": ("height", "weight")}),
        ("Traits", {"fields": ("traits",)}),
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
