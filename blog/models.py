from django.db import models
from django.utils import timezone
from django.utils.html import format_html, strip_tags
from django.utils.text import slugify

from ckeditor_uploader.fields import RichTextUploadingField

from extentions.utils import jalali_converot


class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان دسته بندی')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='آدرس دسته بندی')
    status = models.BooleanField(default=True, verbose_name='آیا نمایش داده شود؟')
    position = models.IntegerField(verbose_name='پوزیشن')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='children', default=None, blank=True,
                               null=True, verbose_name='زیر دسته')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ['parent__id', 'position']

    def __str__(self):
        return self.title


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'پیش نویس'),
        ('p', 'منتشر شده'),
    )
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(max_length=100, allow_unicode=True, blank=True, unique=True, verbose_name='آدرس صفحه')
    category = models.ManyToManyField(Category, verbose_name='دسته بندی', related_name='articles')
    description = RichTextUploadingField(verbose_name='محتوا')
    image = models.ImageField(upload_to='blog', verbose_name='عکس اصلی')
    publish = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='وضعیت')

    meta_title = models.CharField('عنوان متا', help_text='اختیاری', max_length=125, blank=True)
    meta_description = models.TextField('توضیحات متا', help_text='اختیاری', max_length=258, blank=True)

    def __str__(self):
        return self.title

    def jpublish(self):
        return jalali_converot(self.publish)

    jpublish.short_description = 'زمان انتشار'

    def category_published(self):
        return self.category.filter(status=True)

    def thumbnail_tag(self):
        return format_html(
            '<img style="max-width:100px;border-radius: 5px;" height="75px" src="%s"/>' % self.image.url)

    thumbnail_tag.short_description = 'عکس'

    def category_to_str(self):
        return ', '.join([category.title for category in self.category.filter(status=True)])

    category_to_str.short_description = 'دسته بندی'

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ['-publish']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        if not self.meta_title:
            self.meta_title = self.title
        if not self.meta_description:
            self.meta_description = f'{strip_tags(self.description)[:254]} ...'

        super(Article, self).save(*args, **kwargs)
