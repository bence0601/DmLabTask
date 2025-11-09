from models.data_models import City,WeatherData
from dtos.schema import CityDTO,WeatherDataDTO

class CityMapper():
    @staticmethod
    def to_model(dto: CityDTO) -> City:
        return City(
            name=dto.name,
        )

class WeatherDataMapper:
    def to_model(dto: WeatherDataDTO, city_id : int) -> WeatherData:
        return WeatherData(
            city_id=city_id,
            date=dto.date,
            temperature=dto.temperature,
            wind=dto.wind,
            humidity=dto.humidity,
        )