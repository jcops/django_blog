'''模板标签'''
from django import template
from ..models import Post,Category,Tag
from django.db.models.aggregates import Count

register = template.Library()

@register.simple_tag
def get_recent_posts(num=5):
    """最新文章模板标签"""
    return Post.objects.all().order_by('-create_time')[:num]


@register.simple_tag
def archives():
    """归档模板标签"""

    return Post.objects.all()


@register.simple_tag
def get_categories():
    """分类模板标签"""
    # return Category.objects.all()
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag
def get_tags():
    '''标签云'''
    return  Tag.objects.annotate(num_tag=Count('post')).filter(num_tag__gt=0)


