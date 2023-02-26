from django.db import models

from starwars.settings import COLLECTIONS_DIR


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class UserCollection(BaseModel):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    filepath = models.FileField(upload_to=COLLECTIONS_DIR)

    def __str__(self):
        return f"{self.name}: {self.created_at}"
