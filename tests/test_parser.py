import pytest
from unittest.mock import patch, Mock
from src.parser import Parser, HeadHunterAPI


class TestParser:
    """Тесты для абстрактного класса Parser"""

    def test_parser_is_abstract(self):
        """Проверка, что Parser действительно абстрактный класс"""
        with pytest.raises(TypeError):
            parser = Parser()  # Попытка создать экземпляр абстрактного класса

    def test_abstract_method_exists(self):
        """Проверка наличия абстрактного метода connect_api"""
        assert 'connect_api' in Parser.__abstractmethods__


class TestHeadHunterAPI:
    """Тесты для класса HeadHunterAPI"""

    @pytest.fixture
    def hh_api(self):
        """Фикстура для создания экземпляра HeadHunterAPI"""
        return HeadHunterAPI()

    def test_inherits_from_parser(self, hh_api):
        """Проверка наследования от Parser"""
        assert isinstance(hh_api, Parser)

    @patch('requests.get')
    def test_connect_api_success(self, mock_get, hh_api):
        """Тест успешного подключения к API"""
        # Мокируем успешный ответ
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'items': [{'id': '1', 'name': 'Python Developer'}]}
        mock_get.return_value = mock_response

        result = hh_api.connect_api('Python')

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]['id'] == '1'
        mock_get.assert_called_once_with(
            'https://api.hh.ru/vacancies',
            params={'text': 'Python', 'per_page': 100}
        )

    @patch('requests.get')
    def test_connect_api_failure(self, mock_get, hh_api):
        """Тест неудачного подключения к API"""
        # Мокируем неудачный ответ
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = hh_api.connect_api('Python')

        assert result is None
        mock_get.assert_called_once()

    @patch('requests.get')
    @pytest.mark.parametrize('status_code', [400, 500, 503])
    def test_connect_api_error_statuses(self, mock_get, hh_api, status_code):
        """Параметризованный тест для различных кодов ошибок"""
        mock_response = Mock()
        mock_response.status_code = status_code
        mock_get.return_value = mock_response

        result = hh_api.connect_api('Python')

        assert result is None

    @patch('requests.get')
    def test_connect_api_empty_response(self, mock_get, hh_api):
        """Тест пустого ответа от API"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'items': []}
        mock_get.return_value = mock_response

        result = hh_api.connect_api('Python')

        assert isinstance(result, list)
        assert len(result) == 0
