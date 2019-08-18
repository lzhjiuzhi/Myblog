from django.db import models

# Create your models here.
from django.db import models
#导入内建的User模型
from django.contrib.auth.models import User
#timezone 时间事务
from django.utils import timezone
from django.urls import reverse
class ArticlePost (models.Model):
    # author m on_delete for canceling model
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #title
    title = models.CharField(max_length=100)
    #征文
    body = models.TextField()
    #time
    created = models.DateTimeField(default = timezone.now)
    #updated tiem
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])

    total_views = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ('-created',)
        def __str__(self):
            return self.title

