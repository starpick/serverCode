[TOC]

## 第一阶段

1. 搭建 Python Django 后端框架

2. 数据库选择 postgresql，但由于代码的兼容性，在开发阶段可以使用sqlite3代替（不用安装数据库），只需要将 mysite/settings.py 中的DATABASES改成：

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
       }
   }
   ```

3. 创建应用 starpick

4. 简单实现了 login、register 功能

   - 数据库 model 文件：starpick/models.py
   - Urlconf: starpick/urls
   - 请求处理：starpick/handlers 文件夹
     - 认证请求：starpick/handlers/AuthenticationHandler.py