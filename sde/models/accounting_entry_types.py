from django.db import models


class AccountingEntryType(models.Model):
    id = models.IntegerField(primary_key=True)
    name_id = models.IntegerField()
    name = models.TextField()
    name_translation = models.TextField()
    description = models.TextField()
    journal_message_id = models.IntegerField(null=True, default=None)
    message_id = models.IntegerField(null=True, default=None)
    message_translation = models.TextField(null=True, default=None)  # noqa: DJ001

    def __str__(self):
        return f"{self.name}"
