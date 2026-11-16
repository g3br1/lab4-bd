from datetime import datetime
from app.database import SessionLocal
from app.models import WeatherModel

def search_weather():
    db = SessionLocal()
    country_input = input("Введіть назву країни: ").strip()
    date_input = input("Введіть дату у форматі YYYY-MM-DD (або залиште порожнім): ").strip()

    query = db.query(WeatherModel).filter(WeatherModel.country.ilike(f"%{country_input}%"))

    if date_input:
        try:
            search_date = datetime.strptime(date_input, "%Y-%m-%d").date()
            query = query.filter(WeatherModel.last_updated == search_date)
        except ValueError:
            print("Неправильний формат дати! Пошук відбудеться без урахування дати.")

    results = query.limit(10).all()

    if not results:
        print("Нічого не знайдено за вашим запитом.")
    else:
        print(f"\nЗнайдено записів: {len(results)}")
        for r in results:
            print("-" * 40)
            print(f"Країна: {r.country}, Дата: {r.last_updated}")
            print(f"Вітер: {r.wind_kph} км/год ({r.wind_direction}), градусів: {r.wind_degree}°")
            print(f"Стан повітря -> PM2.5: {r.air_quality_pm2_5}, PM10: {r.air_quality_pm10}")
            recommendation = "ТАК" if r.is_good_to_go_out else "НІ"
            print(f"Чи варто виходити на вулицю: {recommendation}")
            print("-" * 40)

    db.close()