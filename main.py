import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect('films_db.db')
        self.searchbutton.clicked.connect(self.search_in_table)
        self.about_program_action.triggered.connect(
            lambda: AboutProgramDialog().exec_())

    def search_in_table(self):
        result = []
        query = self.searchedit.text()
        tmp = self.connection.cursor().execute(
            """SELECT * FROM films_table WHERE title = ?""", (query, )).fetchall()
        tmp = tmp[0]
        for i in tmp:
            result.append(i)
        print(result)
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
        result[11] = self.connection.cursor().execute(
            """SELECT film_crew FROM film_crews WHERE id = ?""", (result[11],)).fetchone()[0]
        print(result)
        # TODO make description, poster, images work
        # TODO do smth with seasons and episodes
        # TODO right now trailer will be just youtube link, make embedded player or connect youtube-dlp
        # TODO make it look prettier
        self.searchresult.setFontPointSize(24)
        try:
            self.searchresult.setText(f"""
            Номер в базе данных: {result[0]}
            Название: {result[1]}
            Жанр: {result[2]}
            Тип кино: {result[3]}
            Дата премьеры: {result[4]}
            Продолжительность в минутах: {result[5]}
            Описание: {result[6]}
            Постер: {result[7]}
            Изображения: {result[8]}
            Трейлер: {result[9]}
            Режиссер и съемочная команда: {result[10]} / {result[12]}
            Актеры: {result[11]}
            Количество сезонов / серий: {result[13]} / {result[14]}
            Рейтинг на IMDb: {result[15]} из 10
            Рейтинг на Rotten Tomatoes: {result[16]}% из 100%
            Рейтинг на КиноПоиск: {result[17]} из 10
            Где смотреть: {result[18]}
            """)
        except IndexError:
            self.searchresult.setText(
                'По вашему запросу не было найдено информации, либо информация по данному запросу некорректна. '
                'Попробуйте изменить свой запрос или отредактируйте некорректную информацию.')

    def closeEvent(self, event):
        self.connection.close()


class AboutProgramDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('about_program.ui', self)
        with open('about_program.txt') as file:
            txt = file.read()
        self.about_text.setText(txt)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainApp()
    ex.show()
    sys.exit(app.exec_())
