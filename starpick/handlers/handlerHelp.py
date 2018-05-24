from django.core import signing
from django.contrib.auth.hashers import make_password, check_password
import json

# 用户基本信息
user_key = 'user'
password_key = 'password'
email_key = 'email'

token_key = 'token'

# 返回给客户端的信息
success = 'success'
error = 'error'

# entry 信息
picture_key = 'picture'
description_key = 'description'

# 用于生成token的信息
HEADER = {'typ': 'JWP', 'alg': 'default'}
KEY = 'CHEN_FENG_YAO'
SALT = 'www.lanou3g.com'
TIME_OUT = 30 * 60  # 30min

# 保存图片
PIC_URL = './assets/imgs'
pic_id = 0

# pick 信息
category_key = 'category'
brand_key = 'brand'
idolName_key = 'idolName'
price_key = 'price'
officialLink_key = 'officialLink'
size_key = 'size'
# pic = 

def encrypt(obj):
    # 加密
    value = signing.dumps(obj, key=KEY, salt=SALT)
    value = signing.b64_encode(value.encode()).decode()
    return value

def decrypt(src):
    # 解密
    src = signing.b64_decode(src.encode()).decode()
    raw = signing.loads(src, key=KEY, salt=SALT)
    # print(type(raw))
    return raw

def toJson(dic):
    return json.dumps(dic)

def makePassword(password):
    return make_password(password, None, 'pbkdf2_sha256')

def checkPassword(password, hashedPass):
    return check_password(password, hashedPass)

# def saveImg(img):
