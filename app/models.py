from io import BytesIO

from django.core.files import File
from django.db import models
from django_extensions.db.fields import AutoSlugField
from PIL import Image


def compress(image):
    """Function to compress images"""
    im = Image.open(image)
    # create a BytesIO object
    im_io = BytesIO()
    # save image to BytesIO object
    # im = im.resize([500,500])
    im = im.convert("RGB")
    im = im.save(im_io, "JPEG", quality=25)
    # create a django-friendly Files object
    new_image = File(im_io, name=image.name)
    return new_image


class Website(models.Model):
    # Define fields for the model
    name = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to="media/website_icons/",
        null=True,
        blank=True,
    )
    url = models.URLField(
        null=True,
        blank=True,
    )
    slug = AutoSlugField(
        null=True, editable=True, default=None, unique=True, populate_from="name"
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image:
            if self.image.size > (300 * 1024):
                # call the compress function
                new_image = compress(self.image)
                # set self.image to new_image
                self.image = new_image
        super().save(*args, **kwargs)

    class Meta:
        app_label = "app"


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ImageField(
        upload_to="media/category_icons/",
        null=True,
        blank=True,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    slug = AutoSlugField(
        null=True, editable=True, default=None, unique=True, populate_from="name"
    )
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        app_label = "app"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category)
    websites = models.ManyToManyField(Website)
    image = models.ImageField(
        upload_to="media/product_pictures/",
        null=True,
        blank=True,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)

    slug = AutoSlugField(
        null=True, editable=True, default=None, unique=True, populate_from="name"
    )
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.image:
            if self.image.size > (300 * 1024):
                # call the compress function
                new_image = compress(self.image)
                # set self.image to new_image
                self.image = new_image

        if not self.meta_title:
            self.meta_title = self.name
        if not self.meta_description:
            self.meta_description = self.description
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "app"


class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.price)

    class Meta:
        app_label = "app"
