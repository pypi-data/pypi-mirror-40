from django.db import models
from django.utils.text import slugify

from . import utils


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, db_index=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField()
    image = models.ImageField(upload_to=utils.photo_upload_to)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @classmethod
    def get_last_post(cls):
        try:
            last_post = Post.objects.all()[0]
        except IndexError:
            last_post = None

        return last_post


class PostPhoto(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=utils.post_photo_upload_to)
    title = models.CharField(
        max_length=255,
        help_text="This text will be used for the img alt attribute and for the image caption",
        blank=True,
        null=True,
    )
    order = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = (
            '-featured',
            'order',
            '-updated',
        )
        index_together = [
            ['featured', 'order', 'updated'],
        ]

    def __str__(self):
        if self.title:
            return self.title
        return super().__str__()
