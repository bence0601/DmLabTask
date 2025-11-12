from pydantic import BaseModel


class ForecastDTO(BaseModel):

    city_name: str
    temperature: float
    wind: float
    humidity: float  # percentage
