from django.db import models
from django.contrib.sites.models import Site




class SiteConfig(models.Model):
    #OneToOneFieldはSITE　ID一つにたいしてConfigを一つ以上持つのは有り得ないとの意味
    site = models.OneToOneField(Site, verbose_name='Site', on_delete=models.PROTECT)
    meta_title = models.CharField('meta_title', max_length=100)
    meta_description = models.CharField('meta_description', max_length=300)
    meta_keywords = models.CharField('SEOキーワード', max_length=300)
    author = models.CharField('管理者', max_length=30)
    top_title = models.CharField('TOPページタイトル',max_length=100)
    top_subtitle = models.CharField('TOPサブページタイトル', max_length=200)
    
    def __str__(self):
        return self.meta_title