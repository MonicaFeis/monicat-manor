from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User


COAT_COLOR_CHOICES = [
    ('cream', 'Cream'),
    ('terracotta', 'Terracotta'),
    ('rust', 'Rust'),
    ('sage', 'Sage'),
    ('honey', 'Honey'),
    ('dusty_rose', 'Dusty Rose'),
    ('ink_brown', 'Ink Brown'),
    ('classic', 'Black & White'),
]


class Cat(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cats')
    name = models.CharField(max_length=50)
    personality = models.TextField(max_length=300)
    coat_color = models.CharField(max_length=20, choices=COAT_COLOR_CHOICES, default='cream')
    drawing_image = models.ImageField(upload_to='cats/')
    is_public = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.name} (by {self.owner.username})"


class Comment(models.Model):
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.cat.name}"


class Reaction(models.Model):
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reactions')
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cat', 'user')

    def __str__(self):
        return f"{self.user.username} reacted to {self.cat.name}"