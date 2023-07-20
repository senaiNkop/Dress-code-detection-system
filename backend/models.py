from django.db import models


# Create your models here.
class Backend(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(null=False)
    thumbnail = models.CharField(max_length=500, null=True, blank=True)

    category = models.CharField(max_length=20, editable=False, default='Backend')

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return self.url
