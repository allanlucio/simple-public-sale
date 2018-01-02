import uuid

from django.db import models

# Create your models here.

class GrupoEvento(models.Model):
    nome = models.TextField(max_length=30)
    id = models.UUIDField(primary_key= True, default=uuid.uuid4(),editable=False)
    online = models.BooleanField(default=False)

    def __str__(self):
        return self.nome