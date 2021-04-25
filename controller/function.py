from controller import auth, config, header, interface, item

import json
import requests

header = header.Header


def search_song_id(para):
    url = interface.search_song_url
    para = '{"hlpretag":"<span class=\\"s-fc7\\">","hlposttag":"</span>","s":"' + para + '","type":"1","offset":"0","total":"true","limit":"' + str(
        config.LIMITED_NUM) + '","csrf_token":""}'
    response = requests.post(url=url, headers=header, data=auth.encrypt(para))

    ids = []
    for l in json.loads(response.text)['result']['songs']:
        ids.append(l["id"])

    return ids


def get_song_url(para):
    url = interface.get_song_url
    para = dict(ids=para["ID"], level="standard", encodeType="aac")
    response = requests.post(url=url, headers=header, data=auth.encrypt(para))
    song_url_json = json.loads(response.text)

    return song_url_json


def get_song_info(para):
    url = interface.get_songDetail_url
    para = dict(c=json.dumps([{"id": id} for id in para["ID"]]), ids=json.dumps(para["ID"]))
    response = requests.post(url=url, headers=header, data=auth.encrypt(para))
    song_info_json = json.loads(response.text)

    return song_info_json


def get_song_lyric(para):
    url = interface.get_songLyric_url
    para = '{"id":"' + para["ID"] + '","lv":-1,"tv":-1,"csrf_token":""}'
    response = requests.post(url=url, headers=header, data=auth.encrypt(para))
    song_lyric_json = json.loads(response.text)
    return song_lyric_json


def get_song_comment(para):

    url = interface.get_songComment_url.format(para["ID"])
    para = '{"rid":"R_SO_4_' + para["ID"] + '","offset":"' + para["offset"] + '","total":"' + "true" + '","limit":"' + para["limit"] + '","csrf_token":""}'
    response = requests.post(url=url, headers=header, data=auth.encrypt(para))
    song_comment_json = json.loads(response.text)

    return song_comment_json


def generate_comment_item(comment):
    commentId = comment["commentId"]
    userId = comment["user"]["userId"]
    nickName = comment["user"]["nickname"]
    avatarUrl = comment["user"]["avatarUrl"]
    content = comment["content"]
    time = comment["time"]
    likedCount = comment["likedCount"]
    ObjInfo = dict(commentId=commentId, userId=userId, nickName=nickName, avatarUrl=avatarUrl, time=time,content=content, likedCount=likedCount)

    ItemObj = item.CommentItem(ObjInfo)

    return ItemObj


def generate_music_item(id):
    itemUrl = get_song_url(dict(ID=id))['data']
    itemInfo = get_song_info(dict(ID=id))['songs']
    itemObj = []
    for i in range(len(id)):
        musicUrl = itemUrl[i]
        for musicInfo in itemInfo:
            if musicInfo["id"] == musicUrl["id"]:

                id = musicInfo["id"]
                url = musicUrl["url"]
                if url is None:
                    break
                name = musicInfo["name"]
                artist = musicInfo["ar"][0]["name"]
                picUrl = musicInfo["al"]["picUrl"]


                ObjInfo = dict(id=id, url=url, name=name, artist=artist, picUrl=picUrl)

        itemObj.append(item.MusicItem(ObjInfo))

    return itemObj
