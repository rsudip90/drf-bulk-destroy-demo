from django.conf import settings
from django.db import models

class Note(models.Model):
    title       = models.CharField(max_length=1024, blank=True, null=True)
    body        = models.TextField(blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    owner       = models.ForeignKey(settings.AUTH_USER_MODEL,
                        null=True, editable=False, db_index=True,
                        on_delete=models.SET_NULL, related_name="note_owner")

    class Meta:
        db_table = "note"

    def __str__(self):
        return f"(pk: {self.pk}, title: {self.title})"
