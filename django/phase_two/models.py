from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.conf import settings

class Item(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='items', default='')    
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = ArrayField(models.CharField(max_length=100), blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.categories = [cat.strip().upper() for cat in self.categories]
        super(Item, self).save(*args, **kwargs)

    
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments', default='')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    rating = models.CharField(max_length=255, default='')
    comment = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(default=timezone.now)