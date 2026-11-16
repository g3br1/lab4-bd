import pandas as pd
from datetime import datetime
from app.database import SessionLocal
from app.models import WeatherModel, AirQuality, WindDirectionEnum
from tqdm import tqdm

def calculate_is_good_to_go(pm2_5: float) -> bool:
    if pd.isna(pm2_5):
        return True
    return pm2_5 < 35.0

def import_csv_data(file_path: str):
    print(f"Зчитування файлу {file_path}...")
    df = pd.read_csv(file_path)
    db = SessionLocal()
    
    try:
        count = 0
        for _, row in tqdm(df.iterrows(), total=len(df), desc="Імпорт у БД", unit=" запис"):
            last_updated = None
            last_updated_val = row.get('last_updated')
            if pd.notna(last_updated_val):
                try:
                    dt = pd.to_datetime(last_updated_val, errors='coerce')
                    if pd.notna(dt):
                        last_updated = dt.date()
                except Exception:
                    pass

            sunrise = None
            sunrise_val = row.get('sunrise')
            if pd.notna(sunrise_val):
                try:
                    dt_sun = pd.to_datetime(str(sunrise_val), errors='coerce')
                    if pd.notna(dt_sun):
                        sunrise = dt_sun.time()
                except Exception:
                    sunrise = None

            wind_direction = WindDirectionEnum.Variable
            wind_dir_str = row.get('wind_direction')
            if pd.notna(wind_dir_str):
                try:
                    wind_direction = WindDirectionEnum(str(wind_dir_str).strip())
                except ValueError:
                    wind_direction = WindDirectionEnum.Variable

            pm2_5 = float(row.get('air_quality_PM2.5', 0)) if pd.notna(row.get('air_quality_PM2.5')) else 0.0
            is_good = calculate_is_good_to_go(pm2_5)

            weather_record = WeatherModel(
                country=str(row.get('country', 'Unknown')),
                wind_degree=int(row.get('wind_degree')) if pd.notna(row.get('wind_degree')) else None,
                wind_kph=float(row.get('wind_kph')) if pd.notna(row.get('wind_kph')) else None,
                wind_direction=wind_direction,
                last_updated=last_updated,
                sunrise=sunrise,
                air_quality=AirQuality(
                    air_quality_co=float(row.get('air_quality_Carbon_Monoxide', 0)) if pd.notna(row.get('air_quality_Carbon_Monoxide')) else None,
                    air_quality_no2=float(row.get('air_quality_Nitrogen_dioxide', 0)) if pd.notna(row.get('air_quality_Nitrogen_dioxide')) else None,
                    air_quality_o3=float(row.get('air_quality_Ozone', 0)) if pd.notna(row.get('air_quality_Ozone')) else None,
                    air_quality_so2=float(row.get('air_quality_Sulphur_dioxide', 0)) if pd.notna(row.get('air_quality_Sulphur_dioxide')) else None,
                    air_quality_pm2_5=pm2_5,
                    air_quality_pm10=float(row.get('air_quality_PM10', 0)) if pd.notna(row.get('air_quality_PM10')) else None,
                    is_good_to_go_out=is_good
                )
            )
            db.add(weather_record)
            count += 1
            
        db.commit()
        print(f"Успішно імпортовано {count} записів у базу даних!")
    except Exception as e:
        db.rollback()
        print(f"Помилка при імпорті даних: {e}")
    finally:
        db.close()