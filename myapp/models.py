from django.db import models
from django.contrib.auth.models import User
# Create your models here.




class Category(models.Model):
    name = models.CharField('カテゴリ名', max_length=50)
    name_en = models.CharField('カテゴリ名英語', max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def post_count(self):
        #下のPost　classのもの
        #category=selfは　自分自身　post_count(self)のselfの値
        n = Post.objects.filter(category = self).count()
        return n

    def __str__(self):
        return self.name



class Post(models.Model):
    #dbから削除するときこのユーザーが投稿したものがあれば保護せよ
    author = models.ForeignKey(User, on_delete=models.PROTECT, blank=False)
    title = models.CharField('タイトル', max_length=50)
    content = models.TextField('内容', max_length=1000)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    thumbnail = models.ImageField(upload_to='images/', blank=True)
    #自動的に今の時間を入れる
    created_at = models.DateTimeField(auto_now_add=True)
    #もう時間はあるので更新するだけであればauto_now
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class Like(models.Model):
    post = models.ForeignKey(Post, verbose_name="投稿", on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name="Likeしたユーザー", on_delete=models.PROTECT)