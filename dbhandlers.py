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

                self.__db.register_user(self.user.username, self.user.password)
            
        return True
    
    def search(self): 
        '''
        Проверка данных пользователя
        '''
        result = False

        if self.__db.validate_user(self.user.username, self.user.password):

            result = True

        return result
        

class RecipeHandler(IDBHandler):
    '''
    Регулятор работы БД с данными рецепта
    '''

    def __init__(self, recipe: namedtuple, author: str) -> None:
        super().__init__()

        self.username = author
        self.recipe = recipe
        self.__db = db.Database
        self.__db.init_db()

    def add_new(self): 
        '''
        Добавление нового рецепта
        '''
        self.__db.add_recipe(username=self.username, recipe=self.recipe)

    def search(self, one_title=None): 
        '''
        Выгрузка всех рецептов пользователя
        '''
        if one_title == None:
            user_recipies = self.__db.get_all_recipies(self.username)

        else:
            user_recipies = self.__db.get_one_recipe(self.username, one_title)

        return user_recipies

    def delete(self, delete_title: str): 
        '''
        Удаление рецепта
        '''
        self.__db.delete_recipe(username=self.username, title= delete_title)
