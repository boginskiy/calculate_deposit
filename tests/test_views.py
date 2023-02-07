from unittest import TestCase
from fastapi.testclient import TestClient
from http import HTTPStatus
from main import app


class MainPageTest(TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.response = self.client.get("/")

    def test_status_code_main_page(self):
        """Проверка статуса ответа главной страницы."""

        self.assertEqual(self.response.status_code,
                         HTTPStatus.OK, 'Ошибка статуса ответа для /')

    def test_html_main_page(self):
        """Проверка типа контента главной страницы."""

        self.assertIn('text/html', self.response.headers.get('content-type'),
                      'Ошибка типа контента, должен быть text/html')


class CalculateDepositTest(TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.test_days = ['31.01.2021', '28.02.2021', '31.03.2021']
        self.test_amount = [10050.0, 10100.25, 10150.75]

    def test_not_fields_body_json(self):
        """Проверка статуса ответа и описание ошибки при обращении к
        /calculate при условии, что ничего не передаем в теле запроса."""

        response = self.client.post("/calculate", json={})
        self.assertEqual(response.status_code,
                         HTTPStatus.BAD_REQUEST,
                         'При отправке пустого запроса поднять ошибку 400')

        self.assertEqual(response.json(),
                         {'error': 'All fields are required'},
                         'Некорректный вывод ошибки при пустом запросе')

    def test_some_fields_body_json(self):
        """Проверка статуса ответа и описание ошибки при обращении к
        /calculate при условии, что передаем неполные данные в теле запроса."""

        response = self.client.post(
            "/calculate",
            json={"date": "10.12.2016", "amount": 10_000, "rate": 1})

        self.assertEqual(response.status_code,
                         HTTPStatus.BAD_REQUEST,
                         'При отправке запроса c отсутствующим полем поднять ошибку 400')

        self.assertEqual(response.json(),
                         {'error': 'field periods: field required'},
                         'Некорректный вывод ошибки при частичном запросе')

    def test_full_fields_body_json(self):
        """Проверка выходных данных: даты начислений и суммы по вкладу, так же
        статус ответа."""

        self.response = self.client.post(
            "/calculate", json={"date": "31.01.2021", "periods": 3,
                                "amount": 10_000, "rate": 6})

        self.assertEqual(self.response.status_code,
                         HTTPStatus.OK,
                         'Ошибка статуса ответа при отправке корректных данных')

        date_array = list(self.response.json().keys())
        for i in range(len(date_array)):
            self.assertEqual(date_array[i], self.test_days[i],
                            f'Ошибка в {i + 1} дате начислений по вкладу')

        amount_array = list(self.response.json().values())
        for i in range(len(amount_array)):
            self.assertEqual(amount_array[i], self.test_amount[i],
                            f'Ошибка в {i + 1} начислении по вкладу')

    def test_type_fields_data_json(self):
        """Проверка типа выходных данных date - str, amount - float."""

        self.response = self.client.post(
            "/calculate", json={"date": "31.01.2021", "periods": 3,
                                "amount": 10_000, "rate": 6})

        result = self.response.json()
        for date, amount in result.items():
            self.assertEqual(type(date), str, f'Неверный тип данных даты {date}')
            self.assertEqual(type(amount), float, f'Неверный тип данных вклада {amount}')

    def test_validation_fields_date(self):
        """Проверка статуса ответа и предупреждения о нарушении валидации поля date."""

        response = self.client.post(
            "/calculate", json={"date": "2021.12.31", "periods": 3,
                                "amount": 10_000, "rate": 6})

        self.assertEqual(response.status_code,
                         HTTPStatus.BAD_REQUEST,
                         'При ошибке валидации поля date поднять ошибку 400')

        self.assertIn("field date: ", response.json()['error'],
                      'Неверный вывод предупреждения о нарушении валидации поля date')

    def test_validation_fields_periods(self):
        """Проверка статуса ответа и предупреждения о нарушении валидации поля periods."""

        error_validation_val = [0, 61]

        for val in error_validation_val:
            response = self.client.post(
                "/calculate", json={"date": "31.12.2021", "periods": val,
                                    "amount": 10_000, "rate": 6})

            self.assertEqual(response.status_code,
                             HTTPStatus.BAD_REQUEST,
                             'При ошибке валидации поля periods поднять ошибку 400')

            self.assertIn("field periods: ", response.json()['error'],
                'Неверный вывод предупреждения о нарушении валидации поля periods')

    def test_validation_fields_amount(self):
        """Проверка статуса ответа и предупреждения о нарушении валидации поля amount."""

        error_validation_val = [9_999, 3_000_001]

        for val in error_validation_val:
            response = self.client.post(
                "/calculate", json={"date": "31.12.2021", "periods": 5,
                                    "amount": val, "rate": 6})

            self.assertEqual(response.status_code,
                             HTTPStatus.BAD_REQUEST,
                             'При ошибке валидации поля amount поднять ошибку 400')

            self.assertIn('field amount: ', response.json()['error'],
                'Неверный вывод предупреждения о нарушении валидации поля amount')

    def test_validation_fields_rate(self):
        """Проверка статуса ответа и предупреждения о нарушении валидации поля rate."""

        error_validation_val = [0.99, 8.01]

        for val in error_validation_val:
            response = self.client.post(
                "/calculate", json={"date": "31.12.2021", "periods": 5,
                                    "amount": 10_000, "rate": val})

            self.assertEqual(response.status_code,
                             HTTPStatus.BAD_REQUEST,
                             'При ошибке валидации поля rate поднять ошибку 400')

            self.assertIn('field rate: ', response.json()['error'],
                'Неверный вывод предупреждения о нарушении валидации поля rate')

    def test_fields_values_periods_num(self):
        """Проверка максимального количества данных через ввод periods."""

        validation_val = (i for i in range(1, 61))

        for val in validation_val:
            response = self.client.post(
                "/calculate", json={"date": "5.11.2021", "periods": val,
                                    "amount": 10_000, "rate": 6})

            self.assertEqual(response.status_code, HTTPStatus.OK,
                             f'Ошибка при формировании данных на {val} периоде')

            self.assertEqual(
                len(response.json()), val,
                f'Ошибка в расчетах при вводе значения {val} поля periods')

    def test_several_years_date(self):
        """Проверка корректного перехода на следующий годовой период."""

        test_several_years = ['05.11.2021', '05.12.2021', '05.01.2022', '05.02.2022']
        response = self.client.post(
            "/calculate", json={"date": "5.11.2021", "periods": 4,
                                "amount": 10_000, "rate": 6})

        for i in range(len(test_several_years)):
            self.assertEqual(list(response.json().keys())[i], test_several_years[i],
                             'Ошибка при переходе от старого к новому году')

    def test_fields_max_values_amount_num(self):
        """Проверка корректности вычислений для максимального значения
        и минимального периода вклада."""

        response = self.client.post(
            "/calculate", json={"date": "5.11.2021", "periods": 1,
                                "amount": 3_000_000, "rate": 6})

        self.assertEqual(response.json()['05.11.2021'], 3015000,
                         'Проверить вычисления для поля amount c max значением')

    def test_fields_values_rate_float_num(self):
        """Проверка корректности вычислений при использовании числа с плавающей точкой
         для поля rate."""

        response = self.client.post(
            "/calculate", json={"date": "31.12.2021", "periods": 1,
                                "amount": 10_000, "rate": 5.59})

        self.assertEqual(response.json()['31.12.2021'], 10046.58,
                         'Проверить вычисления для поля rate на числах с плав. точкой')
