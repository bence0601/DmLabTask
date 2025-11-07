import logging

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from models.data_models import SeedStatus,create_city,create_weather_data

logger = logging.getLogger(__name__)  

def _preseed_database(engine):
    
    default_cities = ["Budapest", "New York", "Debrecen", "Lisszabon","Bécs"]

    with Session(engine) as session:
        try:            
            status = session.query(SeedStatus).first()
            if status and status.seeded:
                logger.info("Preseed already completed. Skipping.")
                return
            
            successfully_seeded = []
            failed_cities = []

            MAX_RETRIES = 2

            for city_name in default_cities:
                attempt = 0
                while attempt<=MAX_RETRIES:
                    try:
                        with session.begin_nested():
                            city_id = create_city(session, city_name)
                            weather_data = create_weather_data(session, city_id)
                            successfully_seeded.append(city_name)
                        break
                    except Exception as e:
                        attempt += 1
                        logger.exception(f"Failed seeding city {city_name}: {e}")
                        if attempt > MAX_RETRIES:
                            failed_cities.append(city_name)
                    
            if successfully_seeded:
                if not status:
                    status = SeedStatus(seeded=True)
                    session.add(status)
                else:
                    status.seeded = True
                
                session.commit()
                logger.info("Successfully seeded")
                
            
            session.rollback()
            logger.error("No cities were successfully seeded")
            raise RuntimeError("Preseed failed for all cities")

        
        except Exception as e:
            session.rollback()
            logger.critical(f"Critical error during database preseed: {e}")

            
        except Exception as e:
            session.rollback()
            logger.error(f"Critical error during database preseed: {e}")


