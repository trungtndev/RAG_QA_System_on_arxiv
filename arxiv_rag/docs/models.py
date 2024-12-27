from django.conf import settings
from django.db import models
import uuid

class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    file_path = models.FileField(upload_to=settings.MEDIA_DIR / "documents", blank=False)

    def __str__(self):
        return self.title