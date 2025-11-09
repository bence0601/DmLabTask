from pydantic import BaseModel, field_validator, Field
import datetime


class CityDTO(BaseModel):
    name: str


class WeatherDataDTO(BaseModel):
    date: datetime.date = Field(default_factory=datetime.date.today)
    temperature: float
    wind: float
    humidity: float  # percentage

    @field_validator("temperature", mode="before")
    @classmethod
    def _kelvin_to_celsius(cls, temp):
        if isinstance(temp, (int, float)):
            return round(temp - 273.15, 2)
        return temp
