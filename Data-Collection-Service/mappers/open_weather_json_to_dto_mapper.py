from dtos.schema import CityDTO, WeatherDataDTO


class WeatherApiToDtoMapper:
    @staticmethod
    def extract_city_dto(response_data: dict) -> CityDTO:
        return CityDTO(name=response_data["name"])

    @staticmethod
    def extract_weather_dto(response_data: dict) -> WeatherDataDTO:
        return WeatherDataDTO(
            temperature=response_data["main"]["temp"],
            wind=response_data["wind"]["speed"],
            humidity=response_data["main"]["humidity"],
        )
