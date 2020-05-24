#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtWidgets import QLabel, QFileDialog, QColorDialog
from PyQt5.QtGui import QColor, QImage, QPixmap, QPainter, QPen, QBrush
from PyQt5.QtGui import QTransform, QIcon
from PyQt5.QtCore import Qt, QPoint
from PIL import ImageQt, Image
from Drawing import Ui_MainWindow as drawing_ui
from Picture import Ui_MainWindow as picture_ui
from Effects import Ui_MainWindow as effects_ui
from Info import Ui_MainWindow as info_ui
import sys
import sqlite3

PATTERNS = {'Сплошной цвет': Qt.SolidPattern, '90%': Qt.Dense1Pattern,
            '75%': Qt.Dense2Pattern, '60%': Qt.Dense3Pattern,
            '50%': Qt.Dense4Pattern, '40%': Qt.Dense5Pattern,
            '20%': Qt.Dense6Pattern, '10%': Qt.Dense7Pattern,
            'Горизонтальная': Qt.HorPattern, 'Вертикальная': Qt.VerPattern,
            'Сетка': Qt.CrossPattern, 'Диагональ правая': Qt.BDiagPattern,
            'Диагональ левая': Qt.FDiagPattern,
            'Сетка (диагональ)': Qt.DiagCrossPattern,
            'Нет заливки': Qt.NoBrush}
LINES = {'Сплошная': Qt.SolidLine, 'Пунктир': Qt.DashLine,
         'Точка': Qt.DotLine, 'Пунктир-точка': Qt.DashDotLine,
         'Пунктир-точка-точка': Qt.DashDotDotLine}


class SelectedArea:
    def __init__(self, x=0, y=0):
        self.x, self.y = x if x > 0 else 0, y if y > 0 else 0
        self.w, self.h, self.image = 0, 0, None

    def check(self, x, y):
        x1, x2 = min(self.x, self.x + self.w), max(self.x, self.x + self.w)
        y1, y2 = min(self.y, self.y + self.h), max(self.y, self.y + self.h)
        if x1 <= x <= x2 and y1 <= y <= y2:
            return True
        return False

    def set_image(self, qimage, mode=0, w=1):
        """Формирует изображение по выделяемой области"""
        image = ImageQt.fromqimage(qimage)
        x, x2 = min(self.x, self.x + self.w), max(self.x, self.x + self.w)
        y, y2 = min(self.y, self.y + self.h), max(self.y, self.y + self.h)
        x, x2, y, y2 = x - w, x2 + w, y - w, y2 + w
        try:
            self.image = ImageQt.toqimage(image.crop((x, y, x2, y2)))
            if mode == 0:
                return 'cache_image::ImageQt.toqimage(' \
                       'ImageQt.fromqimage(self.canvas).' \
                       'crop(({}, {}, {}, {})))'.format(x, y, x2, y2)
            return 'cache_image::ImageQt.toqimage(ImageQt.' \
                   'fromqimage(self.cache_image).' \
                   'crop(({}, {}, {}, {})))'.format(x, y, x2, y2)
        except Exception:
            print('Ошибка при формировании области выделения #1')

    def load_image(self, pixmap):
        """Формирует изображение по QPixmap из буферной переменной"""
        try:
            self.x, self.y, self.image = 0, 0, pixmap.toImage()
            self.w, self.h = self.image.width(), self.image.height()
        except Exception:
            print('Ошибка при формировании области выделения #2')

    def set_wh(self, x, y, x1, y1, shift=None):
        self.w = x - self.x if x >= 0 else -self.x
        self.h = y - self.y if y >= 0 else -self.y
        self.w = x1 - self.x if x >= x1 else self.w
        self.h = y1 - self.y if y >= y1 else self.h
        self.w = self.h if shift else self.w

    def values(self):
        return self.x, self.y, self.w, self.h

    def xy(self):
        return self.x, self.y

    def set_values(self, x, y, w, h, x1, y1):
        self.x, self.y = x if x > 0 else 0, y if y > 0 else 0
        self.w = w if 0 <= self.x + w else -self.x
        self.h = h if 0 <= self.y + h else -self.y
        self.w = self.w if self.x + w <= x1 else x1 - self.w
        self.h = self.h if self.y + h <= y1 else y1 - self.h


class Eraser:
    def __init__(self, color, w):
        self.w, self.color = w, color

    def set_color(self, color):
        self.color = color

    def set_width(self, width):
        self.w = width


class Pencil(Eraser):
    def __init__(self, color, w):
        super().__init__(color, w)


class Paint(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initialisation()
        self.color1, self.color2 = QColor(0, 0, 0), QColor(255, 255, 255)
        self.cur_color, self.line_width, self.cache = 1, 1, []
        self.buffer_image, self.last_files = None, []
        self.bg_style, self.pen_style = Qt.SolidPattern, Qt.SolidLine
        self.x, self.y, self.radius = 0, 0, 5
        im = QImage(self.width(), self.height(), QImage.Format_ARGB32)
        self.canvas, self.cache_image = im, im
        self.canvas.fill(QColor(255, 255, 255))
        self.drawing_mode(), self.set_canvas(), self.update_canvas()
        try:
            self.con = sqlite3.connect('data.db')
            cur = self.con.cursor()
            self.data = list(cur.execute('SELECT * from events'))
            if self.data:
                window = QMessageBox()
                window.setText("Обнаружен автосохранённый файл. Открыть его?")
                window.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                answer = window.exec()
                if answer == QMessageBox.Yes:
                    self.read_db()
                cur.execute('DELETE from events WHERE event')
                self.con.commit()
        except Exception:
            self.con = None
        self.write_to_db('canvas::QImage({}, {}, QImage.Format_ARGB32)'
                         .format(self.canvas.width(), self.canvas.height()))
        self.write_to_db('::self.canvas.fill(QColor(255, 255, 255))')
        self.write_to_db('canvas_px::QPixmap().fromImage(self.canvas)')
        self.write_to_db('::self.set_canvas()')
        self.write_to_db('::self.update_canvas()')

    def setupUI(self, ui_file, ui_page='drawing'):
        """Загружает дизайн текущего окна"""
        self.ui = ui_file()
        self.ui.setupUi(self)
        self.ui.Drawing.clicked.connect(self.drawing_mode)
        self.ui.Picture.clicked.connect(self.picture_mode)
        self.ui.Effects.clicked.connect(self.effects_mode)
        self.ui.btn_Crop.clicked.connect(self.crop_image)
        self.ui.btn_Delete.clicked.connect(self.delete_area)
        self.ui.btn_Copy.clicked.connect(self.get_copy_image)
        self.ui.btn_Paste.clicked.connect(self.get_buffer_image)
        self.ui.btn_Select.clicked.connect(self.select_area)
        self.ui.btn_Ready.clicked.connect(self.change_selected_area)
        self.ui.btn_Info.clicked.connect(self.get_info)
        if self.selected_area:
            self.ui.XSArea.setValue(self.selected_area.x)
            self.ui.YSArea.setValue(self.selected_area.y)
            self.ui.WSArea.setValue(self.selected_area.w)
            self.ui.HSArea.setValue(self.selected_area.h)
        try:
            self.ui.btn_Select.setIcon(QIcon('select.png'))
            self.ui.btn_Copy.setIcon(QIcon('copy.png'))
            self.ui.btn_Crop.setIcon(QIcon('crop.png'))
            self.ui.btn_Delete.setIcon(QIcon('delete.png'))
            self.ui.btn_Paste.setIcon(QIcon('paste.png'))
            self.ui.btn_Info.setIcon(QIcon('info.png'))
        except Exception:
            pass
        if ui_page == 'drawing':
            self.ui.btn_Save.clicked.connect(self.save_file)
            self.ui.btn_Open.clicked.connect(self.open_file)
            self.ui.btn_Eraser.clicked.connect(self.set_eraser)
            self.ui.btn_Pipette.clicked.connect(self.set_pipette)
            self.ui.btn_Palette.clicked.connect(self.set_color_from_palette)
            self.ui.btn_Pencil.clicked.connect(self.set_pencil)
            self.ui.Radius.valueChanged.connect(self.set_radius)
            try:
                self.ui.btn_Save.setIcon(QIcon('save.png'))
                self.ui.btn_Open.setIcon(QIcon('open.png'))
                self.ui.btn_Eraser.setIcon(QIcon('eraser.png'))
                self.ui.btn_Pipette.setIcon(QIcon('pipette.png'))
                self.ui.btn_drawEllipse.setIcon(QIcon('ellipse.png'))
                self.ui.btn_drawRect.setIcon(QIcon('rect.png'))
                self.ui.btn_drawRRect.setIcon(QIcon('rrect.png'))
                self.ui.btn_drawLine.setIcon(QIcon('line.png'))
                self.ui.btn_Pencil.setIcon(QIcon('pencil.png'))
            except Exception:
                pass
            self.ui.sld_Width.valueChanged.connect(self.change_line_w_slider)
            self.ui.spin_Width.valueChanged.connect(self.change_line_w_spin)
            self.ui.sld_Width.setValue(self.line_width)
            self.ui.spin_Width.setValue(self.line_width)
            self.ui.color_label1.clicked.connect(self.set_curr_color1)
            self.ui.color_label2.clicked.connect(self.set_curr_color2)
            self.set_curr_color1() if self.cur_color == 1 \
                else self.set_curr_color2()
            s = f"* {{background-color: rgba{str(self.color1.getRgb())}; " \
                f"border: none}}"
            self.ui.color_label1.setStyleSheet(s)
            s = f"* {{background-color: rgba{str(self.color2.getRgb())}; " \
                f"border: none}}"
            self.ui.color_label2.setStyleSheet(s)
            self.ui.bg_styles.addItems(list(PATTERNS.keys()))
            self.ui.border_styles.addItems(list(LINES.keys()))
            if self.last_files:
                a = [x.split('/')[-1] for x in self.last_files]
                self.ui.LastFiles.addItems(a)
            self.ui.c1.clicked.connect(self.set_color_from_Colors)
            self.ui.c2.clicked.connect(self.set_color_from_Colors)
            self.ui.c3.clicked.connect(self.set_color_from_Colors)
            self.ui.c4.clicked.connect(self.set_color_from_Colors)
            self.ui.c5.clicked.connect(self.set_color_from_Colors)
            self.ui.c6.clicked.connect(self.set_color_from_Colors)
            self.ui.c7.clicked.connect(self.set_color_from_Colors)
            self.ui.c8.clicked.connect(self.set_color_from_Colors)
            self.ui.c9.clicked.connect(self.set_color_from_Colors)
            self.ui.c10.clicked.connect(self.set_color_from_Colors)
            self.ui.c11.clicked.connect(self.set_color_from_Colors)
            self.ui.c12.clicked.connect(self.set_color_from_Colors)
            self.ui.c13.clicked.connect(self.set_color_from_Colors)
            self.ui.c14.clicked.connect(self.set_color_from_Colors)
            self.ui.c15.clicked.connect(self.set_color_from_Colors)
            self.ui.c16.clicked.connect(self.set_color_from_Colors)
            self.ui.c17.clicked.connect(self.set_color_from_Colors)
            self.ui.c18.clicked.connect(self.set_color_from_Colors)
            self.ui.btn_drawLine.clicked.connect(self.select_line)
            self.ui.btn_drawEllipse.clicked.connect(self.select_ellipse)
            self.ui.btn_drawRect.clicked.connect(self.select_rect)
            self.ui.btn_drawRRect.clicked.connect(self.select_rrect)
        if ui_page == 'picture':
            self.ui.btn_Right.clicked.connect(self.rotate)
            self.ui.btn_Left.clicked.connect(self.rotate)
            self.ui.btn_Resize.clicked.connect(self.resize_canvas)
            self.ui.btn_HMirror.clicked.connect(self.im_mirrored)
            self.ui.btn_VMirror.clicked.connect(self.im_mirrored)
        if ui_page == 'effects':
            self.ui.btn_Invert.clicked.connect(self.invert)

    def get_info(self):
        """Выдаёт справку о программе"""
        self.info = Information()
        self.info.show()

    def set_radius(self):
        self.radius = self.ui.Radius.value()

    def change_selected_area(self):
        """Изменяет параметры выделенной области"""
        x, y = self.ui.XSArea.value(), self.ui.YSArea.value()
        w, h = self.ui.WSArea.value(), self.ui.HSArea.value()
        if self.selected_area:
            if not self.selected_area.image:
                try:
                    x1, y1 = self.canvas.width(), self.canvas.height()
                    self.selected_area.set_values(x, y, w, h, x1, y1)
                    name = 'rect'
                    c1, c2 = QColor(214, 240, 255, 128), QColor(0, 0, 0, 0)
                    if self.figure:
                        c1, c2, name = self.color2, self.color1, self.figure
                    test_image = self.draw_figure(x, y, w, h, name, c2, c1, 1)
                    self.draw_no_static_image((0, 0), test_image)
                except Exception:
                    pass
            else:
                self.selected_area.x, self.selected_area.y = x, y
                self.draw_no_static_image((x, y), self.selected_area.image)

    def read_db(self):
        """Считывает информацию об автоматически сохранённом файле"""
        if self.con:
            self.cache = [line[-1] for line in self.data]
            self.change_history(1)

    def change_history(self, mode=0):
        """Отменяет последнее действие пользователя"""
        try:
            if mode == 0 and len(self.cache) > 2:
                self.cache = self.cache[:-1]
                if self.con:
                    cur = self.con.cursor()
                    data = max([x[0] for x in list(cur.execute(
                        "SELECT id FROM events").fetchall())])
                    cur.execute("DELETE from events WHERE id = ?", (data,))
                    self.con.commit()
            for line in self.cache:
                try:
                    if isinstance(line, str):
                        var, val = line.split('::')
                        self.__setattr__(var, eval(val)) if var else eval(val)
                    else:
                        for op in line:
                            var, a = op.split('::')
                            self.__setattr__(var, eval(a)) if var else eval(a)
                except Exception:
                    print(False)
            self.canvas_px = QPixmap().fromImage(self.canvas)
            self.update_canvas()
        except Exception:
            self.ui.errors.setText('Ошибка истории изменений')
            # self.ui.errors - объект QLabel для отображения информации
            # об ошибках, если таковые возникают
        else:
            self.ui.errors.setText('')

    def select_line(self):
        self.selection_flag, self.figure = True, 'line'

    def select_ellipse(self):
        self.selection_flag, self.figure = True, 'ellipse'

    def select_rect(self):
        self.selection_flag, self.figure = True, 'rect'

    def select_rrect(self):
        self.selection_flag, self.figure = True, 'rrect'

    def change_color(self, color):
        """Сменяет значение текущего цвета на выбранное"""
        if color:
            style = f"* {{background-color: rgba{str(color.getRgb())}; " \
                    f"border: none}}"
            if self.cur_color == 1:
                self.color1 = color
                self.ui.color_label1.setStyleSheet(style)
            else:
                self.color2 = color
                self.ui.color_label2.setStyleSheet(style)

    def set_color_from_Colors(self):
        """Устанавливает значение текущего цвета из уже созданной палитры"""
        color = self.sender().palette().button().color()
        self.change_color(color)
        if self.cur_color == 2 and self.eraser:
            self.eraser.set_color(color)
        if self.cur_color == 1 and self.pencil:
            self.pencil.set_color(color)

    def set_color_from_palette(self):
        """Устанавливает значение текущего цвета из диалогового окна"""
        color = QColorDialog.getColor()
        self.change_color(color)
        if self.cur_color == 2 and self.eraser:
            self.eraser.set_color(color)
        if self.cur_color == 1 and self.pencil:
            self.pencil.set_color(color)

    def drawing_mode(self):
        self.setupUI(drawing_ui), self.set_canvas(), self.update()

    def picture_mode(self):
        self.setupUI(picture_ui, 'picture'), self.set_canvas(1), self.update()

    def effects_mode(self):
        self.setupUI(effects_ui, 'effects'), self.set_canvas(), self.update()

    def update(self):
        """Обновляет холст при переходе между режимами,
        учитывая наличие выделенной области"""
        if self.selected_area and self.selected_area.image:
            im = self.selected_area.image
            w, h = self.canvas.width(), self.canvas.height()
            self.ui.main_label.setMaximumSize(w, h)
            self.ui.main_label.resize(w, h)
            self.draw_no_static_image(self.selected_area.xy(), im)
        else:
            self.update_canvas()

    def set_canvas(self, mode=0):
        """Устанавливает холст на QScrollArea"""
        if mode == 1:
            self.ui.Height_value.setValue(self.canvas.height())
            self.ui.Width_value.setValue(self.canvas.width())
        self.canvas_px = QPixmap().fromImage(self.canvas)
        self.ui.main_label = QLabel()
        self.ui.Area.setWidget(self.ui.main_label)

    def initialisation(self):
        """Обновляет некоторые параметры и флаги"""
        self.selected_area, self.selection_flag = None, False
        self.eraser, self.pipette, self.pencil = None, False, None
        self.figure, self.shift = None, False

    def update_canvas(self, mode=0):
        """Обновляет холст"""
        if mode == 1:
            self.ui.Height_value.setValue(self.canvas.height())
            self.ui.Width_value.setValue(self.canvas.width())
        self.ui.main_label.setPixmap(self.canvas_px)
        self.ui.main_label.setMaximumSize(
            self.canvas.width(), self.canvas.height())
        self.ui.main_label.resize(self.canvas.width(), self.canvas.height())

    def set_area_image(self):
        """Создаёт по выделенной области изображение"""
        if self.selected_area:
            if not self.selected_area.image:
                a = self.selected_area.set_image(self.canvas)
                if a:
                    self.write_to_db(a)
            return True
        return False

    def delete_area(self):
        """Удаляет выделенный фрагмент с холста"""
        self.selected_area = SelectedArea(self.x, self.y)
        self.update_canvas()

    def clear_canvas_area(self, xy_wh, color, mode=0):
        """Очищает область экрана по параметрам"""
        try:
            qp = QPainter(self.canvas)
            qp.begin(self), qp.setPen(QColor(0, 0, 0, 0)), qp.setBrush(color)
            qp.drawRect(*xy_wh), qp.end()
            self.canvas_px = QPixmap().fromImage(self.canvas)
            if mode == 0:
                self.write_to_db('::self.clear_canvas_area({}, QColor({}), 1)'
                                 .format(xy_wh, str(color.getRgb())[1:-1]))

        except Exception:
            self.ui.errors.setText('Ошибка при очистке участка холста')
        else:
            self.ui.errors.setText('')

    def draw_no_static_image(self, xy, im):
        """Создаёт временное изображение поверх холста"""
        try:
            image = self.canvas_px.toImage()
            qp = QPainter(image)
            qp.begin(self), qp.drawImage(*xy, im), qp.end()
            self.ui.main_label.setPixmap(QPixmap().fromImage(image))
            self.ui.errors.setText('')
            return image
        except Exception:
            self.ui.errors.setText(
                'Ошибка создания не закреплённого на холсте изображения')
            return im

    def draw_static_image(self, xy, im, mode=0):
        """Рисует на холсте постоянное изображение"""
        qp, w, h = QPainter(self.canvas), im.width(), im.height()
        if w == self.canvas.width() and h == self.canvas.height():
            xy = (0, 0)
        qp.begin(self), qp.drawImage(*xy, im), qp.end()
        self.canvas_px = QPixmap().fromImage(self.canvas)
        if mode == 0:
            self.write_to_db('::self.draw_static_image({}, '
                             'self.cache_image, 1)'.format(xy))

    def draw_figure(self, x, y, w, h, name, bor_color, bg_color, mode=0,
                    bor=None, bg=None, from_cache=False, r=0, width=0):
        """Рисует простую фигуру"""
        test_image = QImage(self.canvas.width(), self.canvas.height(),
                            QImage.Format_ARGB32)
        bg_style, pen_style = bg, bor
        if not bor and not bg:
            try:
                self.bg_style = PATTERNS[self.ui.bg_styles.currentText()]
                self.pen_style = LINES[self.ui.border_styles.currentText()]
            except Exception:
                pass
            bg_style, pen_style = self.bg_style, self.pen_style
        r = self.radius if not r else r
        test_image.fill(QColor(0, 0, 0, 0))
        qp, pen, brush = QPainter(test_image), QPen(), QBrush()
        pen.setColor(bor_color), brush.setColor(bg_color)
        width = self.line_width if not width else width
        pen.setWidth(width), pen.setStyle(pen_style), brush.setStyle(bg_style)
        qp.begin(self), qp.setPen(pen), qp.setBrush(brush)
        try:
            if name == 'rect':
                qp.drawRect(x, y, w, h)
            if name == 'rrect':
                qp.drawRoundedRect(x, y, w, h, r, r)
            if name == 'ellipse':
                qp.drawEllipse(x, y, w, h)
            if name == 'line':
                qp.drawLine(x, y, x + w, y + h)
            if mode == 0 and not from_cache:
                self.write_to_db(f'cache_image::self.draw_figure({x}, {y}, '
                                 f'{w}, {h}, "{name}", QColor('
                                 f'{str(bor_color.getRgb())[1:-1]}), '
                                 f'QColor({str(bg_color.getRgb())[1:-1]}), '
                                 f'0, {pen_style}, {bg_style}, True, {r}, '
                                 f'{width})')
        except Exception:
            self.ui.errors.setText('Ошибка при рисовании')
        else:
            self.ui.errors.setText('')
        qp.end()
        return test_image

    def resize_canvas(self, w=0, h=0, mode=0):
        """Изменяет размер холста"""
        try:
            if not w or not h:
                w = int(self.ui.Width_value.value()) / self.canvas.width()
                h = int(self.ui.Height_value.value()) / self.canvas.height()
            self.canvas_px = self.canvas_px.transformed(
                QTransform().scale(w, h))
            self.canvas = self.canvas_px.toImage()
            self.update_canvas()
            if mode == 0:
                self.write_to_db(f'::self.resize_canvas({w}, {h}, 1)')
        except Exception:
            self.ui.errors.setText('Ошибка при изменении размера изображения')
        else:
            self.ui.errors.setText('')

    def invert(self, mode=0):
        """Создаёт негатив изображения"""
        try:
            if not self.selected_area or \
                    self.selected_area and not self.selected_area.image:
                self.canvas.invertPixels()
                if mode == 0:
                    self.write_to_db('::self.canvas.invertPixels(1)')
                self.canvas_px = QPixmap().fromImage(self.canvas)
                self.ui.main_label.setPixmap(self.canvas_px)
            else:
                self.selected_area.image.invertPixels()
                self.draw_no_static_image(self.selected_area.xy(),
                                          self.selected_area.image)
                if mode == 0:
                    self.write_to_db('::self.cache_image.invertPixels(1)')
        except Exception:
            self.ui.errors.setText('Ошибка при создании негатива')
        else:
            self.ui.errors.setText('')

    def im_mirrored(self):
        """Отражает изображение по вертикали или по горизонтали"""
        try:
            h = (self.sender().text() == 'По горизонтали')
            v = not h
            if not self.selected_area or \
                    self.selected_area and not self.selected_area.image:
                self.canvas = self.canvas.mirrored(h, v)
                self.write_to_db(f'canvas::self.canvas.mirrored({h}, {v})')
                self.canvas_px = QPixmap().fromImage(self.canvas)
                self.ui.main_label.setPixmap(self.canvas_px)
                return
            self.selected_area.image = self.selected_area.image.mirrored(h, v)
            self.write_to_db(f'cache_image::'
                             f'self.cache_image.mirrored({h}, {v})')
            self.draw_no_static_image(
                self.selected_area.xy(), self.selected_area.image)
        except Exception:
            self.ui.errors.setText('Ошибка при отражении изображения')
        else:
            self.ui.errors.setText('')

    def rotate(self):
        """Поворачиает изображение"""
        try:
            if self.set_area_image():
                im = QPixmap().fromImage(self.selected_area.image)
                a = -90 if self.sender().text() == 'Влево' else 90
                im = im.transformed(QTransform().rotate(a))
                self.write_to_db(f'cache_image::QPixmap().fromImage('
                                 f'self.cache_image).transformed('
                                 f'QTransform().rotate({a})).toImage()')
                self.selected_area.image = im.toImage()
                self.draw_no_static_image(self.selected_area.xy(),
                                          im.toImage())
        except Exception:
            self.ui.errors.setText('Ошибка при повороте изображения')
        else:
            self.ui.errors.setText('')

    def get_copy_image(self):
        """Создаёт копию выделенной области"""
        try:
            if self.set_area_image() and self.selected_area.image:
                self.buffer_image, im = None, self.selected_area.image
                self.buffer_image = QPixmap().fromImage(im)
                self.write_to_db('buff_image::QPixmap().'
                                 'fromImage(self.cache_image)')
                self.draw_static_image(self.selected_area.xy(),
                                       self.selected_area.image)
                self.update_canvas()
        except Exception:
            self.ui.errors.setText('Ошибка при копировании изображения')
        else:
            self.ui.errors.setText('')

    def get_buffer_image(self):
        """Создаёт фрагмент выделенной области из буферной переменной"""
        try:
            if self.buffer_image and self.selected_area:
                self.write_to_db('cache_image::self.buff_image.toImage()')
                self.selected_area.load_image(self.buffer_image)
                self.draw_no_static_image(self.selected_area.xy(),
                                          self.selected_area.image)
        except Exception:
            self.ui.errors.setText('Ошибка вставки изображения')
        else:
            self.ui.errors.setText('')

    def set_curr_color1(self):
        self.cur_color = 1
        self.ui.lbl_color1.setStyleSheet(
            "background-color: rgba(128, 128, 128, 128)")
        self.ui.lbl_color2.setStyleSheet("background-color: rgba(0, 0, 0, 0)")

    def set_curr_color2(self):
        self.cur_color = 2
        self.ui.lbl_color2.setStyleSheet(
            "background-color: rgba(128, 128, 128, 128)")
        self.ui.lbl_color1.setStyleSheet("background-color: rgba(0, 0, 0, 0)")

    def save_file(self):
        """Сохраняет файл"""
        try:
            image = ImageQt.fromqimage(self.canvas)
            name = QFileDialog.getSaveFileName(self, 'Сохранить как', '',
                                               "(*.png);;(*.jpg);;(*.bmp)")[0]
            if name:
                image.save(name)
                return True
            self.ui.errors.setText('')
            return False
        except Exception:
            self.ui.errors.setText('Ошибка при сохранении файла')
            return False

    def open_file(self, name=False):
        """Открывает файл"""
        try:
            types = "(*.png);;(*.jpg);;(*.bmp)"
            name = QFileDialog.getOpenFileName(self, 'Открыть', '', types)[0]
            if name:
                self.initialisation()
                if self.con:
                    cur = self.con.cursor()
                    cur.execute("DELETE from events")
                    self.con.commit()
                self.cache = []
                self.write_to_db(f'canvas::ImageQt.'
                                 f'toqimage(Image.open("{name}"))')
                with Image.open(name) as im:
                    self.canvas = ImageQt.toqimage(im)
                    self.canvas.convertTo(QImage.Format_ARGB32)
                    self.write_to_db('::self.canvas.convertTo'
                                     '(QImage.Format_ARGB32)')
                    self.write_to_db('canvas_px::QPixmap().'
                                     'fromImage(self.canvas)')
                    self.write_to_db('::self.set_canvas()')
                    self.write_to_db('::self.update_canvas()')
                    self.canvas_px = QPixmap().fromImage(self.canvas)
                self.update_canvas()
        except Exception:
            self.ui.errors.setText('Ошибка при открытии файла')
        else:
            self.ui.errors.setText('')

    def select_area(self):
        """Устанавливает режим выделения области"""
        if self.selection_flag:
            self.selected_area, self.figure = None, None
        self.selection_flag = not self.selection_flag

    def set_eraser(self):
        """Устанавливает Ластик"""
        color, width = self.color2, self.line_width
        self.eraser = Eraser(color, width) if not self.eraser else None
        self.selected_area, self.selection_flag = None, False
        self.pipette, self.pencil = False, None

    def set_pencil(self):
        color, width = self.color1, self.line_width
        self.pencil = Pencil(color, width) if not self.pencil else None
        self.selected_area, self.selection_flag = None, False
        self.pipette, self.eraser = False, None

    def set_pipette(self):
        """Устанавливает Пипетку"""
        self.pipette, self.eraser, self.pencil = not self.pipette, None, None
        self.selected_area, self.selection_flag = None, False

    def change_line_w_slider(self):
        """Изменяет значение ширины линий от значения слайдера (ползунка)"""
        self.line_width = int(self.ui.sld_Width.value())
        self.ui.spin_Width.setValue(self.line_width)
        if self.eraser:
            self.eraser.set_width(self.line_width)
        if self.pencil:
            self.pencil.set_width(self.line_width)

    def change_line_w_spin(self):
        """Изменяет значение ширины линий от значения QSpinBox"""
        self.line_width = int(self.ui.spin_Width.value())
        self.ui.sld_Width.setValue(self.line_width)
        if self.eraser:
            self.eraser.set_width(self.line_width)
        if self.pencil:
            self.pencil.set_width(self.line_width)

    def crop_image(self):
        """Обрезает изображение по выделенному фрагменту"""
        try:
            if self.set_area_image() and self.selected_area.image:
                self.canvas = self.selected_area.image
                self.write_to_db('canvas::self.cache_image')
                self.canvas_px = QPixmap().fromImage(self.canvas)
                self.selected_area = None
                self.update_canvas()
        except Exception:
            self.ui.errors.setText('Ошибка при обрезке изображения')
        else:
            self.ui.errors.setText('')

    def mousePressEvent(self, event):
        """Анализирует события клика мыши"""
        try:
            self.x, self.y = self.get_mouse_pos(event)
            if self.selection_flag and not self.selected_area:
                self.selected_area = SelectedArea(self.x, self.y)
            elif self.selected_area:
                if not self.selected_area.check(self.x, self.y):
                    if self.selected_area.image:
                        self.draw_static_image(self.selected_area.xy(),
                                               self.selected_area.image)
                    self.update_canvas()
                    self.selected_area = SelectedArea(self.x, self.y)
                else:
                    if not self.selected_area.image and not self.figure:
                        a = self.selected_area.set_image(self.canvas)
                        if a:
                            self.write_to_db(a)
                        self.clear_canvas_area(self.selected_area.values(),
                                               QColor(255, 255, 255))
                        self.draw_no_static_image(self.selected_area.xy(),
                                                  self.selected_area.image)
                    elif not self.selected_area.image and self.figure:
                        (x, y, w, h) = self.selected_area.values()
                        c1, c2, name = self.color2, self.color1, self.figure
                        image = self.draw_figure(x, y, w, h, name, c2, c1)
                        a = self.selected_area.set_image(image, 1,
                                                         self.line_width)
                        if a:
                            self.write_to_db(a)
            elif self.pipette:
                color = QColor(self.canvas.pixel(self.x, self.y))
                self.change_color(color)
                if self.eraser:
                    self.eraser.set_color(self.color2)
                if self.pencil:
                    self.pencil.set_color(self.color1)
            elif self.pencil or self.eraser:
                self.cache.append(list())
                self.con.commit()
        except Exception:
            self.ui.errors.setText('Ошибка при работе с холстом')
        else:
            self.ui.errors.setText('')

    def keyPressEvent(self, event):
        if int(event.modifiers()) == Qt.ControlModifier:
            if event.key() == Qt.Key_C:
                self.get_copy_image()
            elif event.key() == Qt.Key_V:
                self.get_buffer_image()
            elif event.key() == Qt.Key_X:
                self.crop_image()
            elif event.key() == Qt.Key_S:
                self.save_file()
            elif event.key() == Qt.Key_O:
                self.open_file()
            elif event.key() == Qt.Key_Z:
                self.change_history(0)
        elif event.key() == Qt.Key_Delete:
            self.delete_area()
        elif event.key() == Qt.Key_Shift:
            self.shift = not self.shift

    def closeEvent(self, event):
        window = QMessageBox()
        window.setText("Сохранить изменения в файле?")
        window.setStandardButtons(
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        window = window.exec()
        if window == QMessageBox.Yes:
            if self.save_file():
                if self.con:
                    cur = self.con.cursor()
                    cur.execute("DELETE from events")
                    self.con.commit()
                    self.con.close()
                event.accept()
            else:
                event.ignore()
        elif window == QMessageBox.No:
            if self.con:
                cur = self.con.cursor()
                cur.execute("DELETE from events")
                self.con.commit()
                self.con.close()
            event.accept()
        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        try:
            self.x, self.y = self.get_mouse_pos(event)
            if self.selected_area and not self.selected_area.image:
                x1, y1 = self.canvas.width(), self.canvas.height()
                self.selected_area.set_wh(self.x, self.y, x1, y1, self.shift)
                (x, y, w, h) = self.selected_area.values()
                name = 'rect'
                c1, c2 = QColor(214, 240, 255, 128), QColor(0, 0, 0, 0)
                if self.figure:
                    c1, c2, name = self.color2, self.color1, self.figure
                test_image = self.draw_figure(x, y, w, h, name, c2, c1, 1)
                self.draw_no_static_image((0, 0), test_image)
            elif self.selected_area and self.selected_area.image:
                self.draw_no_static_image(
                    (self.x, self.y), self.selected_area.image)
                self.selected_area.x, self.selected_area.y = self.x, self.y
            elif self.eraser:
                xy_wh = (self.x, self.y, self.eraser.w, self.eraser.w)
                self.clear_canvas_area(xy_wh, QColor(self.eraser.color), 1)
                self.update_canvas()
                if isinstance(self.cache[-1], list):
                    self.write_to_db(
                        f'::self.clear_canvas_area({xy_wh}, '
                        f'QColor({str(self.eraser.color.getRgb())[1:-1]}),'
                        f' 1)', 2)
            elif self.pencil:
                xy_wh = (self.x, self.y, self.pencil.w, self.pencil.w)
                self.clear_canvas_area(xy_wh, QColor(self.pencil.color), 1)
                self.update_canvas()
                if isinstance(self.cache[-1], list):
                    self.write_to_db(
                        f'::self.clear_canvas_area({xy_wh}, '
                        f'QColor({str(self.pencil.color.getRgb())[1:-1]})'
                        f', 1)', 2)
            if self.selected_area:
                self.ui.XSArea.setValue(self.selected_area.x)
                self.ui.YSArea.setValue(self.selected_area.y)
                self.ui.WSArea.setValue(self.selected_area.w)
                self.ui.HSArea.setValue(self.selected_area.h)
        except Exception:
            self.ui.errors.setText('Ошибка при работе с холстом')
        else:
            self.ui.errors.setText('')

    def get_mouse_pos(self, event):
        """Изменяет глобальные координаты курсора мыши на окне для холста"""
        pos = self.ui.main_label.mapFrom(self, event.pos())
        self.ui.label_Pos.setText(f'Позиция (x, y): {pos.x()}, {pos.y()}')
        return pos.x(), pos.y()

    def write_to_db(self, val, mode=0):
        """Добавляет действия пользователя в базу данных"""
        if mode:
            self.cache[-1] += [val]
        else:
            self.cache += [val]
        if self.con:
            cur = self.con.cursor()
            cur.execute(f"INSERT INTO events(event) VALUES('{val}')")
            if mode != 2:
                self.con.commit()


class Information(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = info_ui()
        self.ui.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = Paint()
    window.show()
    sys.exit(app.exec())
