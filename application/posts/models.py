from django.db import models
from application.account.models import User


class SomePosts(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    post = models.TextField()
    image = models.ImageField(upload_to='', null=True, blank=True)
    public_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Post'


class Saved(models.Model):
    user = models.ForeignKey(User, related_name='saved_p', on_delete=models.CASCADE)
    post = models.ForeignKey(SomePosts, related_name='saved', on_delete=models.CASCADE)
    saved = models.BooleanField(default=False)

    def __str__(self):
        return self.saved