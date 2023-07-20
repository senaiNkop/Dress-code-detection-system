import numpy as np
import pandas as pd
from datetime import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User


SEX_CHOICES = (
    (0, 'Male'),
    (1, 'Female'),
    (2, 'Others')
)

CATEGORY_CHOICES = (
    (0, 'Proper Dress code'),
    (1, 'Rag Jeans (Improper Dress code)'),
    (2, 'Short Trousers (Improper Dress code)'),
    (3, 'Singlets (Improper Dress code)'),
    (4, 'Dreadlocks (Improper Dress code)'),
    (5, 'Mini skirt (Improper Dress code)'),
    (6, 'Bum Short (Improper Dress code)'),
    (7, 'Revealing Clothes (Improper Dress code)'),
    (8, 'Very Tight Clothes (Improper Dress code)')
)


class DataModelManager(models.Manager):
    @staticmethod
    def convert_data_to_dataframe(values):
        df = pd.DataFrame(data=values, columns=['datetime', 'no_of_images'])
        df['datetime'] = pd.DatetimeIndex(df['datetime'])

        df['week'] = [date.isocalendar().week for date in df['datetime']]

        unique_week = np.unique(df['week'])
        no_of_images_per_unique_week = []

        for week in unique_week:
            images_per_week = df[df['week'] == week]['no_of_images'].sum()
            no_of_images_per_unique_week.append(images_per_week)

        return unique_week, no_of_images_per_unique_week

    def get_user_total_weekly(self, username):
        values = self.get_queryset().filter(username=username).values_list('date_added', 'no_of_images')

        if not values:
            now = datetime.now().isocalendar().week
            return [now], [0]

        unique_week, no_of_images_per_unique_week = self.convert_data_to_dataframe(values)
        return unique_week, no_of_images_per_unique_week

    def get_category_daily(self, username, category):
        if category == 'proper':
            values = self.get_queryset().filter(category="Proper Dress code", username=username)
        else:
            values = self.get_queryset().exclude(category="Proper Dress code").filter(username=username)

        if not values:
            now = datetime.now().isocalendar().week
            return [now], [0]

        values = values.values_list('date_added', 'no_of_images')

        unique_week, no_of_images_per_unique_week = self.convert_data_to_dataframe(values)
        return unique_week, no_of_images_per_unique_week

    def get_sex_count(self, username, sex):
        values = self.get_queryset().filter(sex=sex, username=username).values_list('no_of_images', flat=True)

        return sum(values)

    def get_category_count(self, username, category='proper'):
        if category == 'proper':
            values = self.get_queryset().filter(category='Proper Dress code', username=username).values_list('no_of_images', flat=True)
        else:
            values = self.get_queryset().exclude(category='Proper Dress code').filter(username=username).values_list('no_of_images', flat=True)

        return sum(values)

    def get_sex_and_category_count(self, username, sex, category):
        if category == 'proper':
            values = self.get_queryset().filter(sex=sex, username=username, category='Proper Dress code').values_list('no_of_images', flat=True)
        else:
            values = self.get_queryset().exclude(category='Proper Dress code').filter(sex=sex, username=username).values_list('no_of_images', flat=True)

        return sum(values)


# Create your models here.
class DataModel(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, to_field='username')
    sex = models.CharField(max_length=10)
    category = models.CharField(max_length=255)
    date_added = models.DateTimeField(default=timezone.now)

    images = models.TextField()
    no_of_images = models.IntegerField()

    objects = models.Manager()
    custom_manager = DataModelManager()

    def __str__(self):
        return f"{self.username} -- {self.sex} -- {self.category} == {self.no_of_images}"


