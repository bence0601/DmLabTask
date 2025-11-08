from models.data_models import City,WeatherData
from dtos.schema import CityDTO,WeatherDataDTO

class CityMapper():
    @staticmethod
    def to_model(dto: CityDTO) -> City:
        return City(
            id=dto.id,
            name=dto.name,
            last_fetched=dto.last_fetched,
            data_days_count=dto.data_days_count
        )

class WeatherDataMapper:
    def to_model(dto: WeatherDataDTO) -> WeatherData:
        return WeatherData(
            id=dto.id,
            city_id=dto.city_id,
            date=dto.date,
            temperature=dto.temperature,
            wind=dto.wind,
            humidity=dto.humidity,
            precipitation=dto.precipitation
        )