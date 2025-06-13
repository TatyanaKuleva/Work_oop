
from src.parser import HeadHunterAPI, Parser
from src.vacancies import Vacancy
from src.filehandler import FileHandler, FileManager
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
    df = pd.DataFrame(get_data_list).sort_values('_Vacancy__salary_from', ascending=False)
    df.columns = df.columns.map(lambda x: x.replace('_Vacancy__', ''))

    top_n = int(input('Введите количество вакансий для вывода в топ N: '))
    top_n_salary = df.head(top_n).to_dict('records')
    top_n_save_file = work_file.save_to_file('top_salary.json', top_n_salary)




    # return result
        # top_n_salary.to_dict('records'))[0]['_Vacancy__salary_from']














if __name__ == "__main__":
   print(main())
