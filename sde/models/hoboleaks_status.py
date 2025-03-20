from django.db import models


class HoboleaksStatus(models.Model):
    file = models.TextField()
    deprecated = models.BooleanField()
    stale = models.BooleanField()
    md5 = models.TextField()
    revision = models.IntegerField()
    import_date = models.DateTimeField(auto_now_add=True)
