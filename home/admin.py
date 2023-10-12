from django.contrib import admin
from .models import Post, Comment, Vote

# Method 1
#Customizing the page of Post model in django admin.
class PostAdmin(admin.ModelAdmin):
    # These fields will be shown instaed of __str__() method of Post model.
    list_display = ('user', 'slug', 'updated')
    search_fields = ('slug', 'body')
    # the filter that is on the right side of the page.
    list_filter = ('updated',)
    # with prepopulated_fields django will fill slug field base on body field, starts from
    # first, maximum length is 50 charachters. Just works one time in admin panel not
    # any where else.
    prepopulated_fields = {'slug':('body',)}
    # for user field we can select users base on its id when adding a post in admin page.
    # It is good for when the number of users are a lot.
    raw_id_fields = ('user',)

admin.site.register(Post, PostAdmin)


#Method 2
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'body', 'created', 'is_reply',)
    raw_id_fields = ('user', 'post', 'reply',)


admin.site.register(Vote)