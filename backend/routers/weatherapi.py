import pandas as pd
import openmeteo_requests
import requests_cache
from retry_requests import retry
import logging
from datetime import datetime, timedelta
from neo4j import GraphDatabase
import calendar
import time
import os
from typing import List, Dict, Any

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("weather_updater.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("weather_updater")


class WeatherUpdater:
    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str,
                 batch_size: int = 50, update_interval_hours: float = 2.0):
        """Initialize the weather updater with database connection details."""
        self.neo4j_uri = neo4j_uri
        self.neo4j_user = neo4j_user
        self.neo4j_password = neo4j_password
        self.batch_size = batch_size
        self.update_interval_hours = update_interval_hours

        # Setup the Open-Meteo API client
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        self.openmeteo = openmeteo_requests.Client(session=retry_session)

    def _get_db_driver(self):
        """Create and return a Neo4j driver instance."""
        return GraphDatabase.driver(
            self.neo4j_uri,
            auth=(self.neo4j_user, self.neo4j_password)
        )

    def _get_sri_lanka_season(self, month: int) -> str:
        """Determine the season in Sri Lanka based on the month."""
        if month in [12, 1, 2]:
            return "Northeast Monsoon"
        elif month in [3, 4]:
            return "First Inter-monsoon"
        elif month in [5, 6, 7, 8, 9]:
            return "Southwest Monsoon"
        else:  # 10, 11
            return "Second Inter-monsoon"

    def _determine_weather_description(self, temp: float, precip_prob: float, wind_speed: float) -> str:
        """Determine a descriptive weather condition."""
        if precip_prob > 70:
            return "Cool and Rainy" if temp < 22 else "Warm and Rainy"
        elif precip_prob > 30:
            return "Partly Cloudy with Chance of Rain"
        elif wind_speed > 20:
            return "Windy"
        elif temp > 30:
            return "Hot and Sunny"
        elif temp > 25:
            return "Warm and Sunny"
        return "Pleasant"

    def _get_locations_to_update(self) -> List[Dict[str, Any]]:
        """Get locations that need updating, prioritizing never-updated locations."""
        logger.info("Fetching locations that need updates...")

        try:
            # Read coordinates from CSV
            try:
                coords_df = pd.read_csv("routers/Coordinates.csv")
            except Exception as e:
                logger.error(f"Error reading coordinates file: {str(e)}")
                return []

            # Validate required columns
            required_columns = ["Area", "Latitude", "Longitude"]
            if not all(col in coords_df.columns for col in required_columns):
                logger.error(f"Missing required columns in coordinates file")
                return []

            # Get last update times from database
            with self._get_db_driver() as driver:
                with driver.session() as session:
                    result = session.run("""
                        MATCH (a:Area)
                        OPTIONAL MATCH (a)-[:HAS_WEATHER]->(w:Weather)
                        RETURN a.Areas as area, 
                               a.Latitude as latitude,
                               a.Longitude as longitude,
                               w.last_updated as last_updated
                    """)

                    area_updates = {}
                    for record in result:
                        area = record["area"]
                        area_updates[area] = {
                            "last_updated": datetime.fromisoformat(record["last_updated"]) if record[
                                "last_updated"] else datetime.min,
                            "latitude": record["latitude"],
                            "longitude": record["longitude"]
                        }

            # Determine locations needing update
            cutoff_time = datetime.now() - timedelta(hours=self.update_interval_hours)
            locations_to_update = []

            for _, row in coords_df.iterrows():
                area = row['Area']
                if area not in area_updates:  # New area not in database yet
                    locations_to_update.append({
                        "area": area,
                        "latitude": float(row['Latitude']),
                        "longitude": float(row['Longitude']),
                        "last_updated": datetime.min,
                        "priority": 0  # Highest priority
                    })
                elif area_updates[area]["last_updated"] < cutoff_time:
                    locations_to_update.append({
                        "area": area,
                        "latitude": area_updates[area]["latitude"],
                        "longitude": area_updates[area]["longitude"],
                        "last_updated": area_updates[area]["last_updated"],
                        "priority": 1  # Normal priority
                    })

            # Sort by priority and then by last_updated
            locations_to_update.sort(key=lambda x: (x["priority"], x["last_updated"]))
            logger.info(f"Found {len(locations_to_update)} locations needing update")
            return locations_to_update

        except Exception as e:
            logger.error(f"Error getting locations to update: {str(e)}")
            return []

    def update_batch_of_locations(self) -> bool:
        """Update weather data for a batch of locations."""
        locations = self._get_locations_to_update()
        if not locations:
            logger.info("No locations need updating at this time.")
            return False

        # Process batch
        success_count = 0
        for location in locations[:self.batch_size]:
            try:
                self._update_monthly_weather_data(
                    location["area"],
                    location["latitude"],
                    location["longitude"]
                )
                success_count += 1
            except Exception as e:
                logger.error(f"Failed to update {location['area']}: {str(e)}")

        logger.info(f"Updated {success_count}/{len(locations[:self.batch_size])} locations in batch")
        return success_count > 0

    def _update_monthly_weather_data(self, area: str, lat: float, lon: float):
        """Update weather data for all months for a specific location."""
        current_date = datetime.now()

        # Get current weather data
        current_data = self._get_current_weather(lat, lon)
        if not current_data:
            logger.warning(f"No current weather data for {area}")
            return

        # Get historical climate data for all months
        monthly_data = self._get_historical_weather(lat, lon)
        if not monthly_data:
            logger.warning(f"No historical data for {area}")
            monthly_data = {}

        # Update current month with real-time data
        current_month = current_date.month
        if current_month in monthly_data:
            monthly_data[current_month].update({
                "current_temp": current_data["temp"],
                "max_temp": current_data["max_temp"],
                "min_temp": current_data["min_temp"],
                "precipitation": current_data["precip"],
                "precipitation_prob": current_data["precip_prob"],
                "wind_speed": current_data["wind_speed"],
                "description": current_data["description"]
            })

        # Ensure we have data for all 12 months
        for month_num in range(1, 13):
            if month_num not in monthly_data:
                # Create default data for missing months
                monthly_data[month_num] = {
                    "month_name": calendar.month_name[month_num],
                    "season": self._get_sri_lanka_season(month_num),
                    "description": "No data available",
                    "avg_temp": 0.0,
                    "avg_precip": 0.0,
                    "avg_wind": 0.0,
                    "precip_prob": 0.0
                }

        # Update database with all months
        self._update_database(area, monthly_data, current_date.isoformat())

    def _get_current_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        """Get current weather data from API."""
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": ["temperature_2m", "precipitation_probability", "wind_speed_10m"],
            "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
            "timezone": "Asia/Colombo",
            "forecast_days": 1
        }

        try:
            responses = self.openmeteo.weather_api(
                "https://api.open-meteo.com/v1/forecast",
                params=params
            )
            response = responses[0]

            # Process hourly data
            hourly = response.Hourly()
            current_hour = min(datetime.now().hour, len(hourly.Variables(0).ValuesAsNumpy()) - 1)
            temp = hourly.Variables(0).ValuesAsNumpy()[current_hour]
            precip_prob = hourly.Variables(1).ValuesAsNumpy()[current_hour]
            wind_speed = hourly.Variables(2).ValuesAsNumpy()[current_hour]

            # Process daily data
            daily = response.Daily()
            max_temp = daily.Variables(0).ValuesAsNumpy()[-1]
            min_temp = daily.Variables(1).ValuesAsNumpy()[-1]
            precip = daily.Variables(2).ValuesAsNumpy()[-1]

            return {
                "temp": float(temp),
                "precip_prob": float(precip_prob),
                "wind_speed": float(wind_speed),
                "max_temp": float(max_temp),
                "min_temp": float(min_temp),
                "precip": float(precip),
                "description": self._determine_weather_description(temp, precip_prob, wind_speed)
            }
        except Exception as e:
            logger.error(f"Error getting current weather: {str(e)}")
            return None

    def _get_historical_weather(self, lat: float, lon: float) -> Dict[int, Dict[str, Any]]:
        """Get historical climate data from API and calculate monthly averages."""
        # Calculate date range (today minus one year)
        end_date = datetime.now() - timedelta(days=2)
        start_date = end_date - timedelta(days=365)

        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "wind_speed_10m_max"],
            "timezone": "Asia/Colombo",
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }

        try:
            responses = self.openmeteo.weather_api(
                "https://archive-api.open-meteo.com/v1/archive",
                params=params
            )
            response = responses[0]
            daily = response.Daily()

            # Get all daily data
            dates = pd.to_datetime(daily.Time(), unit='s', utc=True).tz_convert("Asia/Colombo")
            max_temps = daily.Variables(0).ValuesAsNumpy()
            min_temps = daily.Variables(1).ValuesAsNumpy()
            precip = daily.Variables(2).ValuesAsNumpy()
            wind_speeds = daily.Variables(3).ValuesAsNumpy()

            # Create a DataFrame for easier monthly calculations
            df = pd.DataFrame({
                'date': dates,
                'month': dates.month,
                'max_temp': max_temps,
                'min_temp': min_temps,
                'precip': precip,
                'wind_speed': wind_speeds
            })

            # Calculate monthly averages
            monthly_avg = df.groupby('month').agg({
                'max_temp': 'mean',
                'min_temp': 'mean',
                'precip': 'sum',  # Total precipitation for the month
                'wind_speed': 'mean'
            }).reset_index()

            monthly_data = {}
            for _, row in monthly_avg.iterrows():
                month_num = int(row['month'])
                avg_temp = (row['max_temp'] + row['min_temp']) / 2
                total_precip = row['precip']
                avg_wind = row['wind_speed']

                # Calculate precipitation probability based on actual rainy days
                month_df = df[df['month'] == month_num]
                rainy_days = len(month_df[month_df['precip'] > 0.1])  # Days with >0.1mm precipitation
                precip_prob = (rainy_days / len(month_df)) * 100 if len(month_df) > 0 else 0

                monthly_data[month_num] = {
                    "month_name": calendar.month_name[month_num],
                    "season": self._get_sri_lanka_season(month_num),
                    "description": self._determine_weather_description(avg_temp, precip_prob, avg_wind),
                    "avg_temp": float(avg_temp),
                    "avg_precip": float(total_precip),
                    "avg_wind": float(avg_wind),
                    "precip_prob": float(precip_prob)
                }

            return monthly_data

        except Exception as e:
            logger.error(f"Error getting historical weather: {str(e)}")
            return None

    def _update_database(self, area: str, monthly_data: Dict[int, Dict[str, Any]], last_updated: str):
        """Update Neo4j database with weather data."""
        with self._get_db_driver() as driver:
            with driver.session() as session:
                # Update all 12 months
                for month_num in range(1, 13):
                    try:
                        data = monthly_data.get(month_num, {
                            "month_name": calendar.month_name[month_num],
                            "season": self._get_sri_lanka_season(month_num),
                            "description": "No data available",
                            "avg_temp": 0.0,
                            "avg_precip": 0.0,
                            "avg_wind": 0.0,
                            "precip_prob": 0.0
                        })

                        session.run("""
                            MERGE (w:Weather {Month: $month})
                            SET w += $data,
                                w.last_updated = $last_updated
                            WITH w
                            MATCH (a:Area {Areas: $area})
                            MERGE (a)-[r:HAS_WEATHER]->(w)
                            SET a.last_weather_update = $last_updated
                        """, {
                            "month": calendar.month_name[month_num],
                            "area": area,
                            "data": {
                                "season": data["season"],
                                "description": data["description"],
                                "avg_temp": data["avg_temp"],
                                "avg_precip": data["avg_precip"],
                                "avg_wind": data["avg_wind"],
                                "precip_prob": data["precip_prob"],
                                **({k: v for k, v in data.items() if k in [
                                    "current_temp", "max_temp", "min_temp",
                                    "precipitation", "precipitation_prob",
                                    "wind_speed"
                                ]} if "current_temp" in data else {})
                            },
                            "last_updated": last_updated
                        })
                    except Exception as e:
                        logger.error(f"Database error for {area} month {month_num}: {str(e)}")

        logger.info(f"Updated database for {area}")

    def get_update_stats(self) -> Dict[str, Any]:
        """Get statistics about weather updates."""
        try:
            with self._get_db_driver() as driver:
                with driver.session() as session:
                    result = session.run("""
                        MATCH (a:Area)
                        WITH count(a) as total_areas
                        MATCH (a:Area)-[:HAS_WEATHER]->(w:Weather)
                        RETURN total_areas,
                               count(DISTINCT a) as areas_with_weather,
                               min(w.last_updated) as oldest_update,
                               max(w.last_updated) as newest_update
                    """)
                    record = result.single()
                    return dict(record) if record else None
        except Exception as e:
            logger.error(f"Error getting stats: {str(e)}")
            return None