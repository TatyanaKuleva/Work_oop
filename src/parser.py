from abc import ABC, abstractmethod
import requests
import json

class Parser(ABC):
    """Абстрактный класс для работы с API сервиса вакансий"""

    @abstractmethod
    def connect_api(self, keyword):
        """Абстрактный метод для подключения к API"""
        pass


class HeadHunterAPI(Parser):
    """Класс для работы с API HeadHunter и получения вакансий по ключевому слову"""

    def  connect_api(self, keyword):
        url = 'https://api.hh.ru/vacancies'
        params = {'text': keyword, 'per_page':100}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f'Произoшла ошибка: {response.status_code}')
            return None
        data_response = response.json()['items']

        return data_response













