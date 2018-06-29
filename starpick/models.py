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
    header = models.URLField(default='http://touxiang.yeree.com/pics/4d/2387125.jpg')
    
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

class Diss(models.Model):
    # 用户diss内容
    entry = models.ForeignKey(
        'Entry',
        on_delete = models.CASCADE,
        related_name='diss'
    )
    user = models.ForeignKey(
        'User',
        on_delete = models.CASCADE,
        related_name='diss'
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
    likenumber = models.IntegerField(default=0)
    dissnumber = models.IntegerField(default=0)
    commentnumber = models.IntegerField(default=0)

class Pick(models.Model):
    entry = models.ForeignKey(
        'Entry',
        on_delete = models.CASCADE,
        related_name='picks'
    )
    category = models.CharField(max_length=30, default='none')
    brand = models.CharField(max_length=50, default='none')
    idolName = models.CharField(max_length=50, default='none')
    price = models.CharField(max_length=50, default='none')
    officialLink = models.URLField(default='none')
    size = models.CharField(max_length=20, default='none')
    pic = models.URLField(default='http://none.none')

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

class TagHash(models.Model):
    entry = models.ForeignKey(
        'Entry',
        on_delete = models.CASCADE,
        related_name='tagHashes'
    )
    hashName = models.CharField(max_length=30)

class Comment(models.Model):
    # 用户对entry的评论
    entry = models.ForeignKey(
        'Entry',
        on_delete = models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        'User',
        on_delete = models.CASCADE,
        related_name='comments'
    )
    content = models. TextField()