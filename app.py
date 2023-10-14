import tkinter
from tkinter import ttk
import sqlite3


class Main(tkinter.Frame):  # Основное окно
    def __init__(self, root):   # конструктор класса Main
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def open_search_dialog(self):   # Инициализация окна поиска
        Search()

    def search_records(self, name):    # Поиск записей
        name = ('%'+name+'%')
        self.db.c.execute("""SELECT * FROM db WHERE name LIKE ?""", [name])
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def update_record(self, name, tel, email, salary):    # Изменение записи
        self.db.c.execute("""UPDATE db SET name=?, tel=?, email=?, salary=?
        WHERE ID=?""", (name, tel, email, salary, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def delete_records(self):    # удаление записей
        for selection_item in self.tree.selection():
            self.db.c.execute("""DELETE FROM db WHERE id=?""",
                              (self.tree.set(selection_item, "#1")))
        self.db.conn.commit()
        self.view_records()

    def open_update_dialog(self):   # Инициализация окна для изменения записей
        Update()

    def records(self, name, tel, email, salary):    # Инициализация окна для создания записей
        self.db.insert_data(name, tel, email, salary)
        self.view_records()

    def init_main(self):   # Метод для создания основного окна и виджетов
        toolbar = tkinter.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tkinter.TOP, fill=tkinter.X)

        # Кнопка добавления
        self.add_img = tkinter.PhotoImage(file='img/add.png')
        btn_open_dialog = tkinter.Button(toolbar, bg='#d7d8e0', bd=0, image=self.add_img, command=self.open_dialog)
        btn_open_dialog.pack(side=tkinter.LEFT)
        # Создание таблицы treeview
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'tel', 'email', 'salary'), height=45, show='headings')
        self.tree.column('ID', width=38, anchor=tkinter.CENTER)
        self.tree.column('name', width=300, anchor=tkinter.CENTER)
        self.tree.column('tel', width=150, anchor=tkinter.CENTER)
        self.tree.column('email', width=150, anchor=tkinter.CENTER)
        self.tree.column('salary', width=100, anchor=tkinter.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('tel', text='Телефон')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='Зарплата')

        self.tree.pack(side=tkinter.LEFT)
        # Кнопка для изменения записей
        self.update_img = tkinter.PhotoImage(file='img/update.png')
        btn_edit_dialog = tkinter.Button(toolbar, bg='#d7d8e0',
                                         bd=0, image=self.update_img,
                                         command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tkinter.LEFT)
        #  Кнопка для удаления записей
        self.delete_img = tkinter.PhotoImage(file='img/trash.png')
        btn_delete = tkinter.Button(toolbar, bg='#d7d8e0', bd=0,
                                    image=self.delete_img, command=self.delete_records)
        btn_delete.pack(side=tkinter.LEFT)
        # Кнопка для поиска записей
        self.search_img = tkinter.PhotoImage(file='img/search.png')
        btn_search = tkinter.Button(toolbar, bg='#d7d8e0', bd=0, image=self.search_img, command=self.open_search_dialog)
        btn_search.pack(side=tkinter.LEFT)

    def open_dialog(self):  # инициализация окна для добавления записей
        Child()

    def view_records(self):  # взаимодействие с записями
        self.db.c.execute("""SELECT * FROM db""")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def resizable(self, param, param1):
        pass


class Child(tkinter.Toplevel):  # класс окна для добавления записей
    def __init__(self):  # конструктор класса
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):   # создание виджетов окна
        self.title('Добавить')
        self.geometry('400x220')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        #  Создание надписей
        label_name = tkinter.Label(self, text='ФИО')
        label_name.place(x=50, y=50)
        label_select = tkinter.Label(self, text='Телефон')
        label_select.place(x=50, y=80)
        label_sum = tkinter.Label(self, text='E-mail')
        label_sum.place(x=50, y=110)
        label_salary = tkinter.Label(self, text='Зарплата')
        label_salary.place(x=50, y=140)
        #  Создание полей ввода
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)

        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)

        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=110)

        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140)
        #  Создание кнопок
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        #  Добавление комманд к кнопке
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(),
                                                                       self.entry_email.get(),
                                                                       self.entry_tel.get(),
                                                                       self.entry_salary.get()))


class Update(Child):  # класс окна для изменения записей
    def __init__(self):  # конструктор класса
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):  # Создание виджетов в окне update
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_name.get(),  # Функция кнопки
                                                                          self.entry_email.get(),
                                                                          self.entry_tel.get(),
                                                                          self.entry_salary.get()))

        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_ok.destroy()  # Удаление кнопок

    def default_data(self):  # Загрузить данные из таблицы в поля ввода
        self.db.c.execute("""SELECT * FROM db WHERE id=?""", (self.view.tree.set(self.view.tree.selection()[0], '#1')))
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])
        self.entry_salary.insert(0, row[4])


class Search(tkinter.Toplevel):  # класс поиска
    def __init__(self):  # конструктор класса
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):  # Создание окна и виджетов окна поиска
        self.title('Поиск')
        self.geometry('400x220')
        self.resizable(False, False)

        label_search = tkinter.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)
        # Создание кнопки
        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=150, y=50)
        # Функция кнопки
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

    def open_search_dialog(self):
        Search()


class DB():  # Класс базы данных

    def __init__(self):  # Конструктор класса с созданием базы
        self.conn = sqlite3.connect('db.db')
        self.c = self.conn.cursor()
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS db(
        id INTEGER PRIMARY KEY,
        name TEXT,
        tel TEXT,
        email TEXT,
        salary TEXT  
        );
        """)

        self.conn.commit()

    def insert_data(self, name, tel, email, salary):  # Заполнение базы данных
        self.c.execute("""
        INSERT INTO db (name, tel, email, salary)
        VALUES (?, ?, ?, ?)
        """, (name, tel, email, salary))

        self.conn.commit()


if __name__ == '__main__':
    root = tkinter.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Список сотрудников')
    root.geometry('750x500')
    root.resizable(False, False)
    root.mainloop()
