from django.db import models
from django.utils import timezone
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.urls import reverse


class Post(models.Model):
    ACTIVE = 'active'
    DRAFT = 'draft'

    CHOICES_STATUS = (
        (ACTIVE, 'Active'),
        (DRAFT, 'Draft')
    )

    Ctegorychoises=(
                    ('1','home'),
                    ('2','backage'),
                    ('3','visa'),
                    ('4','tickit'),
                    ('5','hotel'),
                    ('6','insurance'),
                    ('7','docoument'),
                    ('8','shipping'),
                     )
    category = models.CharField(choices=Ctegorychoises,max_length=2,default=1,blank=False)
    image = models.ImageField(default='default.jpg',upload_to='plog', blank=False, null=False)
    title = models.CharField(max_length=255)
    intro = models.TextField()
    body =  RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=CHOICES_STATUS, default=ACTIVE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title.name

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class imagepath(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='plog', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name