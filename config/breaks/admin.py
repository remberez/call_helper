from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from .models.organisation import Organisation
from .models.group import Group
from .models.replacement import Replacement, ReplacementEmployee
from .models.status import ReplacementStatus, BreakStatus
from .models.breaks import Break

ADMIN_HTML_LINK_FORMAT = '<a href="{}">{}</a>'


# Inlines
class ReplacementEmployeeInline(admin.TabularInline):
    model = ReplacementEmployee
    fields = ('employee', 'status')


# Models
@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'director_link')
    search_fields = ('name',)
    list_display_links = ('pk', 'name')

    def director_link(self, obj):
        link = reverse(
            'admin:auth_user_change', args=[obj.pk]
        )
        return format_html(ADMIN_HTML_LINK_FORMAT, link, obj.director)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'organisation', 'manager', 'min_active', 'employees_count')
    list_display_links = ('pk', 'name')
    search_fields = ('name', )

    def employees_count(self, obj):
        return obj.employees_count

    employees_count.short_description = 'Количество сотрудников'

    def get_queryset(self, request):
        return Group.objects.annotate(
            employees_count=Count('employees')
        )


@admin.register(Replacement)
class ReplacementAdmin(admin.ModelAdmin):
    list_display = ('pk', 'group', 'date')
    inlines = (
        ReplacementEmployeeInline,
    )
    autocomplete_fields = ('group', )


@admin.register(ReplacementStatus)
class ReplacementStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_active', 'sort')


@admin.register(BreakStatus)
class BreakStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_active', 'sort')


@admin.register(Break)
class BreakAdmin(admin.ModelAdmin):
    list_display = ('pk', 'replacement_link', 'employee_link', 'break_start', 'break_end', 'status')
    list_filter = ('status', )

    def replacement_link(self, obj):
        link = reverse(
            'admin:breaks_replacement_change', args=[obj.pk]
        )
        return format_html(ADMIN_HTML_LINK_FORMAT, link, obj.replacement)

    def employee_link(self, obj):
        link = reverse(
            'admin:auth_user_change', args=[obj.pk]
        )
        return format_html(ADMIN_HTML_LINK_FORMAT, link, obj.employee)
