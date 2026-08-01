"""
Modelos Django — {{PROJECT_NAME}}

Todos os modelos do projeto ficam neste arquivo com app_label = "persistence".
"""
from django.db import models


class EventoAuditoria(models.Model):
    """
    Log de auditoria append-only. Nunca modificar ou deletar registros existentes.
    Invariante: save() com pk existente e delete() levantam ValidationError.
    """
    tipo = models.CharField(max_length=80)
    criado_em = models.DateTimeField(auto_now_add=True)
    criado_por = models.CharField(max_length=150, null=True, blank=True)
    payload = models.JSONField(default=dict, blank=True)

    class Meta:
        app_label = "persistence"
        ordering = ["-criado_em"]
        verbose_name = "Evento de Auditoria"
        verbose_name_plural = "Eventos de Auditoria"

    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise Exception("EventoAuditoria é append-only: modificações são proibidas.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise Exception("EventoAuditoria é append-only: exclusões são proibidas.")
