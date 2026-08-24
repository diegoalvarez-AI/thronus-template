from django.contrib import admin

from persistence.models import EventoAuditoria


@admin.register(EventoAuditoria)
class EventoAuditoriaAdmin(admin.ModelAdmin):
    list_display = ("tipo", "criado_por", "criado_em")
    list_filter = ("tipo",)
    search_fields = ("tipo", "criado_por")
    readonly_fields = ("tipo", "criado_em", "criado_por", "payload")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
