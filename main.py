import os
from app.services import import_csv_data
from app.cli import search_weather

if __name__ == "__main__":
    print("Виберіть дію:")
    print("1 - Імпортувати дані з CSV у базу даних")
    print("2 - Запустити консольний пошук погоди")
    
    choice = input("Ваш вибір (1 або 2): ").strip()
    
    if choice == "1":
        file_path = "GlobalWeatherRepository.csv"
        if os.path.exists(file_path):
            print(f"Знайдено файл: {file_path}")
            import_csv_data(file_path)
        else:
            print(f"Помилка: Файл '{file_path}' не знайдено у кореню проєкту!")
    elif choice == "2":
        search_weather()
    else:
        print("Невірний вибір.")