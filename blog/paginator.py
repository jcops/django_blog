from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


'''分页插件'''

def paginator(request,model_data,num1=5):
    data = {}
    # 生成paginator对象,定义每页显示10条记录
    paginator = Paginator(model_data,num1)

    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)

    # 把当前的页码数转换成整数类型
    currentPage = int(page)

    try:
        print(page)
        post_list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        post_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    data["post_list"] = post_list
    data["page"] = page
    data["request"] = request
    data["currentPage"] =currentPage
    data["paginator"] = paginator
    return  data

