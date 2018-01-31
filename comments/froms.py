'''
使用django的表单功能，需要先导入forms模块，django的表单类必须继承自forms.Form或者forms.ModelForm类
当你的form有一个与之对应的数据库模型，那么使用modelform会更加简单。
'''


# from django import  forms
from django.forms import ModelForm,Textarea,TextInput

from .models import Comment

class CommentForm(ModelForm):
    class Meta:
        # 表明这里整个表单所对应的数据库模型是Comment类
        model = Comment
        # 这里指定了表单需要显示的字段，这里我们制定了name email url text需要显示
        fields = ['name','email','url','text']
        widgets = {'text': Textarea(attrs={'cols':"40", 'rows':"10",'id':"id_text"})}
