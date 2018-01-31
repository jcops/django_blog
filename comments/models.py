from django.db import models


from django.utils.six import python_2_unicode_compatible
# Create your models here.


@python_2_unicode_compatible
class Comment(models.Model):
    name = models.CharField(max_length=100,verbose_name='用户名称')
    email = models.EmailField(max_length=255,verbose_name='邮箱')
    url = models.URLField(blank=True,verbose_name='个人网址')
    text = models.TextField(verbose_name='评论内容')
    # 我们给评论创建一个自动的时间
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='评论时间')

    # 与post数据库相连接，这里是多对一的关系 用ForeignKey连接到Post类 、
    # 即一个comment只能在一篇post里有，但是一个post里可以有很多comment
    post =models.ForeignKey('blog.Post')


    def __str__(self):
        return self.text[:20]

    class Meta:
        ordering=['-created_time']

