import markdown
from django.shortcuts import render,HttpResponse,get_object_or_404
from comments.froms import CommentForm
from  django.views.generic import ListView,DetailView
from .models import Post,Category,Tag
from  django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from  django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .paginator import paginator

#类视图
# class IndexView(ListView):
#     model = Post
#     template_name = 'blog/index.html'
#     context_object_name = 'post_list'
#     #开启分页功能
#     paginate_by = 2
#
#     def get_context_data(self, **kwargs):
#         #获取父类生成的传递给模板的字典
#         context = super().get_context_data(**kwargs)
#         paginator = context.get('paginator')
#         page = context.get('page_obj')
#         is_paginated = context.get('is_paginated')
#         # pagination_data = self.pagination_data(paginator,page,is_paginated)
#         pagination_data = self.pagination_data(paginator, page, is_paginated)
#         #将分页导航条的模板变量更新到context中,返回的为字典
#         context.update(pagination_data)
#
#         #将更新后的context返回,以便ListView使用这个字典的模板变量去渲染模板
#         #此时context字典中已有了显示分页导航条所需的数据
#         return context
#
#     def pagination_data(self,paginator,page,is_paginated):
#         if not  is_paginated:
#             #如果没有分页，此时返回一个空字典
#             return {}
#         #当前页左边连续的页码号，初始值为空
#         left = []
#         #当前页码右边连续的页码号，初始值为空
#         right = []
#         #标示第一页页码后是否需要显示省略号
#         left_ha_more = False
#         #标示最后一页页码前是否需要显示省略号
#         right_has_more = False
#         #标示是否需要显示第一页的页码号
#         #初始False
#         first = False
#         #标示是否需要显示最后一页的页码号
#         # 初始False
#         last = False
#
#         #获取用户当前请求的页码号
#         page_number = page.number
#
#         #获取分页后的总页数
#         total_pages = paginator.num_pages
#
#
#         #获取整个分页页码列表，比如分了4页，那么久是[1,2,3,4]
#         page_range = paginator.page_range
#
#         if page_number == 1:
#             right = page_range[page_number:page_number +2]
#
#
#             if right[-1] < total_pages - 1:
#                 right_has_more = True
#                 print(right[-1],total_pages -1 )
#
#
#             if right[-1] < total_pages:
#                 last = True
#         elif page_number == total_pages:
#             left = page_range[(page_number -3) if (page_number -3 ) > 0 else 0:page_number -1]
#
#             if left[0] >2:
#                 left_ha_more = True
#
#             if left[0] > 1:
#                 first =True
#         else:
#             left = page_range[(page_number -3 ) if (page_number -3) >0 else 0:page_number -1 ]
#             right = page_range[page_number:page_number +2]
#
#             if right[-1] < total_pages -1:
#                 right_has_more = True
#
#             if right[-1] < total_pages:
#                 last =True
#
#             if left[0] >2:
#                 left_ha_more = True
#             if left[0] >1:
#                 first = True
#
#         data = {
#             'left':left,
#             'right':right,
#             'left_has_more':left_ha_more,
#             'righr_has_more':right_has_more,
#             'first':first,
#             'last':last,
#         }
#         return  data



#类视图
class PostDetaiIView(DetailView):
    '''文章详情'''
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post_detail'

    def get(self, request, *args, **kwargs):
        response = super(PostDetaiIView,self).get(request,*args,**kwargs)
        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()
        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post_detail = super(PostDetaiIView,self).get_object(queryset=None)
        # post_detail.body = markdown.markdown(post_detail.body,
        #                                      extensions=[
        #                                          'markdown.extensions.extra',
        #                                          'markdown.extensions.codehilite',
        #                                          'markdown.extensions.toc',
        #                                      ])
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 'markdown.extensions.toc',
            TocExtension(slugify=slugify),
        ])
        post_detail.body = md.convert(post_detail.body)
        post_detail.toc = md.toc
        return post_detail

    def get_context_data(self, **kwargs):
        context = super(PostDetaiIView,self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context


class ArchivesView(ListView):
    '''归档'''
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return super(ArchivesView,self).get_queryset().filter(create_time__year = self.kwargs.get('year'),create_time__month = self.kwargs.get('month'))


class CategoryView(ListView):
    '''分类'''
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
        return  super(CategoryView,self).get_queryset().filter(category = cate)


class TagView(ListView):
    '''标签'''
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag,pk=self.kwargs.get('pk'))
        return super(TagView,self).get_queryset().filter(tags=tag)


def search(request):
    '''搜索'''
    q = request.GET.get('q')
    error_msg= ''

    if not q:
        error_msg="请输入关键词"
        return  render(request,'blog/index.html',{'error_msg':error_msg})
    post_list = Post.objects.filter(Q(title__icontains=q)|Q(body__icontains=q))
    return render(request,'blog/index.html',{'error_msg':error_msg,
                                             'post_list':post_list})
#函数视图
# Create your views here.
# def index(request):
#     """首页"""
#
#         # 获取Book数据表中的所有记录
#     post_list = Post.objects.all()
#     print(post_list)
#     data = paginator(request,post_list,6)
#     #     # 生成paginator对象,定义每页显示10条记录
#     # paginator = Paginator(post_list, 5)
#     #     # 从前端获取当前的页码数,默认为1
#     # page = request.GET.get('page', 1)
#     #     # 把当前的页码数转换成整数类型
#     # currentPage = int(page)
#     #
#     # try:
#     #     print(page)
#     #     post_list = paginator.page(page)  # 获取当前页码的记录
#     # except PageNotAnInteger:
#     #     post_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
#     # except EmptyPage:
#     #     post_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
#
#     return render(request,'blog/index.html',data)
#     # return render(request,'blog/index.html',context={'post_list':post_list})



# def detail(request,pk):
#     """详情页"""
#     post_detail = get_object_or_404(Post,pk=pk)
#     print(post_detail.body)
#     post_detail.increase_views()
#     post_detail.body = markdown.markdown(post_detail.body,
#                                   extensions=[
#                                       'markdown.extensions.extra',
#                                       'markdown.extensions.codehilite',
#                                       'markdown.extensions.toc',
#                                   ])
#     form = CommentForm()
#     comment_list = post_detail.comment_set.all()
#     context = {
#         'post_detail': post_detail,
#         'form': form,
#         'comment_list': comment_list
#     }
#     return render(request, 'blog/detail.html', context=context)

# def archives(request,year,month):
#     post_list = Post.objects.filter(create_time__year=year,
#                                     create_time__month=month).order_by('-create_time')
#     return  render(request,'blog/index.html',context={"post_list": post_list})

# def category(request,pk):
#     """分类页面"""
#     cate = get_object_or_404(Category,pk=pk)#获取分类ID
#     post_list = Post.objects.filter(category=cate)
#     return render(request,'blog/index.html',context={"post_list":post_list})


def index(request):
    '''文章首页'''
    post_list = Post.objects.all()  #导入的Article模型
    p = Paginator(post_list,5)   #分页，10篇文章一页
    if p.num_pages <= 1:  #如果文章不足一页
        post_list = post_list  #直接返回所有文章
        data = ''  #不需要分页按钮
    else:
        page = int(request.GET.get('page',1))  #获取请求的文章页码，默认为第一页
        post_list = p.page(page) #返回指定页码的页面
        left = []  # 当前页左边连续的页码号，初始值为空
        right = []  # 当前页右边连续的页码号，初始值为空
        left_has_more = False  # 标示第 1 页页码后是否需要显示省略号
        right_has_more = False  # 标示最后一页页码前是否需要显示省略号
        first = False   # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        last = False  # 标示是否需要显示最后一页的页码号。
        total_pages = p.num_pages
        page_range = p.page_range
        if page == 1:  #如果请求第1页
            right = page_range[page:page+2]  #获取右边连续号码页
            if right[-1] < total_pages - 1:    # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
                # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
                right_has_more = True
            if right[-1] < total_pages:   # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
                # 所以需要显示最后一页的页码号，通过 last 来指示
                last = True
        elif page == total_pages:  #如果请求最后一页
            left = page_range[(page-3) if (page-3) > 0 else 0:page-1]  #获取左边连续号码页
            if left[0] > 2:
                left_has_more = True  #如果最左边的号码比2还要大，说明其与第一页之间还有其他页码，因此需要显示省略号，通过 left_has_more 来指示
            if left[0] > 1: #如果最左边的页码比1要大，则要显示第一页，否则第一页已经被包含在其中
                first = True
        else:  #如果请求的页码既不是第一页也不是最后一页
            left = page_range[(page-3) if (page-3) > 0 else 0:page-1]   #获取左边连续号码页
            right = page_range[page:page+2] #获取右边连续号码页
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        data = {    #将数据包含在data字典中
            'left':left,
            'right':right,
            'left_has_more':left_has_more,
            'right_has_more':right_has_more,
            'first':first,
            'last':last,
            'total_pages':total_pages,
            'page':page,

        }
    return render(request,'blog/index.html',context={
        'post_list':post_list,'data':data
    })