import json
from src.parser import HeadHunterAPI, Parser
from src.vacancies import Vacancy
from src.filehandler import FileHandler, FileManager
from src.utils import get_top_n_vacancies


def main():
    """Главная фунцкия для работы программы"""
    user_platform = input('Выберите платформу для поиска вакансий. "HH.ru - введите \'H\', другая - введите \'Other\' ').lower()
    if user_platform == 'h':
        hh = HeadHunterAPI()

    search_query= input('Введите поисковый запрос: ').lower()
    result_main_search = hh.connect_api(search_query) # запрос по API к HH по слову
    main_search = FileManager('data/list_vacancies.json') # создает экземпляр класса для сохранение в файл
    list_for_save = main_search.save_to_file(result_main_search) #сохраняет полученные данные в файл

    get_data_list = main_search.get_data_from_file('data/list_vacancies.json') #достает данные из файла
    list_vacancies = Vacancy.cast_to_object_list(get_data_list) #преобразует данные из файла в экземпляры класса Vacancy
    save_to_file = main_search.save_list_vacancies(list_vacancies, 'data/work_list_vacancies.json') #сохраняет измененнные данные в новый файл
    get_data_list_for_top= main_search.get_data_from_file('data/work_list_vacancies.json')# достает данные из файла

    top_n = int(input('Введите количество вакансий для вывода в топ N: ')) #запрашивает у пользвателя кол-во вакансий топ
    get_top_n= get_top_n_vacancies(list_vacancies, 'salary_from', top_n) #формирует топ n из экземпляров классов Vacancy
    save_to_file_top_n = main_search.save_list_vacancies(get_top_n, 'data/top_n_vacancies.json')#сохраняет топ n файл
    for_print_data_list_for_top = main_search.get_data_from_file('data/top_n_vacancies.json') # загружает данные топ n из файла для вывода в консоль
    json_top_n = json.dumps(for_print_data_list_for_top, indent=4, ensure_ascii=False)#переводит в строку json
    print(json_top_n) # выводит в консоль

    search_word = input('Введите слово для поиска вакансий из списка: ').lower() #запрашивает слово для фильтра вакансий
    get_data_list_for_filtr = main_search.get_data_from_file_with_filtr(search_word, 'data/work_list_vacancies.json' )# достает данные из файла с фильтром
    save_to_file_filtr_word = main_search.save_to_file_add(get_data_list_for_filtr, 'data/filtr_word_vacancies.json') #сохраняет отфильтрованные вакансии в файл
    for_print_data_list_filtr_word = main_search.get_data_from_file('data/filtr_word_vacancies.json') # загружает данные отфильтрованных вакансий из файла для вывода в консоль
    json_filtr_word = json.dumps(for_print_data_list_filtr_word, indent=4, ensure_ascii=False)  # переводит в строку json
    print(json_filtr_word)  # выводит в консоль








if __name__ == "__main__":
   print(main())
