from django.db import models
from django.contrib.auth.models import User

class SavedNews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    summary = models.TextField()
    url = models.URLField()
    source = models.CharField(max_length=100)
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.title} - saved by {self.user.username}"
