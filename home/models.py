from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    # Note:
    # related_name is for backward relation.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
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
    
    # using in index.html for getting url. it is better than hard coded urls and 
    # good for when we want change many urls.
    def get_absulute_url(self):
        return reverse('home:post_detail', args=(self.id, self.slug))
    
    
    def like_count(self):
        return self.pvotes.count()
    
    
    def user_can_like(self, user):
        likes = user.uvotes.filter(post=self)
        if likes.exists():
            return False
        return True


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pcomments')
    # reply field pointes to this/Comment model. we can use Comment instead of self.
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='rcomments', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.user} - {self.body[:30]}'

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uvotes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pvotes')
    
    def __str__(self) -> str:
        return f'{self.user} liked {self.post.slug}'
