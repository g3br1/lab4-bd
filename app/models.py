import enum
from sqlalchemy import Column, Integer, Float, String, Date, Time, Boolean, Enum as SQLAlchemyEnum
from app.database import Base

class WindDirectionEnum(str, enum.Enum):
    N = "N"; NNE = "NNE"; NE = "NE"; ENE = "ENE"; E = "E"; ESE = "ESE"; SE = "SE"; SSE = "SSE"
    S = "S"; SSW = "SSW"; SW = "SW"; WSW = "WSW"; W = "W"; WNW = "WNW"; NW = "NW"; NNW = "NNW"
    Variable = "Variable"

class WeatherModel(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(100), nullable=False)
    wind_degree = Column(Integer, nullable=True)
    wind_kph = Column(Float, nullable=True)
    wind_direction = Column(SQLAlchemyEnum(WindDirectionEnum), nullable=True)
    last_updated = Column(Date, nullable=True)
    sunrise = Column(Time, nullable=True)

    # cтан повітря
    air_quality_co = Column(Float, nullable=True)
    air_quality_no2 = Column(Float, nullable=True)
    air_quality_o3 = Column(Float, nullable=True)
    air_quality_so2 = Column(Float, nullable=True)
    air_quality_pm2_5 = Column(Float, nullable=True)
    air_quality_pm10 = Column(Float, nullable=True)
    
    # якщо PM2.5 < 35 -> True, інакше False
    is_good_to_go_out = Column(Boolean, nullable=True)