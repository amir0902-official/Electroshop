from django.db import models
from django.utils import timezone
from django.utils.text import slugify
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField('نام', max_length=125)
    slug = models.SlugField(max_length=125, allow_unicode=True, blank=True, verbose_name='آدرس')
    category = models.ManyToManyField(Category, related_name='products', verbose_name='دسته بندی')
    description = RichTextUploadingField(verbose_name='توضیحات')
    publish = models.DateTimeField(default=timezone.now, verbose_name='تاریخ انتشار')
    price = models.PositiveBigIntegerField('قیمت', help_text='به تومان وارد کنید.')
    quantity = models.PositiveIntegerField('موجودی')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.BooleanField('آیا نمایش داده شود؟', default=True)

    meta_title = models.CharField('عنوان متا', max_length=125, blank=True)
    meta_description = models.TextField('توضیحات متا', max_length=125, blank=True)

    related_products = models.ManyToManyField(
        "self", verbose_name='محصولات مرتبط', blank=True,
        default=None, symmetrical=False, related_name="related_products_list")

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ['-publish']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.meta_title:
            self.meta_title = self.name
        if not self.meta_description:
            self.meta_description = self.description

        super(Product, self).save(*args, **kwargs)


class Photo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photos', verbose_name='محصول')
    photo = models.ImageField(upload_to='products/%Y/%m', verbose_name='تصویر')
    alt = models.CharField('توضیح', max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'

    def __str__(self):
        return f"{self.product.name} - {self.photo.name}"

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 601 or img.width > 701:
            img.thumbnail((600, 700))
        img.save(self.photo.path, quality=70, optimize=True)


class Data(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='data', verbose_name='محصول')
    key = models.CharField(verbose_name='نام داده', max_length=50)
    value = models.CharField(verbose_name='مقدار', max_length=50)

    class Meta:
        verbose_name = 'داده'
        verbose_name_plural = 'اطلاعات'
