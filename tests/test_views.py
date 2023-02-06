from unittest import TestCase
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

    def test_html_main_page(self):
        self.assertIn('text/html', self.response.headers.get('content-type'),
                      'Ошибка типа контента, должен быть text/html')


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
        response = client.post(
            "/calculate", json={"date": "2021.12.31", "periods": 3,
                                "amount": 10_000, "rate": 6})

        self.assertEqual(response.status_code,
                         HTTPStatus.BAD_REQUEST,
                         'При ошибке валидации поля date поднять ошибку 400')
        self.assertEqual(
            response.json(),
            {"error": "field date: time data '2021.12.31' does not match format '%d.%m.%Y'"},
            'Неверный вывод предупреждения о нарушении валидации поля date')

    def test_validation_fields_periods(self):
        error_validation_val = [0, 61]

        for val in error_validation_val:
            response = client.post(
                "/calculate", json={"date": "31.12.2021", "periods": val,
                                    "amount": 10_000, "rate": 6})

            self.assertEqual(response.status_code,
                             HTTPStatus.BAD_REQUEST,
                             'При ошибке валидации поля periods поднять ошибку 400')

            self.assertIn("field periods: ", response.json()['error'],
                'Неверный вывод предупреждения о нарушении валидации поля periods')

    def test_validation_fields_amount(self):
        error_validation_val = [9_999, 3_000_001]

        for val in error_validation_val:
            response = client.post(
                "/calculate", json={"date": "31.12.2021", "periods": 5,
                                    "amount": val, "rate": 6})

            self.assertEqual(response.status_code,
                             HTTPStatus.BAD_REQUEST,
                             'При ошибке валидации поля amount поднять ошибку 400')

            self.assertIn('field amount: ', response.json()['error'],
                'Неверный вывод предупреждения о нарушении валидации поля amount')

    def test_validation_fields_rate(self):
        error_validation_val = [0.99, 8.01]

        for val in error_validation_val:
            response = client.post(
                "/calculate", json={"date": "31.12.2021", "periods": 5,
                                    "amount": 10_000, "rate": val})

            self.assertEqual(response.status_code,
                             HTTPStatus.BAD_REQUEST,
                             'При ошибке валидации поля rate поднять ошибку 400')

            self.assertIn('field rate: ', response.json()['error'],
                'Неверный вывод предупреждения о нарушении валидации поля rate')

    def test_several_years_date(self):
        test_several_years = ['05.11.2021', '05.12.2021', '05.01.2022', '05.02.2022']
        response = client.post(
            "/calculate", json={"date": "5.11.2021", "periods": 4,
                                "amount": 10_000, "rate": 6})
        for i in range(len(test_several_years)):
            self.assertEqual(list(response.json().keys())[i], test_several_years[i],
                             'Ошибка при переходе старого и нового года')

    def test_fields_values_periods_num(self):
        validation_val = (i for i in range(1, 61))

        for val in validation_val:
            response = client.post(
                "/calculate", json={"date": "5.11.2021", "periods": val,
                                    "amount": 10_000, "rate": 6})

            self.assertEqual(response.status_code, HTTPStatus.OK,
                             f'Ошибка при формировании данных на {val} периоде')

            self.assertEqual(
                len(response.json()), val,
                f'Ошибка в расчетах при вводе значения {val} поля periods')

    def test_fields_max_values_amount_num(self):
        response = client.post(
            "/calculate", json={"date": "5.11.2021", "periods": 1,
                                "amount": 3_000_000, "rate": 6})
        self.assertEqual(response.json()['05.11.2021'], 3015000,
                         'Проверить вычисления для поля amount c max значением')

    def test_fields_values_rate_float_num(self):
        response = client.post(
            "/calculate", json={"date": "31.12.2021", "periods": 1,
                                "amount": 10_000, "rate": 5.59})
        self.assertEqual(response.json()['31.12.2021'], 10046.58,
                         'Проверить вычисления для поля rate на числах с плав. точкой')
