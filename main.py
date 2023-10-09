from tkinter import ttk, messagebox
from tkinter.ttk import Treeview
import pymysql.cursors
from config import host, user, password, db_name
import tkinter as tk
from tkinter import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import logging


logging.basicConfig(filename='app.log', level=logging.INFO, filemode='w')
try:
    connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("successfully connect")
    print("#" * 20)

except Exception as ex:
    print("Connection refused...")
    print(ex)

class DatabaseAuthApp:
    def __init__(self):
        self.current_user = ""
        self.root = tk.Tk()
        self.root.title("Авторизація в базі даних")
        self.root.geometry("340x280")

        # Создание элементов интерфейса
        self.label_username = tk.Label(self.root, text="Логін:", font=("Arial", 11))
        self.entry_username = tk.Entry(self.root)
        self.label_password = tk.Label(self.root, text="Пароль:", font=("Arial", 11))
        self.entry_password = tk.Entry(self.root, show="*")
        self.button_login = tk.Button(self.root, text="Ок", font=("Arial", 11), command=self.login)

        # Размещение элементов интерфейса
        self.label_username.place(x=150, y=50)
        self.entry_username.place(x=110, y=75)
        self.label_password.place(x=140, y=100)
        self.entry_password.place(x=110, y=125)
        self.button_login.place(x=150, y=160)

        self.root.mainloop()

    def login(self):
        username = self.entry_username.get()
        password_user = self.entry_password.get()

        with connection.cursor() as cursor:
            query = "SELECT Email, Password, Role FROM Users;"
            cursor.execute(query)

            rows = cursor.fetchall()
            for row in rows:
                if row['Email'] == username:
                    if row['Password'] == password_user:
                        if row['Role'] == 'admin':
                            self.all_table()
                            self.current_user = "Адмін"
                            logging.info("Ви зайшли як Адмін!")
                        elif row['Role'] == 'manager':
                            self.choice()
                            print(2)
                            self.current_user = "Менеджер"
                            logging.info("Ви зайшли як Менеджер!")
                        elif row['Role'] == 'user':
                            self.current_user = "User"
                            messagebox.showinfo("Message", "Ви звичайний користувач, ви не маєете доступу до БД.")
                print(row)

        self.root.mainloop()

    def choice(self):
        self.root.destroy()
        self.root = Tk()
        self.root.title("Database Viewer")
        self.root.geometry("300x200")

        self.crud = Button(self.root, text="CRUD", command=self.all_table, width=15, height=2)
        self.crud.pack(pady=20)

        self.plain = Button(self.root, text="20 QUERIES", command=self.all_queries, width=15, height=2)
        self.plain.pack()

    def all_queries(self):
        logging.info(f"{self.current_user} вибрав all_queries")
        self.root.destroy()
        self.root = tk.Tk()
        self.root.title("Авторизация в базе данных")
        self.root.configure(bg="Gainsboro")
        self.root.geometry("1050x450")
        self.label_title = tk.Label(self.root, text="Запити до БД", font=("Arial", 14))
        self.label_title.place(x=450, y=0)

        self.label_query1 = tk.Label(self.root, text="1) Виконує вибірку даних про пацієнтів та їх діагнози зі зв'язаних \n таблиць і сортує результат за прізвищем пацієнтів",
                                     font=("Arial", 9))

        self.label_query1.place(x=0, y=32)
        self.btn_query1 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query1)
        self.btn_query1.place(x=400, y=30)


        self.label_query2 = tk.Label(self.root, text="2) Виконує вибірку даних про працівників та їх посади зі\nзв'язаних таблиць і сортує результат за назвою посади",
                                     font=("Arial", 9))
        self.label_query2.place(x=0, y=72)
        self.btn_query2 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query2)
        self.btn_query2.place(x=400, y=70)

        self.label_query3 = tk.Label(self.root, text="3) Виконує вибірку пацієнтів, чиє ім`я починається з літери 'А'",
                                     font=("Arial", 9))
        self.label_query3.place(x=0, y=112)
        self.btn_query3 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query3)
        self.btn_query3.place(x=400, y=110)

        self.label_query4 = tk.Label(self.root,
                                     text="4) Виконує вибірку постачальників, у яких прізвище містить\nлітеру 'о'",
                                     font=("Arial", 9))
        self.label_query4.place(x=0, y=152)
        self.btn_query4 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query4)
        self.btn_query4.place(x=400, y=150)

        self.label_query5 = tk.Label(self.root,
                                     text="5) Виконує вибірку пацієнтів, які народилися між\n1980 та 1990 роками",
                                     font=("Arial", 9))
        self.label_query5.place(x=0, y=192)
        self.btn_query5 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query5)
        self.btn_query5.place(x=400, y=190)


        self.label_query6 = tk.Label(self.root,
                                     text="6) Виконує вибірку працівників, у яких обсяг виконаної\nроботи знаходиться у діапазоні від 100 до 200",
                                     font=("Arial", 9))
        self.label_query6.place(x=0, y=232)
        self.btn_query6 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query6)
        self.btn_query6.place(x=400, y=230)

        self.label_query7 = tk.Label(self.root,
                                     text="7) Отримується загальна кількість виконаної роботи\nвсіма працівниками'.",
                                     font=("Arial", 9))
        self.label_query7.place(x=0, y=272)
        self.btn_query7 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query7)
        self.btn_query7.place(x=400, y=270)

        self.label_query8 = tk.Label(self.root,
                                     text="8) Запит, який показує середню ціну поставки ліків",
                                     font=("Arial", 9))
        self.label_query8.place(x=0, y=312)
        self.btn_query8 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query8)
        self.btn_query8.place(x=400, y=310)

        self.label_query9 = tk.Label(self.root,
                                     text="9) Цей запит об'єднує дані про працівників з посадами з \n id 1 і 2, включаючи стовпець id_посади, у один результат",
                                     font=("Arial", 9))
        self.label_query9.place(x=0, y=342)
        self.btn_query9 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query9)
        self.btn_query9.place(x=400, y=340)

        self.label_query10 = tk.Label(self.root,
                                      text="10) Виконує підрахунок сумарного обсягу виконаної роботи\nдля кожної бригади",
                                      font=("Arial", 9))
        self.label_query10.place(x=0, y=382)
        self.btn_query10 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query10)
        self.btn_query10.place(x=400, y=380)

        self.label_query11 = tk.Label(self.root, text="11) Дані про працівників, які мають більший обсяг виконаної роботи ніж \n будь-який працівник з посадою з ідентифікатором 1",
                                      font=("Arial", 9))
        self.label_query11.place(x=500, y=32)
        self.btn_query11 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query11)
        self.btn_query11.place(x=980, y=30)

        self.label_query12 = tk.Label(self.root,
                                      text="12) Дані про працівників, які мають більший обсяг виконаної роботи ніж \n будь-який працівник з посадою з ідентифікатором 1",
                                      font=("Arial", 9))
        self.label_query12.place(x=500, y=72)
        self.btn_query12 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query12)
        self.btn_query12.place(x=980, y=70)

        self.label_query13 = tk.Label(self.root,
                                      text="13) Постачальники, які мають хоча б одну поставку\nз ціною вище середньої ціни поставок",
                                      font=("Arial", 9))
        self.label_query13.place(x=500, y=112)
        self.btn_query13 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query13)
        self.btn_query13.place(x=980, y=110)

        self.label_query14 = tk.Label(self.root,
                                      text="14) Праціники, які мають більше обсягу виконаної роботи, \n ніж будь-який працівник з посадою 'Медсестра'",
                                      font=("Arial", 9))
        self.label_query14.place(x=500, y=152)
        self.btn_query14 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query14)
        self.btn_query14.place(x=980, y=150)

        self.label_query15 = tk.Label(self.root,
                                      text="15) Постачальники, які не мають жодного запису в таблиці Поставка_ліків",
                                      font=("Arial", 9))
        self.label_query15.place(x=500, y=192)
        self.btn_query15 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query15)
        self.btn_query15.place(x=980, y=190)

        self.label_query16 = tk.Label(self.root,
                                      text="16) Отримання посад, у яких немає жодного працівника.",
                                      font=("Arial", 9))
        self.label_query16.place(x=500, y=232)
        self.btn_query16 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query16)
        self.btn_query16.place(x=980, y=230)

        self.label_query17 = tk.Label(self.root,
                                      text="17)Цей запит об'єднує дані про посади з коментарями",
                                      font=("Arial", 9))
        self.label_query17.place(x=500, y=272)
        self.btn_query17 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query17)
        self.btn_query17.place(x=980, y=270)

        self.label_query18 = tk.Label(self.root,
                                      text="18) Об'єднує дві таблиці 'Посада' і 'Постачальник'",
                                      font=("Arial", 9))
        self.label_query18.place(x=500, y=312)
        self.btn_query18 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query18)
        self.btn_query18.place(x=980, y=310)

        self.label_query19 = tk.Label(self.root,
                                      text="19) Запит вибирає всіх працівників, чия посада є 'Лікар'",
                                      font=("Arial", 9))
        self.label_query19.place(x=500, y=352)
        self.btn_query19 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query19)
        self.btn_query19.place(x=980, y=350)

        self.label_query20 = tk.Label(self.root,
                                      text="20) Всі постачальники, які мають поставки ліків з ціною за одиницю менше 100",
                                      font=("Arial", 9))
        self.label_query20.place(x=500, y=392)
        self.btn_query20 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query20)
        self.btn_query20.place(x=980, y=390)

        self.root.mainloop()


    def export_to_pdf(self, title):
        logging.info(f"{self.current_user} роздрукував {title}")
        pdf_filename = f"{title}"
        c = canvas.Canvas(pdf_filename, pagesize=letter)

        # Определяем ширины столбцов
        column_widths = [100, 100, 100]

        # Добавляем заголовки
        for i, column in enumerate(self.columns):
            c.setFont("Helvetica-Bold", 12)
            c.drawString(sum(column_widths[:i]) + 20, 750, column)

        # Добавляем данные
        for row_num, row in enumerate(self.tree.get_children()):
            y = 700 - (row_num + 1) * 20
            values = [self.tree.item(row)["values"][i] for i in range(len(self.columns))]
            for i, value in enumerate(values):
                c.setFont("Helvetica", 12)
                c.drawString(sum(column_widths[:i]) + 20, y, str(value))

        # Сохраняем и закрываем PDF-документ
        c.save()
        print(f"Результаты запроса сохранены в файл: {title}")

    def query1(self):
        logging.info(f"{self.current_user} вибрав query1")
        self.query1 = tk.Tk()
        self.query1.title("Запит №1")
        self.query1.geometry("1000x500")

        self.label_title_q1 = tk.Label(self.query1,
                                       text="Результати запиту",
                                       font=("Arial", 13))
        self.label_title_q1.pack()

        # определяем столбцы
        self.columns = ("id_patient1", "name", "surname", "patronymic", "adress", "symptom", "id_diagnosis", "title", "criticality", "prescribed_medicines", "id_patient", "id_Employee")

        self.tree = ttk.Treeview(self.query1, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("id_patient1", text="id_пацієнта", anchor=W)
        self.tree.heading("name", text="Ім_я", anchor=W)
        self.tree.heading("surname", text="Прізвище", anchor=W)
        self.tree.heading("patronymic", text="По_батькові", anchor=W)
        self.tree.heading("adress", text="Адреса_мешкання", anchor=W)
        self.tree.heading("symptom", text="Симптом", anchor=W)
        self.tree.heading("id_diagnosis", text="id_діагноза", anchor=W)
        self.tree.heading("title", text="Назва", anchor=W)
        self.tree.heading("criticality", text="Критичність", anchor=W)
        self.tree.heading("prescribed_medicines", text="Призначенні_ліки", anchor=W)
        self.tree.heading("id_patient", text="id_пацієнта", anchor=W)
        self.tree.heading("id_Employee", text="id_працівника", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=110)
        self.tree.column("#2", stretch=NO, width=110)
        self.tree.column("#3", stretch=NO, width=110)
        self.tree.column("#4", stretch=NO, width=110)
        self.tree.column("#5", stretch=NO, width=110)
        self.tree.column("#6", stretch=NO, width=110)
        self.tree.column("#7", stretch=NO, width=110)
        self.tree.column("#8", stretch=NO, width=110)
        self.tree.column("#9", stretch=NO, width=110)
        self.tree.column("#10", stretch=NO, width=110)
        self.tree.column("#11", stretch=NO, width=110)
        self.tree.column("#12", stretch=NO, width=110)

        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT Пацієнт.*, Діагноз.* FROM Пацієнт JOIN Діагноз ON Пацієнт.id_пацієнта = Діагноз.id_пацієнта ORDER BY Пацієнт.Прізвище;"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", END, values=(row["id_пацієнта"], row["Ім_я"], row["Прізвище"], row["По_батькові"], row["Адреса_мешкання"], row["Симптом"], row["id_діагноза"], row["Назва"], row["Критичність"], row["Призначенні_ліки"], row["id_пацієнта"], row["id_працівника"]))


        # добавляем полосу прокрутки по горизонтали
        self.scrollbar_x = ttk.Scrollbar(self.query1, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)

        self.button_export = tk.Button(self.query1, text="Експорт в PDF",
                                       command=lambda: self.export_to_pdf("query1.pdf"))
        self.button_export.pack()

        self.query1.mainloop()

    def query2(self):
        logging.info(f"{self.current_user} вибрав query2")
        self.query2 = tk.Tk()
        self.query2.title("Запит №2")
        self.query2.geometry("1000x500")

        self.label_title_q2 = tk.Label(self.query2,
                                       text="Результати запиту",
                                       font=("Arial", 13))
        self.label_title_q2.pack()

        # определяем столбцы
        self.columns = ("id_Employee", "name", "surname", "patronymic", "date_of_birthday", "workload", "id_job", "id_brigade", "id_job2", "title")

        self.tree = ttk.Treeview(self.query2, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("id_Employee", text="id_працівника", anchor=W)
        self.tree.heading("name", text="Ім_я", anchor=W)
        self.tree.heading("surname", text="Прізвище", anchor=W)
        self.tree.heading("patronymic", text="По_батькові", anchor=W)
        self.tree.heading("date_of_birthday", text="Дата_народження", anchor=W)
        self.tree.heading("workload", text="Об_єм_виконаної_роботи", anchor=W)
        self.tree.heading("id_job", text="id_посади", anchor=W)
        self.tree.heading("id_brigade", text="id_бригади", anchor=W)
        self.tree.heading("id_job2", text="id_посади", anchor=W)
        self.tree.heading("title", text="Назва", anchor=W)


        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=110)
        self.tree.column("#2", stretch=NO, width=110)
        self.tree.column("#3", stretch=NO, width=110)
        self.tree.column("#4", stretch=NO, width=110)
        self.tree.column("#5", stretch=NO, width=110)
        self.tree.column("#6", stretch=NO, width=150)
        self.tree.column("#7", stretch=NO, width=110)
        self.tree.column("#8", stretch=NO, width=110)
        self.tree.column("#9", stretch=NO, width=110)
        self.tree.column("#10", stretch=NO, width=110)


        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT Працівник.*, Посада.* FROM Працівник JOIN Посада ON Працівник.id_посади = Посада.id_посади ORDER BY Посада.Назва;"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", END, values=(row["id_працівника"], row["Ім_я"], row["Прізвище"], row["По_батькові"], row["Дата_народження"], row["Об_єм_виконаної_роботи"], row["id_посади"], row["id_бригади"], row["id_посади"], row["Назва"]))

        # добавляем полосу прокрутки по горизонтали
        self.scrollbar_x = ttk.Scrollbar(self.query2, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)

        self.button_export = tk.Button(self.query2, text="Експорт в PDF",
                                       command=lambda: self.export_to_pdf("query2.pdf"))
        self.button_export.pack()

        self.query2.mainloop()

    def query3(self):
        logging.info(f"{self.current_user} вибрав query3")
        self.query3 = tk.Tk()
        self.query3.title("Запит №3")
        self.query3.geometry("1000x500")

        self.label_title_q3 = tk.Label(self.query3,
                                       text="Результати запиту",
                                       font=("Arial", 13))
        self.label_title_q3.pack()

        # определяем столбцы
        self.columns = ("id_patient", "name", "surname", "patronymic", "adress", "symptom")

        self.tree = ttk.Treeview(self.query3, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("id_patient", text="id_пацієнта", anchor=W)
        self.tree.heading("name", text="Ім_я", anchor=W)
        self.tree.heading("surname", text="Прізвище", anchor=W)
        self.tree.heading("patronymic", text="По_батькові", anchor=W)
        self.tree.heading("adress", text="Адреса_мешкання", anchor=W)
        self.tree.heading("symptom", text="Симптом", anchor=W)


        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=120)
        self.tree.column("#2", stretch=NO, width=120)
        self.tree.column("#3", stretch=NO, width=120)
        self.tree.column("#4", stretch=NO, width=120)
        self.tree.column("#5", stretch=NO, width=120)
        self.tree.column("#6", stretch=NO, width=120)


        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT * FROM Пацієнт WHERE Ім_я LIKE 'О%';"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", END, values=(row["id_пацієнта"], row["Ім_я"], row["Прізвище"], row["По_батькові"], row["Адреса_мешкання"], row["Симптом"]))


        # добавляем полосу прокрутки по горизонтали
        self.scrollbar_x = ttk.Scrollbar(self.query3, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)

        self.button_export = tk.Button(self.query3, text="Експорт в PDF",
                                       command=lambda: self.export_to_pdf("query3.pdf"))
        self.button_export.pack()

        self.query3.mainloop()

    def query4(self):
        logging.info(f"{self.current_user} вибрав query4")
        self.query4 = tk.Tk()
        self.query4.title("Запит №4")
        self.query4.geometry("1000x500")

        self.label_title_q4 = tk.Label(self.query4,
                                       text="Результати запиту",
                                       font=("Arial", 13))
        self.label_title_q4.pack()

        # определяем столбцы
        self.columns = ("id_vendor", "name", "surname", "patronymic")

        self.tree = ttk.Treeview(self.query4, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("id_vendor", text="id_постачальника", anchor=W)
        self.tree.heading("name", text="Ім_я", anchor=W)
        self.tree.heading("surname", text="Прізвище", anchor=W)
        self.tree.heading("patronymic", text="По_батькові", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=120)
        self.tree.column("#2", stretch=NO, width=120)
        self.tree.column("#3", stretch=NO, width=120)
        self.tree.column("#4", stretch=NO, width=120)

        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT * FROM Постачальник WHERE Прізвище LIKE '%о%';"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", END, values=(row["id_постачальника"], row["Ім_я"], row["Прізвище"], row["По_батькові"]))


        # добавляем полосу прокрутки по горизонтали
        self.scrollbar_x = ttk.Scrollbar(self.query4, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)

        self.button_export = tk.Button(self.query4, text="Експорт в PDF",
                                       command=lambda: self.export_to_pdf("query4.pdf"))
        self.button_export.pack()

        self.query4.mainloop()

    def query5(self):
        logging.info(f"{self.current_user} вибрав query5")
        self.query5 = tk.Tk()
        self.query5.title("Запит №5")
        self.query5.geometry("1000x500")

        self.label_title_q5 = tk.Label(self.query5,
                                       text="Результати запиту",
                                       font=("Arial", 13))
        self.label_title_q5.pack()

        # определяем столбцы
        self.columns = ("id_Employee", "name", "surname", "patronymic", "date_of_birthday", "workload", "id_job", "id_brigade")

        self.tree = ttk.Treeview(self.query5, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("id_Employee", text="id_працівника", anchor=W)
        self.tree.heading("name", text="Ім_я", anchor=W)
        self.tree.heading("surname", text="Прізвище", anchor=W)
        self.tree.heading("patronymic", text="По_батькові", anchor=W)
        self.tree.heading("date_of_birthday", text="Дата_народження", anchor=W)
        self.tree.heading("workload", text="Об_єм_виконаної_роботи", anchor=W)
        self.tree.heading("id_job", text="id_посади", anchor=W)
        self.tree.heading("id_brigade", text="id_бригади", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=110)
        self.tree.column("#2", stretch=NO, width=110)
        self.tree.column("#3", stretch=NO, width=110)
        self.tree.column("#4", stretch=NO, width=110)
        self.tree.column("#5", stretch=NO, width=110)
        self.tree.column("#6", stretch=NO, width=150)
        self.tree.column("#7", stretch=NO, width=110)
        self.tree.column("#8", stretch=NO, width=110)

        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT * FROM Працівник WHERE Дата_народження BETWEEN '1980-01-01' AND '1990-12-31';"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", END, values=(row["id_працівника"], row["Ім_я"], row["Прізвище"], row["По_батькові"], row["Дата_народження"], row["Об_єм_виконаної_роботи"], row["id_посади"], row["id_бригади"]))

        self.scrollbar_x = ttk.Scrollbar(self.query5, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)

        self.button_export = tk.Button(self.query5, text="Експорт в PDF",
                                       command=lambda: self.export_to_pdf("query5.pdf"))
        self.button_export.pack()

        self.query5.mainloop()


    def query6(self):
        logging.info(f"{self.current_user} вибрав query6")
        self.query6 = tk.Tk()
        self.query6.title("Запит №6")
        self.query6.geometry("1000x500")

        self.label_title_q6 = tk.Label(self.query6,
                                       text="Результати запиту",
                                       font=("Arial", 13))
        self.label_title_q6.pack()

        # определяем столбцы
        self.columns = ("id_Employee", "name", "surname", "patronymic", "date_of_birthday", "workload", "id_job", "id_brigade")

        self.tree = ttk.Treeview(self.query6, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("id_Employee", text="id_працівника", anchor=W)
        self.tree.heading("name", text="Ім_я", anchor=W)
        self.tree.heading("surname", text="Прізвище", anchor=W)
        self.tree.heading("patronymic", text="По_батькові", anchor=W)
        self.tree.heading("date_of_birthday", text="Дата_народження", anchor=W)
        self.tree.heading("workload", text="Об_єм_виконаної_роботи", anchor=W)
        self.tree.heading("id_job", text="id_посади", anchor=W)
        self.tree.heading("id_brigade", text="id_бригади", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=110)
        self.tree.column("#2", stretch=NO, width=110)
        self.tree.column("#3", stretch=NO, width=110)
        self.tree.column("#4", stretch=NO, width=110)
        self.tree.column("#5", stretch=NO, width=110)
        self.tree.column("#6", stretch=NO, width=150)
        self.tree.column("#7", stretch=NO, width=110)
        self.tree.column("#8", stretch=NO, width=110)

        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT * FROM Працівник WHERE Об_єм_виконаної_роботи BETWEEN 80 AND 120;"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", END, values=(row["id_працівника"], row["Ім_я"], row["Прізвище"], row["По_батькові"], row["Дата_народження"], row["Об_єм_виконаної_роботи"], row["id_посади"], row["id_бригади"]))

        self.scrollbar_x = ttk.Scrollbar(self.query6, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)

        self.button_export = tk.Button(self.query6, text="Експорт в PDF",
                                       command=lambda: self.export_to_pdf("query6.pdf"))
        self.button_export.pack()

        self.query6.mainloop()

    def query7(self):
        logging.info(f"{self.current_user} вибрав query7")
        self.query7 = tk.Tk()
        self.query7.title("Запит №7")
        self.query7.geometry("1000x500")

        self.label_title_q7 = tk.Label(self.query7,
                                       text="Результати запиту",
                                       font=("Arial", 13))
        self.label_title_q7.pack()

        # определяем столбцы
        self.columns = ("Total_amount_of_work")

        self.tree = ttk.Treeview(self.query7, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("Total_amount_of_work", text="Загальна_кількість_роботи", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=160)


        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT SUM(Об_єм_виконаної_роботи) AS Загальна_кількість_роботи FROM Працівник;"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", END, values=(row["Загальна_кількість_роботи"]))

        self.scrollbar_x = ttk.Scrollbar(self.query7, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)

        self.button_export = tk.Button(self.query7, text="Експорт в PDF",
                                       command=lambda: self.export_to_pdf("query7.pdf"))
        self.button_export.pack()

        self.query7.mainloop()

    def query8(self):
        logging.info(f"{self.current_user} вибрав query8")
        self.query8 = tk.Tk()
        self.query8.title("Запит №8")
        self.query8.geometry("1000x500")

        self.label_title_q8 = tk.Label(self.query8,
                                       text="Результати запиту",
                                       font=("Arial", 13))
        self.label_title_q8.pack()

        # определяем столбцы
        self.columns = ("Average_Shipping_Price")

        self.tree = ttk.Treeview(self.query8, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("Average_Shipping_Price", text="Середня_ціна_поставки", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=160)


        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT AVG(Ціна_за_одиницю) AS Середня_ціна_поставки FROM Поставка_ліків;"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", END, values=(row["Середня_ціна_поставки"]))

        self.scrollbar_x = ttk.Scrollbar(self.query8, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)

        self.button_export = tk.Button(self.query8, text="Експорт в PDF",
                                       command=lambda: self.export_to_pdf("query8.pdf"))
        self.button_export.pack()

        self.query8.mainloop()

    def query9(self):
        logging.info(f"{self.current_user} вибрав query9")
        self.query9 = tk.Tk()
        self.query9.title("Запит №9")
        self.query9.geometry("1000x500")

        self.label_title_q9 = tk.Label(self.query9,
                                       text="Результати запиту",
                                       font=("Arial", 13))
        self.label_title_q9.pack()

        # определяем столбцы
        self.columns = ("id_Employee", "name", "surname", "id_job")

        self.tree = ttk.Treeview(self.query9, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("id_Employee", text="id_працівника", anchor=W)
        self.tree.heading("name", text="Ім_я", anchor=W)
        self.tree.heading("surname", text="Прізвище", anchor=W)
        self.tree.heading("id_job", text="id_посади", anchor=W)


        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=110)
        self.tree.column("#2", stretch=NO, width=110)
        self.tree.column("#3", stretch=NO, width=110)
        self.tree.column("#4", stretch=NO, width=110)

        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT id_працівника, Ім_я, Прізвище, По_батькові, id_посади FROM Працівник WHERE id_посади = 1 UNION SELECT id_працівника, Ім_я, Прізвище, По_батькові, id_посади FROM Працівник WHERE id_посади = 2;"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", END, values=(row["id_працівника"], row["Ім_я"], row["Прізвище"], row["id_посади"]))

        # добавляем полосу прокрутки по вертикали
        self.scrollbar_y = ttk.Scrollbar(self.query9, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar_y.set)
        self.scrollbar_y.pack(side=RIGHT, fill=Y)

        # добавляем полосу прокрутки по горизонтали
        self.scrollbar_x = ttk.Scrollbar(self.query9, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)

        self.button_export = tk.Button(self.query9, text="Експорт в PDF",
                                       command=lambda: self.export_to_pdf("query9.pdf"))
        self.button_export.pack()


        self.button_export = tk.Button(self.query9, text="Експорт в PDF",
                                       command=lambda: self.export_to_pdf("query9.pdf"))
        self.button_export.pack()


        self.query9.mainloop()

    def query10(self):
        logging.info(f"{self.current_user} вибрав query10")
        self.query10 = tk.Tk()
        self.query10.title("Запит №10")
        self.query10.geometry("1000x500")

        self.label_title_q10 = tk.Label(self.query10,
                                       text="Результати запиту",
                                       font=("Arial", 13))
        self.label_title_q10.pack()

        # определяем столбцы
        self.columns = ("id_brigade", "Total_Volume_of_Work")

        self.tree = ttk.Treeview(self.query10, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю

        self.tree.heading("id_brigade", text="id_бригади", anchor=W)
        self.tree.heading("Total_Volume_of_Work", text="Сумарний_обсяг_роботи", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=110)
        self.tree.column("#2", stretch=NO, width=150)


        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT id_бригади, SUM(Об_єм_виконаної_роботи) AS Сумарний_обсяг_роботи FROM Працівник GROUP BY id_бригади;"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", END, values=(row["id_бригади"], row["Сумарний_обсяг_роботи"]))

        self.scrollbar_x = ttk.Scrollbar(self.query10, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)


        self.button_export = tk.Button(self.query10, text="Експорт в PDF",
                                       command=lambda: self.export_to_pdf("query10.pdf"))
        self.button_export.pack()



        self.query10.mainloop()

    def query11(self):
        logging.info(f"{self.current_user} вибрав query11")
        self.query11 = tk.Tk()
        self.query11.title("Запит №11")
        self.query11.geometry("1000x500")

        self.label_title_q11 = tk.Label(self.query11,
                                       text="Результати запиту",
                                       font=("Arial", 13))
        self.label_title_q11.pack()

        # определяем столбцы
        self.columns = ("id_Employee", "name", "surname")

        self.tree = ttk.Treeview(self.query11, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("id_Employee", text="id_працівника", anchor=W)
        self.tree.heading("name", text="Ім_я", anchor=W)
        self.tree.heading("surname", text="Прізвище", anchor=W)


        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=110)
        self.tree.column("#2", stretch=NO, width=110)
        self.tree.column("#3", stretch=NO, width=110)

        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT id_працівника, Ім_я, Прізвище FROM Працівник WHERE Об_єм_виконаної_роботи > ALL (SELECT Об_єм_виконаної_роботи FROM Працівник WHERE id_посади = 2 AND Об_єм_виконаної_роботи IS NOT NULL);"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", END, values=(row["id_працівника"], row["Ім_я"], row["Прізвище"]))

        self.scrollbar_x = ttk.Scrollbar(self.query11, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)

        self.button_export = tk.Button(self.query11, text="Експорт в PDF",
                                       command=lambda: self.export_to_pdf("query11.pdf"))
        self.button_export.pack()

        self.query11.mainloop()


    def query12(self):
        logging.info(f"{self.current_user} вибрав query12")
        self.query12 = tk.Tk()
        self.query12.title("Запит №12")
        self.query12.geometry("1000x500")

        self.label_title_q12 = tk.Label(self.query12,
                                       text="Результати запиту",
                                       font=("Arial", 13))
        self.label_title_q12.pack()

        # определяем столбцы
        self.columns = ("id_Employee", "name", "surname")

        self.tree = ttk.Treeview(self.query12, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("id_Employee", text="id_працівника", anchor=W)
        self.tree.heading("name", text="Ім_я", anchor=W)
        self.tree.heading("surname", text="Прізвище", anchor=W)


        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=110)
        self.tree.column("#2", stretch=NO, width=110)
        self.tree.column("#3", stretch=NO, width=110)

        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT id_працівника, Ім_я, Прізвище FROM Працівник WHERE Об_єм_виконаної_роботи > ANY (SELECT Об_єм_виконаної_роботи FROM Працівник WHERE id_посади = 1);"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", END, values=(row["id_працівника"], row["Ім_я"], row["Прізвище"]))

        self.scrollbar_x = ttk.Scrollbar(self.query12, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)

        self.button_export = tk.Button(self.query12, text="Експорт в PDF",
                                       command=lambda: self.export_to_pdf("query12.pdf"))
        self.button_export.pack()

        self.query12.mainloop()

    def query13(self):
        logging.info(f"{self.current_user} вибрав query13")
        self.query13 = tk.Tk()
        self.query13.title("Запит №13")
        self.query13.geometry("1000x500")

        self.label_title_q13 = tk.Label(self.query13,
                                       text="Результати запиту",
                                       font=("Arial", 13))
        self.label_title_q13.pack()

        # определяем столбцы
        self.columns = ("id_vendor", "name", "surname", "shipping_amount")

        self.tree = ttk.Treeview(self.query13, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("id_vendor", text="id_постачальника", anchor=W)
        self.tree.heading("name", text="Ім_я", anchor=W)
        self.tree.heading("surname", text="Прізвище", anchor=W)
        self.tree.heading("shipping_amount", text="Сума_доставки", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=120)
        self.tree.column("#2", stretch=NO, width=120)
        self.tree.column("#3", stretch=NO, width=120)
        self.tree.column("#4", stretch=NO, width=120)

        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT p.id_постачальника, p.Ім_я, p.Прізвище, (SELECT SUM(Ціна_за_одиницю * Кількість_одиниць) " \
                    "FROM Поставка_ліків WHERE id_постачальника = p.id_постачальника) AS Сума_доставки FROM " \
                    "Постачальник p WHERE EXISTS (SELECT * FROM Поставка_ліків WHERE id_постачальника = " \
                    "p.id_постачальника AND Ціна_за_одиницю > ( SELECT AVG(Ціна_за_одиницю) FROM Поставка_ліків )); "
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", END, values=(row["id_постачальника"], row["Ім_я"], row["Прізвище"], row["Сума_доставки"]))

        self.scrollbar_x = ttk.Scrollbar(self.query13, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)

        self.button_export = tk.Button(self.query13, text="Експорт в PDF",
                                       command=lambda: self.export_to_pdf("query13.pdf"))
        self.button_export.pack()

        self.query13.mainloop()

    def query14(self):
        logging.info(f"{self.current_user} вибрав query14")
        self.query14 = tk.Tk()
        self.query14.title("Запит №14")
        self.query14.geometry("1000x500")

        self.label_title_q14 = tk.Label(self.query14,
                                       text="Результати запиту",
                                       font=("Arial", 13))
        self.label_title_q14.pack()

        # определяем столбцы
        self.columns = ("id_Employee", "name", "surname")

        self.tree = ttk.Treeview(self.query14, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("id_Employee", text="id_працівника", anchor=W)
        self.tree.heading("name", text="Ім_я", anchor=W)
        self.tree.heading("surname", text="Прізвище", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=110)
        self.tree.column("#2", stretch=NO, width=110)
        self.tree.column("#3", stretch=NO, width=110)

        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT id_працівника, Ім_я, Прізвище FROM Працівник p WHERE Об_єм_виконаної_роботи > ( SELECT " \
                    "MAX(Об_єм_виконаної_роботи) FROM Працівник WHERE id_посади = ( SELECT id_посади FROM Посада " \
                    "WHERE Назва = 'Медсестра' )); "
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", END, values=(row["id_працівника"], row["Ім_я"], row["Прізвище"]))

        self.scrollbar_x = ttk.Scrollbar(self.query14, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)

        self.button_export = tk.Button(self.query14, text="Експорт в PDF",
                                       command=lambda: self.export_to_pdf("query14.pdf"))
        self.button_export.pack()

        self.query14.mainloop()

    def query15(self):
        logging.info(f"{self.current_user} вибрав query15")
        self.query15 = tk.Tk()
        self.query15.title("Запит №15")
        self.query15.geometry("1000x500")

        self.label_title_q15 = tk.Label(self.query15,
                                       text="Результати запиту",
                                       font=("Arial", 13))
        self.label_title_q15.pack()

        # определяем столбцы
        self.columns = ("id_vendor", "name", "surname")

        self.tree = ttk.Treeview(self.query15, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("id_vendor", text="id_постачальника", anchor=W)
        self.tree.heading("name", text="Ім_я", anchor=W)
        self.tree.heading("surname", text="Прізвище", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=120)
        self.tree.column("#2", stretch=NO, width=120)
        self.tree.column("#3", stretch=NO, width=120)

        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT P.id_постачальника, P.Ім_я, P.Прізвище FROM Постачальник P WHERE NOT EXISTS ( SELECT * FROM Поставка_ліків PL WHERE PL.id_постачальника = P.id_постачальника);"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", END, values=(row["id_постачальника"], row["Ім_я"], row["Прізвище"]))

        self.scrollbar_x = ttk.Scrollbar(self.query15, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)

        self.button_export = tk.Button(self.query15, text="Експорт в PDF",
                                       command=lambda: self.export_to_pdf("query15.pdf"))
        self.button_export.pack()

        self.query15.mainloop()

    def query16(self):
        logging.info(f"{self.current_user} вибрав query16")
        self.query16 = tk.Tk()
        self.query16.title("Запит №16")
        self.query16.geometry("1000x500")

        self.label_title_q16 = tk.Label(self.query16,
                                       text="Результати запиту",
                                       font=("Arial", 13))
        self.label_title_q16.pack()

        # определяем столбцы
        self.columns = ("id_job", "title")

        self.tree = ttk.Treeview(self.query16, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("id_job", text="id_посади", anchor=W)
        self.tree.heading("title", text="Назва", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=120)
        self.tree.column("#2", stretch=NO, width=120)

        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT П.id_посади, П.Назва FROM Посада П LEFT JOIN Працівник Пр ON П.id_посади = Пр.id_посади WHERE Пр.id_працівника IS NULL;"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", END, values=(row["id_посади"], row["Назва"]))

        self.scrollbar_x = ttk.Scrollbar(self.query16, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)

        self.button_export = tk.Button(self.query16, text="Експорт в PDF",
                                       command=lambda: self.export_to_pdf("query16.pdf"))
        self.button_export.pack()

        self.query16.mainloop()

    def query17(self):
        logging.info(f"{self.current_user} вибрав query17")
        self.query17 = tk.Tk()
        self.query17.title("Запит №17")
        self.query17.geometry("1000x500")

        self.label_title_q17 = tk.Label(self.query17,
                                       text="Результати запиту",
                                       font=("Arial", 13))
        self.label_title_q17.pack()

        # определяем столбцы
        self.columns = ("id_job", "title", "comment")

        self.tree = ttk.Treeview(self.query17, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("id_job", text="id_посади", anchor=W)
        self.tree.heading("title", text="Назва", anchor=W)
        self.tree.heading("comment", text="Коментар", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=120)
        self.tree.column("#2", stretch=NO, width=120)
        self.tree.column("#3", stretch=NO, width=210)

        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT id_посади, Назва, 'Має максимальну кількість хворих' AS Коментар FROM Посада WHERE " \
                    "id_посади IN ( SELECT id_посади FROM Працівник WHERE Об_єм_виконаної_роботи = (SELECT MAX(" \
                    "Об_єм_виконаної_роботи) FROM Працівник ))UNION SELECT id_посади, Назва, 'Не має в цей час " \
                    "хворих' AS Коментар FROM Посада WHERE id_посади NOT IN ( SELECT id_посади FROM Працівник WHERE " \
                    "Об_єм_виконаної_роботи > 0); "
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", END, values=(row["id_посади"], row["Назва"], row["Коментар"]))

        self.scrollbar_x = ttk.Scrollbar(self.query17, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)

        self.button_export = tk.Button(self.query17, text="Експорт в PDF",
                                       command=lambda: self.export_to_pdf("query17.pdf"))
        self.button_export.pack()

        self.query17.mainloop()

    def query18(self):
        logging.info(f"{self.current_user} вибрав query18")
        self.query18 = tk.Tk()
        self.query18.title("Запит №18")
        self.query18.geometry("1000x500")

        self.label_title_q18 = tk.Label(self.query18,
                                       text="Результати запиту",
                                       font=("Arial", 13))
        self.label_title_q18.pack()

        # определяем столбцы
        self.columns = ("title", "comment")

        self.tree = ttk.Treeview(self.query18, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("title", text="Назва", anchor=W)
        self.tree.heading("comment", text="Коментар", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=120)
        self.tree.column("#2", stretch=NO, width=170)

        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT Назва, 'Це посада в офісі' AS Коментар FROM Посада UNION SELECT CONCAT(Прізвище, ', ', Ім_я), 'Це постачальник' AS Коментар FROM Постачальник;"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", END, values=(row["Назва"], row["Коментар"]))

        self.scrollbar_x = ttk.Scrollbar(self.query18, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)

        self.button_export = tk.Button(self.query18, text="Експорт в PDF",
                                       command=lambda: self.export_to_pdf("query18.pdf"))
        self.button_export.pack()

        self.query18.mainloop()

    def query19(self):
        logging.info(f"{self.current_user} вибрав query19")
        self.query19 = tk.Tk()
        self.query19.title("Запит №19")
        self.query19.geometry("1000x500")

        self.label_title_q19 = tk.Label(self.query19,
                                       text="Результати запиту",
                                       font=("Arial", 13))
        self.label_title_q19.pack()

        # определяем столбцы
        self.columns = ("id_Employee", "name", "surname", "patronymic", "date_of_birthday", "workload", "id_job", "id_brigade")

        self.tree = ttk.Treeview(self.query19, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("id_Employee", text="id_працівника", anchor=W)
        self.tree.heading("name", text="Ім_я", anchor=W)
        self.tree.heading("surname", text="Прізвище", anchor=W)
        self.tree.heading("patronymic", text="По_батькові", anchor=W)
        self.tree.heading("date_of_birthday", text="Дата_народження", anchor=W)
        self.tree.heading("workload", text="Об_єм_виконаної_роботи", anchor=W)
        self.tree.heading("id_job", text="id_посади", anchor=W)
        self.tree.heading("id_brigade", text="id_бригади", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=110)
        self.tree.column("#2", stretch=NO, width=110)
        self.tree.column("#3", stretch=NO, width=110)
        self.tree.column("#4", stretch=NO, width=110)
        self.tree.column("#5", stretch=NO, width=110)
        self.tree.column("#6", stretch=NO, width=150)
        self.tree.column("#7", stretch=NO, width=110)
        self.tree.column("#8", stretch=NO, width=110)

        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT * FROM Працівник WHERE id_посади IN (SELECT id_посади FROM Посада WHERE Назва = 'Лікар');"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", END, values=(row["id_працівника"], row["Ім_я"], row["Прізвище"], row["По_батькові"], row["Дата_народження"], row["Об_єм_виконаної_роботи"], row["id_посади"], row["id_бригади"]))

        self.scrollbar_x = ttk.Scrollbar(self.query19, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)

        self.button_export = tk.Button(self.query19, text="Експорт в PDF",
                                       command=lambda: self.export_to_pdf("query19.pdf"))
        self.button_export.pack()

        self.query19.mainloop()

    def query20(self):
        logging.info(f"{self.current_user} вибрав query20")
        self.query20 = tk.Tk()
        self.query20.title("Запит №20")
        self.query20.geometry("1000x500")

        self.label_title_q20 = tk.Label(self.query20,
                                       text="Результати запиту",
                                       font=("Arial", 13))
        self.label_title_q20.pack()

        # определяем столбцы
        self.columns = ("id_vendor", "name", "surname", "patronymic")

        self.tree = ttk.Treeview(self.query20, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("id_vendor", text="id_постачальника", anchor=W)
        self.tree.heading("name", text="Ім_я", anchor=W)
        self.tree.heading("surname", text="Прізвище", anchor=W)
        self.tree.heading("patronymic", text="По_батькові", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=120)
        self.tree.column("#2", stretch=NO, width=120)
        self.tree.column("#3", stretch=NO, width=120)
        self.tree.column("#4", stretch=NO, width=120)

        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT * FROM Постачальник WHERE id_постачальника IN (SELECT id_постачальника FROM Поставка_ліків WHERE Ціна_за_одиницю < 100);"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", END, values=(row["id_постачальника"], row["Ім_я"], row["Прізвище"], row["По_батькові"]))

        self.scrollbar_x = ttk.Scrollbar(self.query20, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)

        self.button_export = tk.Button(self.query20, text="Експорт в PDF",
                                       command=lambda: self.export_to_pdf("query20.pdf"))
        self.button_export.pack()

        self.query20.mainloop()

    def all_table(self):
        logging.info(f"{self.current_user} вибрав all_table")
        self.root.destroy()
        self.root = Tk()
        self.root.configure(bg="LightGray")
        self.root.title("Database Viewer")
        self.root.geometry("600x600")

        self.label = Label(self.root, text="Доступні таблиці", font=('Arial', 15))
        self.label.pack(pady=10)

        self.button_brigade = Button(self.root, text="Бригада", command=self.crud_brigade, padx=5, pady=5, width=20, font=('Arial', 12))
        self.button_brigade.pack(pady=5)

        self.button_diagnosis = Button(self.root, text="Діагноз", command=self.crud_diagnosis,  padx=5, pady=5, width=20, font=('Arial', 12))
        self.button_diagnosis.pack(pady=5)

        self.button_medicine = Button(self.root, text="Ліки", command=self.crud_medicine, padx=5, pady=5, width=20, font=('Arial', 12))
        self.button_medicine.pack(pady=5)

        self.button_patient = Button(self.root, text="Пацієнт", command = self.crud_patient, padx=5, pady=5, width=20, font=('Arial', 12))
        self.button_patient.pack(pady=5)

        self.button_position = Button(self.root, text="Посада", command= self.crud_position, padx=5, pady=5, width=20, font=('Arial', 12))
        self.button_position.pack(pady=5)

        self.button_delivery_of_medicines = Button(self.root, text="Поставка_ліків", command= self.crud_delivery, padx=5, pady=5, width=20, font=('Arial', 12))
        self.button_delivery_of_medicines.pack(pady=5)

        self.button_provider = Button(self.root, text="Постачальник", command = self.crud_supplier, padx=5, pady=5, width=20, font=('Arial', 12))
        self.button_provider.pack(pady=5)

        self.button_employee = Button(self.root, text="Працівник", command = self.crud_employee, padx=5, pady=5, width=20, font=('Arial', 12))
        self.button_employee.pack(pady=5)

        self.root.mainloop()

    def crud_brigade(self):
        logging.info(f"{self.current_user} вибрав Crud Brigade")
        self.root = Tk()
        self.root.title("Crud Brigade")
        self.root.geometry("780x415")

        self.labelbrigade_id = Label(self.root, text="id_бригади:", font=('Arial', 15))
        self.labelbrigade_id.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        self.entrybrigade_id = Entry(self.root, font=('Arial', 15))
        self.entrybrigade_id.grid(row=0, column=1, padx=10, pady=10)

        self.labelNumber_of_workers = Label(self.root, text="Кількість_працівників:", font=('Arial', 15))
        self.labelNumber_of_workers.grid(row=1, column=0, sticky=W, padx=10, pady=10)

        self.entryNumber_of_workers = Entry(self.root, font=('Arial', 15))
        self.entryNumber_of_workers.grid(row=1, column=1, padx=10, pady=10)

        self.labelBrigade_number = Label(self.root, text="Номер_бригади:", font=('Arial', 15))
        self.labelBrigade_number.grid(row=2, column=0, sticky=W, padx=10, pady=10)

        self.entryBrigade_number = Entry(self.root, font=('Arial', 15))
        self.entryBrigade_number.grid(row=2, column=1, padx=10, pady=10)

        self.labelNumber_of_calls = Label(self.root, text="Кількість_викликів:", font=('Arial', 15))
        self.labelNumber_of_calls.grid(row=3, column=0, sticky=W, padx=10, pady=10)

        self.entryNumber_of_calls = Entry(self.root, font=('Arial', 15))
        self.entryNumber_of_calls.grid(row=3, column=1, padx=10, pady=10)

        self.buttonAdd = Button(self.root, text="Додати", font=('Arial', 15),
                                command=self.insert_brigade)
        self.buttonAdd.grid(row=5, column=0, padx=10, pady=10)

        self.buttonUpdate = Button(self.root, text="Оновити", font=('Arial', 15),
                                   command=self.update_brigade)
        self.buttonUpdate.grid(row=5, column=1, padx=10, pady=10)

        self.buttonDelete = Button(self.root, text="Видалити", font=('Arial', 15),
                                   command=self.delete_brigade)
        self.buttonDelete.grid(row=5, column=2, padx=10, pady=10)

        self.treeview = Treeview(self.root, columns=('brigade_id', 'Number_of_workers', 'Brigade_number', 'Number_of_calls'))
        self.treeview.grid(row=6, column=0, columnspan=3, padx=0, pady=10)
        self.treeview.heading('brigade_id', text='id_бригади')
        self.treeview.heading('Number_of_workers', text='Кількість_працівників')
        self.treeview.heading('Brigade_number', text='Номер_бригади')
        self.treeview.heading('Number_of_calls', text='Кількість_викликів')

        self.treeview.column("#0", width=0, stretch='NO')
        self.treeview.column('brigade_id', width=100)
        self.treeview.column('Number_of_workers', width=200)
        self.treeview.column('Brigade_number', width=200)
        self.treeview.column('Number_of_calls', width=200)


        self.read_brigade()
        self.root.mainloop()

    def read_brigade(self):
        self.treeview.delete(*self.treeview.get_children())
        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM бригада")
        rows = cursor.fetchall()
        for row in rows:
            self.treeview.insert('', 'end', values=row)
        db.close()

    def insert_brigade(self):
        logging.info(f"{self.current_user} вибрав insert brigade")
        brigade_id = self.entrybrigade_id.get()
        Number_of_workers = self.entryNumber_of_workers.get()
        Brigade_number = self.entryBrigade_number.get()
        Number_of_calls = self.entryNumber_of_calls.get()
        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()
        cursor.execute("INSERT INTO бригада (id_бригади, Кількість_працівників, Номер_бригади, Кількість_викликів) VALUES (%s, %s, %s, %s)", (brigade_id, Number_of_workers, Brigade_number, Number_of_calls))
        db.commit()
        db.close()
        self.read_brigade()

    def update_brigade(self):
        logging.info(f"{self.current_user} вибрав update brigade")

        brigade_id = self.entrybrigade_id.get()
        Number_of_workers = self.entryNumber_of_workers.get()
        Brigade_number = self.entryBrigade_number.get()
        Number_of_calls = self.entryNumber_of_calls.get()

        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()

        cursor.execute("UPDATE бригада SET Кількість_працівників=%s, Номер_бригади=%s, Кількість_викликів=%s WHERE id_бригади=%s", (Number_of_workers, Brigade_number, Number_of_calls, brigade_id))

        db.commit()
        db.close()
        self.read_brigade()

    def delete_brigade(self):
        logging.info(f"{self.current_user} вибрав update brigade")

        brigade_id = self.entrybrigade_id.get()

        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()

        cursor.execute("DELETE FROM бригада WHERE id_бригади = %s", (brigade_id))
        db.commit()
        db.close()

        self.read_brigade()

    def crud_diagnosis(self):
        logging.info(f"{self.current_user} вибрав Crud Diagnosis")
        self.root = Tk()
        self.root.title("Crud Diagnosis")
        self.root.geometry("900x500")

        self.labeldiagnosis_id = Label(self.root, text="id_діагноза:", font=('Arial', 15))
        self.labeldiagnosis_id.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        self.entrydiagnosis_id = Entry(self.root, font=('Arial', 15))
        self.entrydiagnosis_id.grid(row=0, column=1, padx=10, pady=10)

        self.labelName = Label(self.root, text="Назва:", font=('Arial', 15))
        self.labelName.grid(row=1, column=0, sticky=W, padx=10, pady=10)

        self.entryName = Entry(self.root, font=('Arial', 15))
        self.entryName.grid(row=1, column=1, padx=10, pady=10)

        self.labelSeverity = Label(self.root, text="Критичність:", font=('Arial', 15))
        self.labelSeverity.grid(row=2, column=0, sticky=W, padx=10, pady=10)

        self.entrySeverity = Entry(self.root, font=('Arial', 15))
        self.entrySeverity.grid(row=2, column=1, padx=10, pady=10)

        self.labelMedication = Label(self.root, text="Призначенні_ліки:", font=('Arial', 15))
        self.labelMedication.grid(row=3, column=0, sticky=W, padx=10, pady=10)

        self.entryMedication = Entry(self.root, font=('Arial', 15))
        self.entryMedication.grid(row=3, column=1, padx=10, pady=10)

        self.labelPatient_id = Label(self.root, text="id_пацієнта:", font=('Arial', 15))
        self.labelPatient_id.grid(row=4, column=0, sticky=W, padx=10, pady=10)

        self.entryPatient_id = Entry(self.root, font=('Arial', 15))
        self.entryPatient_id.grid(row=4, column=1, padx=10, pady=10)

        self.labelEmployee_id = Label(self.root, text="id_працівника:", font=('Arial', 15))
        self.labelEmployee_id.grid(row=5, column=0, sticky=W, padx=10, pady=10)

        self.entryEmployee_id = Entry(self.root, font=('Arial', 15))
        self.entryEmployee_id.grid(row=5, column=1, padx=10, pady=10)

        self.buttonAdd = Button(self.root, text="Додати", font=('Arial', 15),
                                command=self.insert_diagnosis)
        self.buttonAdd.grid(row=7, column=0, padx=10, pady=10)

        self.buttonUpdate = Button(self.root, text="Оновити", font=('Arial', 15),
                                   command=self.update_diagnosis)
        self.buttonUpdate.grid(row=7, column=1, padx=10, pady=10)

        self.buttonDelete = Button(self.root, text="Видалити", font=('Arial', 15),
                                   command=self.delete_diagnosis)
        self.buttonDelete.grid(row=7, column=2, padx=10, pady=10)

        self.treeview = Treeview(self.root, columns=('diagnosis_id', 'Name', 'Severity', 'Medication', 'Patient_id', 'Employee_id'))
        self.treeview.grid(row=8, column=0, columnspan=3, padx=0, pady=10)
        self.treeview.heading('diagnosis_id', text='id_діагноза')
        self.treeview.heading('Name', text='Назва')
        self.treeview.heading('Severity', text='Критичність')
        self.treeview.heading('Medication', text='Призначенні_ліки')
        self.treeview.heading('Patient_id', text='id_пацієнта')
        self.treeview.heading('Employee_id', text='id_працівника')

        self.treeview.column("#0", width=0, stretch='NO')
        self.treeview.column('diagnosis_id', width=100)
        self.treeview.column('Name', width=200)
        self.treeview.column('Severity', width=150)
        self.treeview.column('Medication', width=200)
        self.treeview.column('Patient_id', width=120)
        self.treeview.column('Employee_id', width=120)

        self.read_diagnosis()
        self.root.mainloop()

    def read_diagnosis(self):
        self.treeview.delete(*self.treeview.get_children())
        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Діагноз")
        rows = cursor.fetchall()
        for row in rows:
            self.treeview.insert('', 'end', values=row)
        db.close()

    def insert_diagnosis(self):
        logging.info(f"{self.current_user} вибрав insert diagnosis")
        diagnosis_id = self.entrydiagnosis_id.get()
        Name = self.entryName.get()
        Severity = self.entrySeverity.get()
        Medication = self.entryMedication.get()
        Patient_id = self.entryPatient_id.get()
        Employee_id = self.entryEmployee_id.get()
        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()
        cursor.execute("INSERT INTO діагноз (id_діагноза, Назва, Критичність, Призначенні_ліки, id_пацієнта, id_працівника) VALUES (%s, %s, %s, %s, %s, %s)", (diagnosis_id, Name, Severity, Medication, Patient_id, Employee_id))
        db.commit()
        db.close()
        self.read_diagnosis()

    def update_diagnosis(self):
        logging.info(f"{self.current_user} вибрав update diagnosis")

        diagnosis_id = self.entrydiagnosis_id.get()
        Name = self.entryName.get()
        Severity = self.entrySeverity.get()
        Medication = self.entryMedication.get()
        Patient_id = self.entryPatient_id.get()
        Employee_id = self.entryEmployee_id.get()

        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()

        cursor.execute("UPDATE Діагноз SET Назва=%s, Критичність=%s, Призначенні_ліки=%s, id_пацієнта=%s, id_працівника=%s WHERE id_діагноза=%s", (Name, Severity, Medication, Patient_id, Employee_id, diagnosis_id))

        db.commit()
        db.close()
        self.read_diagnosis()

    def delete_diagnosis(self):
        logging.info(f"{self.current_user} вибрав delete diagnosis")

        diagnosis_id = self.entrydiagnosis_id.get()

        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()

        cursor.execute("DELETE FROM Діагноз WHERE id_діагноза = %s", (diagnosis_id))
        db.commit()
        db.close()

        self.read_diagnosis()

    def crud_medicine(self):
        logging.info(f"{self.current_user} вибрав Crud Medicine")
        self.root = Tk()
        self.root.title("Crud Medicine")
        self.root.geometry("900x500")

        self.labelmedicine_id = Label(self.root, text="id_ліків:", font=('Arial', 15))
        self.labelmedicine_id.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        self.entrymedicine_id = Entry(self.root, font=('Arial', 15))
        self.entrymedicine_id.grid(row=0, column=1, padx=10, pady=10)

        self.labelName = Label(self.root, text="Назва:", font=('Arial', 15))
        self.labelName.grid(row=1, column=0, sticky=W, padx=10, pady=10)

        self.entryName = Entry(self.root, font=('Arial', 15))
        self.entryName.grid(row=1, column=1, padx=10, pady=10)

        self.labelExpiration_date = Label(self.root, text="Термін_придатності:", font=('Arial', 15))
        self.labelExpiration_date.grid(row=2, column=0, sticky=W, padx=10, pady=10)

        self.entryExpiration_date = Entry(self.root, font=('Arial', 15))
        self.entryExpiration_date.grid(row=2, column=1, padx=10, pady=10)

        self.labelPurpose = Label(self.root, text="Призначення:", font=('Arial', 15))
        self.labelPurpose.grid(row=3, column=0, sticky=W, padx=10, pady=10)

        self.entryPurpose = Entry(self.root, font=('Arial', 15))
        self.entryPurpose.grid(row=3, column=1, padx=10, pady=10)

        self.labelSupply_id = Label(self.root, text="id_поставки_ліків:", font=('Arial', 15))
        self.labelSupply_id.grid(row=4, column=0, sticky=W, padx=10, pady=10)

        self.entrySupply_id = Entry(self.root, font=('Arial', 15))
        self.entrySupply_id.grid(row=4, column=1, padx=10, pady=10)

        self.buttonAdd = Button(self.root, text="Додати", font=('Arial', 15),
                                command=self.insert_medicine)
        self.buttonAdd.grid(row=6, column=0, padx=10, pady=10)

        self.buttonUpdate = Button(self.root, text="Оновити", font=('Arial', 15),
                                   command=self.update_medicine)
        self.buttonUpdate.grid(row=6, column=1, padx=10, pady=10)

        self.buttonDelete = Button(self.root, text="Видалити", font=('Arial', 15),
                                   command=self.delete_medicine)
        self.buttonDelete.grid(row=6, column=2, padx=10, pady=10)

        self.treeview = Treeview(self.root, columns=('medicine_id', 'Name', 'Expiration_date', 'Purpose', 'Supply_id'))
        self.treeview.grid(row=7, column=0, columnspan=3, padx=0, pady=10)
        self.treeview.heading('medicine_id', text='id_ліків')
        self.treeview.heading('Name', text='Назва')
        self.treeview.heading('Expiration_date', text='Термін_придатності')
        self.treeview.heading('Purpose', text='Призначення')
        self.treeview.heading('Supply_id', text='id_поставки_ліків')

        self.treeview.column("#0", width=0, stretch='NO')
        self.treeview.column('medicine_id', width=100)
        self.treeview.column('Name', width=200)
        self.treeview.column('Expiration_date', width=200)
        self.treeview.column('Purpose', width=200)
        self.treeview.column('Supply_id', width=200)

        self.read_medicine()
        self.root.mainloop()

    def read_medicine(self):
        self.treeview.delete(*self.treeview.get_children())
        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Ліки")
        rows = cursor.fetchall()
        for row in rows:
            self.treeview.insert('', 'end', values=row)
        db.close()

    def insert_medicine(self):
        logging.info(f"{self.current_user} вибрав insert medicine")
        medicine_id = self.entrymedicine_id.get()
        Name = self.entryName.get()
        Expiration_date = self.entryExpiration_date.get()
        Purpose = self.entryPurpose.get()
        Supply_id = self.entrySupply_id.get()
        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO Ліки (id_ліків, Назва, Термін_придатності, Призначення, id_поставки_ліків) VALUES (%s, %s, %s, %s, %s)",
            (medicine_id, Name, Expiration_date, Purpose, Supply_id))
        db.commit()
        db.close()
        self.read_medicine()

    def update_medicine(self):
        logging.info(f"{self.current_user} вибрав update medicine")

        medicine_id = self.entrymedicine_id.get()
        Name = self.entryName.get()
        Expiration_date = self.entryExpiration_date.get()
        Purpose = self.entryPurpose.get()
        Supply_id = self.entrySupply_id.get()

        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()

        cursor.execute(
            "UPDATE Ліки SET Назва=%s, Термін_придатності=%s, Призначення=%s, id_поставки_ліків=%s WHERE id_ліків=%s",
            (Name, Expiration_date, Purpose, Supply_id, medicine_id))

        db.commit()
        db.close()
        self.read_medicine()

    def delete_medicine(self):
        logging.info(f"{self.current_user} вибрав delete medicine")

        medicine_id = self.entrymedicine_id.get()

        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()

        cursor.execute("DELETE FROM Ліки WHERE id_ліків = %s", (medicine_id))
        db.commit()
        db.close()

        self.read_medicine()

    def crud_patient(self):
        logging.info(f"{self.current_user} вибрав Crud Patient")
        self.root = Tk()
        self.root.title("Crud Patient")
        self.root.geometry("900x650")

        self.labelpatient_id = Label(self.root, text="id_пацієнта:", font=('Arial', 15))
        self.labelpatient_id.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        self.entrypatient_id = Entry(self.root, font=('Arial', 15))
        self.entrypatient_id.grid(row=0, column=1, padx=10, pady=10)

        self.labelFirstName = Label(self.root, text="Ім_я:", font=('Arial', 15))
        self.labelFirstName.grid(row=1, column=0, sticky=W, padx=10, pady=10)

        self.entryFirstName = Entry(self.root, font=('Arial', 15))
        self.entryFirstName.grid(row=1, column=1, padx=10, pady=10)

        self.labelLastName = Label(self.root, text="Прізвище:", font=('Arial', 15))
        self.labelLastName.grid(row=2, column=0, sticky=W, padx=10, pady=10)

        self.entryLastName = Entry(self.root, font=('Arial', 15))
        self.entryLastName.grid(row=2, column=1, padx=10, pady=10)

        self.labelMiddleName = Label(self.root, text="По_батькові:", font=('Arial', 15))
        self.labelMiddleName.grid(row=3, column=0, sticky=W, padx=10, pady=10)

        self.entryMiddleName = Entry(self.root, font=('Arial', 15))
        self.entryMiddleName.grid(row=3, column=1, padx=10, pady=10)

        self.labelAddress = Label(self.root, text="Адреса_мешкання:", font=('Arial', 15))
        self.labelAddress.grid(row=4, column=0, sticky=W, padx=10, pady=10)

        self.entryAddress = Entry(self.root, font=('Arial', 15))
        self.entryAddress.grid(row=4, column=1, padx=10, pady=10)

        self.labelSymptom = Label(self.root, text="Симптом:", font=('Arial', 15))
        self.labelSymptom.grid(row=5, column=0, sticky=W, padx=10, pady=10)

        self.entrySymptom = Entry(self.root, font=('Arial', 15))
        self.entrySymptom.grid(row=5, column=1, padx=10, pady=10)

        self.buttonAdd = Button(self.root, text="Додати", font=('Arial', 15),
                                command=self.insert_patient)
        self.buttonAdd.grid(row=7, column=0, padx=10, pady=10)

        self.buttonUpdate = Button(self.root, text="Оновити", font=('Arial', 15),
                                   command=self.update_patient)
        self.buttonUpdate.grid(row=7, column=1, padx=10, pady=10)

        self.buttonDelete = Button(self.root, text="Видалити", font=('Arial', 15),
                                   command=self.delete_patient)
        self.buttonDelete.grid(row=7, column=2, padx=10, pady=10)

        self.treeview = Treeview(self.root,
                                 columns=('patient_id', 'First_Name', 'Last_Name', 'Middle_Name', 'Address', 'Symptom'))
        self.treeview.grid(row=8, column=0, columnspan=3, padx=0, pady=10)
        self.treeview.heading('patient_id', text='id_пацієнта')
        self.treeview.heading('First_Name', text='Ім_я')
        self.treeview.heading('Last_Name', text='Прізвище')
        self.treeview.heading('Middle_Name', text='По_батькові')
        self.treeview.heading('Address', text='Адреса_мешкання')
        self.treeview.heading('Symptom', text='Симптом')

        self.treeview.column("#0", width=0, stretch='NO')
        self.treeview.column('patient_id', width=100)
        self.treeview.column('First_Name', width=150)
        self.treeview.column('Last_Name', width=150)
        self.treeview.column('Middle_Name', width=150)
        self.treeview.column('Address', width=200)
        self.treeview.column('Symptom', width=200)

        self.read_patient()
        self.root.mainloop()

    def read_patient(self):
        self.treeview.delete(*self.treeview.get_children())
        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Пацієнт")
        rows = cursor.fetchall()
        for row in rows:
            self.treeview.insert('', 'end', values=row)
        db.close()

    def insert_patient(self):
        logging.info(f"{self.current_user} вибрав insert patient")
        patient_id = self.entrypatient_id.get()
        First_Name = self.entryFirstName.get()
        Last_Name = self.entryLastName.get()
        Middle_Name = self.entryMiddleName.get()
        Address = self.entryAddress.get()
        Symptom = self.entrySymptom.get()
        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO Пацієнт (id_пацієнта, Ім_я, Прізвище, По_батькові, Адреса_мешкання, Симптом) VALUES (%s, %s, %s, %s, %s, %s)",
            (patient_id, First_Name, Last_Name, Middle_Name, Address, Symptom))
        db.commit()
        db.close()
        self.read_patient()

    def update_patient(self):
        logging.info(f"{self.current_user} вибрав update patient")

        patient_id = self.entrypatient_id.get()
        First_Name = self.entryFirstName.get()
        Last_Name = self.entryLastName.get()
        Middle_Name = self.entryMiddleName.get()
        Address = self.entryAddress.get()
        Symptom = self.entrySymptom.get()

        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()

        cursor.execute(
            "UPDATE Пацієнт SET Ім_я=%s, Прізвище=%s, По_батькові=%s, Адреса_мешкання=%s, Симптом=%s WHERE id_пацієнта=%s",
            (First_Name, Last_Name, Middle_Name, Address, Symptom, patient_id))

        db.commit()
        db.close()
        self.read_patient()

    def delete_patient(self):
        logging.info(f"{self.current_user} вибрав delete patient")

        patient_id = self.entrypatient_id.get()

        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()

        cursor.execute("DELETE FROM Пацієнт WHERE id_пацієнта = %s", (patient_id))
        db.commit()
        db.close()

        self.read_patient()

    def crud_position(self):
        logging.info(f"{self.current_user} вибрав Crud Position")
        self.root = Tk()
        self.root.title("Crud Position")
        self.root.geometry("480x445")

        self.labelposition_id = Label(self.root, text="id_посади:", font=('Arial', 15))
        self.labelposition_id.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        self.entryposition_id = Entry(self.root, font=('Arial', 15))
        self.entryposition_id.grid(row=0, column=1, padx=10, pady=10)

        self.labelposition_name = Label(self.root, text="Назва:", font=('Arial', 15))
        self.labelposition_name.grid(row=1, column=0, sticky=W, padx=10, pady=10)

        self.entryposition_name = Entry(self.root, font=('Arial', 15))
        self.entryposition_name.grid(row=1, column=1, padx=10, pady=10)

        self.buttonAdd = Button(self.root, text="Додати", font=('Arial', 15), command=self.insert_position)
        self.buttonAdd.grid(row=3, column=0, padx=10, pady=10)

        self.buttonUpdate = Button(self.root, text="Оновити", font=('Arial', 15), command=self.update_position)
        self.buttonUpdate.grid(row=3, column=1, padx=10, pady=10)

        self.buttonDelete = Button(self.root, text="Видалити", font=('Arial', 15), command=self.delete_position)
        self.buttonDelete.grid(row=3, column=2, padx=10, pady=10)

        self.treeview = Treeview(self.root, columns=('position_id', 'position_name'))
        self.treeview.grid(row=4, column=0, columnspan=3, padx=0, pady=10)
        self.treeview.heading('position_id', text='id_посади')
        self.treeview.heading('position_name', text='Назва')

        self.treeview.column("#0", width=0, stretch='NO')
        self.treeview.column('position_id', width=100)
        self.treeview.column('position_name', width=200)

        self.read_position()
        self.root.mainloop()

    def read_position(self):
        self.treeview.delete(*self.treeview.get_children())
        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Посада")
        rows = cursor.fetchall()
        for row in rows:
            self.treeview.insert('', 'end', values=row)
        db.close()

    def insert_position(self):
        logging.info(f"{self.current_user} вибрав insert position")
        position_id = self.entryposition_id.get()
        position_name = self.entryposition_name.get()
        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()
        cursor.execute("INSERT INTO Посада (id_посади, Назва) VALUES (%s, %s)", (position_id, position_name))
        db.commit()
        db.close()
        self.read_position()

    def update_position(self):
        logging.info(f"{self.current_user} вибрав update position")
        position_id = self.entryposition_id.get()
        position_name = self.entryposition_name.get()
        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()
        cursor.execute("UPDATE Посада SET Назва = %s WHERE id_посади = %s", (position_name, position_id))
        db.commit()
        db.close()
        self.read_position()

    def delete_position(self):
        logging.info(f"{self.current_user} вибрав delete position")
        position_id = self.entryposition_id.get()
        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()
        cursor.execute("DELETE FROM Посада WHERE id_посади = %s", position_id)
        db.commit()
        db.close()
        self.read_position()

    def crud_delivery(self):
        logging.info(f"{self.current_user} вибрав Crud Delivery")
        self.root = Tk()
        self.root.title("Crud Delivery")
        self.root.geometry("1100x750")

        self.labeldelivery_id = Label(self.root, text="id_поставки_ліків:", font=('Arial', 15))
        self.labeldelivery_id.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        self.entrydelivery_id = Entry(self.root, font=('Arial', 15))
        self.entrydelivery_id.grid(row=0, column=1, padx=10, pady=10)

        self.labelPrice_per_unit = Label(self.root, text="Ціна_за_одиницю:", font=('Arial', 15))
        self.labelPrice_per_unit.grid(row=1, column=0, sticky=W, padx=10, pady=10)

        self.entryPrice_per_unit = Entry(self.root, font=('Arial', 15))
        self.entryPrice_per_unit.grid(row=1, column=1, padx=10, pady=10)

        self.labelQuantity = Label(self.root, text="Кількість_одиниць:", font=('Arial', 15))
        self.labelQuantity.grid(row=2, column=0, sticky=W, padx=10, pady=10)

        self.entryQuantity = Entry(self.root, font=('Arial', 15))
        self.entryQuantity.grid(row=2, column=1, padx=10, pady=10)

        self.labelDelivery_date = Label(self.root, text="Дата_поставки:", font=('Arial', 15))
        self.labelDelivery_date.grid(row=3, column=0, sticky=W, padx=10, pady=10)

        self.entryDelivery_date = Entry(self.root, font=('Arial', 15))
        self.entryDelivery_date.grid(row=3, column=1, padx=10, pady=10)

        self.labelDelivery_status = Label(self.root, text="Статус_поставки:", font=('Arial', 15))
        self.labelDelivery_status.grid(row=4, column=0, sticky=W, padx=10, pady=10)

        self.entryDelivery_status = Entry(self.root, font=('Arial', 15))
        self.entryDelivery_status.grid(row=4, column=1, padx=10, pady=10)

        self.labelEmployee_id = Label(self.root, text="id_працівника:", font=('Arial', 15))
        self.labelEmployee_id.grid(row=5, column=0, sticky=W, padx=10, pady=10)

        self.entryEmployee_id = Entry(self.root, font=('Arial', 15))
        self.entryEmployee_id.grid(row=5, column=1, padx=10, pady=10)

        self.labelSupplier_id = Label(self.root, text="id_постачальника:", font=('Arial', 15))
        self.labelSupplier_id.grid(row=6, column=0, sticky=W, padx=10, pady=10)

        self.entrySupplier_id = Entry(self.root, font=('Arial', 15))
        self.entrySupplier_id.grid(row=6, column=1, padx=10, pady=10)

        self.buttonAdd = Button(self.root, text="Додати", font=('Arial', 15),
                                command=self.insert_delivery)
        self.buttonAdd.grid(row=8, column=0, padx=10, pady=10)

        self.buttonUpdate = Button(self.root, text="Оновити", font=('Arial', 15),
                                   command=self.update_delivery)
        self.buttonUpdate.grid(row=8, column=1, padx=10, pady=10)

        self.buttonDelete = Button(self.root, text="Видалити", font=('Arial', 15),
                                   command=self.delete_delivery)
        self.buttonDelete.grid(row=8, column=2, padx=10, pady=10)

        self.treeview = Treeview(self.root,
                                 columns=(
                                 'delivery_id', 'Price_per_unit', 'Quantity', 'Delivery_date', 'Delivery_status',
                                 'Employee_id', 'Supplier_id'))
        self.treeview.grid(row=9, column=0, columnspan=3, padx=0, pady=10)
        self.treeview.heading('delivery_id', text='id_поставки_ліків')
        self.treeview.heading('Price_per_unit', text='Ціна_за_одиницю')
        self.treeview.heading('Quantity', text='Кількість_одиниць')
        self.treeview.heading('Delivery_date', text='Дата_поставки')
        self.treeview.heading('Delivery_status', text='Статус_поставки')
        self.treeview.heading('Employee_id', text='id_працівника')
        self.treeview.heading('Supplier_id', text='id_постачальника')

        self.treeview.column("#0", width=0, stretch='NO')
        self.treeview.column('delivery_id', width=150)
        self.treeview.column('Price_per_unit', width=150)
        self.treeview.column('Quantity', width=150)
        self.treeview.column('Delivery_date', width=150)
        self.treeview.column('Delivery_status', width=150)
        self.treeview.column('Employee_id', width=150)
        self.treeview.column('Supplier_id', width=150)

        self.read_delivery()
        self.root.mainloop()

    def read_delivery(self):
        self.treeview.delete(*self.treeview.get_children())
        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Поставка_ліків")
        rows = cursor.fetchall()
        for row in rows:
            self.treeview.insert('', 'end', values=row)
        db.close()

    def insert_delivery(self):
        logging.info(f"{self.current_user} вибрав insert delivery")
        delivery_id = self.entrydelivery_id.get()
        Price_per_unit = self.entryPrice_per_unit.get()
        Quantity = self.entryQuantity.get()
        Delivery_date = self.entryDelivery_date.get()
        Delivery_status = self.entryDelivery_status.get()
        Employee_id = self.entryEmployee_id.get()
        Supplier_id = self.entrySupplier_id.get()
        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO Поставка_ліків (id_поставки_ліків, Ціна_за_одиницю, Кількість_одиниць, Дата_поставки, Статус_поставки, id_працівника, id_постачальника) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (delivery_id, Price_per_unit, Quantity, Delivery_date, Delivery_status, Employee_id, Supplier_id))
        db.commit()
        db.close()
        self.read_delivery()

    def update_delivery(self):
        logging.info(f"{self.current_user} вибрав update delivery")

        delivery_id = self.entrydelivery_id.get()
        Price_per_unit = self.entryPrice_per_unit.get()
        Quantity = self.entryQuantity.get()
        Delivery_date = self.entryDelivery_date.get()
        Delivery_status = self.entryDelivery_status.get()
        Employee_id = self.entryEmployee_id.get()
        Supplier_id = self.entrySupplier_id.get()

        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()

        cursor.execute(
            "UPDATE Поставка_ліків SET Ціна_за_одиницю=%s, Кількість_одиниць=%s, Дата_поставки=%s, Статус_поставки=%s, id_працівника=%s, id_постачальника=%s WHERE id_поставки_ліків=%s",
            (Price_per_unit, Quantity, Delivery_date, Delivery_status, Employee_id, Supplier_id, delivery_id))

        db.commit()
        db.close()
        self.read_delivery()

    def delete_delivery(self):
        logging.info(f"{self.current_user} вибрав delete delivery")

        delivery_id = self.entrydelivery_id.get()

        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()

        cursor.execute("DELETE FROM Поставка_ліків WHERE id_поставки_ліків = %s", (delivery_id))
        db.commit()
        db.close()

        self.read_delivery()

    def crud_supplier(self):
        logging.info(f"{self.current_user} вибрав Crud Supplier")
        self.root = Tk()
        self.root.title("Crud Supplier")
        self.root.geometry("640x500")

        self.labelsupplier_id = Label(self.root, text="id_постачальника:", font=('Arial', 15))
        self.labelsupplier_id.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        self.entrysupplier_id = Entry(self.root, font=('Arial', 15))
        self.entrysupplier_id.grid(row=0, column=1, padx=10, pady=10)

        self.labelFirst_name = Label(self.root, text="Ім_я:", font=('Arial', 15))
        self.labelFirst_name.grid(row=1, column=0, sticky=W, padx=10, pady=10)

        self.entryFirst_name = Entry(self.root, font=('Arial', 15))
        self.entryFirst_name.grid(row=1, column=1, padx=10, pady=10)

        self.labelLast_name = Label(self.root, text="Прізвище:", font=('Arial', 15))
        self.labelLast_name.grid(row=2, column=0, sticky=W, padx=10, pady=10)

        self.entryLast_name = Entry(self.root, font=('Arial', 15))
        self.entryLast_name.grid(row=2, column=1, padx=10, pady=10)

        self.labelMiddle_name = Label(self.root, text="По_батькові:", font=('Arial', 15))
        self.labelMiddle_name.grid(row=3, column=0, sticky=W, padx=10, pady=10)

        self.entryMiddle_name = Entry(self.root, font=('Arial', 15))
        self.entryMiddle_name.grid(row=3, column=1, padx=10, pady=10)

        self.buttonAdd = Button(self.root, text="Додати", font=('Arial', 15),
                                command=self.insert_supplier)
        self.buttonAdd.grid(row=5, column=0, padx=10, pady=10)

        self.buttonUpdate = Button(self.root, text="Оновити", font=('Arial', 15),
                                   command=self.update_supplier)
        self.buttonUpdate.grid(row=5, column=1, padx=10, pady=10)

        self.buttonDelete = Button(self.root, text="Видалити", font=('Arial', 15),
                                   command=self.delete_supplier)
        self.buttonDelete.grid(row=5, column=2, padx=10, pady=10)

        self.treeview = Treeview(self.root, columns=('supplier_id', 'First_name', 'Last_name', 'Middle_name'))
        self.treeview.grid(row=6, column=0, columnspan=3, padx=0, pady=10)
        self.treeview.heading('supplier_id', text='id_постачальника')
        self.treeview.heading('First_name', text='Ім_я')
        self.treeview.heading('Last_name', text='Прізвище')
        self.treeview.heading('Middle_name', text='По_батькові')

        self.treeview.column("#0", width=0, stretch='NO')
        self.treeview.column('supplier_id', width=150)
        self.treeview.column('First_name', width=150)
        self.treeview.column('Last_name', width=150)
        self.treeview.column('Middle_name', width=150)

        self.read_supplier()
        self.root.mainloop()

    def read_supplier(self):
        self.treeview.delete(*self.treeview.get_children())
        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Постачальник")
        rows = cursor.fetchall()
        for row in rows:
            self.treeview.insert('', 'end', values=row)
        db.close()

    def insert_supplier(self):
        logging.info(f"{self.current_user} вибрав insert supplier")
        supplier_id = self.entrysupplier_id.get()
        First_name = self.entryFirst_name.get()
        Last_name = self.entryLast_name.get()
        Middle_name = self.entryMiddle_name.get()
        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO Постачальник (id_постачальника, Ім_я, Прізвище, По_батькові) VALUES (%s, %s, %s, %s)",
            (supplier_id, First_name, Last_name, Middle_name))
        db.commit()
        db.close()
        self.read_supplier()

    def update_supplier(self):
        logging.info(f"{self.current_user} вибрав update supplier")

        supplier_id = self.entrysupplier_id.get()
        First_name = self.entryFirst_name.get()
        Last_name = self.entryLast_name.get()
        Middle_name = self.entryMiddle_name.get()

        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()

        cursor.execute(
            "UPDATE Постачальник SET Ім_я=%s, Прізвище=%s, По_батькові=%s WHERE id_постачальника=%s",
            (First_name, Last_name, Middle_name, supplier_id))

        db.commit()
        db.close()
        self.read_supplier()

    def delete_supplier(self):
        logging.info(f"{self.current_user} вибрав delete supplier")

        supplier_id = self.entrysupplier_id.get()

        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()

        cursor.execute("DELETE FROM Постачальник WHERE id_постачальника = %s", (supplier_id))
        db.commit()
        db.close()

        self.read_supplier()

    def crud_employee(self):
        logging.info(f"{self.current_user} вибрав Crud Employee")
        self.root = Tk()
        self.root.title("Crud Employee")
        self.root.geometry("1150x750")

        self.labelemployee_id = Label(self.root, text="id_працівника:", font=('Arial', 15))
        self.labelemployee_id.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        self.entryemployee_id = Entry(self.root, font=('Arial', 15))
        self.entryemployee_id.grid(row=0, column=1, padx=10, pady=10)

        self.labelFirst_name = Label(self.root, text="Ім_я:", font=('Arial', 15))
        self.labelFirst_name.grid(row=1, column=0, sticky=W, padx=10, pady=10)

        self.entryFirst_name = Entry(self.root, font=('Arial', 15))
        self.entryFirst_name.grid(row=1, column=1, padx=10, pady=10)

        self.labelLast_name = Label(self.root, text="Прізвище:", font=('Arial', 15))
        self.labelLast_name.grid(row=2, column=0, sticky=W, padx=10, pady=10)

        self.entryLast_name = Entry(self.root, font=('Arial', 15))
        self.entryLast_name.grid(row=2, column=1, padx=10, pady=10)

        self.labelMiddle_name = Label(self.root, text="По_батькові:", font=('Arial', 15))
        self.labelMiddle_name.grid(row=3, column=0, sticky=W, padx=10, pady=10)

        self.entryMiddle_name = Entry(self.root, font=('Arial', 15))
        self.entryMiddle_name.grid(row=3, column=1, padx=10, pady=10)

        self.labelDate_of_birth = Label(self.root, text="Дата_народження:", font=('Arial', 15))
        self.labelDate_of_birth.grid(row=4, column=0, sticky=W, padx=10, pady=10)

        self.entryDate_of_birth = Entry(self.root, font=('Arial', 15))
        self.entryDate_of_birth.grid(row=4, column=1, padx=10, pady=10)

        self.labelWork_volume = Label(self.root, text="Об_єм_виконаної_роботи:", font=('Arial', 15))
        self.labelWork_volume.grid(row=5, column=0, sticky=W, padx=10, pady=10)

        self.entryWork_volume = Entry(self.root, font=('Arial', 15))
        self.entryWork_volume.grid(row=5, column=1, padx=10, pady=10)

        self.labelPosition_id = Label(self.root, text="id_посади:", font=('Arial', 15))
        self.labelPosition_id.grid(row=6, column=0, sticky=W, padx=10, pady=10)

        self.entryPosition_id = Entry(self.root, font=('Arial', 15))
        self.entryPosition_id.grid(row=6, column=1, padx=10, pady=10)

        self.labelBrigade_id = Label(self.root, text="id_бригади:", font=('Arial', 15))
        self.labelBrigade_id.grid(row=7, column=0, sticky=W, padx=10, pady=10)

        self.entryBrigade_id = Entry(self.root, font=('Arial', 15))
        self.entryBrigade_id.grid(row=7, column=1, padx=10, pady=10)

        self.buttonAdd = Button(self.root, text="Додати", font=('Arial', 15),
                                command=self.insert_employee)
        self.buttonAdd.grid(row=9, column=0, padx=10, pady=10)

        self.buttonUpdate = Button(self.root, text="Оновити", font=('Arial', 15),
                                   command=self.update_employee)
        self.buttonUpdate.grid(row=9, column=1, padx=10, pady=10)

        self.buttonDelete = Button(self.root, text="Видалити", font=('Arial', 15),
                                   command=self.delete_employee)
        self.buttonDelete.grid(row=9, column=2, padx=10, pady=10)

        self.treeview = Treeview(self.root, columns=(
        'employee_id', 'First_name', 'Last_name', 'Middle_name', 'Date_of_birth', 'Work_volume', 'Position_id',
        'Brigade_id'))
        self.treeview.grid(row=10, column=0, columnspan=3, padx=0, pady=10)
        self.treeview.heading('employee_id', text='id_працівника')
        self.treeview.heading('First_name', text='Ім_я')
        self.treeview.heading('Last_name', text='Прізвище')
        self.treeview.heading('Middle_name', text='По_батькові')
        self.treeview.heading('Date_of_birth', text='Дата_народження')
        self.treeview.heading('Work_volume', text='Об_єм_виконаної_роботи')
        self.treeview.heading('Position_id', text='id_посади')
        self.treeview.heading('Brigade_id', text='id_бригади')

        self.treeview.column("#0", width=0, stretch='NO')
        self.treeview.column('employee_id', width=100)
        self.treeview.column('First_name', width=150)
        self.treeview.column('Last_name', width=150)
        self.treeview.column('Middle_name', width=150)
        self.treeview.column('Date_of_birth', width=150)
        self.treeview.column('Work_volume', width=200)
        self.treeview.column('Position_id', width=100)
        self.treeview.column('Brigade_id', width=100)

        self.read_employee()
        self.root.mainloop()

    def read_employee(self):
        self.treeview.delete(*self.treeview.get_children())
        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Працівник")
        rows = cursor.fetchall()
        for row in rows:
            self.treeview.insert('', 'end', values=row)
        db.close()

    def insert_employee(self):
        logging.info(f"{self.current_user} вибрав insert employee")
        employee_id = self.entryemployee_id.get()
        First_name = self.entryFirst_name.get()
        Last_name = self.entryLast_name.get()
        Middle_name = self.entryMiddle_name.get()
        Date_of_birth = self.entryDate_of_birth.get()
        Work_volume = self.entryWork_volume.get()
        Position_id = self.entryPosition_id.get()
        Brigade_id = self.entryBrigade_id.get()
        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO Працівник (id_працівника, Ім_я, Прізвище, По_батькові, Дата_народження, Об_єм_виконаної_роботи, id_посади, id_бригади) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (employee_id, First_name, Last_name, Middle_name, Date_of_birth, Work_volume, Position_id, Brigade_id))
        db.commit()
        db.close()
        self.read_employee()

    def update_employee(self):
        logging.info(f"{self.current_user} вибрав update employee")

        employee_id = self.entryemployee_id.get()
        First_name = self.entryFirst_name.get()
        Last_name = self.entryLast_name.get()
        Middle_name = self.entryMiddle_name.get()
        Date_of_birth = self.entryDate_of_birth.get()
        Work_volume = self.entryWork_volume.get()
        Position_id = self.entryPosition_id.get()
        Brigade_id = self.entryBrigade_id.get()

        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()

        cursor.execute(
            "UPDATE Працівник SET Ім_я=%s, Прізвище=%s, По_батькові=%s, Дата_народження=%s, Об_єм_виконаної_роботи=%s, id_посади=%s, id_бригади=%s WHERE id_працівника=%s",
            (First_name, Last_name, Middle_name, Date_of_birth, Work_volume, Position_id, Brigade_id, employee_id))

        db.commit()
        db.close()
        self.read_employee()

    def delete_employee(self):
        logging.info(f"{self.current_user} вибрав update employee")

        employee_id = self.entryemployee_id.get()

        db = pymysql.connect(host="localhost", user="root", password=password, database=db_name)
        cursor = db.cursor()

        cursor.execute("DELETE FROM Працівник WHERE id_працівника = %s", (employee_id))
        db.commit()
        db.close()

        self.read_employee()





if __name__ == '__main__':
    logging()
    # Создание экземпляра приложения
    app = DatabaseAuthApp()
