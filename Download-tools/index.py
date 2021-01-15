from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

import urllib.request
import humanize
from PyQt5.uic import loadUiType
import pafy
import os
from os import path

ui, _ = loadUiType('main.ui')


class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.InitUT()
        self.Handel_Buttons()

    def InitUT(self):
        ## nơi chứa tất cả các thay đổi ui trong tải

        self.tabWidget.tabBar().setVisible(False)
        self.Apply_Abun_style()
        self.Move_box1()
        self.Move_box2()
        self.Move_box3()
        self.Move_box4()

    def Handel_Buttons(self):
        ##Nơi xử lý tất cả các nút trong ứng dụng
        self.pushButton_8.clicked.connect(self.Download)
        self.pushButton_2.clicked.connect(self.Handel_Browse)

        self.pushButton_3.clicked.connect(self.Get_Video_data)
        self.pushButton_5.clicked.connect(self.Download_video)
        self.pushButton_4.clicked.connect(self.Save_Brose)

        self.pushButton_7.clicked.connect(self.Playlist_download)
        self.pushButton_6.clicked.connect(self.Play_list_broswer)

        self.pushButton.clicked.connect(self.Open_Home)
        self.pushButton_9.clicked.connect(self.Open_Download)
        self.pushButton_11.clicked.connect(self.Open_Youtube)
        self.pushButton_10.clicked.connect(self.Open_Setting)

        self.pushButton_12.clicked.connect(self.Apply_Darkorange_style)
        self.pushButton_13.clicked.connect(self.Apply_Abun_style)
        self.pushButton_14.clicked.connect(self.Apply_darkblue_style)
        self.pushButton_15.clicked.connect(self.Apply_Darkk_style)
        self.pushButton_16.clicked.connect(self.Apply_Darkgray_style)

    def Handel_Progress(self, blocknum, blocksize, totalsize):

        ##tính toán trong chương trình
        reade_data = blocknum * blocksize
        if totalsize > 0:
            downoload_precentage = reade_data * 100 / totalsize

            self.progressBar.setValue(downoload_precentage)
            QApplication.processEvents()

    def Handel_Browse(self):
        ##Cho phép tác động vào os để chọn nơi lưu
        save_location = QFileDialog.getSaveFileName(self, caption='Save as', directory=".", filter="All Files(*.*)")
        '''save_location,_  = QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath() , '*.xlsm')'''

        self.lineEdit_2.setText(str(save_location[0]))

    def Download(self):
        ##tải file
        print('bắt đầu tải')
        download_url = self.lineEdit.text()
        print(download_url)

        print(self.lineEdit_2.text())

        save_location = self.lineEdit_2.text()
        print(save_location)
        if download_url == '' or save_location == '':
            QMessageBox.warning(self, "DATA ERROR", "Provide a valid ")
        else:
            try:
                urllib.request.urlretrieve(download_url, save_location, self.Handel_Progress)
                QMessageBox.information(self, "tải thành công", "kết thúc")
            except Exception:
                QMessageBox(self, "tải bị lỗi", "kiem tra url")
                return

        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.progressBar.setValue(0)

    def Save_Brose(self):
        ##lưu
        pass

    # video nè
    ##
    ### tải 1 video nè  #######
    #######
    ####

    def Save_Brose(self):
        save_location = QFileDialog.getSaveFileName(self, caption='Save as', directory=".", filter="All Files(*.*)")
        '''save_location,_  = QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath() , '*.xlsm')'''

        self.lineEdit_4.setText(str(save_location[0]))

    def Get_Video_data(self):
        video_url = self.lineEdit_3.text()

        if video_url == '':
            QMessageBox.warning(self, "dữ liệu  bị lỗi", "kiem tra url")
        else:
            video = pafy.new(video_url)
            print(video.title)
            print(video.duration)
            print(video.viewcount)
            print(video.author)

            video_stream = video.videostreams
            for stream in video_stream:
                print(stream.get_filesize())
                size = humanize.naturalsize(stream.get_filesize())
                data = "{} {} {} {}".format(stream.mediatype, stream.extension, stream.quality, size)
                self.comboBox.addItem(data)

    def Download_video(self):
        video_url = self.lineEdit_3.text()
        save_lovation = self.lineEdit_4.text()

        if video_url == '' or save_lovation == '':
            QMessageBox.warning(self, "dữ liệu bị lỗi", "kiểm tra lại đường dẫn!!!")
        else:
            video = pafy.new(video_url)
            video_stream = video.streams
            video_quality = self.comboBox.currentIndex()
            download = video_stream[video_quality].download(filepath=save_lovation, callback=self.Video_prosess)
            QMessageBox.information(self, "tải thành công", "kết thúc")

        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.progressBar_2.setValue(0)

    def Video_prosess(self, total, received, ratio, rate, time):
        read_data = received
        if total > 0:
            download_per = read_data * 100 / total
            self.progressBar_2.setValue(download_per)

            reamining_time = round(time / 60, 2)

            self.label_5.setText(str('{} phút còn  lại '.format(reamining_time)))
            QApplication.processEvents()

    #######################################

    #####Youtube playlist ###############

    def Playlist_download(self):
        playlist_url = self.lineEdit_5.text()
        save_location = self.lineEdit_6.text()

        if playlist_url == '' or save_location == '':
            QMessageBox.warning(self, "URL ERROR", "kiểm tra dữ liệu đầu vào đường dẫn và nơi lưu ")

        else:
            playlist = pafy.get_playlist(playlist_url)

            playlist_video = playlist['items']

            self.lcdNumber_2.display(len(playlist_video))

        os.chdir(save_location)
        if os.path.exists(str(playlist['title'])):
            os.chdir(str(playlist['title']))
        else:
            os.mkdir(str(playlist['title']))
            os.chdir(str(playlist['title']))

        current_video_in_dowload = 1
        quality = self.comboBox_2.currentIndex()
        QApplication.processEvents()

        for video in playlist_video:
            current_video = video['pafy']
            current_video_stream = current_video.videostreams
            self.lcdNumber.display(current_video_in_dowload)
            download = current_video_stream[quality].download(callback=self.Playlist_prosess)
            QApplication.processEvents()

            current_video_in_dowload += 1

    def Playlist_prosess(self, total, received, ratio, rate, time):
        read_data = received
        if total > 0:
            dowload_per = read_data * 100 / total
            self.progressBar_3.setValue(dowload_per)

            reamining_time = round(time / 60, 2)

            self.label_6.setText(str('{} phút còn  lại '.format(reamining_time)))
            QApplication.processEvents()

    def Play_list_broswer(self):
        playlis_save_location = QFileDialog.getExistingDirectory(self, "Chọn nơi lưu")
        self.lineEdit_6.setText(playlis_save_location)

    ######################Main#########################
    #####################HOME########################3
    def Open_Home(self):

        self.tabWidget.setCurrentIndex(0)

    def Open_Download(self):
        self.tabWidget.setCurrentIndex(1)

    def Open_Youtube(self):
        self.tabWidget.setCurrentIndex(2)

    def Open_Setting(self):
        self.tabWidget.setCurrentIndex(3)

    #######################################################
    ############theme##########################

    def Apply_Darkorange_style(self):
        style = open('theme/qdarkorange.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_Abun_style(self):
        style = open('theme/abun.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_darkblue_style(self):
        style = open('theme/darkblue.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_Darkk_style(self):
        style = open('theme/qdarkk.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_Darkgray_style(self):
        style = open('theme/qdarkgray.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    ###################################################
    ###############Home #################################
    def Move_box1(self):
        box_animation = QPropertyAnimation(self.groupBox, b"geometry")
        box_animation.setDuration(2000)
        box_animation.setStartValue(QRect(0, 0, 0, 0))
        box_animation.setEndValue(QRect(40, 60, 241, 141))
        box_animation.start()
        self.box_animation = box_animation

    def Move_box2(self):
        box_animation2 = QPropertyAnimation(self.groupBox_2, b"geometry")
        box_animation2.setDuration(2000)
        box_animation2.setStartValue(QRect(0, 0, 0, 0))
        box_animation2.setEndValue(QRect(330, 60, 241, 141))
        box_animation2.start()
        self.box_animation2 = box_animation2

    def Move_box3(self):
        box_animation3 = QPropertyAnimation(self.groupBox_3, b"geometry")
        box_animation3.setDuration(2000)
        box_animation3.setStartValue(QRect(0, 0, 0, 0))
        box_animation3.setEndValue(QRect(40, 230, 241, 141))
        box_animation3.start()
        self.box_animation3 = box_animation3

    def Move_box4(self):
        box_animation4 = QPropertyAnimation(self.groupBox_4, b"geometry")
        box_animation4.setDuration(2000)
        box_animation4.setStartValue(QRect(0, 0, 0, 0))
        box_animation4.setEndValue(QRect(330, 230, 241, 141))
        box_animation4.start()
        self.box_animation4 = box_animation4


#####################end###########################
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
'''
import requests as rq
url="https://raw.githubusercontent.com/Kanmani92/shell.txt/master/phptest2.PHP"
a=rq.get(url)
open("phptest2.PHP",'wb').write(a.content)
print("ok")
'''
