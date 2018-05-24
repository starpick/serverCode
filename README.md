

[TOC]

## part 1

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

## part 2

1. 在用户注册成功或登录成功后给用户返回一个 token 作为用户标识

   返回格式：

   ```json
   {
       "success": "True",
       "token": "token..."
   }
   ```

   客户端存储该标识，待向服务端发送请求时使用

2. 用户上传一个 entry 需要依次执行以下几个步骤：

   1. 上传 entry 信息：

      ```json
      {
          "token": "token",
          "picture": "picture",
          "description": "description"
      }
      ```

      成功上传 entry 信息后，服务端返回成功信息和 entry id

      ```json
      {
          "success": "True",
          "entryId": "id"
      }
      ```

   2. 上传 pick 信息

      包括 tag 信息和 pick 具体信息

      请求信息：

      会判断 entryId 是否属于 token 所代表的用户，否则返回错误

      ```json
      {
          "token": "token..",
          "entryId": "id",
          ...
      }
      ```

      上传pic需要提供的信息还有：

      ```
      category_key = 'category'
      brand_key = 'brand'
      idolName_key = 'idolName'
      price_key = 'price'
      officialLink_key = 'officialLink'
      size_key = 'size'
      ```

      同时提供tag信息，只提供一个tag信息：

      ```
      tagX = Info['tagX']
      tagY = Info['tagY']
      tagContent = Info['tagContent']
      ```

   3. tag

      目前是tag 和 pick 一起上传，可考虑获取 entryid 和 pickid 后，将tag单独上传这种方法