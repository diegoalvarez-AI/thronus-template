import json

from django.db import OperationalError, connection
from django.http import HttpResponse


def health_view(request):
    """Endpoint de healthcheck. Retorna 200 se o banco responde, 503 caso contrário."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        payload = {"status": "ok", "db": "ok"}
        status = 200
    except OperationalError as exc:
        payload = {"status": "degraded", "db": "error", "detail": str(exc)}
        status = 503

    return HttpResponse(json.dumps(payload), content_type="application/json", status=status)
