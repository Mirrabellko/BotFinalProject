from abc import ABC, abstractmethod
from collections import namedtuple

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

    def add_new(): 
        '''
        Добавление нового пользователя
        '''
    

    def search(): 
        '''
        Проверка данных пользователя
        '''

        

class RecipeHandler(IDBHandler):
    '''
    Регулятор работы БД с данными рецепта
    '''

    def __init__(self, recipe: namedtuple) -> None:
        super().__init__()
        self.recipe = recipe

    def add_new(data: namedtuple): 
        '''
        Добавление нового рецепта
        '''

    def search(): 
        '''
        Выгрузка всех рецептов пользователя
        '''

    def delete(): 
        '''
        Удаление рецепта
        '''
