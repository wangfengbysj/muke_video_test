
<h1 align='center'>Django进阶</h1>
<p align='center'>
<img src="https://img.shields.io/badge/License-MIT-green"/><br/>
</p>
<ul>
    <li>基于Django的知识点：model层，views 层 template层，路由
    <li>模板使用mako，user系统，分页系统
    <li>celery + redis 异步队列在Django中的使用
    <li>supervisor + gunicorn + nginx 部署 Django服务
</ul>

---
## video系统服务启动说明

### 视频存储Nginx服务器

- 视频服务上传nginx目录为：`www/django_video`
- 上传服务配置

	```
	server {
        charset utf-8;
        listen 8088;
        server_name http_host2;
        root /usr/share/nginx/html/django_video/;
        autoindex on;
        add_header Cache-Control "no-cache, must-revalidate";
        location / {
            add_header Access-Control-Allow-Origin *;
        }
    }
	```
	
### Celery redis服务
### ffmpeg命令配置
### 启动celery线程服务

- 启动命令：`python manage.py celery worker -c 4 --loglevel=info`

### 单线程启动video服务
- 查询venv环境：`pyenv virtualenvs`
- 启动虚拟环境：`pyenv activate django_advanced`
- 启动django服务：`python manage.py runserver`
- 访问video服务：`http://127.0.0.1:8000/dashboard/login`

### gunicore服务配置
- 配置服务【conf.py】

```python
# coding=utf-8
import multiprocessing
bind = '127.0.0.1:8000'
workers = multiprocessing.cpu_count()*1
worker_class = 'gevent'
```
- 在video目录中：`gunicorn --config=conf.py config.wsgi:application`

### supervisor启动服务
- 启动命令：`supervisord -c /Users/wangfeng/.pyenv/versions/3.6.4/envs/django_advanced/etc/supervisord.conf`
- 查看服务：`supervisorctl`

## 环境设置

### 启动设置是UTF8环境
```python
PYTHONIOENCODING=utf-8 python manage.py runserver
PYTHONIOENCODING=utf-8 python manage.py shell
PYTHONIOENCODING=utf-8 ipython
```

### 生成requirements.txt
`pip freeze > requirements.txt`
### 导入requirements.txt
`pip intall -r requirement.txt`

### 配置目录
- templates目录在settings.py文件中设置DIRS

```python
'DIRS': [os.path.join(BASE_DIR,'templates')]
View.py中返回值
return render(request, 模版文件路径和名字, {key:value})

TEMPLATE = 'index.html'
return render(request, self.TEMPLATE, data)
```
- static目录在settings中设置

```
STATICFILES_DIRS=(os.path.join(BASE_DIR, 'static'), )
{% load static %}
{% static '文件路径/文件名'%}
```   

## 模版配置

### 1、默认模版自定义filter

- 创建过滤器，文件名templatetags\myfilter.py

	
	> from django import template

	> register = template.Library()
	
	> @register.filter()<br/>
	> def <mark>test</mark>(value,args):<br/>
	>> return value * args<br/>
	
	> def test_add(value,args):<br/>
	>> return value + args<br/>
	
- 页面加载过滤器

	`{% load myfilter %}`
- 页面使用过滤器

	> {{ count | <mark>test</mark>:10}}


### 2、jinjia2
- settings中TEMPLATES配置

	> 'BACKEND': 'django.template.backends.jinja2.Jinja2',<br/>
	>  'DIRS': [os.path.join(BASE_DIR, 'templates')],<br/>
	>  'environment': 'app.base\_jinja2.environment'<br/>

- environment加载程序

	```python
	from jinja2 import Environment
	from django.contrib.staticfiles.storage import staticfiles_storage
	from django.urls import reverse
	
	from .myfilter import test
	
	
	def environment(**options):
	    env = Environment(**options)
	    env.globals.update({
	        'static':staticfiles_storage,
	        'url':reverse
	    })
	    env.filters['test'] = test
	    return env
  	```
	  
- 自定义filter

	```python
	def test(value, args):
   	 	print('value is {0}, args is {1}'.format(value, args))
   	 	return int(value) * int(args)
	```
	- 页面使用自定义fiilter
	
		`{{age | test(2)}}`

### 3、Mako

- mako 页面标签
		
	```python
	${页面数据}
	
	<%!
	    页面python脚本
	%>
	
	%for i in range(20):
	  循环语句
	    <input type="text" value="${i}"/>
	%endfor
	```

- mako render的内容

	```python
	from mako.lookup import TemplateLookup
	from django.template import RequestContext
	from django.conf import settings
	from django.template.context import Context
	from django.http import HttpResponse
	
	def render_to_response(request, template, data=None):
	    context_instance = RequestContext(request)
	    path = settings.TEMPLATES[0]['DIRS'][0]
	    lookup = TemplateLookup(
	        directories=[path],
	        output_encoding='utf-8',
	        input_encoding='utf-8'
	    )
	    mako_template = lookup.get_template(template)
	
	    if not data:
	        data = {}
	    if context_instance:
	        context_instance.update(data)
	    else:
	        context_instance = Context(data)
	    result = {}
	
	    for d in context_instance:
	        result.update(d)
	    result['csrf_token'] = '<input type="hidden" name="csrfmiddlewaretoken" value="{0}" />'.format(request.META['CSRF_COOKIE'])
	    return HttpResponse(mako_template.render(**result))
	```
	
- views使用mako render处理response内容

	```python
    def get(self,request):
        data = {'name':'dewei', 'age':30}
        return render_to_response(request,self.TEMPLATE, data=data)
	```
	
## 配置django的mysql数据源

  - pymysql安装命令

  > pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pymysl
  
  - 配置<mark>settings.py</mark>同级目录的`__init__.py`文件
    
  > import pymysql <br/>
  > pymysql.version\_info = (1, 4, 13, "final", 0)<br/>
  > pymysql.install\_as\_MySQLdb()<br/>

  - 配置settings.py
    
  ```python
    import pymysql # 配置MySQL
    pymysql.install_as_MySQLdb()
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',   # 数据库引擎
            'NAME': 'mydb',         # 你要存储数据的库名，事先要创建之
            'USER': 'root',         # 数据库用户名
            'PASSWORD': '1234',     # 密码
            'HOST': 'localhost',    # 主机
            'PORT': '3306',         # 数据库使用的端口
        }
    }
  ```
  
  - admin页面加载ORM对象，需在app模块目录的的admin.py中添加数据对象配置
  
  	```python
  	# encoding:utf-8
	from django.contrib import admin
	from django.utils.html import format_html
	
	from .models import Message
	
	# Register your models here.
	@admin.register(Message)
	class MessageAdmin(admin.ModelAdmin):
   	    #可显示的数据库字段
	    list_display = ['id','content','message_typ','times', 'return_href'] 
	    #只读的字段
	    readonly_fields = ('created_time',)
	    #右边栏过滤器
	    list_filter = ['message_type'] 
	    #排序
	    ordering = ['id']
	    #每页显示数据的条数
	    list_per_page = 5
	    #搜索
	    search_fields = ['content']
	    
	    #修改数据库字段时触发动作
	    def save_model(self, request, obj, form, change):
	        if change:
	            obj.content = obj.content+'update'
	
	        super(MessageAdmin, self).save_model(request, obj, form, change)
	        
	    #return_href字段显示链接
	    def return_href(self,obj):
	        return format_html('<a href={}>跳转</a>','http://www.baidu.com')

  	```
	
## ORM(SQLAlChemy)配置
- 安装

	`pip install sqlalchemy`<br/>
	`Pip install pymysql`
- 数据库表结构更新模

	`sqlalchemy-migrate alembic`
- 同步数据库方法

	-  文件保存**sqlalchemy_test.py**
	
	```python
	Base = declarative_base()  ->实例化base模块
	engine = create_engine(‘mysql+pymysql://root:@localhost:3306/sqlalchemy_test’)  -> 链接数据库引擎
	Base.metadata.create_all(engine)
	
	def init():
	
	def drop():
	
	if __name__ == '__main__':
   	 init()
	```
	- python sqlalchemy_test.py
- 插入数据，使用ipython 并导入 **sqlalchemy_test.py**

	```python
	ipython
	Python 3.9.0 (v3.9.0:9cf6752276, Oct  5 2020, 11:29:23) 
	Type 'copyright', 'credits' or 'license' for more information
	IPython 7.19.0 -- An enhanced Interactive Python. Type '?' for help.
	
	In [1]: from sqlalchemy_test import User
	
	In [2]: user = User(name='dewei')
	
	In [3]: from sqlalchemy_test import db_session
	
	In [4]: db_session.add(user)
	
	In [5]: db_session.commit()
	
	In [6]: db_session.close()
	```
- 查询数据

	```python
	In [14]: dewei = db_session.query(User).filter_by(name='dewei').one()

	In [15]: dewei.name
	Out[15]: 'dewei'
	```
## redis 

- 单独调用redis安装

	`pip install redis`

- django配置redis安装

	`pip install django-redis`
	
	- django中settings.py添加配置redis
	
		```python
		CACHES = {
		    "default": {
		        "BACKEND": "django_redis.cache.RedisCache",
		        "LOCATION": "redis://127.0.0.1:6379",
		        "OPTIONS": {
		            "CLIENT_CLASS": "django_redis.client.DefaultClient",
		            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
		            # "PASSWORD": "密码"
		        }
		    }
		}
		```
- redis的使用
	- 不依赖django使用redis配置方法

		```python
		import redis 
		conn = redis.Redis(host='127.0.0.1', port='6379')
		```
	- django中rediscover使用

 		```python
		import json
		from django_redis import get_redis_connection
		_cache = get_redis_connection('default')
		value = _cache.get(key)
		_cache.set(key, json.dumps(rs))
		```

## Mongo

- mongo安装

	```python
	pip intall pymongo
	```
	
	- 如果使用表关联需要安装如下

		```python
		pip install mongoengine
		```
- 在Django中settings文件中添加配置

	```
	from pymongo import MongoClient
	MONGOCLIENT =  MongoClient(host='127.0.0.1',port=27017)
	```
- 代码中使用方法

	```python
	from django.conf import settings
	conn = settings.MONGOCLIENT['test_mongo']
	db = conn['user']
	db.insert(param)
	db.find(param)
	db.find_one(param)
	db.update({'_id':id}, {'$set',param})
	```

## 用户登录
- 身份验证

	`from django.contrib.auth import authenticate, login, logout`
	`user = authenticate(username=username,password=password)`
- 登录

	`login(request,user)`
- 注销

	`logout(request)`
	
- 创建密码
	
	```python
	from django.contrib.auth.hashers import make_password
	hash_password = make_password('password')
	```
	- 使用明文密码创建用户
	
	> user = User.objects**<mark>.create_user</mark>**(username=username,password=password)
	
## 权限访问
- 用户添加、删除权限

	```python
	In [1]: from django.contrib.auth.models import User,Permission

	In [2]: a_permission = Permission.objects.get(codename='look_a_page')
	
	In [3]: user = User.objects.get(username='wangf')
	
	In [4]: user
	Out[4]: <User: wangf>
	
	In [5]: user.user_permissions.add(a_permission)
	In [6]: user.user_permissions.remove(a_permission)
	```
- 判断权限

	```python
    if not request.user.has_perm('app.look_a_page'):
        raise Http404()
	```
- template中判断权限
	> perms.应用名.权限名
	
	```python
	{% if not perms.app.look_a_page %}
		您没有权限访问
	{% else %}
		欢迎访问A页面
	{% endif %}
	```
	
## 权限组
- 权限组创建，绑定用户

	```python
	In [2]: from django.contrib.auth.models import User,Permission,Group

	In [3]: Group.objects.create(name='b')
	Out[3]: <Group: b>
	
	In [4]: group = Group.objects.get(name='b')
	
	In [6]: user = User.objects.get(username='wangf')
		
	In [8]: permissions = Permission.objects.filter(content_type_id=8)
	
	In [11]: for i in permissions:
	    ...:     group.permissions.add(i)
	    ...: 
	In [12]: group.permissions.values()	
	In [13]: user.groups.add(group)
	```
- 权限组删除

	```python
	user.groups.remove(group)
	```

## Django集成Celery（安装方式）

- 在requirements.txt中添加如下4个库

```python
celery
django-celery
celery-with-redis
redis==2.10.6
```
- 在settings中进入如下配置

```python
import djcelery
djcelery.setup_loader()
INSTALLED_APPS = [
	"djcelery"
]
BROKER_URL='redis://localhost:6379/2'
CELERY_RESULT_BACKEND='redis://localhost:6379/3'
CELERY_IMPORTS=('app.tasks.task')
```

- celery方法定义

```python
#coding:utf-8
import time
from celery import task

@task
def say_hello():
	print("ready...")
	time.sleep(2)
	print("end...")
```

- celery异步函数在视图中使用

```python
from app.tasks.task import say_hello
say_hello.delay(参数列表)
```
- celery与python服务启动方法
	- 首次配置完成后执行sql同步方法

	```python
	python manage.py makemigrations
	python manage.py migrate
	```
	- 启动服务
		- 先执行 `python manage.py runserver`
		- 再执行 `python manage.py celery worker -c 4 --loglevel=info`
	- 确保电脑已经安装了redis并启动了 <mark>***redis-server***</mark>