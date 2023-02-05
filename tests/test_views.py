from unittest import TestCase
from deposit.views import *
from fastapi.testclient import TestClient
from http import HTTPStatus
from main import app

client = TestClient(app)


class MainPageTest(TestCase):
    def setUp(self):
        self.response = client.get("/")

    def test_status_code_main_page(self):
        self.assertEqual(self.response.status_code,
                         HTTPStatus.OK, 'Ошибка статуса ответа для /')

    # def test_data_main_page(self):
    #     assert self.response.json() == {"aaaa": 1234}, "Ошибка контента главной страницы"


class CalculateDepositTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.response = client.post(
            "/calculate", json={"date": "31.01.2021", "periods": 3,
                                "amount": 10_000, "rate": 6})

        cls.test_days = ['31.01.2021', '28.02.2021', '31.03.2021']
        cls.test_amount = [10050.0, 10100.25, 10150.75]

    def test_not_fields_body_json(self):
        response = client.post("/calculate", json={})
        self.assertEqual(response.status_code,
                         HTTPStatus.BAD_REQUEST,
                         'При отправке пустого запроса поднять ошибку 400')

        self.assertEqual(response.json(),
                         {'error': 'All fields are required'},
                         'Некорректный вывод ошибки при пустом запросе')

    def test_some_fields_body_json(self):
        response = client.post("/calculate",
                               json={"date": "10.12.2016", "amount": 10_000, "rate": 1})
        self.assertEqual(response.status_code,
                         HTTPStatus.BAD_REQUEST,
                         'При отправке запроса c отсутствующим полем поднять ошибку 400')

        self.assertEqual(response.json(),
                         {'error': 'field periods: field required'},
                         'Некорректный вывод ошибки при частичном запросе')

    def test_full_fields_body_json(cls):
        cls.assertEqual(cls.response.status_code,
                         HTTPStatus.OK,
                         'Ошибка статуса ответа при отправке корректных данных')

        date_array = list(cls.response.json().keys())
        for i in range(len(date_array)):
            cls.assertEqual(date_array[i], cls.test_days[i],
                            f'Ошибка в {i + 1} дате начислений по вкладу')

        amount_array = list(cls.response.json().values())
        for i in range(len(amount_array)):
            cls.assertEqual(amount_array[i], cls.test_amount[i],
                            f'Ошибка в {i + 1} начислении по вкладу')

    def test_type_fields_data_json(cls):
        result = cls.response.json()
        for date, amount in result.items():
            cls.assertEqual(type(date), str, f'Неверный тип данных даты {date}')
            cls.assertEqual(type(amount), float, f'Неверный тип данных вклада {amount}')

    def test_validation_fields_date(self):
        response_date = client.post(
            "/calculate", json={"date": "2021.12.31", "periods": 3,
                                "amount": 10_000, "rate": 6})

        self.assertEqual(response_date.status_code,
                         HTTPStatus.BAD_REQUEST,
                         'При ошибке валидации поля date поднять ошибку 400')
        self.assertEqual(
            response_date.json(),
            {"error": "field date: time data '2021.12.31' does not match format '%d.%m.%Y'"},
            'Неверный вывод предупреждения о нарушении валидации поля date')

    def test_validation_fields_periods(self):
        response_date = client.post(
            "/calculate", json={"date": "31.12.2021", "periods": 100,
                                "amount": 10_000, "rate": 6})

        self.assertEqual(response_date.status_code,
                         HTTPStatus.BAD_REQUEST,
                         'При ошибке валидации поля periods поднять ошибку 400')

        self.assertEqual(
            response_date.json(),
            {"error": "field periods: ensure this value is less than or equal to 60"},
            'Неверный вывод предупреждения о нарушении валидации поля periods')

    def test_validation_fields_amount(self):
        response_date = client.post(
            "/calculate", json={"date": "31.12.2021", "periods": 60,
                                "amount": 10_000_000, "rate": 6})

        self.assertEqual(response_date.status_code,
                         HTTPStatus.BAD_REQUEST,
                         'При ошибке валидации поля amount поднять ошибку 400')
        self.assertEqual(
            response_date.json(),
            {'error': 'field amount: ensure this value is less than or equal to 3000000'},
            'Неверный вывод предупреждения о нарушении валидации поля amount')

    def test_validation_fields_rate(self):
        response_date = client.post(
            "/calculate", json={"date": "31.12.2021", "periods": 60,
                                "amount": 10_000, "rate": 15})

        self.assertEqual(response_date.status_code,
                         HTTPStatus.BAD_REQUEST,
                         'При ошибке валидации поля rate поднять ошибку 400')
        self.assertEqual(
            response_date.json(),
            {'error': 'field rate: ensure this value is less than or equal to 8'},
            'Неверный вывод предупреждения о нарушении валидации поля amount')


# Проверить переходные даты годовые
# Проверить максимальные и минимальные значения
#
