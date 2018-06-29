from django.core import signing
from django.contrib.auth.hashers import make_password, check_password
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from ..models import *

# handler 模板
# def getLikeEntries(request):
#     Info = getInfo(request)
#     response = HttpResponse()
#     try:
#     except:
#         return SERVER_ERROR_RES

# ------------------------ key --------------------------
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

# pick 信息
category_key = 'category'
brand_key = 'brand'
idolName_key = 'idolName'
price_key = 'price'
officialLink_key = 'officialLink'
size_key = 'size'
# pic = 

# -------------------------------------------------------
# 保存图片
PIC_URL = './assets/imgs'
pic_id = 0

# 用于生成token的信息
HEADER = {'typ': 'JWP', 'alg': 'default'}
KEY = 'CHEN_FENG_YAO'
SALT = 'www.lanou3g.com'
TIME_OUT = 30 * 60  # 30min


# -------------------------------------------------------
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
def getToken(tokenStr):
    try:
        token = Token.objects.get(token = tokenStr)
        return token
    except:
        return None

def getInfo(request):
    '''获取request内容'''
    if request.method == 'GET':
        return request.GET
    if request.method == 'POST':
        return request.POST
    return None

# ----------------------RESPONSE------------------------------
SERVER_ERROR_RES = HttpResponse()
SERVER_ERROR_RES.content = toJson({
    success: False,
    error: 'server error'
})
SERVER_ERROR_RES.status_code = 500

ERR_TOKEN_RES = HttpResponse()
ERR_TOKEN_RES.content = {success: False, error: 'invalid token'}

TOKEN_ENTRY_ERR_RES = HttpResponse()
TOKEN_ENTRY_ERR_RES.content = toJson({
    success: False,
    error: 'token and entry are not belong to the same user'
})

UNAUTHORIZE_RES = HttpResponse()
UNAUTHORIZE_RES.content = toJson({success: False, error: 'unauthorized'})


# ------------- get ------------
def entryForm(entry):
    hashTags = entry.tagHashes.all()
    hashList = []
    for i in range(0, len(hashTags)):
        hashList.append(hashTags[i].hashName)
    entryInfo = {
        "entryId": entry.id,
        "picture": entry.picture,
        "description": entry.descreption,
        "likenumber": entry.likenumber,
        "dissnumber": entry.dissnumber,
        'hashTags': hashList,
        'userId': entry.user.id
    }
    return entryInfo

def getEntry(entryId):
    try:
        print('getentry')
        entry = Entry.objects.get(id=entryId)
        return entryForm(entry)
    except:
        print('error in getEntry')
        return None

def getTag(tag):
    try:
        return {
            'tagX': tag.x,
            'tagY': tag.y,
            'tagContent': tag.content,
            'entryId': tag.entry.id,
            'pickId': tag.pick.id
        }
    except:
        print('error in getTag')
        return None

def getTagAndEntry(entryId):
    try:
        entry = Entry.objects.get(id=entryId)
        tagList = []
        tags = entry.tags.all()
        for i in range(0, len(tags)):
            tagList.append(getTag(tags[i]))
        entryInfo = entryForm(entry)
        entryInfo['tags'] = tagList
        return entryInfo
    except:
        print('error in getTagAndEntry')
        return None

def getPick(pick):
    try:
        return {
            "category": pick.category,
            "brand": pick.brand,
            "idolName": pick.idolName,
            "price": pick.price,
            "officialLink": pick.officialLink,
            "size": pick.size,
            "pic": pick.pic,
            "entryId": pick.entry.id
        }
    except:
        return None