import logging

from sqlalchemy.orm import Session

from models.data_models import SeedStatus
from repositories.city_repository import create_city
from repositories.weather_repository import create_weather_data_for_preseed

logger = logging.getLogger(__name__)

def preseed_database(engine):

    default_cities = ["Budapest", "New York", "Debrecen", "Lisszabon", "Bécs"]

    with Session(engine) as session:
            status = session.query(SeedStatus).first()
            if status and status.seeded:
                logger.info("Preseed already completed. Skipping.")
                return

            successfully_seeded = []
            failed_cities = []

            MAX_RETRIES = 2

            for city_name in default_cities:
                attempt = 0
                while attempt <= MAX_RETRIES:
                    try:
                        with session.begin_nested():
                            city = create_city(session, city_name)
                            create_weather_data_for_preseed(session, city.id)
                            successfully_seeded.append(city_name)
                        break
                    except Exception as e:
                        attempt += 1
                        logger.exception(f"Failed seeding city {city_name}: {e}")
                        if attempt > MAX_RETRIES:
                            failed_cities.append(city_name)

            if len(successfully_seeded)==5:
                if not status:
                    status = SeedStatus(seeded=True)
                    session.add(status)
                else:
                    status.seeded = True

                session.commit()
                logger.info("Successfully seeded")
                return



