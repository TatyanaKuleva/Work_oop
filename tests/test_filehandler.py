
import pytest
import json
import os
from src.filehandler import FileManager, FileHandler
from src.vacancies import Vacancy
import tempfile


def test_add_data_to_file(temp_file, sample_vacancies):
    """Тест добавления данных в файл"""
    fm = FileManager(temp_file)
    fm.add_data_to_file(sample_vacancies)

    with open(temp_file, 'r') as f:
        content = f.readlines()

    assert len(content) == len(sample_vacancies)
    assert "Python Developer" in content[0]
    assert "JavaScript Developer" in content[1]


def test_save_list_vacancies(temp_file, sample_vacancies):
    """Тест сохранения списка вакансий в JSON"""
    fm = FileManager(temp_file)
    fm.save_list_vacancies(sample_vacancies, temp_file)

    with open(temp_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    assert len(data) == len(sample_vacancies)
    assert data[0]['_name'] == "Python Developer"
    assert data[1]['_name'] == "JavaScript Developer"


def test_get_data_from_file(temp_file, sample_vacancies):
    """Тест чтения данных из файла"""
    fm = FileManager(temp_file)
    fm.save_list_vacancies(sample_vacancies, temp_file)

    data = fm.get_data_from_file(temp_file)

    assert len(data) == len(sample_vacancies)
    assert isinstance(data, list)
    assert all(isinstance(item, dict) for item in data)


def test_get_data_from_file(temp_file, sample_vacancies):
    """Тест чтения данных из файла"""
    fm = FileManager(temp_file)
    fm.save_list_vacancies(sample_vacancies, temp_file)

    data = fm.get_data_from_file(temp_file)

    assert len(data) == len(sample_vacancies)
    assert isinstance(data, list)
    assert all(isinstance(item, dict) for item in data)


def test_get_data_from_file_with_filtr(temp_file, sample_vacancies):
    """Тест фильтрации данных из файла"""
    fm = FileManager(temp_file)
    fm.save_list_vacancies(sample_vacancies, temp_file)

    # Фильтр по ключевому слову
    filtered_data = fm.get_data_from_file_with_filtr("python", temp_file)

    assert len(filtered_data) == 1
    assert filtered_data[0]['_name'] == "Python Developer"

    # Фильтр по уровню
    filtered_data = fm.get_data_from_file_with_filtr("senior", temp_file)
    assert len(filtered_data) == 1
    assert filtered_data[0]['_name'] == "JavaScript Developer"


def test_delete_data_in_file(temp_file, sample_vacancies):
    """Тест удаления данных из файла"""
    fm = FileManager(temp_file)
    fm.save_list_vacancies(sample_vacancies, temp_file)

    fm.delete_data_in_file("_name", "Python Developer")
    with open(temp_file, 'r') as f:
        remaining_vacancies = json.load(f)
    assert len(remaining_vacancies) == len(sample_vacancies) - 1


def test_save_to_file(temp_file):
    """Тест сохранения произвольных данных в файл"""
    fm = FileManager(temp_file)
    test_data = {"key": "value", "list": [1, 2, 3]}
    fm.save_to_file(test_data)

    with open(temp_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    assert data == test_data


def test_file_not_found():
    """Тест обработки отсутствующего файла"""
    fm = FileManager("nonexistent_file.json")
    with pytest.raises(FileNotFoundError):
        fm.get_data_from_file("nonexistent_file.json")


