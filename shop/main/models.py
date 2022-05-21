from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to='images')

    def __repr__(self) -> str:
        return 'Image({0})'.format(str(self.image))

    def __str__(self) -> str:
        return str(self.image)

    def image_to_show(self):
        return mark_safe('<img src="{}" width="100" />'.format(self.image.url))
    image_to_show.short_description = 'Image to show'
    image_to_show.allow_tags = True


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
