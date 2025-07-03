import pytest

from src.vacancies import Vacancy



def test_vacancy_init(first_vacancy):
    assert first_vacancy.name == "first_work"
    assert first_vacancy.url == "http//001.first_work"
    assert first_vacancy.salary_from == 1000
    assert first_vacancy.salary_to == 2000
    assert first_vacancy.currency_salary =='RUR'
    assert first_vacancy.requirement == 'first_work requirement'
    assert first_vacancy.responsibility == 'first_work requirement'


def test_vacancy_str(first_vacancy):

    expected_str = ("first_work, ссылка http//001.first_work, зарплата от 1000 до 2000, в RUR  требования "
                    "first_work requirement и обязанности first_work requirement")
    assert str(first_vacancy) == expected_str


def test_invalid_url():
    with pytest.raises(ValueError):
        Vacancy(
            name="Test",
            url="invalid_url",
            salary_from=1000,
            salary_to=2000,
            currency_salary="USD"
        )


def test_salary_comparison():
    vacancy1 = Vacancy("A", "https://hh.ru/1", 100000, 150000, "RUR")
    vacancy2 = Vacancy("B", "https://hh.ru/2", 80000, 120000, "RUR")

    assert vacancy2 < vacancy1
    assert not vacancy1 < vacancy2


def test_no_salary_comparison():
    vacancy1 = Vacancy("A", "https://hh.ru/1", 0, 0, "RUR")
    vacancy2 = Vacancy("B", "https://hh.ru/2", 80000, 120000, "RUR")

    with pytest.raises(TypeError):
        vacancy1 < vacancy2


def test_created_vacancy():
    test_data = {
        "name": "Backend Developer",
        "alternate_url": "https://hh.ru/vacancy/789",
        "salary": {
            "from": 150000,
            "to": 200000,
            "currency": "RUR"
        },
        "snippet": {
            "requirement": "Python, Django",
            "responsibility": "API development"
        }
    }

    vacancy = Vacancy.created_vacancy(test_data)
    assert vacancy.name == "Backend Developer"
    assert vacancy.salary_from == 150000
    assert vacancy.requirement == "Python, Django"


def test_cast_to_object_list():
    test_data = [
        {
            "name": "Frontend",
            "alternate_url": "https://hh.ru/vacancy/111",
            "salary": None,
            "snippet": {"requirement": "", "responsibility": ""}
        },
        {
            "name": "Backend",
            "alternate_url": "https://hh.ru/vacancy/222",
            "salary": {
                "from": 100000,
                "to": None,
                "currency": "RUR"
            },
            "snippet": {"requirement": "Python", "responsibility": "Backend"}
        }
    ]

    vacancies = Vacancy.cast_to_object_list(test_data)
    assert len(vacancies) == 2
    assert vacancies[0].name == "Frontend"
    assert vacancies[0].salary_from == 0
    assert vacancies[1].salary_to == 100000



