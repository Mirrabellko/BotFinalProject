from abc import ABC, abstractmethod
from collections import namedtuple

import database as db

class IDBHandler(ABC):
    '''
    Интерфейс для работы с БД для пользователя
    '''

    @abstractmethod
    def add_new(data: namedtuple): pass

    @abstractmethod
    def search(): pass



class UserHandler(IDBHandler):
    '''
    Регулятор работы БД с данными пользователя
    '''

    def __init__(self, user: namedtuple) -> None:
        super().__init__()

        self.user = user
        self.__db = db.Database
        self.__db.init_db()

    def add_new(self): 
        '''
        Добавление нового пользователя
        '''

        if not self.__db.validate_user(self.user.username, self.user.password):

                self.__db.register_user(self.user.username, self.user.password, self.user.email, self.user.telegram_id)
            
        return True
    
    def search(self): 
        '''
        Проверка данных пользователя
        '''

        result = False

        if self.__db.validate_user(self.user.username, self.user.password):

            result = True

        return result

    def check_password(self):

        '''
        Проверка пароля пользователя
        '''
        result = False

        if self.__db.check_password(self.user.username, self.user.password):

            result = True

        return result

class RecipeHandler(IDBHandler):
    '''
    Регулятор работы БД с данными рецепта
    '''

    def __init__(self, author: str, recipe = None) -> None:
        super().__init__()

        self.username = author
        self.recipe = recipe
        self.__db = db.Database
        self.__db.init_db()

    def add_new(self): 
        '''
        Добавление нового рецепта
        '''
        result = False

        if self.__db.add_recipe(self.username, self.recipe):
            result = True
        
        return result

    def search(self, one_title=None): 
        '''
        Выгрузка всех рецептов пользователя
        '''

        if one_title == None:
            user_recipies = self.__db.get_all_recipies(self.username)

        else:
            user_recipies = self.__db.get_one_recipe(self.username, one_title)

        print("user_recipies: ", user_recipies)
        result = self.__make_good_view(user_recipies)

        return result

    def delete(self, delete_title: str): 
        '''
        Удаление рецепта
        '''

        self.__db.delete_recipe(self.username, delete_title)

        return True

    def __make_good_view(self, recipies: tuple) -> str:
        '''
        Конвертер данных их кортежа в строку
        title, category, ingredients, steps, cook_time
        '''
        all_data = ''
        for i in range(0, len(recipies)):

            all_data += f'Рецепт № {i+1}\nВид блюда: {recipies[i][1]}\nИнгридиенты: {recipies[i][2]}\nШаги приготовления: {recipies[i][3]}\nВремя приготовления: {recipies[i][4]}\n\n'
            all_data += '________________\n\n'

        return all_data