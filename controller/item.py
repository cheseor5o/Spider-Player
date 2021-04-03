from controller import config, function


class MusicItem:
    def __init__(self, info):
        self.id = info['id']
        self.url = info['url']
        self.name = info['name']
        self.artist = info['artist']
        self.picUrl = info['picUrl']
        self.total = 0
        self.max = config.MAX_COMMENT_NUM

        self.para = {
            "ID": str(self.id),
            "offset": "0",
            "total": "true",
            "limit": "20",
            "max": str(self.max)
        }

    def __repr__(self):
        return "{ 'Music Item':" + str(self.id) + "}"

    def get_song_lyric(self):
        lyric = function.get_song_lyric(dict(ID=str(self.id)))
        return lyric["lrc"]["lyric"]

    def get_song_comment(self):
        para = self.para
        offset = int(self.para["offset"])
        limit = int(self.para["limit"])
        comments_list = []

        for i in range(int(int(self.para["max"]) / 20)):
            para["offset"] = str(offset)
            para["limit"] = str(limit + offset)
            comments = function.get_song_comment(para)
            for i in comments["comments"]:
                comments_list.append(function.generate_comment_item(i))

            offset += 20

        return comments_list

    def get_comment_total(self):
        para = self.para
        comments = function.get_song_comment(para)
        self.total = comments["total"]
        return self.total


class CommentItem:
    def __init__(self, info):
        self.commentId = info['commentId']
        self.content = info['content']
        self.nickName = info['nickName']
        self.userId = info['userId']
        self.avatarUrl = info['avatarUrl']
        self.time = info['time']
        self.likedCount = info['likedCount']

    def __repr__(self):
        return "{ 'Comment Item':" + str(self.commentId) + "}"
