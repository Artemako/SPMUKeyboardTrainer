import sys
import pyqtgraph
from PyQt6 import QtWidgets, QtTest, QtCore, QtGui
from design.main_design import Ui_MainWindow
from design.statistic_design import Ui_Statistics
from design.table_results_design import Ui_Table_results
from design.about_design import Ui_About
from design.wiki_design import Ui_Wiki
from design.texts_design import Ui_Texts
import requests
import sqlite3
import datetime


class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.retranslateUi(self)

        self.condition_activity_textline = False
        self.text_load = False
        self.wiki_text_load = False
        self.text_string = "None"
        self.responce_text = "None"
        self.responce_title = "None"
        self.input_text = "None"
        self.number_of_characters = 0
        self.index_current_character = 0
        self.set_last_symbol(self.textline.text()[self.index_current_character])
        self.number_of_errors = 0
        self.symbols_in_second = [0]
        self.current_time = 0
        self.current_language = "ru"

        self.main_db = sqlite3.connect('databases/db_main.db')

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.update_tick_timer())

        self.table_results = QtGui.QAction()
        self.table_results = self.menubar.addAction("Результаты")

        self.texts = QtGui.QAction()
        self.texts = self.menubar.addAction("Тексты")

        self.about = QtGui.QAction()
        self.about = self.menubar.addAction("О программе")

        self.highlightingkey.close()
        self.highlightingkeyshift.close()

        self.add_functions()

    def add_functions(self):
        self.startstopbutton.clicked.connect(lambda: self.start_stop_button_clicked())
        self.textline.textEdited.connect(lambda: self.checking_input_in_textline())

        self.load.triggered.connect(lambda: self.load_custom_file())
        self.table_results.triggered.connect(lambda: self.show_table_results_window())
        self.about.triggered.connect(lambda: self.show_about_window())
        self.action_Wiki.triggered.connect(lambda: self.show_wiki_window())
        self.texts.triggered.connect(lambda: self.show_texts_window())

        self.lesson1.triggered.connect(lambda: self.open_lessons_db("lesson1"))
        self.lesson2.triggered.connect(lambda: self.open_lessons_db("lesson2"))
        self.lesson3.triggered.connect(lambda: self.open_lessons_db("lesson3"))
        self.lesson4.triggered.connect(lambda: self.open_lessons_db("lesson4"))
        self.lesson5.triggered.connect(lambda: self.open_lessons_db("lesson5"))
        self.lesson6.triggered.connect(lambda: self.open_lessons_db("lesson6"))
        self.lesson7.triggered.connect(lambda: self.open_lessons_db("lesson7"))
        self.lesson8.triggered.connect(lambda: self.open_lessons_db("lesson8"))
        self.lesson9.triggered.connect(lambda: self.open_lessons_db("lesson9"))
        self.lesson10.triggered.connect(lambda: self.open_lessons_db("lesson10"))

    def add_functions_wiki(self):
        self.wiki_text_load = False
        self.wikiWindow.wikifindbutton.clicked.connect(lambda: self.create_request())
        self.wikiWindow.wikiluckybutton.clicked.connect(lambda: self.create_random_request())

        self.wikiWindow.loadwikitextbutton.clicked.connect(lambda: self.load_wiki_text_and_close())

    def add_functions_texts(self):
        self.update_choice_title()
        self.textsWindow.choice_title.currentIndexChanged.connect(lambda: self.show_current_index_title_text())

    def show_current_index_title_text(self):
        try:
            cursor_table = self.main_db.cursor()
            cursor_table.execute(f"SELECT text FROM texts WHERE title LIKE '%{self.textsWindow.choice_title.currentText()}%'")
            data = cursor_table.fetchone()
            self.textsWindow.selected_text.setText(data[0])
        except:
            self.textsWindow.selected_text.setText("Нет загруженных текстов")

    def update_choice_title(self):
        cursor_table = self.main_db.cursor()
        cursor_table.execute(f"SELECT title FROM texts")
        data = cursor_table.fetchall()
        items = []
        for elem in data:
            items.append(elem[0])
        self.textsWindow.choice_title.addItems(items)
        self.show_current_index_title_text()

    def delete_pass(self):
        pass

    def load_wiki_text_and_close(self):
        if self.wiki_text_load:
            self.remake_text([self.responce_text])
            self.wikiWindow.close()

            self.textline_focus()
            self.condition_activity_textline_false()
            self.text_load = True
        else:
            self.wikiWindow.wikitext.setText("Нельзя загрузить, так как была замечена ошибка.")

    def create_request(self):
        self.input_text = self.wikiWindow.wikisearchline.text()
        url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + str(self.input_text).replace(" ", "_")
        self.find_current_request(url)

    def create_random_request(self):
        self.input_text = self.wikiWindow.wikisearchline.text()
        url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
        self.find_current_request(url)

    def find_current_request(self, current_url):
        print(current_url)
        try:
            response = requests.get(current_url)
            response.raise_for_status()
            self.responce_text = response.json()["extract"]
            self.responce_title = response.json()["title"]

            if not self.check_title_offline_db(self.responce_title):
                self.insert_textid_text_db()

            self.wiki_text_load = True
            self.wikiWindow.wikitext.setText(self.responce_text)

        except Exception as e:
            if self.check_title_offline_db(self.input_text):
                self.import_text_offline_db(self.input_text)
                self.wiki_text_load = True
                self.wikiWindow.wikitext.setText(self.responce_text)
            else:
                self.wikiWindow.wikitext.setText(f"Произошла ошибка.\n{e}")
                self.wiki_text_load = False

    def check_title_offline_db(self, enter):
        cursor_table = self.main_db.cursor()
        cursor_table.execute(f"SELECT title FROM texts WHERE title LIKE '%{enter}%'")
        return cursor_table.fetchone() is not None

    def import_text_offline_db(self, enter):
        cursor_table = self.main_db.cursor()
        cursor_table.execute(f"SELECT title, text FROM texts WHERE title LIKE '%{enter}%'")
        data = cursor_table.fetchone()
        self.responce_text = data[1]
        self.responce_title = data[0]

    def insert_textid_text_db(self):
        cursor_table = self.main_db.cursor()
        rows = [self.responce_title, self.responce_text]
        cursor_table.execute('insert into texts (title, text) values (?,?)', rows)
        self.main_db.commit()

    def highlight_keys(self):
        dict_ru = {
            "ё": [(0, 0), (50, 50), False],
            "1": [(50, 0), (50, 50), False],
            "2": [(100, 0), (50, 50), False],
            "3": [(150, 0), (50, 50), False],
            "4": [(200, 0), (50, 50), False],
            "5": [(250, 0), (50, 50), False],
            "6": [(300, 0), (50, 50), False],
            "7": [(350, 0), (50, 50), False],
            "8": [(400, 0), (50, 50), False],
            "9": [(450, 0), (50, 50), False],
            "0": [(500, 0), (50, 50), False],
            "-": [(550, 0), (50, 50), False],
            "=": [(600, 0), (50, 50), False],

            "!": [(50, 0), (50, 50), True],
            "\"": [(100, 0), (50, 50), True],
            "№": [(150, 0), (50, 50), True],
            ";": [(200, 0), (50, 50), True],
            "%": [(250, 0), (50, 50), True],
            ":": [(300, 0), (50, 50), True],
            "?": [(350, 0), (50, 50), True],
            "*": [(400, 0), (50, 50), True],
            "(": [(450, 0), (50, 50), True],
            ")": [(500, 0), (50, 50), True],
            "_": [(550, 0), (50, 50), True],
            "+": [(600, 0), (50, 50), True],

            "й": [(75, 50), (50, 50), False],
            "ц": [(125, 50), (50, 50), False],
            "у": [(175, 50), (50, 50), False],
            "к": [(225, 50), (50, 50), False],
            "е": [(275, 50), (50, 50), False],
            "н": [(325, 50), (50, 50), False],
            "г": [(375, 50), (50, 50), False],
            "ш": [(425, 50), (50, 50), False],
            "щ": [(475, 50), (50, 50), False],
            "з": [(525, 50), (50, 50), False],
            "х": [(575, 50), (50, 50), False],
            "ъ": [(625, 50), (50, 50), False],

            "ф": [(88, 100), (50, 50), False],
            "ы": [(138, 100), (50, 50), False],
            "в": [(188, 100), (50, 50), False],
            "а": [(238, 100), (50, 50), False],
            "п": [(288, 100), (50, 50), False],
            "р": [(338, 100), (50, 50), False],
            "о": [(388, 100), (50, 50), False],
            "л": [(438, 100), (50, 50), False],
            "д": [(488, 100), (50, 50), False],
            "ж": [(538, 100), (50, 50), False],
            "э": [(588, 100), (50, 50), False],

            "\\": [(637, 100), (50, 50), False],
            "\/": [(637, 100), (50, 50), True],

            "я": [(112, 150), (50, 50), False],
            "ч": [(162, 150), (50, 50), False],
            "с": [(212, 150), (50, 50), False],
            "м": [(262, 150), (50, 50), False],
            "и": [(312, 150), (50, 50), False],
            "т": [(362, 150), (50, 50), False],
            "ь": [(412, 150), (50, 50), False],
            "б": [(462, 150), (50, 50), False],
            "ю": [(512, 150), (50, 50), False],
            ".": [(562, 150), (50, 50), False],

            ",": [(562, 150), (50, 50), True],

            " ": [(200, 200), (300, 50), False]
        }

        dict_en = {
            "`": [(0, 0), (50, 50), False],
            "1": [(50, 0), (50, 50), False],
            "2": [(100, 0), (50, 50), False],
            "3": [(150, 0), (50, 50), False],
            "4": [(200, 0), (50, 50), False],
            "5": [(250, 0), (50, 50), False],
            "6": [(300, 0), (50, 50), False],
            "7": [(350, 0), (50, 50), False],
            "8": [(400, 0), (50, 50), False],
            "9": [(450, 0), (50, 50), False],
            "0": [(500, 0), (50, 50), False],
            "-": [(550, 0), (50, 50), False],
            "=": [(600, 0), (50, 50), False],

            "~": [(0, 0), (50, 50), True],
            "!": [(50, 0), (50, 50), True],
            "@": [(100, 0), (50, 50), True],
            "#": [(150, 0), (50, 50), True],
            "$": [(200, 0), (50, 50), True],
            "%": [(250, 0), (50, 50), True],
            "^": [(300, 0), (50, 50), True],
            "&": [(350, 0), (50, 50), True],
            "*": [(400, 0), (50, 50), True],
            "(": [(450, 0), (50, 50), True],
            ")": [(500, 0), (50, 50), True],
            "_": [(550, 0), (50, 50), True],
            "+": [(600, 0), (50, 50), True],

            "q": [(75, 50), (50, 50), False],
            "w": [(125, 50), (50, 50), False],
            "e": [(175, 50), (50, 50), False],
            "r": [(225, 50), (50, 50), False],
            "t": [(275, 50), (50, 50), False],
            "y": [(325, 50), (50, 50), False],
            "u": [(375, 50), (50, 50), False],
            "i": [(425, 50), (50, 50), False],
            "o": [(475, 50), (50, 50), False],
            "p": [(525, 50), (50, 50), False],
            "[": [(575, 50), (50, 50), False],
            "]": [(625, 50), (50, 50), False],

            "{": [(575, 50), (50, 50), True],
            "}": [(625, 50), (50, 50), True],

            "a": [(88, 100), (50, 50), False],
            "s": [(138, 100), (50, 50), False],
            "d": [(188, 100), (50, 50), False],
            "f": [(238, 100), (50, 50), False],
            "g": [(288, 100), (50, 50), False],
            "h": [(338, 100), (50, 50), False],
            "j": [(388, 100), (50, 50), False],
            "k": [(438, 100), (50, 50), False],
            "l": [(488, 100), (50, 50), False],
            ";": [(538, 100), (50, 50), False],
            "'": [(588, 100), (50, 50), False],

            ":": [(537, 100), (50, 50), True],
            "\"": [(587, 100), (50, 50), True],

            "\\": [(637, 100), (50, 50), False],
            "|": [(637, 100), (50, 50), True],

            "z": [(112, 150), (50, 50), False],
            "x": [(162, 150), (50, 50), False],
            "c": [(212, 150), (50, 50), False],
            "v": [(262, 150), (50, 50), False],
            "b": [(312, 150), (50, 50), False],
            "n": [(362, 150), (50, 50), False],
            "m": [(412, 150), (50, 50), False],
            ",": [(462, 150), (50, 50), False],
            ".": [(512, 150), (50, 50), False],
            "/": [(562, 150), (50, 50), False],

            "<": [(462, 150), (50, 50), True],
            ">": [(512, 150), (50, 50), True],
            "?": [(562, 150), (50, 50), True],

            " ": [(200, 200), (300, 50), False]
        }

        symbol = self.text_string[0]
        lower_symbol = symbol.lower()
        in_ru = lower_symbol in dict_ru.keys()
        in_en = lower_symbol in dict_en.keys()
        if self.current_language == "ru":
            if in_ru:
                value = dict_ru[lower_symbol]
            elif in_en:
                value = dict_en[lower_symbol]
                self.change_language()
            else:
                value = [(0, 0), (0, 0), False]
        else:
            if in_en:
                value = dict_en[lower_symbol]
            elif in_ru:
                value = dict_ru[lower_symbol]
                self.change_language()
            else:
                value = [(0, 0), (0, 0), False]

        x, y = value[0]
        width, height = value[1]
        shift = value[2]

        if lower_symbol != symbol or shift:
            self.highlightingkeyshift.show()
        else:
            self.highlightingkeyshift.close()

        self.highlightingkey.setGeometry(QtCore.QRect(x + 10, y + 60, width, height))

    def change_language(self):
        if self.current_language == "ru":
            self.current_language = "en"
            self.ruseng.setPixmap(QtGui.QPixmap("pics/eng.png"))
        else:
            self.current_language = "ru"
            self.ruseng.setPixmap(QtGui.QPixmap("pics/rus.png"))

    def seconds_to_str(self, seconds):
        mm, ss = divmod(seconds, 60)
        return "%02d:%02d" % (mm, ss)

    def update_tick_timer(self):
        self.current_time += 1
        self.symbols_in_second.append((self.index_current_character / self.current_time) * 60)
        self.show_time()

    def show_time(self):
        self.labeltimer.setText(self.seconds_to_str(self.current_time))

    def start_timer(self):
        self.timer.start(1000)

    def stop_timer(self):
        self.timer.stop()

    def clear_timer(self):
        self.current_time = 0
        self.labeltimer.setText(self.seconds_to_str(self.current_time))

    def load_custom_file(self):
        custom_file = ""
        custom_file, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', './', "Text files (*.txt)")
        print(custom_file)
        if custom_file != "":
            try:
                f = open(custom_file, 'r', encoding='utf-8')
                self.text_string = ""
                file = f.readlines()

                self.responce_text = "".join(file)
                self.responce_title = QtCore.QFileInfo(custom_file).fileName()

                self.insert_textid_text_db()

                self.create_text(file)
            except UnicodeDecodeError:
                self.textline.setText("Проблемы с кодировкой... Выберите урок или загрузите текст")
                self.animation_error()

    def textline_focus(self):
        self.textline.setFocus()
        self.textline.setCursorPosition(0)

    def clear_result(self):
        self.textline.setText("Выберите урок или загрузите текст")
        self.text_string = ""
        self.number_of_characters = 0
        self.index_current_character = 0
        self.number_of_errors = 0
        self.current_language = "en"
        self.change_language()
        self.text_load = False
        self.symbols_in_second = [0]
        self.clear_timer()
        self.update_results()

    def condition_activity_textline_false(self):
        self.textline.setReadOnly(True)
        self.startstopbutton.setText("Старт")
        self.stop_timer()
        self.highlightingkey.close()
        self.highlightingkeyshift.close()
        if self.text_load and self.condition_activity_textline:
            self.show_results_window()
            self.clear_result()

        self.condition_activity_textline = False
        print("condition_activity_textline_false")

    def condition_activity_textline_true(self):
        self.textline.setReadOnly(False)
        self.condition_activity_textline = True
        self.startstopbutton.setText("Стоп")
        self.number_of_characters = len(self.text_string)
        self.index_current_character = 0
        self.update_results()
        self.highlight_keys()
        self.highlightingkey.show()
        self.textline_focus()
        self.start_timer()
        print("condition_activity_textline_true")

    def start_stop_button_clicked(self):
        if not self.condition_activity_textline and self.text_load:
            self.condition_activity_textline_true()
        else:
            self.condition_activity_textline_false()
            if not self.text_load:
                self.animation_error()

    def animation_error(self):
        self.textline.setReadOnly(True)
        self.textline.setStyleSheet("background-color: rgb(246, 128, 140);\n"
                                    "border: 4px solid #ED1F33;")
        QtTest.QTest.qWait(150)
        self.textline.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                    "border: 4px solid rgb(245, 121, 32);")
        self.textline.setReadOnly(False)

    def keyPressEvent(self, event):
        # if event.key() == QtCore.Qt.Key.Key_Space:
        #    self.animation_error()
        pass

    def set_last_symbol(self, symbol):
        self.lastsymbol.setText(symbol)

    def checking_input_in_textline(self):
        print("checking_input_in_textline")
        cursor_position = self.textline.cursorPosition() - 1
        if len(self.text_string) > 0:
            if len(self.textline.text()) == 0:
                self.textline.setText(self.text_string)
                self.index_current_character += 1
                self.textline_focus()
            elif self.textline.text()[cursor_position] == self.text_string[0]:
                self.set_last_symbol(self.textline.text()[cursor_position])
                self.text_string = self.text_string[1:]
                self.textline.setText(self.text_string)
                self.index_current_character += 1
                self.textline_focus()
            else:
                self.set_last_symbol(self.textline.text()[cursor_position])
                self.textline.setText(self.text_string)
                self.textline_focus()
                self.number_of_errors += 1
                self.animation_error()

        self.update_results()

        if len(self.text_string) == 0:
            self.condition_activity_textline_false()
            self.text_load = False
        else:
            self.highlight_keys()

        print("+", self.text_string, "-", sep="")

    def remake_text(self, text):
        self.text_string = ""
        print(text)
        if len(text) == 0:
            self.text_string = "Empty file, but loaded."
        else:
            for index in range(0, len(text)):
                line = text[index].rstrip()
                print(line)
                self.text_string += line + " "
            self.text_string = self.text_string[:-1]
        self.textline.setText(self.text_string)

    def open_lessons_db(self, key_lesson):
        cursor_lessons = self.main_db.cursor()
        cursor_lessons.execute(f"SELECT * FROM Lessons WHERE lesson LIKE '%{key_lesson}%'")
        title_and_text = cursor_lessons.fetchone()
        self.responce_text = title_and_text[1]
        self.responce_title = title_and_text[0]
        self.create_text([title_and_text[1]])

    def create_text(self, file):
        print(file)
        self.remake_text(file)

        # sys.stdin.close()
        self.textline_focus()
        self.condition_activity_textline_false()
        self.text_load = True

    def update_results(self):
        x = self.index_current_character
        y = self.number_of_characters
        if y != 0:
            percent = int(x / y * 100)
        else:
            percent = "?"
        self.numberofchars.setText("Количество символов: " + str(x) + " из " + str(y) + ", " + str(percent) + "%")

    def show_results_window(self):
        self.resultsWindow = ResultDialogApp()
        self.set_results()
        self.resultsWindow.exec()

    def show_about_window(self):
        self.aboutWindow = AboutDialogApp()
        self.aboutWindow.exec()

    def show_table_results_window(self):
        self.tableWindow = TableDialogApp()
        self.update_table_results()
        self.tableWindow.exec()

    def show_wiki_window(self):
        self.wikiWindow = WikiDialogApp()
        self.add_functions_wiki()
        self.wikiWindow.exec()

    def show_texts_window(self):
        self.textsWindow = TextsDialogApp()
        self.add_functions_texts()
        self.textsWindow.exec()


    def update_table_results(self):
        cursor_table = self.main_db.cursor()
        cursor_table.execute(
            "SELECT date, time, symbols, errors, speed, text FROM user_results, texts WHERE user_results.text_id = texts.title")
        cursor_table_too = self.main_db.cursor()
        cursor_table_too.execute(
            "SELECT date, time, symbols, errors, speed, text FROM user_results, lessons WHERE user_results.text_id = lessons.lesson")
        lines = sorted(list(cursor_table.fetchall() + cursor_table_too.fetchall()), key=lambda tup: tup[0], reverse=True)
        self.tableWindow.table_view.setHorizontalHeaderLabels(
            ["Дата", "Время", "Количество символов", "Количество ошибок", "Скорость", "Текст"])
        self.tableWindow.table_view.setColumnCount(6)
        self.tableWindow.table_view.setRowCount(len(lines))
        print(lines)
        for row_position in range(0, len(lines)):
            for column_position in range(0, 6):
                self.tableWindow.table_view.setItem(row_position, column_position,
                                                    QtWidgets.QTableWidgetItem(lines[row_position][column_position]))

    def add_query_to_table_results(self, data):
        cursor_table = self.main_db.cursor()
        rows = [(str(data[0]), str(data[1]), str(data[2]), str(data[3]), str(data[4]), str(data[5]))]
        cursor_table.executemany('insert into user_results values (?,?,?,?,?,?)', rows)
        self.main_db.commit()

    def set_results(self):
        x = self.index_current_character
        y = self.number_of_characters
        z = self.number_of_errors
        t = self.current_time
        if x != 0:
            if t == 0:
                t = 1
            v = f"{((x / t) * 60):.{2}f}"
            if y != 0:
                percent1 = int(x / y * 100)
            else:
                percent1 = "?"
            if (y + z) != 0:
                percent2 = int(x / (x + z) * 100)
            else:
                percent2 = "?"
        else:
            t = 0
            v = 0
            percent1 = 0
            percent2 = 100

        self.resultsWindow.results.setText(
            "<html><head/><body><p>Время: " + self.seconds_to_str(t) + "</p><p>Количество символов: " + str(
                x) + " из " + str(y) + ", " + str(percent1) + "%</p><p>Количество ошибок: " + str(
                self.number_of_errors) + ", " + str(percent2) + "%</p><p>Скорость: " + str(
                v) + " симв/мин</p></body></html>")
        self.resultsWindow.graphWidget.setBackground('w')
        pen = pyqtgraph.mkPen(color=(245, 121, 32), width=2)
        self.resultsWindow.graphWidget.setMouseEnabled(False, False)
        self.resultsWindow.graphWidget.plot(list(range(0, self.current_time + 1)), self.symbols_in_second, pen=pen)
        date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        self.add_query_to_table_results(
            [date, self.seconds_to_str(t), str(x) + " из " + str(y) + ", " + str(percent1) + "%",
             str(self.number_of_errors) + ", " + str(percent2) + "%", str(v) + " симв/мин", self.responce_title])


class ResultDialogApp(QtWidgets.QDialog, Ui_Statistics):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.retranslateUi(self)


class AboutDialogApp(QtWidgets.QDialog, Ui_About):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.retranslateUi(self)


class TableDialogApp(QtWidgets.QDialog, Ui_Table_results):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.table_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)


class WikiDialogApp(QtWidgets.QDialog, Ui_Wiki):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.retranslateUi(self)


class TextsDialogApp(QtWidgets.QDialog, Ui_Texts):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.retranslateUi(self)


def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainApp()
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
