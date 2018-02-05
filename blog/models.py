from django.db import models
from  django.contrib.auth.models import User
from django.utils.six import python_2_unicode_compatible
from django.urls import reverse
import  markdown
from django.utils.html import strip_tags

from ditor.models import UEditorField
# Create your models here.


@python_2_unicode_compatible
class Category(models.Model):
    """分类"""
    name = models.CharField(max_length=100,verbose_name='分类')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Tag(models.Model):
    """标签Tag"""
    name = models.CharField(max_length=100,verbose_name='标签')


    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Post(models.Model):
    """文章"""
    STATUS_CHOICES = (
        ('draft','草稿'),
        ('published','已发布'),
        )
    title = models.CharField(max_length=70,verbose_name='文章标题')
    body = UEditorField('内容', height=300, width=800,max_length=1024000000000,
                           default=u'', blank=True, imagePath="images/",
                           toolbars='besttome', filePath='files/')
    create_time = models.DateTimeField(verbose_name='文章创建时间')
    modified_time = models.DateTimeField(verbose_name='文章最后修改时间')
    excerpt = models.CharField(max_length=200,blank=True,verbose_name='文章摘要')
    category = models.ForeignKey(Category,verbose_name='分类')
    tags = models.ManyToManyField(Tag,blank=True,verbose_name='标签')
    author = models.ForeignKey(User,verbose_name='文章作者')
    views = models.PositiveIntegerField(default=0,verbose_name='阅读量')

    #统计阅读量方法
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    #重写save方法
    def save(self,*args,**kwargs):
        #如果没有填写摘要
        if not self.excerpt:
            #实例化一个markdown类,用于渲染body的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            #strip_tags去掉HTML文本的全部HTML标签
            #从文本摘取前54个字符赋给excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        #调用父类的save方法将数据保存到数据库中
        super(Post, self).save(*args,**kwargs)
    class Meta:
        ordering = ['-create_time']
        verbose_name = "文章"
        verbose_name_plural = verbose_name

