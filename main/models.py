from os import path, remove
from pathlib import Path
from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.conf import settings

from imagekitio import ImageKit

# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to='images', null=True)
    url = models.CharField(max_length=1000, null=True)

    def __repr__(self) -> str:
        return 'Image({0})'.format(str(self.image))

    def __str__(self) -> str:
        return str(self.image)

    def image_to_show(self):
        return mark_safe('<img src="{}" width="100" />'.format(self.url))
    image_to_show.short_description = 'Image to show'
    image_to_show.allow_tags = True

    def save(self, *args, **kwargs) -> None:
        img_uploaded = False
        if kwargs.get('img_uploaded') is not None:
            del kwargs['img_uploaded']
            img_uploaded = True
        super().save(*args, **kwargs)
        if not img_uploaded:
            imagekit = ImageKit(
                settings.IMAGEKIT_PUBLIC_KEY,
                settings.IMAGEKIT_PRIVATE_KEY,
                settings.IMAGEKIT_URL_ENDPOINT
            )
            img_path = path.join(Path(path.abspath(__file__)).parent.parent.absolute(), self.image.path)
            with open(img_path, 'rb') as img:
                response = imagekit.upload_file(
                    file=img,
                    file_name=str(self),
                    options= {
                        "folder" : "/django-shop/",
                        "is_private_file": False,
                        "use_unique_file_name": True
                    }
                )
                self.url = response['response']['url']
                self.save(img_uploaded=True)
            remove(img_path)


class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def __repr__(self) -> str:
        return 'Category({0})'.format(self.name)
    
    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True, blank=True)
    description = models.TextField()
    price = models.FloatField()
    amount = models.IntegerField(default=0)
    images = models.ManyToManyField(Image, null=True, blank=True)

    def __repr__(self) -> str:
        return 'Product({0})'.format(self.name)
    
    def __str__(self) -> str:
        return self.name


class Response(models.Model):
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def short_text(self):
        return self.text if len(self.text) <= 30 else self.text[:27] + "..."

    def __repr__(self) -> str:
        return 'Response({0})'.format(self.short_text())
    
    def __str__(self) -> str:
        return self.short_text()
