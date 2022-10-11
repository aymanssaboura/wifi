from django.db import models
from django.utils import timezone
from django.conf import settings
# from django.conf import settings

from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=2, choices=(('1','backeage'),('2','flight'),('3','transport'),('4','farry'),('5','visa'),('6','hotel'),('7','insurance'),('8','document'),('9','shipping'),), default=1  )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
