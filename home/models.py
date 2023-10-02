from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    
    def __str__(self):
        return f"{self.id}- {self.user}, {self.slug}"
