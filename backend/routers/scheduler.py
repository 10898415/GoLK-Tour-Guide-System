import logging
import threading
import time
import schedule
from datetime import datetime, timedelta
from routers.weatherapi import WeatherUpdater
import os
from dotenv import load_dotenv
from routers.chatbot import username, password, uri
from neo4j import GraphDatabase

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scheduler.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("weather_scheduler")

# Get database credentials from environment variables
NEO4J_URI = uri
NEO4J_USER = username
NEO4J_PASSWORD = password

# Configuration
BATCH_SIZE = int(os.getenv("WEATHER_BATCH_SIZE", "58"))  # Locations per batch
UPDATE_INTERVAL_HOURS = float(os.getenv("WEATHER_UPDATE_INTERVAL", "2"))  # Hours between updates for each location
SCHEDULER_INTERVAL_MINUTES = int(os.getenv("SCHEDULER_INTERVAL_MINUTES", "2"))  # Minutes between batch runs


def reset_location_update_timestamps():
    """
    Reset the last_updated timestamps in database to force a complete refresh.
    This ensures locations will be updated on next scheduler run.
    """
    logger.info("Resetting location update timestamps to trigger full refresh")
    try:
        with GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)) as driver:
            with driver.session() as session:
                # Set a very old timestamp for all Areas so they'll be updated
                result = session.run("""
                    MATCH (a:Area)
                    SET a.last_weather_update = '2000-01-01T00:00:00'
                    RETURN count(a) as reset_count
                """)
                record = result.single()
                reset_count = record["reset_count"] if record else 0

                # Also reset Weather nodes timestamps
                result = session.run("""
                    MATCH (w:Weather)
                    SET w.last_updated = '2000-01-01T00:00:00'
                    RETURN count(w) as weather_reset_count
                """)
                record = result.single()
                weather_reset_count = record["weather_reset_count"] if record else 0

                logger.info(f"Reset {reset_count} areas and {weather_reset_count} weather nodes")
                return reset_count > 0
    except Exception as e:
        logger.error(f"Failed to reset timestamps: {str(e)}")
        return False


def run_weather_batch_update():
    """Run a batch update of the weather data for all months."""
    logger.info(f"Starting scheduled weather batch update (batch size: {BATCH_SIZE})")
    try:
        # Create updater with batch processing enabled
        updater = WeatherUpdater(
            NEO4J_URI,
            NEO4J_USER,
            NEO4J_PASSWORD,
            batch_size=BATCH_SIZE,
            update_interval_hours=UPDATE_INTERVAL_HOURS
        )

        # Update a batch of locations with proper historical data
        locations = updater._get_locations_to_update()

        if not locations:
            logger.warning("No locations need updating. Forcing reset of timestamps.")
            if reset_location_update_timestamps():
                logger.info("Successfully reset timestamps. Fetching locations again.")
                locations = updater._get_locations_to_update()
            else:
                logger.error("Failed to reset timestamps for a refresh.")

        logger.info(f"Found {len(locations)} locations to update")

        # Process batch
        success_count = 0
        for location in locations[:BATCH_SIZE]:
            try:
                area = location["area"]
                latitude = location["latitude"]
                longitude = location["longitude"]

                logger.info(f"Updating weather data for {area}")
                updater._update_monthly_weather_data(area, latitude, longitude)

                success_count += 1
            except Exception as e:
                logger.error(f"Failed to update {location['area']}: {str(e)}")

        logger.info(f"Updated {success_count}/{min(len(locations), BATCH_SIZE)} locations in batch")

        # Get and log statistics
        stats = updater.get_update_stats()
        if stats:
            logger.info(f"Weather stats: {stats['areas_with_weather']}/{stats['total_areas']} areas have weather data")
            if 'oldest_update' in stats and stats['oldest_update']:
                oldest_date = datetime.fromisoformat(stats['oldest_update'])
                days_old = (datetime.now() - oldest_date).days
                logger.info(f"Oldest update is {days_old} days old from {oldest_date.isoformat()}")

        logger.info("Weather batch update completed successfully")
        return success_count > 0
    except Exception as e:
        logger.error(f"Weather batch update failed: {str(e)}")
        return False


def run_scheduler():
    """Run the scheduler in a separate thread."""
    logger.info(f"Starting scheduler thread (running every {SCHEDULER_INTERVAL_MINUTES} minutes)")

    # Force a database reset on startup to ensure all locations get updated
    reset_location_update_timestamps()

    # Run immediately on startup
    run_weather_batch_update()

    # Schedule to run every X minutes
    schedule.every(SCHEDULER_INTERVAL_MINUTES).minutes.do(run_weather_batch_update)

    # Run the scheduler loop
    while True:
        schedule.run_pending()
        time.sleep(10)  # Check every 10 seconds


class WeatherScheduler:
    """Weather scheduler class that manages the background thread."""

    def __init__(self):
        """Initialize the scheduler."""
        self.scheduler_thread = None
        self.is_running = False

    def start(self):
        """Start the scheduler in a separate thread."""
        if not self.is_running:
            logger.info("Starting weather scheduler")
            self.is_running = True
            self.scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
            self.scheduler_thread.start()
            return True
        else:
            logger.warning("Scheduler is already running")
            return False

    def force_refresh(self):
        """Force a refresh of all weather data."""
        logger.info("Forcing a complete weather data refresh")
        reset_location_update_timestamps()
        return run_weather_batch_update()

    def is_alive(self):
        """Check if the scheduler thread is alive."""
        if self.scheduler_thread:
            return self.scheduler_thread.is_alive()
        return False

    def get_status(self):
        """Get the current status of the scheduler."""
        return {
            "running": self.is_running,
            "alive": self.is_alive(),
            "batch_size": BATCH_SIZE,
            "update_interval_hours": UPDATE_INTERVAL_HOURS,
            "scheduler_interval_minutes": SCHEDULER_INTERVAL_MINUTES
        }


# Global instance to be imported by other modules
weather_scheduler = WeatherScheduler()