from typing import Optional, List
from enum import Enum

from fastapi import FastAPI, BackgroundTasks, Query, Path
from fastapi.responses import FileResponse
from routers import chatbot
import logging
from routers.scheduler import weather_scheduler, run_weather_batch_update

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("main")

app = FastAPI(title="GoLK - AI Tour Guide")

# Include chatbot routes
app.include_router(chatbot.router, prefix="/api", tags=["Chatbot"])


@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")


@app.get("/")
def home():
    return {"message": "Welcome to GoLK - Your AI-Powered Sri Lanka Tour Guide!"}


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("Starting application")

    # Start the weather scheduler in the background
    weather_scheduler.start()
    logger.info("Weather scheduler started")


class Month(str, Enum):
    """Enum for month selection in the weather endpoint."""
    January = "January"
    February = "February"
    March = "March"
    April = "April"
    May = "May"
    June = "June"
    July = "July"
    August = "August"
    September = "September"
    October = "October"
    November = "November"
    December = "December"
    All = "all"


@app.get("/weather/{month}", tags=["Weather"])
async def get_weather_by_month(
        month: Month = Path(..., description="Month to get weather data for")
):
    """
    Get weather data for a specific month or all months.

    Returns weather information for Sri Lanka based on the specified month.
    """
    from routers.scheduler import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
    from neo4j import GraphDatabase

    logger.info(f"Weather data requested for month: {month}")

    try:
        # Connect to Neo4j
        driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USER, NEO4J_PASSWORD)
        )

        with driver.session() as session:
            if month == Month.All:
                # Get weather data for all months
                result = session.run("""
                    MATCH (w:Weather)
                    RETURN w.Month as month, 
                           w.Description as description,
                           w.Season as season,
                           w.avg_temp as avg_temp,
                           w.avg_precip as avg_precip,
                           w.precipitation_prob as precip_prob
                    ORDER BY CASE w.Month
                        WHEN 'January' THEN 1
                        WHEN 'February' THEN 2
                        WHEN 'March' THEN 3
                        WHEN 'April' THEN 4
                        WHEN 'May' THEN 5
                        WHEN 'June' THEN 6
                        WHEN 'July' THEN 7
                        WHEN 'August' THEN 8
                        WHEN 'September' THEN 9
                        WHEN 'October' THEN 10
                        WHEN 'November' THEN 11
                        WHEN 'December' THEN 12
                    END
                """)
            else:
                # Get weather data for specific month
                result = session.run("""
                    MATCH (w:Weather {Month: $month})
                    RETURN w.Month as month, 
                           w.Description as description,
                           w.Season as season,
                           w.avg_temp as avg_temp,
                           w.avg_precip as avg_precip,
                           w.precipitation_prob as precip_prob
                """, {"month": month})

            # Process results
            weather_data = []
            for record in result:
                weather_data.append({
                    "month": record["month"],
                    "description": record["description"],
                    "season": record["season"],
                    "average_temperature": record["avg_temp"],
                    "average_precipitation": record["avg_precip"],
                    "precipitation_probability": record["precip_prob"]
                })

            if not weather_data:
                return {"message": f"No weather data found for {month}"}

            return {"weather_data": weather_data}

    except Exception as e:
        logger.error(f"Error retrieving weather data: {str(e)}")
        return {"error": "Failed to retrieve weather data", "details": str(e)}
    finally:
        if 'driver' in locals():
            driver.close()


@app.post("/weather/update/month/{month}", tags=["Weather"])
async def update_specific_month(
        background_tasks: BackgroundTasks,
        month: Month = Path(..., description="Month to update weather data for"),
        areas: List[str] = Query(None, description="Specific areas to update (all areas if not specified)")
):
    """
    Update weather data for a specific month across all or selected areas.

    This endpoint allows targeted updates for specific months' weather data.
    """
    logger.info(f"Manual update for month {month} triggered")

    def run_month_update():
        from routers.scheduler import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
        from routers.weatherapi import WeatherUpdater
        from neo4j import GraphDatabase
        import pandas as pd

        try:
            # Create updater
            updater = WeatherUpdater(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

            # Read coordinates
            try:
                coords_df = pd.read_csv("routers/Coordinates.csv")
            except pd.errors.ParserError:
                coords_df = pd.read_csv(
                    "routers/Coordinates.csv",
                    engine='python',
                    on_bad_lines='skip'
                )

            # Filter areas if specified
            if areas:
                coords_df = coords_df[coords_df['Area'].isin(areas)]

            # Connect to Neo4j to ensure Weather node for month exists
            driver = GraphDatabase.driver(
                NEO4J_URI,
                auth=(NEO4J_USER, NEO4J_PASSWORD)
            )

            with driver.session() as session:
                # Create or ensure Weather node for this month exists
                session.run("""
                    MERGE (w:Weather {Month: $month})
                    ON CREATE SET w.Description = 'Pending Update'
                """, {"month": month})

            # For each area, update the relationship to this month's weather node
            for _, row in coords_df.iterrows():
                area = row['Area']
                lat = float(row['Latitude'])
                lon = float(row['Longitude'])

                with driver.session() as session:
                    # Create relationship between area and this month's weather
                    session.run("""
                        MATCH (a:Area {Areas: $area})
                        MATCH (w:Weather {Month: $month})
                        MERGE (a)-[r:HAS_WEATHER]->(w)
                    """, {"area": area, "month": month})

                # Now trigger actual weather data update for this location
                updater._update_monthly_weather_data(area, lat, lon)

            logger.info(f"Completed update for month {month}")

        except Exception as e:
            logger.error(f"Error updating month {month}: {str(e)}")
        finally:
            if 'driver' in locals():
                driver.close()

    background_tasks.add_task(run_month_update)

    return {
        "message": f"Weather update for {month} has been triggered",
        "areas": "all areas" if not areas else areas
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 