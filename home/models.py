from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    slug = models.SlugField()
    # Note:
    # <auto_now_add> will only save date and time when the record is created and
    # <auto_now> will save date and time each time the record changes.
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        # For every where that we want use ordering.
        ordering = ['-created']
    
    
    def __str__(self):
        return f"{self.id}- {self.user}, {self.slug}"
    
    def get_absulute_url(self):
        return reverse('home:post_detail', args=(self.id, self.slug))
