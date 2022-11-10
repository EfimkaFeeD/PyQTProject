import sqlite3
import sys
import mpv
from os.path import exists
from os import getcwd
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.result = []
        uic.loadUi('ui/main.ui', self)
        self.setFixedSize(1280, 960)
        self.setWindowTitle('Фильмотека')
        self.setWindowIcon(QIcon('ui/icons/window-icon-light.png'))
        self.connection = sqlite3.connect('films_db.db')
        self.searchnamebutton.clicked.connect(lambda: self.search_in_table(1))
        self.searchoriginalnamebutton.clicked.connect(lambda: self.search_in_table(2))
        self.about_program_action.triggered.connect(
            lambda: AboutProgramDialog().exec_())
        self.help_action.triggered.connect(lambda: HelpDialog().exec_())
        self.castbutton.clicked.connect(lambda: self.check_for_casts())
        self.descriptionbutton.clicked.connect(lambda: self.check_for_description())
        self.trailerbutton.clicked.connect(lambda: self.trailer())

    def search_in_table(self, name_type):
        try:
            result = []
            query = self.searchedit.text()
            if name_type == 1:
                tmp = self.connection.cursor().execute(
                    """SELECT * FROM films_table WHERE title = ?""", (query, )).fetchall()
            elif name_type == 2:
                tmp = self.connection.cursor().execute(
                    """SELECT * FROM films_table WHERE original_title = ?""", (query,)).fetchall()

            tmp = tmp[0]

            for i in tmp:
                result.append(i)

            result[3] = self.connection.cursor().execute(
                """SELECT name FROM genres WHERE id = ?""", (result[3], )).fetchone()[0]
            result[4] = self.connection.cursor().execute(
                """SELECT type FROM types WHERE id = ?""", (result[4],)).fetchone()[0]
            result[7] = self.connection.cursor().execute(
                """SELECT description FROM descriptions WHERE id = ?""", (result[7],)).fetchone()[0]
            result[8] = self.connection.cursor().execute(
                """SELECT poster FROM posters WHERE id = ?""", (result[8],)).fetchone()[0]
            result[9] = self.connection.cursor().execute(
                """SELECT image FROM images WHERE id = ?""", (result[9],)).fetchone()[0]
            result[10] = self.connection.cursor().execute(
                """SELECT trailer FROM trailers WHERE id = ?""", (result[10],)).fetchone()[0]
            result[13] = self.connection.cursor().execute(
                """SELECT actors FROM casts WHERE id = ?""", (result[13],)).fetchone()[0]

            self.result = result
            # TODO do smth with seasons and episodes
            # TODO make it look prettier
            self.searchresult.setFontPointSize(24)

            if exists('images/posters/' + result[8]):
                self.film_poster.setPixmap(QPixmap(f'images/posters/{result[8]}'))
            else:
                self.film_poster.setText('Что-то пошло не так')

            if exists('images/film_images/' + result[9]):
                self.film_image.setPixmap(QPixmap(f'images/film_images/{result[9]}'))
            else:
                self.film_image.setText('Что-то пошло не так')

            self.searchresult.setText(f"""Номер в базе данных: {result[0]}
Название: {result[1]}
Оригинальное название: {result[2]}
Жанр: {result[3]}
Тип кино: {result[4]}
Дата премьеры: {result[5]}
Продолжительность в минутах: {result[6]}
Режиссер: {result[11]}
Главные актеры: {result[12]}
Количество сезонов / серий: {result[14]} / {result[15]}
Рейтинг на IMDb: {result[16]} из 10
Рейтинг на Rotten Tomatoes: {result[17]}% из 100%
Рейтинг на КиноПоиск: {result[18]} из 10
Сборы: {result[19]}
Где смотреть: {result[20]}
""")
        except IndexError:
            self.searchresult.setFontPointSize(24)
            self.searchresult.setText(
                'По вашему запросу не было найдено информации, либо информация по данному запросу некорректна. '
                'Попробуйте изменить свой запрос или отредактируйте некорректную информацию.')

    def trailer(self):
        try:
            file = getcwd() + '/trailers/' + self.result[10]
            import locale
            locale.setlocale(locale.LC_NUMERIC, "C")
            player = mpv.MPV(input_default_bindings=True, input_vo_keyboard=True, osc=True)
            player.play(file)
        except IndexError:
            self.searchresult.setText('Информации о трейлере для данного фильма нет.')

    def check_for_description(self):
        try:
            DescriptionDialog(self.result[7]).exec_()
        except IndexError:
            self.searchresult.setText('Информации об описании для данного фильма нет.')

    def check_for_casts(self):
        try:
            CastDialog(self.result[13]).exec_()
        except IndexError:
            self.searchresult.setText('Информации об актерах для данного фильма нет.')

    def closeEvent(self, event):
        self.connection.close()


class AboutProgramDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/about_program.ui', self)
        self.setFixedSize(960, 720)
        with open('about_program.txt') as file:
            txt = file.read()
        self.about_text.setFontPointSize(24)
        self.about_text.setText(txt)


class CastDialog(QDialog):
    def __init__(self, name):
        super().__init__()
        uic.loadUi('ui/cast.ui', self)
        self.setFixedSize(960, 720)
        self.setWindowTitle('Актеры')
        self.setWindowIcon(QIcon('ui/icons/window-icon-light.png'))
        with open(f'text/casts/{name}.txt') as file:
            txt = file.read()
        self.cast_text.setFontPointSize(24)
        self.cast_text.setText(txt)


class DescriptionDialog(QDialog):
    def __init__(self, name):
        super().__init__()
        uic.loadUi('ui/description.ui', self)
        self.setFixedSize(960, 720)
        self.setWindowTitle('Описание')
        self.setWindowIcon(QIcon('ui/icons/window-icon-light.png'))
        with open(f'text/descriptions/{name}.txt') as file:
            txt = file.read()
        self.description_text.setFontPointSize(24)
        self.description_text.setText(txt)

"""
class TrailerDialog(QDialog):
    def __init__(self, file):
        super().__init__()
        uic.loadUi('ui/trailer.ui', self)
        self.setFixedSize(960, 720)
        self.setWindowTitle('Трейлер')
        self.setWindowIcon(QIcon('ui/icons/window-icon-light.png'))
        player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        player.setMedia(QMediaContent(QUrl.fromLocalFile(file)))
        player.setVideoOutput(self.trailervideo)
        player.play()
"""


class HelpDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/help.ui', self)
        self.setFixedSize(960, 720)
        self.setWindowTitle('Помощь')
        self.setWindowIcon(QIcon('ui/icons/window-icon-light.png'))
        with open('help.txt') as file:
            txt = file.read()
        self.help_text.setFontPointSize(24)
        self.help_text.setText(txt)


class FilterDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/filter.ui', self)
        self.setFixedSize(1280, 960)
        self.setWindowTitle('Фильтрация')
        self.setWindowIcon(QIcon('ui/icons/window-icon-light.png'))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ft = MainApp()
    ft.show()
    sys.exit(app.exec_())
