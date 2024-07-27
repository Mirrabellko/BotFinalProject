import sqlite3
import hashlib

from collections import namedtuple

from config import *


class Database:

    IS_DB_EXISTS = None

    def __init__(self) -> None:
        
        if self.IS_DB_EXISTS == None:
            self.init_db()
            self.IS_DB_EXISTS = True
        else:
            return self
    
    def __start_connection(self):
        '''
        Подключение к базе
        '''
        conn = sqlite3.connect(DBPATH)
        cursor = conn.cursor()
        return conn, cursor
    
    def __finish_connection(self, conn: sqlite3.Connection):
        '''
        Отключение от базы
        '''
        conn.commit()
        conn.close()

    def __hash_password(pswd: str):
        '''
        Хеширование пароля пользователя
        '''
        sha256 = hashlib.sha256()
        sha256.update(pswd.encode())
        pswd_hash = sha256.hexdigest()

        return pswd_hash

    def init_db(self):
        '''
        Инициализация базы данных
        '''
        conn, cursor = self.__start_connection()

        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS User (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(250) NOT NULL UNIQUE,
                    password_hash VARCHAR(50) NOT NULL,
                    email VARCHAR(50) NOT NULL
                    )
                    ''')
        

        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Recipe (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title VARCHAR(50) NOT NULL,
                    category VARCHAR(50) NOT NULL,
                    ingredients TEXT NOT NULL,
                    steps INTEGER NOT NULL,
                    cook_time INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES Users(id),
                    )
                    ''')

        self.__finish_connection(conn)

    def register_user(self, username: str, password: str):
        '''
        Регистрация в базе
        '''

        conn, cursor = self.__start_connection()

        trans = username, self.__hash_password(password)
    
        cursor.execute("INSERT INTO Users (username, password) VALUES(?, ?);", trans)
        self.__finish_connection(conn)

        print(f"Логин {username} зарегистрирован!")

        return True

    def validate_user(self, username: str, password: str):
        '''
        Проверка ранней регистрации пользователя в базе
        '''
        
        result = False
        
        conn, cursor = self.__start_connection()

        cursor.execute("SELECT * FROM Users WHERE username = ?", (username, ))

        user_result = cursor.fetchone()

        self.__finish_connection(conn)

        if user_result:
            result = True

        return result
    
    def check_password(self, username: str, password: str):
        '''
        Проверка пароля пользователя в базе
        '''
        result = False
        
        conn, cursor = self.__start_connection()

        cursor.execute("SELECT password_hash FROM Users WHERE username = ?", (username, ))

        user_result = cursor.fetchone()

        self.__finish_connection(conn)

        if user_result == self.__hash_password(password):
            result = True

        return result

    def __get_user_id(self, username: str):
        '''
        Получить id пользователя
        '''

        conn, cursor = self.__start_connection()

        cursor.execute("SELECT * FROM Users WHERE username = ?", (username, ))
        result = cursor.fetchone()

        self.__finish_connection(conn)

        return result

    def __get_recipe_id(self, username: str, title: str):
        '''
        Получить id рецепта
        '''
        conn, cursor = self.__start_connection()

        cursor.execute("SELECT id FROM Recipe WHERE user_id = ? AND title = ?", (self.get_user_id(username), title))
        result = cursor.fetchone()

        self.__finish_connection(conn)

        return result
    
    def get_all_recipies(self, username: str):
        '''
        Получить рецепты пользователя
        '''

        conn, cursor = self.__start_connection()

        cursor.execute("SELECT * FROM Recipe WHERE username = ?", (username, ))
        result = cursor.fetchone()

        self.__finish_connection(conn)

        print('Рецепты выгружены')

        return result

    def get_one_recipe(self, username: str, title: str):

        '''
        Проверить был ли добавлен ранее рецепт
        '''

        result = False
        
        conn, cursor = self.__start_connection()

        cursor.execute("SELECT * FROM Recipe WHERE username = ? AND title =?", (username, title))

        user_result = cursor.fetchone()

        self.__finish_connection(conn)

        if user_result:
            result = True

        return result

    def add_recipe(self, username: str, recipe: namedtuple):
        '''
        Добавить рецепт
        '''
        conn, cursor = self.__start_connection()

        try:
            cursor.execute(
                    f'''
                    INSERT INTO Comment (title, category, ingredients, steps, cook_time, user_id) VALUES
                    {recipe.title}, {recipe.category}, {recipe.ingredients}, {recipe.steps}, {recipe.cook_time}, {self.__get_user_id(username)}
                    ''')
            print("Комментарий успешно добавлен")
        except sqlite3.IntegrityError as error:
            print("Данный комментарий уже был добавлен ранее")
            
        self.__finish_connection(conn)

    def delete_recipe(self, username: str, title: str):
        '''
        Удаление рецепта
        '''
        conn, cursor = self.__start_connection()

        target = self.__get_recipe_id(username, title)

        try:
            cursor.execute("DELETE FROM Recipe WHERE id=?", (target, ))
            print("Рецепт успешно добавлен")

        except sqlite3.IntegrityError as error:
            print("Рецепт не был добавлен")

        self.__finish_connection(conn)

