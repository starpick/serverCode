from django.db import models
# from cPickle import load, dump

# Create your models here.

class User(models.Model):
    # 用户基本信息
    def __str__(self):
        return self.email + str(self.id)
    user_name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    # picture 是否作为外键？还是直接保存 URL？
    header = models.URLField()
    
class Follow(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='follows'
    )
    # 如果关注用户被注销？数组
    follow = models.ForeignKey(
        'User',
        on_delete = models.CASCADE,
        related_name='followers'
    )

class Token(models.Model):
    # 用于验证用户身份的token
    token = models.CharField(max_length=500)
    user = models.ForeignKey(
        'User',
        on_delete = models.CASCADE,
        related_name='token'
    )

class Like(models.Model):
    # 用户点赞内容
    entry = models.ForeignKey(
        'Entry',
        on_delete = models.CASCADE,
        related_name='likes'
    )
    user = models.ForeignKey(
        'User',
        on_delete = models.CASCADE,
        related_name='likes'
    )

class Entry(models.Model):
    # 上传的每一项，每个 entry 包含多个pick
    user = models.ForeignKey(
        'User',
        on_delete = models.SET_NULL,
        related_name='entry',
        null=True,
    )
    picture = models.URLField(default='')
    descreption = models.TextField()

class Pick(models.Model):
    entry = models.ForeignKey(
        'Entry',
        on_delete = models.CASCADE,
        related_name='picks'
    )
    category = models.CharField(max_length=30)
    brand = models.CharField(max_length=50)
    idolName = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    officialLink = models.URLField()
    size = models.CharField(max_length=20)
    pic = models.URLField()

class Tag(models.Model):
    # 每一张图片上的tags，每一个tag和一个pick相关
    entry = models.ForeignKey(
        'Entry',
        on_delete = models.CASCADE,
        related_name='tags'
    )
    pick = models.OneToOneField(
        'Pick',
        on_delete = models.CASCADE,
        related_name='tag'
    )
    # 以图片左上角为原点的坐标
    x = models.FloatField()
    y = models.FloatField()
    content = models.CharField(max_length=50)

    