import sqlite3
import hashlib

from collections import namedtuple

from config import *


class Database:

    @staticmethod
    def __start_connection():
        '''
        Подключение к базе
        '''
        conn = sqlite3.connect(DBPATH)
        cursor = conn.cursor()
        return conn, cursor
    
    @staticmethod
    def __finish_connection( conn: sqlite3.Connection):
        '''
        Отключение от базы
        '''
        conn.commit()
        conn.close()

    @staticmethod
    def __hash_password(pswd: str):
        '''
        Хеширование пароля пользователя
        '''
        sha256 = hashlib.sha256()
        sha256.update(pswd.encode())
        pswd_hash = sha256.hexdigest()

        return pswd_hash

    @staticmethod
    def init_db():
        '''
        Инициализация базы данных
        '''
        conn, cursor = Database.__start_connection()

        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS User (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(250) NOT NULL UNIQUE,
                    password_hash VARCHAR(50) NOT NULL,
                    email VARCHAR(50),
                    telegram_id INTEGER
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
                    FOREIGN KEY (user_id) REFERENCES User(id)
                    )
                    ''')

        Database.__finish_connection(conn)

    @staticmethod
    def register_user(username: str, password: str, email: str, telegram_id):
        '''
        Регистрация в базе
        '''

        conn, cursor = Database.__start_connection()

        trans = username, Database.__hash_password(password), email, telegram_id
    
        cursor.execute("INSERT INTO User (username, password_hash, email, telegram_id) VALUES(?, ?, ?, ?);", trans)
        Database.__finish_connection(conn)

        print(f"Логин {username} зарегистрирован!")

        return True

    @staticmethod
    def validate_user(username: str, password: str):
        '''
        Проверка ранней регистрации пользователя в базе
        '''
        
        result = False
        
        conn, cursor = Database.__start_connection()

        cursor.execute("SELECT * FROM User WHERE username = ?", (username, ))

        user_result = cursor.fetchone()

        Database.__finish_connection(conn)

        if user_result:
            result = True

        return result
    
    @staticmethod
    def check_password(username: str, password: str):
        '''
        Проверка пароля пользователя в базе
        '''
        result = False
        
        conn, cursor = Database.__start_connection()

        cursor.execute("SELECT password_hash FROM User WHERE username = ?", (username, ))

        user_result = cursor.fetchone()[0]

        Database.__finish_connection(conn)

        if user_result == Database.__hash_password(password):
            result = True

        return result

    @staticmethod
    def get_user_id(username: str):
        '''
        Получить id пользователя
        '''

        conn, cursor = Database.__start_connection()

        cursor.execute("SELECT * FROM User WHERE username = ?", (username, ))
        result = cursor.fetchone()

        Database.__finish_connection(conn)

        return result[0]

    @staticmethod
    def get_recipe_id(username: str, title: str):
        '''
        Получить id рецепта
        '''
        conn, cursor = Database.__start_connection()

        cursor.execute("SELECT id FROM Recipe WHERE user_id = ? AND title = ?", (Database.get_user_id(username), title))
        result = cursor.fetchone()[0]

        Database.__finish_connection(conn)

        return result
    
    @staticmethod
    def get_all_recipies(username: str):
        '''
        Получить рецепты пользователя
        '''

        conn, cursor = Database.__start_connection()

        cursor.execute("SELECT * FROM Recipe WHERE user_id = ?", (Database.get_user_id(username), ))
        result = cursor.fetchall()

        Database.__finish_connection(conn)

        if result:
            return result
        
        else:
            return None

    @staticmethod
    def get_one_recipe(username: str, title: str):

        '''
        Проверить был ли добавлен ранее рецепт
        '''
        
        conn, cursor = Database.__start_connection()

        cursor.execute("SELECT * FROM Recipe WHERE user_id = ? AND title =?", (Database.get_user_id(username), title))

        user_result = cursor.fetchone()

        Database.__finish_connection(conn)

        if user_result:
            return user_result
        
        else:
            return None

    @staticmethod
    def add_recipe(username: str, recipe: namedtuple):
        '''
        Добавить рецепт
        '''
        result = False

        conn, cursor = Database.__start_connection()

        user_id = Database.get_user_id(username)

        trans = recipe.title.replace('\n', ''), recipe.category, recipe.ingredients, recipe.steps, recipe.cook_time, user_id

        try:
            cursor.execute('INSERT INTO Recipe (title, category, ingredients, steps, cook_time, user_id) VALUES(?, ?, ?, ?, ?, ?);', trans)
            result = True

        except sqlite3.Error as error:
            print("Что-то пошло не так...")
        
        Database.__finish_connection(conn)

        return result

    @staticmethod
    def delete_recipe(username: str, title: str):
        '''
        Удаление рецепта
        '''
        result = False

        conn, cursor = Database.__start_connection()

        target = Database.get_recipe_id(username, title)

        try:
            cursor.execute("DELETE FROM Recipe WHERE id=?", (target, ))
            result = True
            print("Рецепт успешно удален")

        except sqlite3.IntegrityError as error:
            print("Рецепт не был добавлен")

        Database.__finish_connection(conn)

        return result

    @staticmethod
    def get_username_by_telegram_id(telegram_id: int):

        conn, cursor = Database.__start_connection()

        cursor.execute("SELECT username FROM User WHERE telegram_id = ?", (telegram_id, ))
        result = cursor.fetchone()

        Database.__finish_connection(conn)

        return result