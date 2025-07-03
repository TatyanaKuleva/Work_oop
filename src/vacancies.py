
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
        self._name = name
        self._url = url
        self._salary_from = salary_from
        self._salary_to = salary_to
        self._currency_salary = currency_salary
        self.requirement = requirement
        self.responsibility = responsibility
        self.__validate_name()
        self.__validate_url()


    def __str__(self):
        return (f'{self._name}, ссылка {self._url}, зарплата от {self._salary_from} до '
                f'{self._salary_to}, в {self._currency_salary}  требования {self.requirement} и обязанности {self.responsibility}')



    @property
    def name(self):
        return self._name

    def __validate_name(self) -> None:
        """Приватный метод валидации имени вакансии"""
        if not isinstance(self._name, str):
            raise TypeError("Название вакансии не определено")

    # @name.setter
    # def name(self, value):
    #     if not isinstance(value, str):
    #         raise TypeError ('Название вакансии не определено')
    #     self._name = value

    @property
    def url(self):
        return self._url

    def __validate_url(self) -> None:
        """Приватный метод валидации cсылки на вакансию"""
        if not isinstance(self._url, str):
            raise TypeError("Ссылка не соответствует формату")
        elif not re.match(r'http', self._url):
            raise ValueError ('Неверная ссылка')

    # @url.setter
    # def url(self, value):
    #     if isinstance(value, str) and re.match(r'http', value):
    #         self._url = value
    #     else:
    #         raise ValueError ('Ссылка не соответствует формату')

    @property
    def currency_salary(self):
        return self._currency_salary

    @property
    def salary_from(self):
        return self._salary_from

    @salary_from.setter
    def salary_from(self, value):
        if value == 'нет данных' or value == 0:
            self.__salary_from = 0
        self._salary_from = value

    @property
    def salary_to(self):
        return self._salary_to

    @salary_to.setter
    def salary_to(self, value):
        if value == 'нет данных' or value == 0:
            self._salary_to = 0
        self._salary_to =value

    def __lt__(self, other):
        if not isinstance(other._salary_from, (int)) or other._salary_from == 0 or self._salary_from == 0:
            raise TypeError("невозможно сравнить")

        compare_vacancy = other if isinstance(other, int) else other._salary_from
        return self._salary_from < other._salary_from


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
    # hh = HeadHunterAPI()
    # dict = hh.connect_api('python')
    # vv = Vacancy.cast_to_object_list(dict)
    # for v in vv:
    #     print(v.__dict__)
    #     print(type(v))

    #
    # vv = Vacancy(name="___hjh", url="jhj", salary_from=1000, salary_to=2000, currency_salary="USD")
    # #
    # print(vv)

    vacancy1 = Vacancy("A", "https://hh.ru/1", 100000, 150000, "RUR")
    vacancy2 = Vacancy("B", "https://hh.ru/2", 80000, 120000, "RUR")

    print(vacancy2 < vacancy1)
    print(vacancy1 < vacancy2)

