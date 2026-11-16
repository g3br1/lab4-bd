import enum
from sqlalchemy import Column, Integer, String, Float, Date, Time, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class WindDirectionEnum(str, enum.Enum):
    N = "N"; NNE = "NNE"; NE = "NE"; ENE = "ENE"; E = "E"; ESE = "ESE"; SE = "SE"; SSE = "SSE"
    S = "S"; SSW = "SSW"; SW = "SW"; WSW = "WSW"; W = "W"; WNW = "WNW"; NW = "NW"; NNW = "NNW"
    Variable = "Variable"

class WeatherModel(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, index=True, nullable=False)
    wind_degree = Column(Integer, nullable=False)
    wind_kph = Column(Float, nullable=False)
    wind_direction = Column(Enum(WindDirectionEnum), nullable=False)
    last_updated = Column(Date, index=True, nullable=False)
    sunrise = Column(Time, nullable=False)
    is_good_to_go_out = Column(Boolean, nullable=False)

    air_quality = relationship(
        "AirQuality",
        back_populates="weather",
        uselist=False,
        cascade="all, delete-orphan"
    )


class AirQuality(Base):
    __tablename__ = "air_quality"

    id = Column(Integer, primary_key=True, index=True)
    weather_id = Column(
        Integer,
        ForeignKey("weather_data.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )
    air_quality_co = Column(Float, nullable=True)
    air_quality_no2 = Column(Float, nullable=True)
    air_quality_o3 = Column(Float, nullable=True)
    air_quality_so2 = Column(Float, nullable=True)
    air_quality_pm2_5 = Column(Float, nullable=True)
    air_quality_pm10 = Column(Float, nullable=True)

    weather = relationship("WeatherModel", back_populates="air_quality")