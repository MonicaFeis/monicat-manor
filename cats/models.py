from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Matches the data-value attributes in cat_form.html palette
COAT_COLOR_CHOICES = [
    ('deep_blue', 'Deep Blue'),
    ('periwinkle', 'Periwinkle'),
    ('dusty_violet', 'Dusty Violet'),
    ('mint', 'Mint'),
    ('rose', 'Rose'),
    ('honey', 'Honey'),
    ('ink_brown', 'Ink Brown'),
    ('classic', 'Classic Black'),
]


class Cat(models.Model):
    """A single cat portrait created by a user."""

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='cats'
    )
    name = models.CharField(max_length=50)
    personality = models.TextField(max_length=300)
    coat_color = models.CharField(
        max_length=20, choices=COAT_COLOR_CHOICES, default='deep_blue'
    )
    drawing_image = models.ImageField(upload_to='cats/')
    is_public = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.name} (by {self.owner.username})"


class Comment(models.Model):
    """A comment left on a public cat."""

    cat = models.ForeignKey(
        Cat, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    body = models.TextField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.cat.name}"


class Reaction(models.Model):
    """A lightweight 'paw'/like on a cat. One per user per cat, permanent."""

    cat = models.ForeignKey(
        Cat, on_delete=models.CASCADE, related_name='reactions'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reactions'
    )
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cat', 'user')

    def __str__(self):
        return f"{self.user.username} reacted to {self.cat.name}"


class DailyPet(models.Model):
    """A daily 'pet' on a cat - resets every day, powers the Cat of the Day
    spotlight and gives users a reason to return."""

    cat = models.ForeignKey(
        Cat, on_delete=models.CASCADE, related_name='pets'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='daily_pets'
    )
    date = models.DateField(default=timezone.localdate)

    class Meta:
        unique_together = ('cat', 'user', 'date')

    def __str__(self):
        return f"{self.user.username} petted {self.cat.name} on {self.date}"