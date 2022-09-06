from django.db import models


class BaseManager(models.Manager):
    def active(self):
        return self.filter(status=True)


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')
