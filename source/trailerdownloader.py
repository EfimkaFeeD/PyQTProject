import sys
import yt_dlp
import shutil
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from os.path import exists
from os import rename, getcwd


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/trailerdownloader.ui', self)
        self.data = {}
        self.path = ''
        self.filename = ''
        self.outputname = ''
        self.setFixedSize(1280, 960)
        self.setWindowTitle('Скачивание трейлера')
        self.setWindowIcon(QIcon('ui/icons/window-icon-light.png'))
        self.downloadended.setFontPointSize(24)
        self.filenameoutput.setFontPointSize(24)
        self.trailerinfo.setFontPointSize(24)
        self.downloadbutton.clicked.connect(lambda:self.download_trailer())
        self.checkfilebutton.clicked.connect(lambda:self.check_file())
        self.renamebutton.clicked.connect(lambda:self.rename_file())
        self.movebutton.clicked.connect(lambda:self.move_file())

    def download_trailer(self):
        url = self.urlinput.text()
        ydl_opts = {}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                self.data = ydl.sanitize_info(info)
            self.output_result()
        except Exception:
            self.downloadended.setText('Проверьте URL')

    def output_result(self):
        tmp = self.data['requested_downloads']
        tmp = tmp[0]
        self.path = tmp['filepath']
        self.filename = tmp['_filename']
        self.downloadended.setText('Скачивание завершено')
        self.filenameoutput.setText(self.filename)

    def check_file(self):
        try:
            tmp = self.data['requested_downloads']
            if exists(self.path):
                self.trailerinfo.setText('Скачивание прошло успешно, файл находится в папке, '
                                         'продолжайте следовать инструкции.')
            else:
                self.trailerinfo.setText('Что-то пошло не так, попробуйте повторить попытку скачивания.')
            self.nameinput.setText(self.filename)
            self.nameoutput.setText(self.filename[self.filename.rfind('.'):])
        except KeyError:
            self.trailerinfo.setText('Что-то пошло не так, попробуйте повторить попытку скачивания.')

    def rename_file(self):
        try:
            name_input = self.nameinput.text()
            name_output = self.nameoutput.text()
            self.outputname = name_output
            rename(name_input, name_output)
            self.namemove.setText(self.outputname)
        except FileNotFoundError:
            self.trailerinfo.setText('Что-то пошло не так, проверьте наличие файла в папке.')


    def move_file(self):
        try:
            move_name = self.namemove.text()
            before = getcwd() + '/' + move_name
            after = getcwd() + '/trailers/' + move_name
            shutil.move(before, after)
        except shutil.Error:
            self.trailerinfo.setText('Что-то пошло не так, проверьте наличие файла в папке.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    td = MainApp()
    td.show()
    sys.exit(app.exec_())
