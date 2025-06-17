import json
from abc import ABC, abstractmethod
from fileinput import filename
from src.vacancies import Vacancy
from src.parser import HeadHunterAPI
import json


class FileHandler(ABC):

    # @abstractmethod
    # def save_to_file(self,filename, data):
    #     pass

    @abstractmethod
    def add_data_to_file(self, vacancies, filename):
        pass

    @abstractmethod
    def get_data_from_file(self, filename):
        pass

    @abstractmethod
    def delete_data_in_file(self, filename, vacancy):
        pass


class FileManager(FileHandler):

    def save_list_vacancies(self, filename, data):
        result = []
        for item in data:
            result.append(vars(item))

        with open(filename, 'w', encoding='utf-8') as file:
             json.dump(result, file,  ensure_ascii=False, indent=4)


    def save_to_file(self, filename, data):
        with open(filename, 'w', encoding='utf-8') as file:
             json.dump(data, file,  ensure_ascii=False, indent=4)


    def add_data_to_file(self, vacancies, filename):
        with open(filename, 'w') as file:
            for vacancy in vacancies:
                file.write(f'{vacancy}\n')

    def get_data_from_file(self, filename):
        with open(filename, 'r', encoding="utf-8") as file:
            data = json.load(file)
        return data


    def delete_data_in_file(self, filename, vacancy):
        """Читает файл, удаляет заданную строку и перезаписывает файл"""
        try:
          with open(filename, 'r+') as file:
              lines = file.readlines()
              new_lines = [line for line in lines if line.strip() != vacancy]
              with open(filename, 'w') as file:
                  file.writelines(new_lines)
        except FileNotFoundError:
            print(f'Файл не найден {filename}')
        except Exception as e:
          print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    hh = HeadHunterAPI()
    dict = hh.connect_api('python')
    # vv = Vacancy.cast_to_object_list(dict)
    obj = FileManager()
    res = obj.save_to_file('res.json', dict)
    print(res)
    # vv = Vacancy('jh', 'https://api.hh.ru/areas/160', {'from': 2000, 'to': None, 'currency': 'USD', 'gross': False},
    #              'ghjg', 'hjhk')




