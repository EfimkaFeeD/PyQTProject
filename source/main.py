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
        self.connection = sqlite3.connect('default/films_db.db')
        self.searchnamebutton.clicked.connect(lambda: self.search_in_table(1))
        self.searchoriginalnamebutton.clicked.connect(lambda: self.search_in_table(2))
        self.about_program_action.triggered.connect(
            lambda: AboutProgramDialog().exec_())
        self.add_info_action.triggered.connect(lambda: AddingDialog().exec_())
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

            series = str(result[4])

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

            self.searchresult.setFontPointSize(24)

            if exists('images/posters/' + result[8]):
                self.film_poster.setPixmap(QPixmap(f'images/posters/{result[8]}'))
            else:
                self.film_poster.setText('Что-то пошло не так')

            if exists('images/film_images/' + result[9]):
                self.film_image.setPixmap(QPixmap(f'images/film_images/{result[9]}'))
            else:
                self.film_image.setText('Что-то пошло не так')

            if series == '3':
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
            else:
                self.searchresult.setText(f"""Номер в базе данных: {result[0]}
Название: {result[1]}
Оригинальное название: {result[2]}
Жанр: {result[3]}
Тип кино: {result[4]}
Дата премьеры: {result[5]}
Продолжительность в минутах: {result[6]}
Режиссер: {result[11]}
Главные актеры: {result[12]}
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
        with open('default/about_program.txt') as file:
            txt = file.read()
        self.about_text.setFontPointSize(24)
        self.about_text.setText(txt)


class HelpDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/help.ui', self)
        self.setFixedSize(960, 720)
        self.setWindowTitle('Помощь')
        self.setWindowIcon(QIcon('ui/icons/window-icon-light.png'))
        with open('default/help.txt') as file:
            txt = file.read()
        self.help_text.setFontPointSize(24)
        self.help_text.setText(txt)


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


class FilterDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/filter.ui', self)
        self.setFixedSize(1280, 960)
        self.setWindowTitle('Фильтрация')
        self.setWindowIcon(QIcon('ui/icons/window-icon-light.png'))


class AddingDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/adding.ui', self)
        self.setFixedSize(1280, 960)
        self.setWindowTitle('Добавление')
        self.setWindowIcon(QIcon('ui/icons/window-icon-light.png'))
        self.connection = sqlite3.connect('default/films_db.db')
        self.checkbutton.clicked.connect(lambda: self.check_info())
        self.addbutton.clicked.connect(lambda: self.adding_info())
        self.check = []

    def check_info(self):
        self.check = []
        if not self.nameedit.text():
            self.check.append('Добавьте название')
        if not self.originalnameedit.text():
            self.check.append('Добавьте оригинальное название')
        if not self.genreedit.text():
            self.check.append('Добавьте жанр')
        if not self.typeedit.text():
            self.check.append('Добавьте тип')
        if not self.dateedit.text():
            self.check.append('Добавьте дату премьеры')
        if not self.durationedit.text():
            self.check.append('Добавьте продолжительность')
        if not self.descriptionedit.text():
            self.check.append('Добавьте файл с описанием')
        if not self.posteredit.text():
            self.check.append('Добавьте файл с постером')
        if not self.imageedit.text():
            self.check.append('Добавьте файл с изображением')
        if not self.traileredit.text():
            self.check.append('Добавьте файл с трейлером')
        if not self.directoredit.text():
            self.check.append('Добавьте режиссера')
        if not self.mainactorsedit.text():
            self.check.append('Добавьте главных актеров')
        if not self.castedit.text():
            self.check.append('Добавьте файл с актерами')
        if not self.seasonsedit.text():
            self.check.append('Добавьте количество сезонов')
        if not self.episodesedit.text():
            self.check.append('Добавьте количество серий')
        if not self.imdbratingedit.text():
            self.check.append('Добавьте рейтинг на IMDb')
        if not self.rottentomatoesratingedit.text():
            self.check.append('Добавьте рейтинг на Rotten Tomatoes')
        if not self.kinopoiskratingedit.text():
            self.check.append('Добавьте рейтинг на Кинопоиск')
        if not self.boxofficeedit.text():
            self.check.append('Добавьте сборы')
        if not self.wheretowatchedit.text():
            self.check.append('Добавьте где смотреть')

        if self.check:
            self.checktext.setText('\n'.join(self.check))
        else:
            self.checktext.setText('Все хорошо, можете добавлять в базу данных')

    def adding_info(self):
        if self.checktext.toPlainText() == 'Все хорошо, можете добавлять в базу данных':
            num = self.connection.cursor().execute("""SELECT id FROM films_table""").fetchall()
            num = int(num[-1][0]) + 1
            self.connection.cursor().execute("""INSERT INTO casts(id, actors) VALUES(?, ?)""", (num, self.castedit.text()))
            self.connection.cursor().execute("""INSERT INTO descriptions(id, description) VALUES(?, ?)""", (num, self.descriptionedit.text()))
            self.connection.cursor().execute("""INSERT INTO images(id, image) VALUES(?, ?)""", (num, self.imageedit.text()))
            self.connection.cursor().execute("""INSERT INTO posters(id, poster) VALUES(?, ?)""", (num, self.posteredit.text()))
            self.connection.cursor().execute("""INSERT INTO trailers(id, trailer) VALUES(?, ?)""", (num, self.traileredit.text()))
            self.connection.commit()
            cast = int(self.connection.cursor().execute("""SELECT id FROM casts WHERE actors = ?""", (self.castedit.text(),)).fetchone()[0])
            description = int(self.connection.cursor().execute("""SELECT id FROM descriptions WHERE description = ?""", (self.descriptionedit.text(),)).fetchone()[0])
            genre = int(self.connection.cursor().execute("""SELECT id FROM genres WHERE name = ?""", (self.genreedit.text(),)).fetchone()[0])
            image = int(self.connection.cursor().execute("""SELECT id FROM images WHERE image = ?""", (self.imageedit.text(),)).fetchone()[0])
            poster = int(self.connection.cursor().execute("""SELECT id FROM posters WHERE poster = ?""", (self.posteredit.text(),)).fetchone()[0])
            trailer = int(self.connection.cursor().execute("""SELECT id FROM trailers WHERE trailer = ?""", (self.traileredit.text(),)).fetchone()[0])
            type_of_film = int(self.connection.cursor().execute("""SELECT id FROM types WHERE type = ?""", (self.typeedit.text(),)).fetchone()[0])
            self.connection.cursor().execute("""INSERT INTO films_table(id, title, original_title, genre, type, date, duration, description, poster, images, trailer, director, main_actors, cast, seasons, episodes, imdb_rating, rottentomatoes_rating, kinopoisk_rating, box_office, where_to_watch) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (num, self.nameedit.text(), self.originalnameedit.text(), genre, type_of_film, self.dateedit.text(), self.durationedit.text(), description, poster, image, trailer, self.directoredit.text(), self.mainactorsedit.text(), cast, self.seasonsedit.text(), self.episodesedit.text(), self.imdbratingedit.text(), self.rottentomatoesratingedit.text(), self.kinopoiskratingedit.text(), self.boxofficeedit.text(), self.wheretowatchedit.text()))
            self.connection.commit()
            self.addtext.setText('Ваши данные успешно добавлены в базу данных')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ft = MainApp()
    ft.show()
    sys.exit(app.exec_())
