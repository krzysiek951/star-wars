from django.db import models

from starwars.settings import COLLECTIONS_DIR


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class UserCollection(BaseModel):
    api = models.CharField(max_length=255)
    resource = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    filepath = models.FileField(upload_to=COLLECTIONS_DIR)

    def __str__(self):
        return f"{self.api} {self.resource}: {self.created_at}"
