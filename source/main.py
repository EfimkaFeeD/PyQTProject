import sqlite3
import sys
from os.path import exists
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import  QVideoWidget


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.result = []
        uic.loadUi('ui/main.ui', self)
        self.setFixedSize(1280, 960)
        self.setWindowTitle('Фильмотека')
        self.setWindowIcon(QIcon('ui/icons/window-icon-light.png'))
        self.connection = sqlite3.connect('films_db.db')
        self.searchbutton.clicked.connect(self.search_in_table)
        self.about_program_action.triggered.connect(
            lambda: AboutProgramDialog().exec_())
        self.castbutton.clicked.connect(lambda: CastDialog(self.result[12]).exec_())
        self.descriptionbutton.clicked.connect(lambda: DescriptionDialog(self.result[6]).exec_())
        self.trailerbutton.clicked.connect(lambda: TrailerDialog().exec_())

    def search_in_table(self):
        try:
            result = []
            query = self.searchedit.text()
            tmp = self.connection.cursor().execute(
                """SELECT * FROM films_table WHERE title = ?""", (query, )).fetchall()

            tmp = tmp[0]

            for i in tmp:
                result.append(i)

            result[2] = self.connection.cursor().execute(
                """SELECT name FROM genres WHERE id = ?""", (result[2], )).fetchone()[0]
            result[3] = self.connection.cursor().execute(
                """SELECT type FROM types WHERE id = ?""", (result[3],)).fetchone()[0]
            result[6] = self.connection.cursor().execute(
                """SELECT description FROM descriptions WHERE id = ?""", (result[6],)).fetchone()[0]
            result[7] = self.connection.cursor().execute(
                """SELECT poster FROM posters WHERE id = ?""", (result[7],)).fetchone()[0]
            result[8] = self.connection.cursor().execute(
                """SELECT image FROM images WHERE id = ?""", (result[8],)).fetchone()[0]
            result[9] = self.connection.cursor().execute(
                """SELECT trailer FROM trailers WHERE id = ?""", (result[9],)).fetchone()[0]
            result[12] = self.connection.cursor().execute(
                """SELECT actors FROM casts WHERE id = ?""", (result[12],)).fetchone()[0]
            self.result = result
            # TODO do smth with seasons and episodes
            # TODO make it look prettier
            self.searchresult.setFontPointSize(24)

            if exists('images/posters/' + result[7]):
                self.film_poster.setPixmap(QPixmap(f'images/posters/{result[7]}'))
            else:
                self.film_poster.setText('Что-то пошло не так')

            if exists('images/film_images/' + result[8]):
                self.film_image.setPixmap(QPixmap(f'images/film_images/{result[8]}'))
            else:
                self.film_image.setText('Что-то пошло не так')

            self.searchresult.setText(f"""Номер в базе данных: {result[0]}
Название: {result[1]}
Жанр: {result[2]}
Тип кино: {result[3]}
Дата премьеры: {result[4]}
Продолжительность в минутах: {result[5]}
Описание: {result[6]}
Постер: {result[7]}
Изображение: {result[8]}
Трейлер: {result[9]}
Режиссер: {result[10]}
Главные актеры: {result[11]}
Все актеры: {result[12]}
Количество сезонов / серий: {result[13]} / {result[14]}
Рейтинг на IMDb: {result[15]} из 10
Рейтинг на Rotten Tomatoes: {result[16]}% из 100%
Рейтинг на КиноПоиск: {result[17]} из 10
Где смотреть: {result[18]}
""")
        except IndexError:
            self.searchresult.setFontPointSize(24)
            self.searchresult.setText(
                'По вашему запросу не было найдено информации, либо информация по данному запросу некорректна. '
                'Попробуйте изменить свой запрос или отредактируйте некорректную информацию.')

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


class TrailerDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/trailer.ui', self)
        self.setFixedSize(960, 720)
        self.setWindowTitle('Трейлер')
        self.setWindowIcon(QIcon('ui/icons/window-icon-light.png'))
        player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        player.setMedia(QMediaContent(QUrl('https://www.youtube.com/watch?v=BmllggGO4pM')))
        player.setVideoOutput(self.trailervideo)
        player.play()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ft = MainApp()
    ft.show()
    sys.exit(app.exec_())