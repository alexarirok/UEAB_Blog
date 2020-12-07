from django.db import models
from django.db.models.signals import pre_save
from tinymce import HTMLField
from django.urls import reverse
from django.contrib.auth import get_user_model
from markdown_deux import markdown
from django.utils.safestring import mark_safe
from .utils import get_read_time 

User = get_user_model()

class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username  
    
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()
    
    def __str__(self):
        return self.user.username
     
class Category(models.Model):
    title = models.CharField(max_length=20)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username



class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = HTMLField()
    read_time = models.IntegerField(default = 0)
    comment_count = models.IntegerField(default = 0)
    view_count = models.IntegerField(default = 0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail =models.ImageField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()
    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)
    

    def __str__(self):
        return self.title

    def get_readtime(self):
        result = get_readtime.of_text(self.content)
        return result.text
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={
            'id': self.pk
        })
    
    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)
        
    def get_update_url(self):
        return reverse('post-update', kwargs={
            'id': self.pk
        })
        
    def get_delete_url(self):
        return reverse('post-delete', kwargs={
            'id': self.pk
        })
        
    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')
    
    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()
    
    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()
    
def pre_save_post_reciever(sender, instance, *args, **kwargs):
    if instance.content:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var

pre_save.connect(pre_save_post_reciever, sender=Post)

class Signup(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email


