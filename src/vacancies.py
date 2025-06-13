import json
import re
from itertools import count
from typing import Optional, Dict, List, Any

from mypy.stubutil import NOT_IMPORTABLE_MODULES

from src.parser import HeadHunterAPI

class Vacancy:
    name: str
    url: str
    salary_from: Optional[int]
    salary_to: Optional[int]
    currency_salary: Optional[str]
    requirement: str
    responsibility: str
    # __slots__ = ('name', 'url', 'salary', 'requirement', 'responsibility')


    def __init__(self, name, url, salary_from, salary_to, currency_salary, requirement = '', responsibility = '' ):
        self.__name = name
        self.__url = url
        self.__salary_from = salary_from
        self.__salary_to = salary_to
        self.__currency_salary = currency_salary
        # self.__salary = salary
        self.__requirement = requirement
        self.__responsibility = responsibility


    def __str__(self):
        return (f'{self.__name}, ссылка {self.url}, зарплата от {self.__salary_from} до '
                f'{self.__salary_to}, в {self.__currency_salary}  требования {self.__requirement} и обязанности {self.__responsibility}')



    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError ('Название вакансии не определено')
        self.__name = value

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        if not isinstance(value, str):
            raise TypeError('Ссылка не является строкой')
        elif not re.match(r'http', value):
            raise ValueError ('Ссылка не соответствует формату')
        self.__url = value

    @property
    def salary_from(self):
        return self.__salary_from

    @salary_from.setter
    def salary_from(self, value):
        if value == 'нет данных' or value == 0:
            self.__salary_from = 0
        self.__salary_from = value

    @property
    def salary_to(self):
        return self.__salary_to

    @salary_to.setter
    def salary_to(self, value):
        if value == 'нет данных' or value == 0:
            self.__salary_to = 0
        self.__salary_to =value

    def __lt__(self, other):
        if not isinstance(other.__salary_from, (int)) or other.__salary_from == 0 or self.__salary_from == 0:
            raise TypeError("невозможно сравнить")

        compare_vacancy = other if isinstance(other, int) else other.__salary_from
        return self.__salary_from < other.__salary_from


    @classmethod
    def created_vacancy(cls, data):
        name = data.get('name', '')
        url = data.get('alternate_url', '')
        salary = data.get('salary', '')
        if salary is not None:
            salary_from = salary['from']
            if salary_from is None:
                salary_from = 0
            salary_to = salary['to']
            if salary_to is None:
                salary_to = salary_from
            currency_salary = salary['currency']

        else:
            salary_from = 0
            salary_to = 0
            currency_salary = 'нет данных'

        requirement = data.get('snippet', {}).get('requirement', '')
        responsibility = data.get('snippet', {}).get('responsibility', '')
        return cls(name=name, url=url, salary_from=salary_from, salary_to=salary_to, currency_salary=currency_salary, requirement=requirement, responsibility=responsibility)

    @classmethod
    def cast_to_object_list(cls, list_dict_vacancy):
        result = []
        for vacancy in list_dict_vacancy:
            result.append(cls.created_vacancy(vacancy))
        return result



if __name__ == "__main__":
    hh = HeadHunterAPI()
    dict = hh.connect_api('python')
    vv = Vacancy.cast_to_object_list(dict)
    for v in vv:
        print(v.__dict__)
        print(type(v))


    # vv = Vacancy('jh', 'https://api.hh.ru/areas/160', {'from': 2000, 'to': None, 'currency': 'USD', 'gross': False}, 'ghjg', 'hjhk' )
    # # vv.salary = {'from': 2000, 'to': None, 'currency': 'USD', 'gross': False}
    # print(vv)
