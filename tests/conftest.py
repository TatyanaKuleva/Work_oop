import pytest
import tempfile
import os

from src.vacancies import Vacancy

@pytest.fixture
def first_vacancy():
    return Vacancy(name="first_work", url="http//001.first_work", salary_from=1000, salary_to=2000, currency_salary = 'RUR',
                   requirement = 'first_work requirement',
                   responsibility = 'first_work requirement')


@pytest.fixture
def sample_vacancies():
    return [
        Vacancy("Python Developer", "http://example.com", "100000-150000", "Python, Django", "Middle"),
        Vacancy("JavaScript Developer", "http://example.com", "120000-180000", "JavaScript, React", "Senior")
    ]

@pytest.fixture
def temp_file():
    # Создаем временный файл для тестов
    with tempfile.NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8') as f:
        yield f.name
    # Удаляем файл после теста
    os.unlink(f.name)


