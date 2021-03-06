import sys
import scipy.misc
from PyQt5.QtWidgets import (QApplication, QLineEdit, QPushButton,
                             QGridLayout, QWidget, QToolTip, QMessageBox)
from PyQt5.QtGui import (QIcon, QFont)
from skimage import io
import numpy as np

np.set_printoptions(precision=4, threshold=np.nan, linewidth=np.nan, suppress=True)


def black_white_2(img):
    img1 = np.zeros((img.shape[0], img.shape[1], 3))
    img = (img[:, :, 0] + img[:, :, 1] + img[:, :, 2]) // 3
    img1[:, :, 0] = img
    img1[:, :, 1] = img
    img1[:, :, 2] = img
    return img1


def check_path(path):
    if path[0] == '"':
        path = path[1:-1]
    return path


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.button1 = QPushButton('Чёрно-белое', self)
        self.button2 = QPushButton('Инверсия цвета', self)
        self.button3 = QPushButton('Увеличение и уменьшение яркости.', self)
        self.button4 = QPushButton('Добавление шумов', self)
        self.button5 = QPushButton('Сепия', self)
        self.button6 = QPushButton('Оттенки синего', self)
        self.button7 = QPushButton('Обводка границ', self)
        self.button8 = QPushButton('Отразить относительно вертикали', self)
        self.button9 = QPushButton('Отразить относительно горизонтали', self)
        self.button10 = QPushButton('Наложение', self)
        self.textfield = QLineEdit(self)
        self.textfield2 = QLineEdit(self)
        self.textfield3 = QLineEdit(self)
        self.grid = QGridLayout(self)
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.button1.setToolTip('Сделает изображение чёрно-белым.')
        self.button2.setToolTip('Изменит все цвета на противоположные.')
        self.button3.setToolTip('Напишите в нижней ячейке число. Отрицательное - изображение потемнеет.')
        self.button4.setToolTip('Напишите в нижней ячейке натуральное число. По умолчанию поставьте 50.')
        self.button5.setToolTip('Получится фото в старинном стиле. Введите натуральное число (рекомендованно 30).')
        self.button6.setToolTip('Получится фото в оттенках синего. Введите натуральное число.')
        self.button7.setToolTip('Введите натуральное число, чем меньше число, тем более неявные границы обводятся.')
        self.button8.setToolTip('Перевернёт изображение справа налево')
        self.button9.setToolTip('Перевернёт изображение сверху вниз')
        self.button10.setToolTip('Введите в первое поле ввода две ссылки на изображения через тройной пробел.'
                                 ' В поле ввода чисел введите'
                                 ' кол-во процентов занимаемое на картинке 1-ым изображением')
        self.textfield.setFocus()
        self.textfield.setToolTip('Введите сюда только путь к фотографии.')
        self.textfield2.setToolTip('Введите сюда только путь к файлу, в который надо поместить результат.')
        self.textfield2.setFocus()
        self.textfield3.setFocus()
        self.textfield3.setToolTip('Введите сюда число при необходимости.')
        self.grid.addWidget(self.textfield, 1, 1)  # 2nd row, 1st column
        self.grid.addWidget(self.button1, 3, 1)  # 2nd row, 2nd column
        self.grid.addWidget(self.button2, 3, 2)
        self.grid.addWidget(self.button3, 4, 1)
        self.grid.addWidget(self.button4, 4, 2)
        self.grid.addWidget(self.button5, 5, 1)
        self.grid.addWidget(self.textfield2, 1, 2)
        self.grid.addWidget(self.textfield3, 9, 2)
        self.grid.addWidget(self.button6, 5, 2)
        self.grid.addWidget(self.button7, 6, 1)
        self.grid.addWidget(self.button8, 6, 2)
        self.grid.addWidget(self.button9, 7, 1)
        self.grid.addWidget(self.button10, 7, 2)
        self.setLayout(self.grid)
        self.button1.clicked.connect(self.black_white)
        self.button2.clicked.connect(self.negative)
        self.button3.clicked.connect(self.lighter_darker)
        self.button4.clicked.connect(self.adding_noises)
        self.button5.clicked.connect(self.sepia)
        self.button6.clicked.connect(self.blue_colors)
        self.button7.clicked.connect(self.border)
        self.button8.clicked.connect(self.flip_vertical)
        self.button9.clicked.connect(self.flip_horizontal)
        self.button10.clicked.connect(self.overlay)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Program for changing colors of photos')
        self.show()

    def black_white(self):
        try:
            inp = check_path(self.textfield.text())
            out = check_path(self.textfield2.text())
            img = io.imread(r'' + inp).astype(np.int)
            img1 = np.zeros((img.shape[0], img.shape[1], 3))
            img = (img[:, :, 0] + img[:, :, 1] + img[:, :, 2]) // 3
            img1[:, :, 0] = img
            img1[:, :, 1] = img
            img1[:, :, 2] = img
            io.imsave(r'' + out, img1.astype(np.uint(8)))
        except:
            self.textfield3.setText('Что-то пошло не так. Перепроверьте правильность введёных данных.')

    def negative(self):
        try:
            inp = check_path(self.textfield.text())
            out = check_path(self.textfield2.text())
            img = io.imread(r'' + inp).astype(np.int)
            img1 = np.abs(img - 255)
            io.imsave(r'' + out, img1.astype(np.uint(8)))
        except:
            self.textfield3.setText('Что-то пошло не так. Перепроверьте правильность введёных данных.')

    def lighter_darker(self):
        try:
            inp = check_path(self.textfield.text())
            out = check_path(self.textfield2.text())
            factor = int(self.textfield3.text())
            img = io.imread(r'' + inp).astype(np.int)
            img += factor
            img[(img > 255)] = 255
            img[(img < 0)] = 0
            io.imsave(r'' + out, img.astype(np.uint(8)))
        except:
            self.textfield3.setText('Что-то пошло не так. Перепроверьте правильность введёных данных.')

    def adding_noises(self):
        try:
            inp = check_path(self.textfield.text())
            out = check_path(self.textfield2.text())
            factor = int(self.textfield3.text())
            img = io.imread(r'' + inp).astype(np.int)
            img += np.random.randint(-factor - 1, factor + 1, (img.shape[0], img.shape[1], 3))
            img[(img > 255)] = 255
            img[(img < 0)] = 0
            io.imsave(r'' + out, img.astype(np.uint(8)))
        except:
            self.textfield3.setText('Что-то пошло не так. Перепроверьте правильность введёных данных.')

    def sepia(self):
        try:
            inp = check_path(self.textfield.text())
            out = check_path(self.textfield2.text())
            depth = int(self.textfield3.text())
            img = io.imread(r'' + inp).astype(np.int)
            img = black_white_2(img)
            img[:, :, 0] += depth * 2
            img[:, :, 1] += depth
            img[(img > 255)] = 255
            img[(img < 0)] = 0
            io.imsave(r'' + out, img.astype(np.uint(8)))
        except:
            self.textfield3.setText('Что-то пошло не так. Перепроверьте правильность введёных данных.')

    def blue_colors(self):
        try:
            inp = check_path(self.textfield.text())
            out = check_path(self.textfield2.text())
            depth = -int(self.textfield3.text())
            img = io.imread(r'' + inp).astype(np.int)
            img = black_white_2(img)
            img[:, :, 0] += depth * 2
            img[:, :, 1] += depth
            img[(img > 255)] = 255
            img[(img < 0)] = 0
            io.imsave(r'' + out, img.astype(np.uint(8)))
        except:
            self.textfield3.setText('Что-то пошло не так. Перепроверьте правильность введёных данных.')

    def border(self):
        try:
            inp = check_path(self.textfield.text())
            out = check_path(self.textfield2.text())
            depth = int(self.textfield3.text())
            img = io.imread(r'' + inp).astype(np.int)
            arr = set()
            for i in range(1, img.shape[0] - 1):
                for j in range(img.shape[1]):
                    a1, b1, c1 = img[i - 1, j]
                    a2, b2, c2 = img[i, j]
                    a3, b3, c3 = img[i + 1, j]
                    if abs(a1 - a2) + abs(b1 - b2) + abs(c1 - c2) >= depth and abs(a2 - a3) + abs(b2 - b3) + abs(
                            c2 - c3) >= depth:
                        arr.add((i, j))
            for i in range(img.shape[0]):
                for j in range(1, img.shape[1] - 1):
                    a1, b1, c1 = img[i, j - 1]
                    a2, b2, c2 = img[i, j]
                    a3, b3, c3 = img[i, j + 1]
                    if abs(a1 - a2) + abs(b1 - b2) + abs(c1 - c2) >= depth and abs(a2 - a3) + abs(b2 - b3) + abs(
                            c2 - c3) >= depth:
                        arr.add((i, j))
            for i, j in arr:
                img[i, j] = [0, 0, 0]
            io.imsave(r'' + out, img.astype(np.uint(8)))
        except:
            self.textfield3.setText('Что-то пошло не так. Перепроверьте правильность введёных данных.')

    def flip_vertical(self):
        try:
            inp = check_path(self.textfield.text())
            out = check_path(self.textfield2.text())
            img = io.imread(r'' + inp).astype(np.int)
            img = img[:, ::-1]
            io.imsave(r'' + out, img.astype(np.uint(8)))
        except:
            self.textfield3.setText('Что-то пошло не так. Перепроверьте правильность введёных данных.')

    def flip_horizontal(self):
        try:
            inp = check_path(self.textfield.text())
            out = check_path(self.textfield2.text())
            img = io.imread(r'' + inp).astype(np.int)
            img = img[::-1]
            io.imsave(r'' + out, img.astype(np.uint(8)))
        except:
            self.textfield3.setText('Что-то пошло не так. Перепроверьте правильность введёных данных.')

    def overlay(self):
        try:
            inp1, inp2 = self.textfield.text().split('   ')
            inp1 = check_path(inp1)
            inp2 = check_path(inp2)
            out = check_path(self.textfield2.text())
            proc = int(self.textfield3.text())
            img1 = io.imread(r'' + inp1).astype(np.int)
            img2 = io.imread(r'' + inp2).astype(np.int)
            img1 = scipy.misc.imresize(img1, (img2.shape[0], img2.shape[1]))
            img = (img1 * (proc / 100) + img2 * ((100 - proc) / 100)) // 1
            io.imsave(r'' + out, img.astype(np.uint(8)))
        except:
            self.textfield3.setText('Что-то пошло не так. Перепроверьте правильность введёных данных.')

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("favicons71.jpg"))
    window = Window()
    sys.exit(app.exec())
