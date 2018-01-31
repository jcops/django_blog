## 环境说明
- python 3.5
- django 1.11
- xadmin
- sqlit3
- bootstrap


![预览图:](http://images.cnblogs.com/cnblogs_com/guigujun/1143402/o_tel.png)
## 如何使用：
- 在vps上安装前置环境：pip install -r requirement.txt
- clone master下的分支 git clone https://github.com/1049759078/django_blog.git
- 生成数据库文件: 首先：python manage.py makemigrations 其次：python manage.py migrate
- 生成管理员账号：python manage.py createsuperuser
- 生成搜索缓存：python manage.py rebulid_index
- 配置uwgsi.ini文件
- 配置niginx文件
- 让项目跑起来：uwsgi uwsgi
## 自定义blog内容：
- bolg的模板放在根目录的templates/
- 修改templates/base.html 就能粗略的自定义bolg的样式
- 其他细节请自行定制和修改
## 实现功能
- day01 创建blog项目，并设置好中文与时区
- day02 编写blog 应用的的主要url逻辑，django的xadmin后台套用与扩展
- day03 编写首页模板,数据库的model,主要有三个类 post(文章主体)、category(分类) 以及tag(标签)
- day04 套用网页模板blackandwhite 编写分类 归档 最近更新 界面

- day05 增加文章目录的侧边栏 增加粗略的搜索页面
- day06 使用autocjs 生成动态侧边栏。修改首页logo,增加文章内容的排版css，对中文有更好的支持
- day07 增加了漂亮的分页显示 自动生成文章摘要 使用來必力第三方评论 增加粒子碰撞背景
- day08 用haystack实现全文搜索与关键字高亮 ，重新排版template文件夹
- day09 bolg基本开发完成，整理开发日志，写出使用说明