
from src.parser import HeadHunterAPI, Parser
from src.vacancies import Vacancy
from src.filehandler import FileHandler, FileManager
from src.utils import sorted_data_by_set_number, filtr_data_by_set_word

import pandas as pd



def main():
    """Главная фунцкия для работы программы"""
    user_platform = input('Выберите платформу для поиска вакансий. "HH.ru - введите \'H\', другая - введите \'Other\' ').lower()
    if user_platform == 'h':
        hh = HeadHunterAPI()

    search_query= input('Введите поисковый запрос: ').lower()
    result_dict = hh.connect_api(search_query)
    work_file = FileManager()
    list_for_save = work_file.save_to_file('list_vacancies.json', result_dict)

    get_data_list = work_file.get_data_from_file('list_vacancies.json')
    list_vacancies = Vacancy.cast_to_object_list(get_data_list)
    save_to_file = work_file.save_list_vacancies('vacancy.json', list_vacancies)
    get_data_list = work_file.get_data_from_file('vacancy.json')
    top_n = int(input('Введите количество вакансий для вывода в топ N: '))
    top_n_salary = sorted_data_by_set_number(get_data_list, '_Vacancy__salary_from',top_n)
    top_n_save_file = work_file.save_to_file('top_salary.json', top_n_salary)
    search_word = input('Введите слово для поиска вакасий по требованиям: ').split()
    vacancies_search_word = filtr_data_by_set_word(get_data_list, '_Vacancy__requirement', search_word)
    vacancies_search_word_save_file = work_file.save_to_file('vacancies_with_search_word.json',vacancies_search_word)















if __name__ == "__main__":
   print(main())
