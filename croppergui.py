import os
import collections
import math
import random
import sys

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QPushButton,
    QWidget, QLineEdit, QGridLayout
)
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PIL import Image


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()
        self.dir_num = 0

    def initUI(self):

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.textbox = QLineEdit(readOnly=True)
        self.textbox2 = QLineEdit(readOnly=True)

        self.button = QPushButton('파일 열기')
        self.button.clicked.connect(self.on_click)
        self.button2 = QPushButton('실행')
        self.button2.clicked.connect(self.showDialog)

        grid = QGridLayout(self.centralWidget())

        grid.addWidget(self.textbox, 0, 0, 1, 10)
        grid.addWidget(self.textbox2, 2, 0, 2, 9)
        grid.addWidget(self.button, 1, 1, 1, 1)
        grid.addWidget(self.button2, 2, 9, 1, 1)
        grid.setRowStretch(4, 2)

        self.setWindowTitle('File Dialog')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "QFileDialog.getOpenFileName()",
            "",
            "All Files (*);;Comma seperated files (*.csv)", options=options
        )
        if fileName:
            self.textbox.setText(fileName)
            print(fileName)

        self.file = fileName
        self.dir_num = 0

    @QtCore.pyqtSlot()
    def on_click(self):
        self.openFileNameDialog()
        print('PyQt5 button click')

    def showDialog(self):
        img  = Image.open(self.file)

        # PNG를 JPEG로 저장하기 위해서 필요함
        img = img.convert('RGB')
        WIDTH, HEIGHT = img.size

        wanted_num_of_crops = random.randint(5, 10)
        div = math.floor(HEIGHT / wanted_num_of_crops)

        # self.textbox.setText(f"이미지의 높이는 {HEIGHT} 정도 입니다.")
        # self.textbox.setText(f"이미지를 {wanted_num_of_crops}개로 나누면, 약 {div} 정도의 사이즈를 가집니다.")
        self.textbox2.setText(f"{wanted_num_of_crops}개의 이미지로 나눕니다.")
        # print(f"이미지의 높이는 {HEIGHT} 정도 입니다.")
        # print(f"이미지를 {wanted_num_of_crops}개로 나누면, 약 {div} 정도의 사이즈를 가집니다.")
        # print(f"{wanted_num_of_crops}개의 이미지로 나눕니다.")

        first_div = random.randint(10, div)

        num_of_crops = 0
        cur_height = first_div
        crop_positions = []

        while (cur_height < HEIGHT - 10) and (num_of_crops < wanted_num_of_crops):
            cur_height = random.randint(cur_height, cur_height + div)
            crop_positions.append(cur_height)
            num_of_crops += 1

        print(crop_positions)
        file_name = self.file.split('/')[-1].split('.')[0]
        cur_dir = os.getcwd()
        directory = os.getcwd() + '/results/' + file_name + '-' + str(self.dir_num+1)

        if not os.path.exists(directory):
            os.makedirs(directory)

# (가로 시작점, 세로 시작점, 가로 범위, 세로 범위)
        Area = collections.namedtuple("Area", "start_width start_height end_width end_height")
        crop_area = Area(start_width=0, start_height=0, end_width=WIDTH, end_height=0)
        for num, crop_height in enumerate(crop_positions, start=1):
            if num < wanted_num_of_crops:
                crop_area = Area._make([0, crop_area.end_height+1, WIDTH, crop_height])
                cropped_img = img.crop(crop_area)
                cropped_img.save(f"{directory}/{num}.jpeg", format='JPEG')
            else:
                crop_area = Area._make([0, crop_area.end_height+1, WIDTH, HEIGHT])
                cropped_img = img.crop(crop_area)
                cropped_img.save(f"{directory}/{num}.jpeg", format='JPEG')
                break
        # print(num)

        self.textbox2.repaint()
        self.dir_num += 1


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
