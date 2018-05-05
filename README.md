

## 第一阶段

1. 搭建 Python Django 后端框架

   安装 django 即可（应该）

   ```shell
   pip install django
   # 为了实现跨域
   pip install django-cors-middleware
   pip install django-cors-headers
   ```

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

5. 注意事项

   由于 Django 的安全机制，在客户端发出 post 请求时，需要进行 CSRF防御机制

   防御机制太麻烦了 cut down 先

6. 运行

   在根目录下：python manage.py runserver

   如懒得装数据库就把数据库改成sqlite

   为了创建数据库，需要在根目录下运行命令：

   ```shell
   python manage.py migrate
   ```

7. 客户端交互

   地址：

   - 注册：http://127.0.0.1:8000/starpick/register
   - 登录：http://127.0.0.1:8000/starpick/login

   需要提交内容：

   user

   password

   用post方法提交form类型数据

   像这样：

   ```javascript
   var postdata = new FormData()
   postdata.append('user', 'abc')
   postdata.append('password', 'hahaha')
   ```

   为什么不用 json 呢？因为Django 解析起来太麻烦了（不是懒得找api）

   服务端返回数据：

   register、login均返回json数据：

   1. 请求不完整

      状态码：400

      信息：`{"success": false, "error": "bad request"}`

   2. 注册时用户已注册、登录时用户不存在或密码错误

      状态码：200

      信息：`{"success": false, "error": "..."}`

   3. 成功

      状态码：200

      信息：`{"success": true}`

   ​

   ​