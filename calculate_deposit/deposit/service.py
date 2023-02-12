from .schemas import DataCalculate_IN
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session
from .models import Calculator

COUNT_DEPOSIT = 1
MONTHS = 12


def coef_calculate(amount):
    """Функция рассчитывает коэффициент, на который необходимо
     умножить текущий размер вклада, чтобы получить вклад
     с начисленным процентом."""

    return COUNT_DEPOSIT + (amount / MONTHS)


def current_deposit(coef, amount, delta_date):
    """Функция составляет массив из ежемесячных фин. результатов по вкладу,
     нарастающим эффектом. Может пригодится -> f"{result:.2f}"."""

    array_amounts = []
    for _ in range(delta_date):
        current_amount = round(coef * amount, 2)
        array_amounts.append(current_amount)
        amount = current_amount
    return array_amounts


def quantity_months(start_date, delta_date):
    """Функция составляет массив из рассчетных дат от начальной
     до конечной. Интервал месяц."""

    count, array_dates = 0, []
    while count < delta_date:
        current_date = start_date + relativedelta(months=count)
        array_dates.append(current_date.strftime("%d.%m.%Y"))
        count += 1
    return array_dates


def insert_new_entry_db(db, data, max_amount):
    """Функция записи данных в БД."""

    date = data['date'].strftime("%d.%m.%Y")
    periods = data['periods']
    amount = data['amount']
    rate = round(data['rate'] * 100, 2)
    final_profit = round(max_amount - amount, 2)
    every_month_profit = round(final_profit / periods, 2)
    entry = Calculator(date=date, periods=periods, amount=amount,
                       rate=rate, month_profit=every_month_profit,
                       final_profit=final_profit)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def main_calculate_deposit(db: Session, item: DataCalculate_IN):
    """Главная функция. Возвращает словарь, где ключом является
    интервалы дат, а значением нарастающие суммы депозита.
    Запись данных в БД инициируется тут."""

    data = item.dict()
    coef = coef_calculate(data['rate'])

    array_amounts = current_deposit(coef, data['amount'], data['periods'])
    array_dates = quantity_months(data['date'], data['periods'])
    insert_new_entry_db(db, data, array_amounts[-1])

    return dict(zip(array_dates, array_amounts))


def get_data_deposit(db: Session):
    """Функция возвращает последние данные в БД."""

    return db.query(Calculator).order_by(Calculator.id.desc()).limit(1)[::-1]
