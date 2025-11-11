from pydantic import BaseModel


class ForecastDTO(BaseModel):

    temperature: float
    wind: float
    humidity: float  # percentage
