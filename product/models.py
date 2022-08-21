from django.db import models
from django.utils import timezone
from PIL import Image
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name = models.CharField('نام', max_length=250)
    slug = models.SlugField(max_length=125, allow_unicode=True, verbose_name='آدرس')
    status = models.BooleanField('آیا نمایش داده شود؟', default=True)
    position = models.PositiveSmallIntegerField('جایگاه', unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', default=None, blank=True,
                               null=True, verbose_name='زیر دسته')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ['parent__id', 'position']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('نام', max_length=125)
    slug = models.SlugField(max_length=125, allow_unicode=True, verbose_name='آدرس')
    category = models.ManyToManyField(Category, related_name='products', verbose_name='دسته بندی')
    description = RichTextUploadingField(verbose_name='توضیحات')
    publish = models.DateTimeField(default=timezone.now, verbose_name='تاریخ انتشار')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField('آیا نمایش داده شود؟', default=True)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ['-publish']

    def __str__(self):
        return self.name


class Photo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photos', verbose_name='محصول')
    photo = models.ImageField(upload_to='products/%Y/%m', verbose_name='تصویر')
    alt = models.CharField('توضیح', max_length=100)

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 601 or img.width > 701:
            img.thumbnail((600, 700))
        img.save(self.photo.path, quality=70, optimize=True)
