import json

from PyQt5.QtGui import *
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
import requests

from view import windowUI
from controller import function
import time


class Main_Window(QMainWindow, windowUI.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Main_Window, self).__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.signal()

        self.setWindow = Set_Window()

        self.return_toolButton.hide()
        self.tabWidget.hide()
        self.tabWidget.setGeometry(QtCore.QRect(100, 87, 530, 160))
        self.musicPic_label.setScaledContents(True)

    def signal(self):
        self.search_toolButton.clicked.connect(self.search_song)
        self.return_toolButton.clicked.connect(self.return_home)
        self.liked_pushButton.clicked.connect(self.go_liked)
        self.home_pushButton.clicked.connect(self.go_home)
        self.set_toolButton.clicked.connect(self.show_setWindow)

    def search_song(self):
        try:
            if self.searchContent_lineEdit.text() == "" or self.searchContent_lineEdit.text().isspace():
                self.searchResult_label.setText("请输入正确的歌曲名称!")
            else:
                id_list = function.search_song_id(self.searchContent_lineEdit.text())
                music_list = function.generate_music_item(id_list)
                self.searchResult_label.setText("找到 %d 首单曲" % (len(music_list)-1))
                self.disply_song(music_list)
        except Exception as e:
            print(e)

    def disply_song(self,music_list):
        self.musicInfo_label.hide()
        self.musicPic_label.hide()
        self.musicUrl_label.hide()
        self.tabWidget.hide()
        self.return_toolButton.hide()

        self.tableWidget.show()

        self.tableWidget.setColumnWidth(0,30)
        self.tableWidget.setColumnWidth(1,150)
        self.tableWidget.setColumnWidth(2,100)
        self.tableWidget.setColumnWidth(3,80)
        self.tableWidget.setColumnWidth(4,79)
        self.tableWidget.setRowCount(len(music_list))

        self.tableWidget.setCellWidget(0, 0, QLabel("ID"))
        self.tableWidget.setCellWidget(0, 1, QLabel("Name"))
        self.tableWidget.setCellWidget(0, 2, QLabel("Artist"))

        self.tableWidget.setCellWidget(0, 3, QLabel("Like"))
        self.tableWidget.setCellWidget(0, 4, QLabel("Play"))
        self.tableWidget.setCellWidget(0, 5, QLabel("Check"))

        n = 1
        for i in music_list:
            self.tableWidget.setCellWidget(n,0,QLabel(str(n)))
            self.tableWidget.setCellWidget(n,1,QLabel(i.name))
            self.tableWidget.setCellWidget(n,2,QLabel(i.artist))
            self.tableWidget.setCellWidget(n,3,self.disply_button("like",i.id))
            self.tableWidget.setCellWidget(n,4,self.disply_button("play",i.id))
            self.tableWidget.setCellWidget(n,5,self.disply_button("check",i.id))
            n+=1

    def disply_button(self,button_type,music_id):
        if button_type == "like":
            like_icon = QtGui.QIcon()
            liked_icon = QtGui.QIcon()
            like_icon.addPixmap(QtGui.QPixmap(":/img/Like.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            liked_icon.addPixmap(QtGui.QPixmap(":/img/Liked.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            likeBtn = QtWidgets.QToolButton()
            likeBtn.setAutoRaise(True)
            if self.whether_like(music_id):
                likeBtn.setIcon(liked_icon)
            else:
                likeBtn.setIcon(like_icon)

            likeBtn.clicked.connect(lambda: self.like_music(music_id,likeBtn))
            return likeBtn
        if button_type == "play":
            label = QLabel("<a href=\"https://blog.csdn.net/humanking7\">Play</a>")
            label.setOpenExternalLinks(True)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/img/Play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            playBtn = QtWidgets.QToolButton()
            playBtn.setIcon(icon)
            playBtn.setAutoRaise(True)
            label.setPixmap(QtGui.QPixmap(":/img/Play.png"))

            return playBtn

        if button_type == "check":
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/img/Enter.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            checkBtn = QtWidgets.QToolButton()
            checkBtn.setIcon(icon)
            checkBtn.setAutoRaise(True)
            checkBtn.clicked.connect(lambda: self.enter_music(music_id))
            return checkBtn

    def like_music(self,music_id,likeBtn):
        like_icon = QtGui.QIcon()
        liked_icon = QtGui.QIcon()
        like_icon.addPixmap(QtGui.QPixmap(":/img/Like.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        liked_icon.addPixmap(QtGui.QPixmap(":/img/Liked.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        if self.whether_like(music_id):
            likeBtn.setIcon(like_icon)
            self.operate_favour("sub",music_id)
        else:
            likeBtn.setIcon(liked_icon)
            self.operate_favour("add",music_id)

    def operate_favour(self,operation,music_Id):
        if operation == "sub":
            with open("./model/like_data.json") as f:
                music_list = json.load(f)
            music_list.remove(music_Id)
            with open("./model/like_data.json", "w") as f:
                json.dump(music_list, f)
        if operation == "add":
            with open("./model/like_data.json") as f:
                music_list = json.load(f)
            music_list.append(music_Id)
            with open("./model/like_data.json", "w") as f:
                json.dump(music_list, f)

    def whether_like(self,music_id):
        with open("./model/like_data.json", encoding='utf-8') as f:
            music_list = json.load(f)
        if music_id in music_list:return True
        else: return False

    def enter_music(self,music_id):
        self.searchResult_label.hide()
        self.tableWidget.hide()
        self.return_toolButton.show()
        self.tabWidget.show()
        self.musicInfo_label.show()
        self.musicPic_label.show()
        self.musicUrl_label.show()
        try:
            l = [music_id]
            music = function.generate_music_item(l)
            music = music[0]

            try:
                lyric = music.get_song_lyric()
                if lyric == "":
                    self.lyric_plainTextEdit.setPlainText("该首歌暂无歌词!")
                else:
                    self.lyric_plainTextEdit.setPlainText(lyric)
            except:
                self.lyric_plainTextEdit.setPlainText("该首歌暂无歌词!")
            comment_list = music.get_song_comment()
            comment_total = music.get_comment_total()
            plaintext = "该首歌曲共有 %s 个评论 \n\n" % str(comment_total)
            try:
                for i in comment_list:
                    plaintext += str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(i.time/1000)))) + "  " + str(i.nickName) + ": " + str(i.content) + "\n"
                self.comment_plainTextEdit.setPlainText(plaintext)

            except Exception as e:
                plaintext += "评论格式加载出错!"
                self.comment_plainTextEdit.setPlainText(plaintext)

            try:

                url = music.url
                picUrl = music.picUrl
                picRes = requests.get(picUrl)
                img = QImage.fromData(picRes.content)
                self.musicPic_label.setPixmap(QPixmap.fromImage(img))
                self.musicInfo_label.setText("歌名: " + str(music.name) + "\n" + "歌手: " + str(music.artist) )
                self.musicUrl_label.setText("<a href=\"%s\">立即播放!</a>"%music.url)
                self.musicUrl_label.setOpenExternalLinks(True)
            except Exception as e:
                pass

        except Exception as e:
            print(e)

    def return_home(self):
        self.musicInfo_label.hide()
        self.musicPic_label.hide()
        self.musicUrl_label.hide()
        self.return_toolButton.hide()
        self.tabWidget.hide()
        self.searchResult_label.show()
        self.tableWidget.show()

    def go_home(self):
        pass

    def go_liked(self):
        try:
            self.musicInfo_label.hide()
            with open("./model/like_data.json") as f:
                music_list = json.load(f)
            music_list = function.generate_music_item(music_list)
            self.disply_song(music_list)
            self.searchResult_label.setText("收藏 %d 首歌曲" %(len(music_list)-1))
        except Exception as  e:
            print(e)

    def show_setWindow(self):
        self.setWindow.show()


class Set_Window(QMainWindow, windowUI.Ui_Dialog):
    def __init__(self, parent=None):
        super(Set_Window, self).__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)