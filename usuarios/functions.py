from django.db import models, connection
from .models import VIEW_USUARIOS_GRUPO

def deletaVendedor(self, vend_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM usuarios_vendedor WHERE id = %s", [vend_id])
    return True

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
