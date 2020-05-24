# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'info.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 650)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 580, 630))
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Справка ViGeoPaint"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">   </span><span style=\" font-size:11pt; font-style:italic;\">ViGeoPaint</span><span style=\" font-size:11pt;\"> - простой растровый графический редактор. </span><span style=\" font-size:11pt; font-style:italic;\">ViGeoPaint</span><span style=\" font-size:11pt;\"> предназначен для обработки изображений PNG, JPEG и BMP форматов. В данном редакторе реализованы почти все самые необходимые для работы функции. На данный момент в приложении не реализованы некоторые функции, но они будут добавлены в дальнейшем. В программе есть возможность применять некоторые эффекты к изображению.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600; font-style:italic;\">Подготовка к рисованию</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">   1. Открыть файл: </span><span style=\" font-size:11pt; font-weight:600;\">Открыть</span><span style=\" font-size:11pt;\"> (Ctrl+O);</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">   2. Сохранить файл: </span><span style=\" font-size:11pt; font-weight:600;\">Сохранить</span><span style=\" font-size:11pt;\"> (Ctrl+S);</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">   3. Ширина линий устанавливается с помошью слайдера &quot;</span><span style=\" font-size:11pt; font-weight:600;\">Ширина</span><span style=\" font-size:11pt;\">&quot;;</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">   4. Радиус округлённых концов </span><span style=\" font-size:11pt; font-weight:600;\">Прямоугольника с закругленными концами </span><span style=\" font-size:11pt;\">устанавливается в значениях для радиуса.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">   5. Выбор цвета осуществляется в палитре или произвольно в окне </span><span style=\" font-size:11pt; font-weight:600;\">Цвета.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600; font-style:italic;\">Рисование</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">   1. Рисование </span><span style=\" font-size:11pt; font-weight:600;\">Карандашом</span><span style=\" font-size:11pt;\"> осуществляется квадратами цвета </span><span style=\" font-size:11pt; font-weight:600;\">Цвет №1. </span><span style=\" font-size:11pt;\">В связи с тим не следует слишком быстро водить мышью по холсту при рисовании.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">   2. Очистка области </span><span style=\" font-size:11pt; font-weight:600;\">Ластиком</span><span style=\" font-size:11pt;\"> осуществляется аналогично рисованию </span><span style=\" font-size:11pt; font-weight:600;\">Карандашом</span><span style=\" font-size:11pt;\">, но только цветом </span><span style=\" font-size:11pt; font-weight:600;\">Цвет №2</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">   3. </span><span style=\" font-size:11pt; font-weight:600;\">Пипетка</span><span style=\" font-size:11pt;\"> захватывает значение цвета выбранного пикселя на холсте</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">   4. Выделение области позволяет сдвигать кусок изображения, передвигать его, изменять </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">   5. Изменение параметров выделяемой области производится во вкладке внизу окна по нажатию кнопки </span><span style=\" font-size:11pt; font-weight:600;\">Готово </span><span style=\" font-size:11pt;\">(Внимание! Изменение размеров изображения в выделенной области не возможно!)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">   6. Для захвата выделенной области - нажмите на неё</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">   7. Для прикрепления фрагмента выделенной области к холсту нажмите вне ёё.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">   8. Рисование </span><span style=\" font-size:11pt; font-weight:600;\">Фигур</span><span style=\" font-size:11pt;\"> осуществляется аналогично выделению области, но только с использованием непосредственно фигур</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">   9. Для фигуры можно установить </span><span style=\" font-size:11pt; font-weight:600;\">Контур</span><span style=\" font-size:11pt;\"> и </span><span style=\" font-size:11pt; font-weight:600;\">Заливку.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt; font-weight:600;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600; font-style:italic;\">Операции с выделенной областью</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">   1. Для копирования выделенной области нажмите </span><span style=\" font-size:11pt; font-weight:600;\">Копировать</span><span style=\" font-size:11pt;\"> (Ctrl+C)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">   2. Для вставки скопированной области нажмите </span><span style=\" font-size:11pt; font-weight:600;\">Вставить</span><span style=\" font-size:11pt;\"> (Ctrl+V)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">   3. Для удаления выделенной области нажмите </span><span style=\" font-size:11pt; font-weight:600;\">Удалить</span><span style=\" font-size:11pt;\"> (Delete)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">   4. Для обрезания изображения по выделенной области нажмите </span><span style=\" font-size:11pt; font-weight:600;\">Обрезать</span><span style=\" font-size:11pt;\"> (Ctrl+X).</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600; font-style:italic;\">Изменение параметров изображения</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">   1. Перейдите в окно </span><span style=\" font-size:11pt; font-weight:600;\">Изображения</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">   2. Для изменения размера установите необходимый размер (Ширина, Высота) в пикселях и нажмите </span><span style=\" font-size:11pt; font-weight:600;\">Изменить размер</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">   3. Для поворота фрагмента выделенной области выделить область (см. Рисование, п.4, 6, 7) и нажмете </span><span style=\" font-size:11pt; font-weight:600;\">Вправо</span><span style=\" font-size:11pt;\"> или </span><span style=\" font-size:11pt; font-weight:600;\">Влево</span><span style=\" font-size:11pt;\">. Поворот осуществляется на 90 градусов по часовой или против часов стрелки.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">   4. Для отражения изображения нажмите </span><span style=\" font-size:11pt; font-weight:600;\">По горизонтали</span><span style=\" font-size:11pt;\"> (отражение относительно вертикальной оси) или </span><span style=\" font-size:11pt; font-weight:600;\">По вертикали</span><span style=\" font-size:11pt;\"> (отражение относительно горизонтальной оси).</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600; font-style:italic;\">Эффекты</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">   1. Перейдите в окно </span><span style=\" font-size:11pt; font-weight:600;\">Эффекты</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">   2. Для применения эффекта к части изображения выделить область и примените эффект.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">   3. </span><span style=\" font-size:11pt; font-weight:600;\">Негатив</span><span style=\" font-size:11pt;\"> изменяет цвет изображения на противоположный (Белое станет чёрным, бежевый - синеватым)</span></p></body></html>"))
