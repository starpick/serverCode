

[TOC]

abc

abc12345

## part 1 start/register/login

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

   注册：

   user

   email

   password

   （返回一个token，以此作为标识）

   登录：

   email

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

## part 2 upload

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

      post：`http://127.0.0.1:8000/starpick/upload_entry`

      需以表单形式提交以下信息：

      （picture 先以URL代替，只能是URL格式，以后再整）

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

      Post: `http://127.0.0.1:8000/starpick/upload_pick`

      包括 tag 信息和 pick 具体信息

      请求信息：

      会判断 entryId 是否属于 token 所代表的用户，否则返回错误

      ```json
      {
          "token": "token..",
          "entryId": "id",
      }
      ```

      上传pick需要提供的信息还有：

      ```
      category_key = 'category'
      brand_key = 'brand'
      idolName_key = 'idolName'
      price_key = 'price'
      officialLink_key = 'officialLink'
      size_key = 'size'
      ```

      同时提供tag信息，只提供一个tag信息（pick 和 tag 1对1）：

      ```
      tagX = Info['tagX']
      tagY = Info['tagY']
      tagContent = Info['tagContent']
      ```

3. 点赞（like）

   1. like

      点赞只需提供两个信息：

      - `token`
      - `entryId`

   2. dislike

      同上，提供`token`和 `entryId`

4. 获取信息

   1. 获取entry

      提供 `entryId`

      如：`http://127.0.0.1:8000/starpick/get_entry?entryId=9`

   2. 获取 tag

      提供`entryId`

      如：`http://127.0.0.1:8000/starpick/get_tags?entryId=12`

   3. 获取 pick

      提供 `tagId`

      如：`http://127.0.0.1:8000/starpick/get_pick?tagId=10`

## part 3 like/unlike

1. 用户点赞（点击爱心）

   `http://127.0.0.1:8000/starpick/like`

   提供：(post get 均可)

   ```json
   {
       "token": "...",
       "entryId": "..."
   }
   ```

   如果用户已经“喜欢”过了则无效

2. 用户取消赞

   `http://127.0.0.1:8000/starpick/unlike`

   提供：(post get 均可)

   提供内容同上

   如果用户没有赞过则无效

3. 给定 email，返回用户所有赞的entry

   `http://127.0.0.1:8000/starpick/get_likes`

   ```json
   {
      "email": "..."
   }
   ```

   每个返回的entry格式如下：

   ```json
   "entry": [
           {
               "entryId": 10,
               "picture": "http://127.0.0.1:8000/admin/starpick/entry/",
               "description": "12345678",
               "tags": [
                   {
                       "tagX": 0,
                       "tagY": 0,
                       "tagContent": "tagContent",
                       "entryId": 10,
                       "pickId": 2
                   },
                   {
                       "tagX": 0,
                       "tagY": 0,
                       "tagContent": "tagContent",
                       "entryId": 10,
                       "pickId": 3
                   }
               ]
           }
   ```

4. 给定 email 和 entryId，查询该用户是否赞过该entry

   `http://127.0.0.1:8000/starpick/query_like`

   提供：

   ```json
   {
       "email": "...",
       "entryId": "..."
   }
   ```

   返回格式如下：

   `{"success": true, "like": false}`

5. 获取用户发送的所有entry

   提供email：`{"email": "…"}`

   返回格式同上上



## part 4 关注

注：更新注册、登录返回值，除了返回token外，还返回一id字段表示用户的id

如：

```json
{
    "success": true,
    "token": "token",
    "id": 17
}
```

1. 用户关注另一用户

   `http://127.0.0.1:8000/starpick/follow/follow`

   提供:

   ```json
   {
       "token": "token",
       "followerId": "the user id of the followed user"
   }
   ```

2. 取关

   提供信息同上

   `http://127.0.0.1:8000/starpick/follow/unfollow`

3. 获得关注的用户列表

   提供id即可，如：`http://127.0.0.1:8000/starpick/follow/getfollowings?id=16`

   返回关注者的userid

   如:

   ```json
   {
       "success": true,
       "follows": [
           {
               "userId": 2
           },
           {
               "userId": 8
           }
       ]
   }
   ```




## part 5 评论

1. 发送评论

   Url: `http://127.0.0.1:8000/starpick/comment/makecomment`

   提供内容：

   ```json
   {
       "token": "token...",
       "entryId": "entryId",
       "content": "content..."
   }
   ```

   成功返回 commentId，如：

   ```json
   {
       "success": true,
       "commentId": 3
   }
   ```

2. 删评

   URL：`http://127.0.0.1:8000/starpick/comment/deleteComments`

   提供：

   ```json
   {
       "token": "token",
       "commentId": 0
   }
   ```

   返回：

   ```json
   {
       "success": true,
       "message": "delete comment success"
   }
   ```

3. 获取一个entry的所有评论

   URL: `http://127.0.0.1:8000/starpick/comment/getComments?entryId=12`

   提供： entryId

   返回类似如下：

   ```json
   {
       "success": true,
       "comments": [
           {
               "userid": 14,
               "username": "abc",
               "content": "jfalk",
               "commentId": 1
           },
           {
               "userid": 17,
               "username": "abc123",
               "content": "jfalk",
               "commentId": 3
           }
       ]
   }
   ```

   

更新：每次请求entry时，同时返回"likenumber"选项，表示该entry的赞数, `commentnumber`表示该entry的评论数

如：

```json
{
    "success": true,
    "entry": [
        {
            "entryId": 9,
            "picture": "http://127.0.0.1:8000/admin/starpick/entry/",
            "description": "da1hkd@1.cosm",
            "likenumber": 2,
            "commentnumber": 0,
            "tags": []
        }
    ]
}
```



PS:更改：

请求单个pick`get_pick`，给定 pickId

格式：`http://127.0.0.1:8000/starpick/get_pick?pickId=14`



## part 6 hashtag

1. 为一个entry设置hashtag

   `http://127.0.0.1:8000/starpick/upload_hashtag`

   提供：`hashName`, `entryId`

2. 获取某一hashTag的所有entry

   `http://127.0.0.1:8000/starpick/get_entrys_by_hash?hashName="wla"`

   提供`hashName`, get post 均可

   返回 `entries`数组

3. 更新：

   每次请求entry时，返回的结果中包含它所有的hashtag:

   如：

   ```json
   {
       "success": true,
       "entry": {
           "entryId": 10,
           "picture": "http://127.0.0.1:8000/admin/starpick/entry/",
           "description": "12345678",
           "likenumber": 0,
           "hashTags": [
               "walala",
               "wala"
           ]
       }
   }
   ```

4. 修复了上传图片URL的问题

需要进行数据库迁移：

```shel
python manage.py makemigrations starpick
python manage.py migrate
```

## part 7 diss

1. 用户diss

   `http://127.0.0.1:8000/starpick/diss`

   提供：(post get 均可)

   ```json
   {
       "token": "...",
       "entryId": "..."
   }
   ```

   如果用户已经diss过了则无效

2. 用户取消赞

   `http://127.0.0.1:8000/starpick/undiss`

   提供：(post get 均可)

   提供内容同上

   如果用户没有diss过则无效

3. 给定 email，返回用户所有diss的entry

   `http://127.0.0.1:8000/starpick/get_disses`

   ```json
   {
      "email": "..."
   }
   ```

   每个返回的entry格式如下：

   ```json
   "entry": [
           {
               "entryId": 10,
               "picture": "http://127.0.0.1:8000/admin/starpick/entry/",
               "description": "12345678",
               "tags": [
                   {
                       "tagX": 0,
                       "tagY": 0,
                       "tagContent": "tagContent",
                       "entryId": 10,
                       "pickId": 2
                   },
                   {
                       "tagX": 0,
                       "tagY": 0,
                       "tagContent": "tagContent",
                       "entryId": 10,
                       "pickId": 3
                   }
               ]
           }
   ```

4. 给定 email 和 entryId，查询该用户是否diss过该entry

   `http://127.0.0.1:8000/starpick/query_diss`

   提供：

   ```json
   {
       "email": "...",
       "entryId": "..."
   }
   ```

   返回格式如下：

   `{"success": true, "diss": false}`

更新 entry 返回内容：添加 `dissnumber`项，如：

```json
{
    "success": true,
    "entry": [
        {
            "entryId": 13,
            "picture": "http://127.0.0.1:8000/admin/starpick/entry/",
            "description": "entry",
            "likenumber": 0,
            "dissnumber": 2,
            "commentnumber": 0,
            "tags": [
                {
                    "tagX": 1,
                    "tagY": 2,
                    "tagContent": "xixi",
                    "entryId": 13,
                    "pickId": 13
                }
            ]
        }
    ]
}
```

