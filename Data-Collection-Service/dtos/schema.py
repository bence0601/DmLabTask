from pydantic import BaseModel
from datetime import date

class CityDTO(BaseModel):
    id: int
    name: str
    last_fetched: date
    data_days_count: int


class WeatherDataDTO(BaseModel):
    id: int
    city_id: int
    date: date
    temperature: float
    wind: float
    humidity: float
    precipitation: float
