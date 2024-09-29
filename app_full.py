from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pendulum
from sqlalchemy import create_engine, text
from config import host, port, user, password, database
import subprocess

class Ui_MainWindow(object):

        def get_data_form_db(self, query):
                # Создание строки подключения для SQLAlchemy
                db_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
                # Создание движка SQLAlchemy
                db_engine = create_engine(db_string)
                # Использование pd.read_sql для загрузки таблицы в DataFrame
                df = pd.read_sql(query, con=db_engine)
                return df    
        
        def write_data_from_df(self, df, table_name):
                # Создание строки подключения для SQLAlchemy
                db_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
                # Создание движка SQLAlchemy
                db_engine = create_engine(db_string)
                # Использование pd.read_sql для загрузки таблицы в DataFrame
                df.to_sql(table_name, db_engine, if_exists='append', index=False)

        def write_data(self, query):
                db_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
                # Создание движка SQLAlchemy
                db_engine = create_engine(db_string)
                with db_engine.connect() as connection:
                        connection.execute(text(query))
                        connection.commit()

        def setupUi(self, MainWindow):
                profile_list = [
                        "Прикладная информатика",
                        "Экономика",
                        "Юриспруденция (гражданско-правовой)",
                        "Юриспруденция (уголовно-правовой)"
                        ]
                
                profile_repl_dict = {1: "Прикладная информатика",
                                2: "Экономика",
                                3: "Юриспруденция (гражданско-правовой)",
                                4: "Юриспруденция (уголовно-правовой)"
                                }
                
                publishers = self.get_data_form_db('select * from publishers')

                publishers_repl_dict = publishers[['id', 'publisher_name']].copy().set_index('id')['publisher_name'].to_dict()

                user_types = ['student', 'teacher', 'librarian']


                all_books = self.get_data_form_db('select * from books')

                type_repl = {'student': 'Студент', 'teacher': 'Преподаватель', 'librarian': 'Библиатекарь'}

                book_status_repl = {'in the library': 'В библиотеке', 'in operation': 'На руках'}

                all_users = self.get_data_form_db('select * from users')

                users_repl_dict = all_users[['id', 'full_name']].copy().set_index('id')['full_name'].to_dict()

                MainWindow.setObjectName("MainWindow")
                MainWindow.resize(1164, 855)
                self.centralwidget = QtWidgets.QWidget(MainWindow)
                self.centralwidget.setObjectName("centralwidget")
                self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
                self.tabWidget.setGeometry(QtCore.QRect(10, 0, 1141, 821))
                self.tabWidget.setObjectName("tabWidget")

        #
        #                               BOOK_FIND
        #
                self.book_find = QtWidgets.QWidget()
                self.book_find.setObjectName("book_find")
                self.book_find_table = QtWidgets.QTableWidget(self.book_find)
                self.book_find_table.setGeometry(QtCore.QRect(10, 310, 1111, 471))
                self.book_find_table.setStyleSheet("QTableWidget {\n"
        "    border: 2px solid black; /* Устанавливаем толщину границ таблицы */\n"
        "}\n"
        "\n"
        "QTableWidget::item {\n"
        "    border: 1px solid gray; /* Устанавливаем толщину границ ячеек */\n"
        "}\n"
        "\n"
        "QHeaderView::section {\n"
        "    font-weight: bold; /* Жирный шрифт для заголовков */\n"
        "    background-color: #f0f0f0; /* Цвет фона заголовков (по желанию) */\n"
        "}")
                self.book_find_table.setObjectName("book_find_table")
                all_books_find = all_books.copy()
                all_books_find['profile_id'] = all_books_find['profile_id'].replace(profile_repl_dict)
                all_books_find['book_status'] = all_books_find['book_status'].replace(book_status_repl)
                all_books_find['user_id'] = all_books_find['user_id'].fillna(0).astype(int).replace(users_repl_dict)
                all_books_find['publisher_id'] = all_books_find['profile_id'].fillna(0).replace(publishers_repl_dict)
                all_books_find.sort_values('id', inplace=True)

                # Очистка таблицы перед заполнением новыми данными
                self.book_find_table.setRowCount(0)
                self.book_find_table.setColumnCount(len(all_books_find.columns))  # Устанавливаем количество столбцов
                self.book_find_table.setHorizontalHeaderLabels(['ID', 'Наименование', 'Категория', 'Издательство', 'ISBN', 'Статус', 'Теущий пользователь', 'Дата статуса'])
                for index, row in all_books_find.iterrows():
                        row_position = self.book_find_table.rowCount()
                        self.book_find_table.insertRow(row_position)
                        for column, value in enumerate(row):
                                self.book_find_table.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(value)))
                self.book_find_table.resizeColumnsToContents()

                self.book_find_header = QtWidgets.QLabel(self.book_find)
                self.book_find_header.setGeometry(QtCore.QRect(270, 30, 491, 81))
                self.book_find_header.setStyleSheet("font-size: 30px; /* Установите желаемый размер шрифта */\n""")
                self.book_find_header.setObjectName("book_find_header")
                self.book_find_profile_select = QtWidgets.QComboBox(self.book_find)
                self.book_find_profile_select.setGeometry(QtCore.QRect(30, 130, 341, 51))
                self.book_find_profile_select.setObjectName("book_fin_profile_select")
                self.book_find_profile_select.addItems(profile_list)


                self.book_find_publisher_select = QtWidgets.QComboBox(self.book_find)
                self.book_find_publisher_select.setGeometry(QtCore.QRect(400, 130, 351, 51))
                self.book_find_publisher_select.setObjectName("book_find_publisher_select")
                self.book_find_publisher_select.addItems(publishers['publisher_name'].to_list())
                self.book_find_publisher_select.setEditable(True)
                book_find_publisher_compl = QtWidgets.QCompleter(publishers['publisher_name'].to_list(), self.book_find_publisher_select) # completer
                self.book_find_publisher_select.setCompleter(book_find_publisher_compl)

                self.book_find_status_select = QtWidgets.QComboBox(self.book_find)
                self.book_find_status_select.setGeometry(QtCore.QRect(780, 130, 291, 51))
                self.book_find_status_select.setObjectName("book_find_status_select")
                self.book_find_status_select.addItems(book_status_repl.values())

                self.book_find_profile_label = QtWidgets.QLabel(self.book_find)
                self.book_find_profile_label.setGeometry(QtCore.QRect(20, 180, 341, 61))
                self.book_find_profile_label.setStyleSheet("font-size: 20px")
                self.book_find_profile_label.setObjectName("book_find_profile_label")
                self.book_find_publisher_label = QtWidgets.QLabel(self.book_find)
                self.book_find_publisher_label.setGeometry(QtCore.QRect(440, 180, 291, 61))
                self.book_find_publisher_label.setStyleSheet("font-size: 20px")
                self.book_find_publisher_label.setObjectName("book_find_publisher_label")
                self.book_find_status_label = QtWidgets.QLabel(self.book_find)
                self.book_find_status_label.setGeometry(QtCore.QRect(870, 180, 291, 61))
                self.book_find_status_label.setStyleSheet("font-size: 20px")
                self.book_find_status_label.setObjectName("book_find_status_label")
                self.book_find_confirm = QtWidgets.QPushButton(self.book_find)
                self.book_find_confirm.setGeometry(QtCore.QRect(470, 240, 161, 41))
                self.book_find_confirm.setObjectName("book_find_confirm")
                self.book_find_confirm.clicked.connect(self.book_find_confirm_filter)
                self.tabWidget.addTab(self.book_find, "")

        #
        #                               USER_FIND
        #
                self.user_find = QtWidgets.QWidget()
                self.user_find.setObjectName("user_find")
                self.user_find_table = QtWidgets.QTableWidget(self.user_find)
                self.user_find_table.setGeometry(QtCore.QRect(10, 220, 1101, 531))
                self.user_find_table.setStyleSheet("QTableWidget {\n"
                                                        "    border: 2px solid black; /* Устанавливаем толщину границ таблицы */\n"
                                                        "}\n"
                                                        "\n"
                                                        "QTableWidget::item {\n"
                                                        "    border: 1px solid gray; /* Устанавливаем толщину границ ячеек */\n"
                                                        "}\n"
                                                        "\n"
                                                        "QHeaderView::section {\n"
                                                        "    font-weight: bold; /* Жирный шрифт для заголовков */\n"
                                                        "    background-color: #f0f0f0; /* Цвет фона заголовков (по желанию) */\n"
                                                        "}")
                

                self.user_find_table.setObjectName("user_find_table")
                self.user_find_table.setColumnCount(0)
                self.user_find_table.setRowCount(0)

                all_users_find = all_users.copy().replace(type_repl)
                all_users_find['profile_id'] = all_users_find['profile_id'].replace(profile_repl_dict)
                

                # Очистка таблицы перед заполнением новыми данными
                self.user_find_table.setRowCount(0)
                self.user_find_table.setColumnCount(len(all_users_find.columns))  # Устанавливаем количество столбцов
                self.user_find_table.setHorizontalHeaderLabels(['ID', 'Полное имя', 'Направления обучения', 'Телефон', 'Тип пользователя'])

                # Заполнение таблицы данными
                for index, row in all_users_find.iterrows():
                        row_position = self.user_find_table.rowCount()
                        self.user_find_table.insertRow(row_position)
                        for column, value in enumerate(row):
                                self.user_find_table.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(value)))
                self.user_find_table.resizeColumnsToContents()

                
                self.user_find_header = QtWidgets.QLabel(self.user_find)
                self.user_find_header.setGeometry(QtCore.QRect(360, 0, 441, 81))
                self.user_find_header.setStyleSheet("font-size: 30px; /* Установите желаемый размер шрифта */\n""")
                self.user_find_header.setObjectName("user_find_header")
                self.user_find_profile_select = QtWidgets.QComboBox(self.user_find)
                self.user_find_profile_select.setGeometry(QtCore.QRect(0, 80, 431, 51))
                self.user_find_profile_select.setObjectName("user_find_profile_select")
                self.user_find_profile_select.addItems(profile_list)
                self.user_find_profile_select.setEditable(True)
                user_find_profile_compl = QtWidgets.QCompleter(profile_list, self.user_find_profile_select) # completer
                self.user_find_profile_select.setCompleter(user_find_profile_compl)

                self.user_find_profile_label = QtWidgets.QLabel(self.user_find)
                self.user_find_profile_label.setGeometry(QtCore.QRect(90, 130, 341, 61))
                self.user_find_profile_label.setStyleSheet("font-size: 20px")
                self.user_find_profile_label.setObjectName("user_find_profile_label")
                self.user_find_type_select = QtWidgets.QComboBox(self.user_find)
                self.user_find_type_select.setGeometry(QtCore.QRect(450, 80, 361, 51))
                self.user_find_type_select.setObjectName("user_find_type_select")
                self.user_find_type_select.addItems(user_types)

                self.user_find_type_label = QtWidgets.QLabel(self.user_find)
                self.user_find_type_label.setGeometry(QtCore.QRect(520, 130, 341, 61))
                self.user_find_type_label.setStyleSheet("font-size: 20px")
                self.user_find_type_label.setObjectName("user_find_type_label")
                self.user_find_confirm = QtWidgets.QPushButton(self.user_find)
                self.user_find_confirm.setGeometry(QtCore.QRect(870, 80, 161, 41))
                self.user_find_confirm.setObjectName("user_find_confirm")
                self.user_find_confirm.clicked.connect(self.user_find_confirm_filter)
                self.tabWidget.addTab(self.user_find, "")

        #
        #                               BOOK_ADDITION
        #
                self.book_addition = QtWidgets.QWidget()
                self.book_addition.setObjectName("book_addition")
                self.add_book_title = QtWidgets.QLabel(self.book_addition)
                self.add_book_title.setGeometry(QtCore.QRect(260, 110, 551, 61))
                self.add_book_title.setStyleSheet("font-size: 24px")
                self.add_book_title.setObjectName("add_book_title")
                self.book_add_confirm_button = QtWidgets.QPushButton(self.book_addition)
                self.book_add_confirm_button.setGeometry(QtCore.QRect(350, 570, 311, 71))
                self.book_add_confirm_button.setStyleSheet("font-size: 20px")
                self.book_add_confirm_button.clicked.connect(self.add_book)
                self.book_add_confirm_button.setObjectName("book_add_confirm_button")
                self.book_add_name_edit_label = QtWidgets.QLabel(self.book_addition)
                self.book_add_name_edit_label.setGeometry(QtCore.QRect(570, 230, 401, 61))
                self.book_add_name_edit_label.setStyleSheet("font-size: 20px")
                self.book_add_name_edit_label.setObjectName("book_add_name_edit_label")
                self.book_add_profile_id_label = QtWidgets.QLabel(self.book_addition)
                self.book_add_profile_id_label.setGeometry(QtCore.QRect(570, 310, 491, 61))
                self.book_add_profile_id_label.setStyleSheet("font-size: 20px")
                self.book_add_profile_id_label.setObjectName("book_add_profile_id_label")
                self.book_add_publisher_label = QtWidgets.QLabel(self.book_addition)
                self.book_add_publisher_label.setGeometry(QtCore.QRect(570, 400, 291, 61))
                self.book_add_publisher_label.setStyleSheet("font-size: 20px")
                self.book_add_publisher_label.setObjectName("book_add_publisher_label")
                self.book_add_isbn_edit = QtWidgets.QTextEdit(self.book_addition)
                self.book_add_isbn_edit.setGeometry(QtCore.QRect(30, 480, 521, 51))
                self.book_add_isbn_edit.setObjectName("book_add_isbn_edit")
                self.book_add_isbn_label = QtWidgets.QLabel(self.book_addition)
                self.book_add_isbn_label.setGeometry(QtCore.QRect(580, 480, 261, 61))
                self.book_add_isbn_label.setStyleSheet("font-size: 20px")
                self.book_add_isbn_label.setObjectName("book_add_isbn_label")
                self.book_add_name_edit = QtWidgets.QTextEdit(self.book_addition)
                self.book_add_name_edit.setGeometry(QtCore.QRect(30, 240, 521, 51))
                self.book_add_name_edit.setObjectName("book_name_edit")
                self.book_add_publisher_select = QtWidgets.QComboBox(self.book_addition)
                self.book_add_publisher_select.setGeometry(QtCore.QRect(30, 400, 521, 51))
                self.book_add_publisher_select.setObjectName("book_add_publisher_edit")
                self.book_add_publisher_select.addItems(publishers['publisher_name'].to_list())
                self.book_add_publisher_select.setEditable(True)
                book_add_publisher_compl = QtWidgets.QCompleter(publishers['publisher_name'].to_list(), self.book_add_publisher_select) # completer
                self.book_add_publisher_select.setCompleter(book_add_publisher_compl)

                self.book_add_profile_select = QtWidgets.QComboBox(self.book_addition)
                self.book_add_profile_select.setGeometry(QtCore.QRect(30, 320, 521, 51))
                self.book_add_profile_select.addItems(profile_list)
                self.book_add_profile_select.setObjectName("book_add_profile_select")
                self.tabWidget.addTab(self.book_addition, "")
#
#                               USER_ADD
#
                self.user_add = QtWidgets.QWidget()
                self.user_add.setObjectName("user_add")
                self.user_add_header = QtWidgets.QLabel(self.user_add)
                self.user_add_header.setGeometry(QtCore.QRect(330, 40, 401, 61))
                self.user_add_header.setStyleSheet("font-size: 24px")
                self.user_add_header.setObjectName("user_add_header")
                self.user_add_profile_label = QtWidgets.QLabel(self.user_add)
                self.user_add_profile_label.setGeometry(QtCore.QRect(560, 230, 401, 61))
                self.user_add_profile_label.setStyleSheet("font-size: 20px")
                self.user_add_profile_label.setObjectName("user_add_profile_label")
                self.user_add_type_label = QtWidgets.QLabel(self.user_add)
                self.user_add_type_label.setGeometry(QtCore.QRect(570, 380, 261, 61))
                self.user_add_type_label.setStyleSheet("font-size: 20px")
                self.user_add_type_label.setObjectName("user_add_type_label")
                self.user_add_name_label = QtWidgets.QLabel(self.user_add)
                self.user_add_name_label.setGeometry(QtCore.QRect(560, 160, 261, 61))
                self.user_add_name_label.setStyleSheet("font-size: 20px")
                self.user_add_name_label.setObjectName("user_add_name_label")
                self.user_add_phone_label = QtWidgets.QLabel(self.user_add)
                self.user_add_phone_label.setGeometry(QtCore.QRect(560, 300, 291, 61))
                self.user_add_phone_label.setStyleSheet("font-size: 20px")
                self.user_add_phone_label.setObjectName("user_add_phone_label")
                self.user_add_profile_select = QtWidgets.QComboBox(self.user_add)
                self.user_add_profile_select.setGeometry(QtCore.QRect(10, 240, 521, 51))
                self.user_add_profile_select.addItems(profile_list)
                self.user_add_profile_select.setObjectName("user_add_profile_select")
                self.user_add_name_edit = QtWidgets.QTextEdit(self.user_add)
                self.user_add_name_edit.setGeometry(QtCore.QRect(10, 170, 521, 51))
                self.user_add_name_edit.setObjectName("user_add_name_edit")
                self.user_add_phone_edit = QtWidgets.QTextEdit(self.user_add)
                self.user_add_phone_edit.setGeometry(QtCore.QRect(10, 310, 521, 51))
                self.user_add_phone_edit.setObjectName("user_add_phone_edit")
                self.user_add_type_select = QtWidgets.QComboBox(self.user_add)
                self.user_add_type_select.setGeometry(QtCore.QRect(10, 380, 521, 51))
                self.user_add_type_select.addItems(user_types)
                self.user_add_type_select.setObjectName("user_add_type_select")
                self.user_add_confirm = QtWidgets.QPushButton(self.user_add)
                self.user_add_confirm.setGeometry(QtCore.QRect(340, 480, 311, 71))
                self.user_add_confirm.setStyleSheet("font-size: 20px")
                self.user_add_confirm.setObjectName("user_add_confirm")
                self.user_add_confirm.clicked.connect(self.add_user)
                self.tabWidget.addTab(self.user_add, "")
        #
        #                               BOOK_EX
        #
                self.book_ex = QtWidgets.QWidget()
                self.book_ex.setObjectName("book_ex")
                self.ex_confirm = QtWidgets.QPushButton(self.book_ex)
                self.ex_confirm.setGeometry(QtCore.QRect(430, 510, 181, 71))
                self.ex_confirm.setObjectName("ex_confirm")
                self.ex_confirm.clicked.connect(self.book_ex_confirm)

                self.ex_publisher_label = QtWidgets.QLabel(self.book_ex)
                self.ex_publisher_label.setGeometry(QtCore.QRect(580, 320, 291, 61))
                self.ex_publisher_label.setStyleSheet("font-size: 20px")
                self.ex_publisher_label.setObjectName("ex_publisher_label")
                self.ex_user_name_label = QtWidgets.QLabel(self.book_ex)
                self.ex_user_name_label.setGeometry(QtCore.QRect(580, 250, 401, 61))
                self.ex_user_name_label.setStyleSheet("font-size: 20px")
                self.ex_user_name_label.setObjectName("ex_user_name_label")
                self.ex_book_name_label = QtWidgets.QLabel(self.book_ex)
                self.ex_book_name_label.setGeometry(QtCore.QRect(580, 180, 261, 61))
                self.ex_book_name_label.setStyleSheet("font-size: 20px")
                self.ex_book_name_label.setObjectName("ex_book_name_label")
                self.ex_header = QtWidgets.QLabel(self.book_ex)
                self.ex_header.setGeometry(QtCore.QRect(430, 70, 181, 61))
                self.ex_header.setStyleSheet("font-size: 24px")
                self.ex_header.setObjectName("ex_header")

                self.ex_book_name_select = QtWidgets.QComboBox(self.book_ex)
                self.ex_book_name_select.setGeometry(QtCore.QRect(20, 190, 521, 51))
                self.ex_book_name_select.addItems(all_books['book_name'].to_list())
                self.ex_book_name_select.setObjectName("ex_book_name_select")
                self.ex_book_name_select.setEditable(True)
                ex_book_name_compl = QtWidgets.QCompleter(all_books['book_name'].to_list(), self.ex_book_name_select) # completer
                self.ex_book_name_select.setCompleter(ex_book_name_compl)

                self.ex_user_name_select = QtWidgets.QComboBox(self.book_ex)
                self.ex_user_name_select.setGeometry(QtCore.QRect(20, 260, 521, 51))
                self.ex_user_name_select.addItems(all_users['full_name'].to_list())
                self.ex_user_name_select.setObjectName("ex_user_name_select")
                self.ex_user_name_select.setEditable(True)
                ex_user_name_compl = QtWidgets.QCompleter(all_users['full_name'].to_list(), self.ex_user_name_select) # completer
                self.ex_user_name_select.setCompleter(ex_user_name_compl)

                self.ex_publisher_select = QtWidgets.QComboBox(self.book_ex)
                self.ex_publisher_select.setGeometry(QtCore.QRect(20, 330, 521, 51))
                self.ex_publisher_select.addItems(publishers["publisher_name"].to_list())
                self.ex_publisher_select.setObjectName("ex_publisher_select")
                self.ex_publisher_select.setEditable(True)
                ex_user_publisher_compl = QtWidgets.QCompleter(publishers["publisher_name"].to_list(), self.ex_publisher_select) # completer
                self.ex_publisher_select.setCompleter(ex_user_publisher_compl)

                self.ex_profile_select = QtWidgets.QComboBox(self.book_ex)
                self.ex_profile_select.setGeometry(QtCore.QRect(20, 400, 521, 51))
                self.ex_profile_select.setObjectName("ex_profile_select")
                self.ex_profile_select.addItems(profile_list)

                self.ex_profile_label = QtWidgets.QLabel(self.book_ex)
                self.ex_profile_label.setGeometry(QtCore.QRect(580, 390, 451, 61))
                self.ex_profile_label.setStyleSheet("font-size: 20px")
                self.ex_profile_label.setObjectName("ex_profile_label")
                self.tabWidget.addTab(self.book_ex, "")

        #
        #                               BOOK_INC
        #
                self.book_inc = QtWidgets.QWidget()
                self.book_inc.setObjectName("book_inc")
                self.inc_book_name_label = QtWidgets.QLabel(self.book_inc)
                self.inc_book_name_label.setGeometry(QtCore.QRect(600, 180, 261, 61))
                self.inc_book_name_label.setStyleSheet("font-size: 20px")
                self.inc_book_name_label.setObjectName("inc_book_name_label")
                self.inc_confirm = QtWidgets.QPushButton(self.book_inc)
                self.inc_confirm.setGeometry(QtCore.QRect(450, 510, 181, 71))
                self.inc_confirm.setObjectName("inc_confirm")
                self.inc_confirm.clicked.connect(self.book_inc_confirm)
                self.inc_user_name_label = QtWidgets.QLabel(self.book_inc)
                self.inc_user_name_label.setGeometry(QtCore.QRect(600, 250, 401, 61))
                self.inc_user_name_label.setStyleSheet("font-size: 20px")
                self.inc_user_name_label.setObjectName("inc_user_name_label")
                self.inc_publisher_label = QtWidgets.QLabel(self.book_inc)
                self.inc_publisher_label.setGeometry(QtCore.QRect(600, 320, 291, 61))
                self.inc_publisher_label.setStyleSheet("font-size: 20px")
                self.inc_publisher_label.setObjectName("inc_publisher_label")
                self.inc_header = QtWidgets.QLabel(self.book_inc)
                self.inc_header.setGeometry(QtCore.QRect(410, 70, 181, 61))
                self.inc_header.setStyleSheet("font-size: 24px")
                self.inc_header.setObjectName("inc_header")

                self.inc_book_name_select = QtWidgets.QComboBox(self.book_inc)
                self.inc_book_name_select.setGeometry(QtCore.QRect(50, 190, 521, 51))
                self.inc_book_name_select.addItems(all_books['book_name'].to_list())
                self.inc_book_name_select.setObjectName("inc_book_name_select")
                self.inc_book_name_select.setEditable(True)
                inc_book_name_compl = QtWidgets.QCompleter(all_books['book_name'].to_list(), self.inc_book_name_select) # completer
                self.inc_book_name_select.setCompleter(inc_book_name_compl)

                self.inc_user_name_select = QtWidgets.QComboBox(self.book_inc)
                self.inc_user_name_select.setGeometry(QtCore.QRect(50, 260, 521, 51))
                self.inc_user_name_select.addItems(all_users['full_name'].to_list())
                self.inc_user_name_select.setObjectName("inc_user_name_select")
                self.inc_user_name_select.setEditable(True)
                inc_user_name_compl = QtWidgets.QCompleter(all_users['full_name'].to_list(), self.inc_user_name_select) # completer
                self.inc_user_name_select.setCompleter(inc_user_name_compl)


                self.inc_publisher_select = QtWidgets.QComboBox(self.book_inc)
                self.inc_publisher_select.setGeometry(QtCore.QRect(50, 330, 521, 51))
                self.inc_publisher_select.addItems(publishers['publisher_name'].to_list())
                self.inc_publisher_select.setObjectName("inc_publisher_select")
                self.inc_publisher_select.setEditable(True)
                inc_publisher_compl = QtWidgets.QCompleter(publishers['publisher_name'].to_list(), self.inc_publisher_select) # completer
                self.inc_publisher_select.setCompleter(inc_publisher_compl)

                self.inc_profile_select = QtWidgets.QComboBox(self.book_inc)
                self.inc_profile_select.setGeometry(QtCore.QRect(50, 400, 521, 51))
                self.inc_profile_select.addItems(profile_list)
                self.inc_profile_select.setObjectName("inc_profile_select")
                self.inc_profile_label = QtWidgets.QLabel(self.book_inc)
                self.inc_profile_label.setGeometry(QtCore.QRect(600, 390, 491, 61))
                self.inc_profile_label.setStyleSheet("font-size: 20px")
                self.inc_profile_label.setObjectName("inc_profile_label")
                self.tabWidget.addTab(self.book_inc, "")
                MainWindow.setCentralWidget(self.centralwidget)
                self.menubar = QtWidgets.QMenuBar(MainWindow)
                self.menubar.setGeometry(QtCore.QRect(0, 0, 1164, 21))
                self.menubar.setObjectName("menubar")
                MainWindow.setMenuBar(self.menubar)
                self.statusbar = QtWidgets.QStatusBar(MainWindow)
                self.statusbar.setObjectName("statusbar")
                MainWindow.setStatusBar(self.statusbar)

                self.retranslateUi(MainWindow)
                self.tabWidget.setCurrentIndex(5)
                QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def retranslateUi(self, MainWindow):
                _translate = QtCore.QCoreApplication.translate
                MainWindow.setWindowTitle(_translate("MainWindow", "LIBRARY_IS"))
                self.book_find_header.setText(_translate("MainWindow", "Список библиотечных материалов"))
                self.book_find_profile_label.setText(_translate("MainWindow", "Направление обучения (категория)"))
                self.book_find_publisher_label.setText(_translate("MainWindow", "Наименование издания"))
                self.book_find_status_label.setText(_translate("MainWindow", "Статус"))
                self.book_find_confirm.setText(_translate("MainWindow", "Подтвердить фильтрацию"))
                self.tabWidget.setTabText(self.tabWidget.indexOf(self.book_find), _translate("MainWindow", "Поиск книги"))
                self.user_find_header.setText(_translate("MainWindow", "Список пользователей"))
                self.user_find_profile_label.setText(_translate("MainWindow", "Направление обучения"))
                self.user_find_type_label.setText(_translate("MainWindow", "Тип пользователя"))
                self.user_find_confirm.setText(_translate("MainWindow", "Подтвердить фильтрацию"))
                self.tabWidget.setTabText(self.tabWidget.indexOf(self.user_find), _translate("MainWindow", "Поиск пользователя"))
                self.add_book_title.setText(_translate("MainWindow", "Добавление нового библиотечного материала"))
                self.book_add_confirm_button.setText(_translate("MainWindow", "Добавить"))
                self.book_add_name_edit_label.setText(_translate("MainWindow", "Наименование библиотечного материала"))
                self.book_add_profile_id_label.setText(_translate("MainWindow", "Направление обучения (категория)"))
                self.book_add_publisher_label.setText(_translate("MainWindow", "Наименование издания"))
                self.book_add_isbn_label.setText(_translate("MainWindow", "ISBN"))
                self.tabWidget.setTabText(self.tabWidget.indexOf(self.book_addition), _translate("MainWindow", "Добавить книгу"))
                self.user_add_header.setText(_translate("MainWindow", "Добавление нового пользователя"))
                self.user_add_profile_label.setText(_translate("MainWindow", "Направление обучения"))
                self.user_add_type_label.setText(_translate("MainWindow", "Тип пользователя"))
                self.user_add_name_label.setText(_translate("MainWindow", "Полное имя (ФИО)"))
                self.user_add_phone_label.setText(_translate("MainWindow", "Контактный номер телефона"))
                self.user_add_confirm.setText(_translate("MainWindow", "Добавить"))
                self.tabWidget.setTabText(self.tabWidget.indexOf(self.user_add), _translate("MainWindow", "Добавить пользователя"))
                self.ex_confirm.setText(_translate("MainWindow", "Подтвердить"))
                self.ex_publisher_label.setText(_translate("MainWindow", "Наименование издания"))
                self.ex_user_name_label.setText(_translate("MainWindow", "Полное имя пользователя"))
                self.ex_book_name_label.setText(_translate("MainWindow", "Название книги"))
                self.ex_header.setText(_translate("MainWindow", "Выдача книги"))
                self.ex_profile_label.setText(_translate("MainWindow", "Наименование профиля (категория)"))
                self.tabWidget.setTabText(self.tabWidget.indexOf(self.book_ex), _translate("MainWindow", "Выдача книги"))
                self.inc_book_name_label.setText(_translate("MainWindow", "Название книги"))
                self.inc_confirm.setText(_translate("MainWindow", "Подтвердить"))
                self.inc_user_name_label.setText(_translate("MainWindow", "Полное имя пользователя"))
                self.inc_publisher_label.setText(_translate("MainWindow", "Наименование издания"))
                self.inc_header.setText(_translate("MainWindow", "Возврат книги"))
                self.inc_profile_label.setText(_translate("MainWindow", "Направление обучения (категория)"))
                self.tabWidget.setTabText(self.tabWidget.indexOf(self.book_inc), _translate("MainWindow", "Возврат книги"))

        def add_user(self):
                # Сбор данных из текстовых полей
                user_name = self.user_add_name_edit.toPlainText().strip()
                profile_name = self.user_add_profile_select.currentText()  # Получаем выбранный элемент из QComboBox
                phone = self.user_add_phone_edit.toPlainText().strip()
                user_type = self.user_add_type_select.currentText()

                # Проверка на заполнение всех полей
                if not all([user_name, profile_name, phone, user_type]):
                        QtWidgets.QMessageBox.warning(None, "Ошибка", "Пожалуйста, заполните все поля.")

                profile_dict = {"Прикладная информатика": 1,
                                "Экономика": 2,
                                "Юриспруденция (гражданско-правовой)": 3,
                                "Юриспруденция (уголовно-правовой)": 4
                                }
                
                profile_id = profile_dict[profile_name]

                publishers = self.get_data_form_db('select * from publishers')

                user_data = {'id': [self.get_data_form_db('select max(id) from users').iloc[0].item() + 1],
                        'full_name': [user_name],
                        'profile_id': [profile_id],
                        'contact_phone_number': [phone],
                        'user_type': [user_type]
                        }
                user_df = pd.DataFrame(user_data)

                all_user = self.get_data_form_db('select * from users')
                if all_user[(all_user.full_name == user_data['full_name'][0])&\
                                (all_user.profile_id == user_data['profile_id'][0])&\
                                (all_user.contact_phone_number == user_data['contact_phone_number'][0])&\
                                (all_user.user_type == user_data['user_type'][0])].empty:
                        self.write_data_from_df(user_df, 'users')
                        QtWidgets.QMessageBox.information(None, "Успех", "Добавление выполнено успешно!")
                else:
                        QtWidgets.QMessageBox.warning(None, "Ошибка", "Такой пользователь уже есть.")

        def add_book(self):
                # Сбор данных из текстовых полей
                book_name = self.book_add_name_edit.toPlainText().strip()
                profile_name = self.book_add_profile_select.currentText()  # Получаем выбранный элемент из QComboBox
                publisher_name = self.book_add_publisher_select.currentText()
                isbn = self.book_add_isbn_edit.toPlainText().strip()

                # Проверка на заполнение всех полей
                if not all([book_name, profile_name, publisher_name, isbn]):
                        QtWidgets.QMessageBox.warning(None, "Ошибка", "Пожалуйста, заполните все поля.")

                profile_dict = {"Прикладная информатика": 1,
                                "Экономика": 2,
                                "Юриспруденция (гражданско-правовой)": 3,
                                "Юриспруденция (уголовно-правовой)": 4
                                }
                
                profile_id = profile_dict[profile_name]

                publishers = self.get_data_form_db('select * from publishers')

                publisher_id = publishers[publishers.publisher_name == publisher_name]['id'].item()

                book_data = {'id': [self.get_data_form_db('select max(id) from books').iloc[0].item() + 1],
                        'book_name': [book_name],
                        'profile_id': [profile_id],
                        'publisher_id': [publisher_id],
                        'isbn': [isbn],
                        'book_status': ['in the library'],
                        'user_id': [0],
                        'status_date': datetime.now()
                        }
                book_df = pd.DataFrame(book_data)

                all_books = self.get_data_form_db('select * from books')
                if all_books[(all_books.book_name == book_data['book_name'][0])&\
                                (all_books.isbn == book_data['isbn'][0])&\
                                (all_books.publisher_id == book_data['publisher_id'][0])].empty:
                        self.write_data_from_df(book_df, 'books')
                        QtWidgets.QMessageBox.information(None, "Успех", "Добавление выполнено успешно!")
                else:
                        QtWidgets.QMessageBox.warning(None, "Ошибка", "Такая книга уже есть.")

        def book_inc_confirm(self):
                book_name = self.inc_book_name_select.currentText()
                user_name = self.inc_user_name_select.currentText()
                publisher_name = self.inc_publisher_select.currentText()
                profile_name = self.inc_profile_select.currentText()

                profile_dict = {"Прикладная информатика": 1,
                                "Экономика": 2,
                                "Юриспруденция (гражданско-правовой)": 3,
                                "Юриспруденция (уголовно-правовой)": 4
                                }
                
                profile_id = profile_dict[profile_name]
                users = self.get_data_form_db('select * from users')
                publishers = self.get_data_form_db('select * from publishers')
                publisher_id = publishers[publishers['publisher_name'] == publisher_name]['id'].item()
                query = f"""
                        select * from books
                        where book_name = '{book_name}'
                        and publisher_id = {publisher_id}
                        and profile_id = {profile_id}
                        and book_status = 'in operation'
                        limit 1
                        """
                book_in_db = self.get_data_form_db(query)

                if book_in_db.empty:
                        QtWidgets.QMessageBox.warning(None, "Ошибка", "Такой книги нет или она находится в библиотеке.")
                else:   
                        query = f"""
                                UPDATE books
                                SET book_status = 'in the library'
                                WHERE id = {book_in_db['id'].item()}
                                """
                        self.write_data(query)
                        QtWidgets.QMessageBox.information(None, "Успех", "Успешный возврат!")

        def book_ex_confirm(self):
                book_name = self.inc_book_name_select.currentText()
                user_name = self.inc_user_name_select.currentText()
                publisher_name = self.inc_publisher_select.currentText()
                profile_name = self.inc_profile_select.currentText()

                profile_dict = {"Прикладная информатика": 1,
                                "Экономика": 2,
                                "Юриспруденция (гражданско-правовой)": 3,
                                "Юриспруденция (уголовно-правовой)": 4
                                }
                
                profile_id = profile_dict[profile_name]
                users = self.get_data_form_db('select * from users')
                publishers = self.get_data_form_db('select * from publishers')
                publisher_id = publishers[publishers['publisher_name'] == publisher_name]['id'].item()
                query = f"""
                        select * from books
                        where book_name = '{book_name}'
                        and publisher_id = {publisher_id}
                        and profile_id = {profile_id}
                        and book_status = 'in the library'
                        limit 1
                        """
                book_in_db = self.get_data_form_db(query)

                if book_in_db.empty:
                        QtWidgets.QMessageBox.warning(None, "Ошибка", "Такой книги нет или она на руках.")
                else:   
                        query = f"""
                                UPDATE books
                                SET book_status = 'in operation'
                                WHERE id = {book_in_db['id'].item()}
                                """
                        self.write_data(query)
                        QtWidgets.QMessageBox.information(None, "Успех", "Книга успешно выдана!")

        def user_find_confirm_filter(self):

                profile_dict = {"Прикладная информатика": 1,
                                "Экономика": 2,
                                "Юриспруденция (гражданско-правовой)": 3,
                                "Юриспруденция (уголовно-правовой)": 4
                                }
                
                profile_repl_dict = {1: "Прикладная информатика",
                                2: "Экономика",
                                3: "Юриспруденция (гражданско-правовой)",
                                4: "Юриспруденция (уголовно-правовой)"
                                }
                
                type_repl = {'student': 'Студент', 'teacher': 'Преподаватель', 'librarian': 'Библиатекарь'}

                all_users = self.get_data_form_db('select * from users')
                profile_filter = profile_dict[self.user_find_profile_select.currentText()]
                type_filter = self.user_find_type_select.currentText()


                all_users = all_users[(all_users.profile_id == profile_filter) & (all_users.user_type == type_filter)].replace(type_repl)

                all_users['profile_id'] = all_users['profile_id'].replace(profile_repl_dict)

                # Очистка таблицы перед заполнением новыми данными
                self.user_find_table.setRowCount(0)
                self.user_find_table.setColumnCount(len(all_users.columns))  # Устанавливаем количество столбцов
                self.user_find_table.setHorizontalHeaderLabels(['ID', 'Полное имя', 'ID направления обучения', 'Телефон', 'Тип пользователя'])

                # Заполнение таблицы данными
                for index, row in all_users.iterrows():
                        row_position = self.user_find_table.rowCount()
                        self.user_find_table.insertRow(row_position)
                        for column, value in enumerate(row):
                                self.user_find_table.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(value)))
                self.user_find_table.resizeColumnsToContents()

        def book_find_confirm_filter(self):

                all_users = self.get_data_form_db('select * from users')

                users_repl_dict = all_users[['id', 'full_name']].copy().set_index('id')['full_name'].to_dict()

                publishers = self.get_data_form_db('select * from publishers')

                publishers_repl_dict = publishers[['id', 'publisher_name']].copy().set_index('id')['publisher_name'].to_dict()

                book_status_filter = self.book_find_status_select.currentText()
                book_profile_filter = self.book_find_profile_select.currentText()
                book_publisher_filter = self.book_find_publisher_select.currentText()

                profile_name_to_id = {"Прикладная информатика": 1,
                                "Экономика": 2,
                                "Юриспруденция (гражданско-правовой)": 3,
                                "Юриспруденция (уголовно-правовой)": 4
                                }
                
                profile_repl_dict = {1: "Прикладная информатика",
                                2: "Экономика",
                                3: "Юриспруденция (гражданско-правовой)",
                                4: "Юриспруденция (уголовно-правовой)"
                                }
                
                book_status_repl = {'В библиотеке': 'in the library', 'На руках': 'in operation'}
                
                book_profile_filter = profile_name_to_id[book_profile_filter]
                book_publisher_filter = publishers[publishers.publisher_name == book_publisher_filter]['id'].item()
                book_status_filter = book_status_repl[book_status_filter]

                book_status_repl = {'in the library': 'В библиотеке', 'in operation': 'На руках'}

                all_books = self.get_data_form_db('select * from books')
                all_books_find = all_books[(all_books.profile_id == book_profile_filter)&\
                                           (all_books.publisher_id == book_publisher_filter)&\
                                           (all_books.book_status == book_status_filter)]
                
                all_books_find['profile_id'] = all_books_find['profile_id'].replace(profile_repl_dict)
                all_books_find['book_status'] = all_books_find['book_status'].replace(book_status_repl)
                all_books_find['user_id'] = all_books_find['user_id'].fillna(0).astype(int).replace(users_repl_dict)
                all_books_find['publisher_id'] = all_books_find['profile_id'].fillna(0).replace(publishers_repl_dict)
                all_books_find.sort_values('id', inplace=True)

                # Очистка таблицы перед заполнением новыми данными
                self.book_find_table.setRowCount(0)
                self.book_find_table.setColumnCount(len(all_books_find.columns))  # Устанавливаем количество столбцов
                self.book_find_table.setHorizontalHeaderLabels(['ID', 'Наименование', 'Категория', 'Издательство', 'ISBN', 'Статус', 'Теущий пользователь', 'Дата статуса'])
                for index, row in all_books_find.iterrows():
                        row_position = self.book_find_table.rowCount()
                        self.book_find_table.insertRow(row_position)
                        for column, value in enumerate(row):
                                self.book_find_table.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(value)))
                self.book_find_table.resizeColumnsToContents()

                

    
                


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setStyle("Fusion")
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
