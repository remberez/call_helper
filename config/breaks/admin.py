from django.contrib import admin
from .models.organisation import Organisation
from .models.group import Group
from .models.replacement import Replacement, ReplacementStatus, ReplacementEmployee


# Inlines
class ReplacementEmployeeInline(admin.TabularInline):
    model = ReplacementEmployee
    fields = ('employee', 'status')


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'director')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'organisation', 'manager')


@admin.register(Replacement)
class ReplacementAdmin(admin.ModelAdmin):
    list_display = ('pk', 'group', 'date')
    inlines = (
        ReplacementEmployeeInline,
    )

