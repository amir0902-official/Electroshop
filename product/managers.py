from django.db import models


class ProductManager(models.Manager):
    def active(self):
        return self.filter(status=True)


class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)
