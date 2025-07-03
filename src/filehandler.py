
from abc import ABC, abstractmethod
from fileinput import filename
from src.vacancies import Vacancy
from src.parser import HeadHunterAPI
import json
import re


class FileHandler(ABC):


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
    path: str

    def __init__(self, path):
        self.path = path

    def save_list_vacancies(self, data, path_to_save):
        result = []
        for item in data:
            result.append(vars(item))

        with open(path_to_save, 'w', encoding='utf-8') as file:
             json.dump(result, file,  ensure_ascii=False, indent=4)


    def save_to_file(self, data):
        with open(self.path, 'w', encoding='utf-8') as file:
             json.dump(data, file,  ensure_ascii=False, indent=4)

    def save_to_file_add(self, data, path_to_save):
        with open(path_to_save, 'w', encoding='utf-8') as file:
            json.dump(data, file,  ensure_ascii=False, indent=4)

    def add_data_to_file(self, vacancies):
        with open(self.path, 'w') as file:
            for vacancy in vacancies:
                file.write(f'{vacancy}\n')

    def get_data_from_file(self, path_get_data):
        with open(path_get_data, 'r', encoding="utf-8") as file:
            data = json.load(file)
        return data

    def get_data_from_file_with_filtr(self, search_word, path_get_data):
        with open(path_get_data, 'r', encoding="utf-8") as file:
            data = json.load(file)
        pattern = re.compile(search_word, flags=re.IGNORECASE)
        result_list = []
        for item in data:
            for value in item.values():
                str_value = str(value)
                if re.search(pattern, str_value, flags=0):
                    result_list.append(item)
                    break
        return result_list

    def delete_data_in_file(self, key_for_del, value_for_del):
        """Читает файл, удаляет заданную строку и перезаписывает файл"""
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                if isinstance(data, list):
                    initial_length = len(data)
                    # Фильтруем список, исключая элемент с заданным ключом и значением
                    data = [item for item in data if item.get(key_for_del) != value_for_del]
                    if len(data) == initial_length:
                        return False  # Элемент не найден
                elif isinstance(data, dict):
                    if key_for_del in data and data[key_for_del] == value_for_del:
                        del data[key_for_del]
                else:
                    return False  # Элемент не найден

            with open(self.path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            return True

        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {self.path} не найден")
        except json.JSONDecodeError:
            raise ValueError("Файл содержит некорректные JSON данные")
        except Exception as e:
            raise Exception(f"Произошла ошибка: {str(e)}")


if __name__ == "__main__":
    fm = FileManager("test")
    fm.save_list_vacancies([Vacancy("Python Developer", "http://example.com", "100000-150000", "Python, Django", "Middle"),
        Vacancy("JavaScript Developer", "http://example.com", "120000-180000", "JavaScript, React", "Senior")], "test")

    with open("test", 'r', encoding='utf-8') as f:
        data = json.load(f)

    # vacancy_to_delete = str(Vacancy("Python Developer", "http://example.com", "100000-150000", "Python, Django", "Middle"))
    fm.delete_data_in_file("_name", "Python Developer")

    with open("test", 'r') as f:
        data = json.load(f)

    print(len(data))

    # print(remaining_vacancies)























