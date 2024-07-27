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
                    email VARCHAR(50)
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
    def register_user(username: str, password: str):
        '''
        Регистрация в базе
        '''

        conn, cursor = Database.__start_connection()

        trans = username, Database.__hash_password(password)
    
        cursor.execute("INSERT INTO User (username, password_hash) VALUES(?, ?);", trans)
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

        user_result = cursor.fetchone()

        Database.__finish_connection(conn)

        if user_result == Database.__hash_password(password):
            result = True

        return result

    @staticmethod
    def __get_user_id(username: str):
        '''
        Получить id пользователя
        '''

        conn, cursor = Database.__start_connection()

        cursor.execute("SELECT * FROM User WHERE username = ?", (username, ))
        result = cursor.fetchone()

        Database.__finish_connection(conn)

        return result

    @staticmethod
    def __get_recipe_id(username: str, title: str):
        '''
        Получить id рецепта
        '''
        conn, cursor = Database.__start_connection()

        cursor.execute("SELECT id FROM Recipe WHERE user_id = ? AND title = ?", (Database.get_user_id(username), title))
        result = cursor.fetchone()

        Database.__finish_connection(conn)

        return result
    
    @staticmethod
    def get_all_recipies(username: str):
        '''
        Получить рецепты пользователя
        '''

        conn, cursor = Database.__start_connection()

        cursor.execute("SELECT * FROM Recipe WHERE username = ?", (username, ))
        result = cursor.fetchone()

        Database.__finish_connection(conn)

        print('Рецепты выгружены')

        return result

    @staticmethod
    def get_one_recipe(username: str, title: str):

        '''
        Проверить был ли добавлен ранее рецепт
        '''

        result = False
        
        conn, cursor = Database.__start_connection()

        cursor.execute("SELECT * FROM Recipe WHERE username = ? AND title =?", (username, title))

        user_result = cursor.fetchone()

        Database.__finish_connection(conn)

        if user_result:
            result = True

        return result

    @staticmethod
    def add_recipe(username: str, recipe: namedtuple):
        '''
        Добавить рецепт
        '''
        conn, cursor = Database.__start_connection()

        try:
            cursor.execute(
                    f'''
                    INSERT INTO Comment (title, category, ingredients, steps, cook_time, user_id) VALUES
                    {recipe.title}, {recipe.category}, {recipe.ingredients}, {recipe.steps}, {recipe.cook_time}, {Database.__get_user_id(username)}
                    ''')
            print("Комментарий успешно добавлен")
        except sqlite3.IntegrityError as error:
            print("Данный комментарий уже был добавлен ранее")
            
        Database.__finish_connection(conn)

    @staticmethod
    def delete_recipe(username: str, title: str):
        '''
        Удаление рецепта
        '''
        conn, cursor = Database.__start_connection()

        target = Database.__get_recipe_id(username, title)

        try:
            cursor.execute("DELETE FROM Recipe WHERE id=?", (target, ))
            print("Рецепт успешно добавлен")

        except sqlite3.IntegrityError as error:
            print("Рецепт не был добавлен")

        Database.__finish_connection(conn)

