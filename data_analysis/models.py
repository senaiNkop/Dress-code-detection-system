from django.db import models
from django.shortcuts import reverse
from django.utils import timezone

# Create your models here.


class DataAnalysis(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique_for_date='published_date')

    published_date = models.DateField(default=timezone.now)
    tools_used = models.CharField(max_length=1000)
    description = models.TextField(blank=True, null=True)

    download_link = models.URLField(blank=True, null=True)
    thumbnail = models.CharField(max_length=500, null=True, blank=True)

    category = models.CharField(max_length=20, default='Data Science', editable=False)

    def __str__(self):
        return f"{self.title} on {self.published_date}"

    class Meta:
        ordering = ('-published_date', )
        verbose_name_plural = 'Data Analysis'

    def get_absolute_url(self):
        return reverse('data-analysis', args=[self.slug])
