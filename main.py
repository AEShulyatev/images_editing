import sys
from PyQt5.QtWidgets import (QApplication, QLineEdit, QPushButton,
                             QGridLayout, QWidget)
from PyQt5.QtGui import QIcon
from skimage import io
import numpy as np
np.set_printoptions(precision=4, threshold=np.nan, linewidth=np.nan, suppress=True)


def exception():
    textfield3.setText('Что-то пошло не так. Перепроверьте правильность введёных данных.')


def black_white():
    try:
        inp = textfield.text()
        out = textfield2.text()
        img = io.imread(r''+inp).astype(np.int)
        img1 = np.zeros((img.shape[0], img.shape[1], 3))
        img = (img[:, :, 0] + img[:, :, 1] + img[:, :, 2]) // 3
        img1[:, :, 0] = img
        img1[:, :, 1] = img
        img1[:, :, 2] = img
        io.imsave(r''+out, img1.astype(np.uint(8)))
    except:
        exception()


def negative():
    try:
        inp = textfield.text()
        out = textfield2.text()
        img = io.imread(r'' + inp).astype(np.int)
        img1 = np.abs(img-255)
        io.imsave(r'' + out, img1.astype(np.uint(8)))
    except:
        exception()


def lighter_darker():
    try:
        inp = textfield.text()
        out = textfield2.text()
        factor = int(textfield3.text())
        img = io.imread(r'' + inp).astype(np.int)
        img += factor
        img[(img > 255)] = 255
        img[(img < 0)] = 0
        io.imsave(r'' + out, img.astype(np.uint(8)))
    except:
        exception()


def adding_noises():
    try:
        inp = textfield.text()
        out = textfield2.text()
        factor = int(textfield3.text())
        img = io.imread(r'' + inp).astype(np.int)
        img += np.random.randint(-factor-1, factor+1, (img.shape[0], img.shape[1], 3))
        img[(img > 255)] = 255
        img[(img < 0)] = 0
        io.imsave(r'' + out, img.astype(np.uint(8)))
    except:
        exception()


def black_white_2(img):
    try:
        img1 = np.zeros((img.shape[0], img.shape[1], 3))
        img = (img[:, :, 0] + img[:, :, 1] + img[:, :, 2])//3
        img1[:, :, 0] = img
        img1[:, :, 1] = img
        img1[:, :, 2] = img
        return img1
    except:
        exception()


def sepia():
    try:
        inp = textfield.text()
        out = textfield2.text()
        depth = int(textfield3.text())
        img = io.imread(r'' + inp).astype(np.int)
        img = black_white_2(img)
        img[:, :, 0] += depth * 2
        img[:, :, 1] += depth
        img[(img > 255)] = 255
        img[(img < 0)] = 0
        io.imsave(r'' + out, img.astype(np.uint(8)))
    except:
        exception()


def blue_colors():
    try:
        inp = textfield.text()
        out = textfield2.text()
        depth = -int(textfield3.text())
        img = io.imread(r'' + inp).astype(np.int)
        img = black_white_2(img)
        img[:, :, 0] += depth * 2
        img[:, :, 1] += depth
        img[(img > 255)] = 255
        img[(img < 0)] = 0
        io.imsave(r'' + out, img.astype(np.uint(8)))
    except:
        exception()


def ui():
    try:
        inp = textfield.text()
        out = textfield2.text()
        depth = int(textfield3.text())
        img = io.imread(r'' + inp).astype(np.int)
        arr = set()
        for i in range(1, img.shape[0]-1):
            for j in range(img.shape[1]):
                a1, b1, c1 = img[i-1, j]
                a2, b2, c2 = img[i, j]
                a3, b3, c3 = img[i+1, j]
                if abs(a1-a2) + abs(b1-b2) + abs(c1-c2) >= depth and abs(a2-a3) + abs(b2-b3) + abs(c2-c3) >= depth:
                    arr.add((i, j))
        for i in range(img.shape[0]):
            for j in range(1, img.shape[1]-1):
                a1, b1, c1 = img[i, j-1]
                a2, b2, c2 = img[i, j]
                a3, b3, c3 = img[i, j+1]
                if abs(a1-a2) + abs(b1-b2) + abs(c1-c2) >= depth and abs(a2-a3) + abs(b2-b3) + abs(c2-c3) >= depth:
                    arr.add((i, j))
        for i, j in arr:
            img[i, j] = [0, 0, 0]
        io.imsave(r'' + out, img.astype(np.uint(8)))
    except:
        exception()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(r"C:\Users\User\Desktop\favicons71.jpg"))
    window = QWidget()
    window.setWindowTitle('Program for changing colors of photos')
    button1 = QPushButton('Чёрно-белое')
    button1.setToolTip('Сделает изображение чёрно-белым.')
    button2 = QPushButton('Инверсия цвета')
    button2.setToolTip('Изменит все цвета на противоположные.')
    button3 = QPushButton('Увеличение и уменьшение яркости.')
    button3.setToolTip('Напишите в нижней ячейке число. Отрицательное - изображение потемнеет.')
    button4 = QPushButton('Добавление шумов')
    button4.setToolTip('Напишите в нижней ячейке натуральное число. По умолчанию поставьте 50.')
    button5 = QPushButton('Сепия')
    button5.setToolTip('Получится фото в старинном стиле. Введите натуральное число (рекомендованно 30).')
    button6 = QPushButton('Оттенки синего')
    button6.setToolTip('Получится фото в оттенках синего. Введите натуральное число.')
    button7 = QPushButton('Обводка границ')
    button7.setToolTip('Введите натуральное число, чем меньше число, тем более неявные границы обводятся.')
    textfield = QLineEdit()
    textfield.setFocus()
    textfield.setToolTip('Введите сюда только путь к фотографии.')
    textfield2 = QLineEdit()
    textfield2.setToolTip('Введите сюда только путь к файлу, в который надо поместить результат.')
    textfield2.setFocus()
    textfield3 = QLineEdit()
    textfield3.setFocus()
    textfield3.setToolTip('Введите сюда число при необходимости.')
    grid = QGridLayout()
    grid.addWidget(textfield, 1, 1)  # 2nd row, 1st column
    grid.addWidget(button1, 3, 1)  # 2nd row, 2nd column
    grid.addWidget(button2, 3, 2)
    grid.addWidget(button3, 4, 1)
    grid.addWidget(button4, 4, 2)
    grid.addWidget(button5, 5, 1)
    grid.addWidget(textfield2, 1, 2)
    grid.addWidget(textfield3, 6, 2)
    grid.addWidget(button6, 5, 2)
    grid.addWidget(button7, 6, 1)
    window.setLayout(grid)
    button1.clicked.connect(black_white)
    button2.clicked.connect(negative)
    button3.clicked.connect(lighter_darker)
    button4.clicked.connect(adding_noises)
    button5.clicked.connect(sepia)
    button6.clicked.connect(blue_colors)
    button7.clicked.connect(ui)
    window.show()
    sys.exit(app.exec())
