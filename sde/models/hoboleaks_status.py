from django.db import models


class HoboleaksStatus(models.Model):
    deprecated = models.BooleanField()
    stale = models.BooleanField()
    revision = models.IntegerField()
    import_date = models.DateTimeField(auto_now_add=True)
    file = models.TextField()
    md5 = models.TextField()

    def __str__(self):
        return f"{self.file}"
