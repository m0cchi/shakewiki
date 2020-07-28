from django.db import models


class Article(models.Model):
    path = models.CharField(max_length=512)
