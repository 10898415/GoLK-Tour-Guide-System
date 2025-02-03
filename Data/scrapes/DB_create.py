from neo4j import GraphDatabase

###############################################################################
# 1) EDIT THESE TO MATCH YOUR SETUP
###############################################################################
URI = "bolt://localhost:7687"   # Neo4j Desktop default Bolt port
USER = "neo4j"                  # Typically "neo4j" for local dev
PASSWORD = "admin123"           # Change if you set a different password
DATABASE = "GoLK"              # Use "neo4j" if you have not created "GoLK"
###############################################################################


params = {
    "file_path_root": "file:///",

    # CSV files
    "file_0": "SriLanka.csv",
    "file_1": "DistrictEthnicity.csv",
    "file_2": "areas.csv",
    "file_3": "restaurants.csv",
    "file_4": "Hospitals.csv",
    "file_5": "places.csv",
    "file_6": "PoliceStations.csv",
    "file_7": "accomadation.csv",
    "file_8": "weather.csv",
    "file_9": "City_Distances.csv",

    "idsToSkip": []   # Used by WHERE NOT row.[field] IN $idsToSkip
}

# The entire Cypher script (constraints + CSV loading).
# This matches what you provided earlier, just without ":param" or ":use."
cypher_script = """
/////////////////////////////////////////////////////////////////////////
// 1) CREATE CONSTRAINTS
/////////////////////////////////////////////////////////////////////////
CREATE CONSTRAINT `Country_Country_uniq` IF NOT EXISTS
FOR (n: `Country`)
REQUIRE (n.`Country`) IS UNIQUE;

CREATE CONSTRAINT `Province_Province_uniq` IF NOT EXISTS
FOR (n: `Province`)
REQUIRE (n.`Province`) IS UNIQUE;

CREATE CONSTRAINT `District_District_uniq` IF NOT EXISTS
FOR (n: `District`)
REQUIRE (n.`District`) IS UNIQUE;

CREATE CONSTRAINT `Areas_Area_uniq` IF NOT EXISTS
FOR (n: `Area`)
REQUIRE (n.`Areas`) IS UNIQUE;

CREATE CONSTRAINT `Nearest_Hospital_Hospital_uniq` IF NOT EXISTS
FOR (n: `Hospital`)
REQUIRE (n.`Nearest Hospital`) IS UNIQUE;

CREATE CONSTRAINT `restaurant_Resturant_uniq` IF NOT EXISTS
FOR (n: `Resturant`)
REQUIRE (n.`restaurant`) IS UNIQUE;

CREATE CONSTRAINT `Place_to Visit_Place_uniq` IF NOT EXISTS
FOR (n: `Place`)
REQUIRE (n.`Place to Visit`) IS UNIQUE;

CREATE CONSTRAINT `Nearest_Police Station_PoliceStation_uniq` IF NOT EXISTS
FOR (n: `PoliceStation`)
REQUIRE (n.`Nearest Police Station`) IS UNIQUE;

CREATE CONSTRAINT `Accommodation_Place Name_Accomadation_uniq` IF NOT EXISTS
FOR (n: `Accomadation`)
REQUIRE (n.`Accommodation Place Name`) IS UNIQUE;

CREATE CONSTRAINT `Description_Weather_uniq` IF NOT EXISTS
FOR (n: `Weather`)
REQUIRE (n.`Description`) IS UNIQUE;

/////////////////////////////////////////////////////////////////////////
// 2) LOAD NODES FROM CSV
/////////////////////////////////////////////////////////////////////////
LOAD CSV WITH HEADERS FROM ($file_path_root + $file_0) AS row
WITH row
WHERE NOT row.`Country` IN $idsToSkip AND NOT row.`Country` IS NULL
CALL {
  WITH row
  MERGE (n: `Country` { `Country`: row.`Country` })
  SET n.`Country` = row.`Country`
  SET n.`Suwa Seriya Ambulance` = toInteger(trim(row.`Suwa Seriya Ambulance`))
  SET n.`Police Emergency Service` = toInteger(trim(row.`Police Emergency Service`))
  SET n.`Government Information Center` = toInteger(trim(row.`Government Information Center`))
  SET n.`Bomb Disposal Unit` = toInteger(trim(row.`Bomb Disposal Unit`))
  SET n.`National Help Desk` = toInteger(trim(row.`National Help Desk`))
  SET n.`Sri Lanka Tourism Development Authority` = toInteger(trim(row.`Sri Lanka Tourism Development Authority`))
  SET n.`Bandaranaike International Airport` = toInteger(trim(row.`Bandaranaike International Airport`))
  SET n.`Department of Immigration` = toInteger(trim(row.`Department of Immigration`))
  SET n.`SriLankan Airlines` = row.`SriLankan Airlines`
  SET n.`Sri Lanka Railways` = toInteger(trim(row.`Sri Lanka Railways`))
  SET n.`Children Helpline` = toInteger(trim(row.`Children Helpline`))
  SET n.`Women Helpline` = toInteger(trim(row.`Women Helpline`))
  SET n.`Ministry of Foreign Affairs` = toInteger(trim(row.`Ministry of Foreign Affairs`))
  SET n.`Ministry of Health` = toInteger(trim(row.`Ministry of Health`))
  SET n.`Trilingual Health Line` = toInteger(trim(row.`Trilingual Health Line`))
  SET n.`Ceylon Electricity Board` = toInteger(trim(row.`Ceylon Electricity Board`))
  SET n.`National Water Supply and Drainage Board` = toInteger(trim(row.`National Water Supply and Drainage Board`))
  SET n.`Description` = row.`Description`
  SET n.`Nationality` = row.`Nationality`
  SET n.`Currency` = row.`Currency`
  SET n.`National Sport` = row.`National Sport`
  SET n.`National Bird` = row.`National Bird`
  SET n.`National Flower` = row.`National Flower`
  SET n.`National Tree` = row.`National Tree`
  SET n.`Official languages` = row.`Official languages`
  SET n.`Major Ethnic` = row.`Major Ethnic`
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_1) AS row
WITH row
WHERE NOT row.`Province` IN $idsToSkip AND NOT row.`Province` IS NULL
CALL {
  WITH row
  MERGE (n: `Province` { `Province`: row.`Province` })
  SET n.`Province` = row.`Province`
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_1) AS row
WITH row
WHERE NOT row.`District` IN $idsToSkip AND NOT row.`District` IS NULL
CALL {
  WITH row
  MERGE (n: `District` { `District`: row.`District` })
  SET n.`District` = row.`District`
  SET n.`Sinhalese` = row.`Sinhalese`
  SET n.`Sri Lankan Tamils` = row.`Sri Lankan Tamils`
  SET n.`Indian Tamils` = row.`Indian Tamils`
  SET n.`Sri Lankan Moors` = row.`Sri Lankan Moors`
  SET n.`Others` = row.`Others`
  SET n.`Most Used Language` = row.`Most Used Language`
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_2) AS row
WITH row
WHERE NOT row.`Areas` IN $idsToSkip AND NOT row.`Areas` IS NULL
CALL {
  WITH row
  MERGE (n: `Area` { `Areas`: row.`Areas` })
  SET n.`Areas` = row.`Areas`
  SET n.`Description` = row.`Description`
  SET n.`Population` = toInteger(trim(row.`Population`))
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_4) AS row
WITH row
WHERE NOT row.`Nearest Hospital` IN $idsToSkip AND NOT row.`Nearest Hospital` IS NULL
CALL {
  WITH row
  MERGE (n: `Hospital` { `Nearest Hospital`: row.`Nearest Hospital` })
  SET n.`Nearest Hospital` = row.`Nearest Hospital`
  SET n.`Contact Number` = toInteger(trim(row.`Contact Number`))
  SET n.`Google Map Link` = row.`Google Map Link`
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_3) AS row
WITH row
WHERE NOT row.`restaurant` IN $idsToSkip AND NOT row.`restaurant` IS NULL
CALL {
  WITH row
  MERGE (n: `Resturant` { `restaurant`: row.`restaurant` })
  SET n.`restaurant` = row.`restaurant`
  SET n.`ratings` = row.`ratings`
  SET n.`google_map_link` = row.`google_map_link`
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_5) AS row
WITH row
WHERE NOT row.`Place to Visit` IN $idsToSkip AND NOT row.`Place to Visit` IS NULL
CALL {
  WITH row
  MERGE (n: `Place` { `Place to Visit`: row.`Place to Visit` })
  SET n.`Place to Visit` = row.`Place to Visit`
  SET n.`Activity Type` = row.`Activity Type`
  SET n.`Description` = row.`Description`
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_6) AS row
WITH row
WHERE NOT row.`Nearest Police Station` IN $idsToSkip AND NOT row.`Nearest Police Station` IS NULL
CALL {
  WITH row
  MERGE (n: `PoliceStation` { `Nearest Police Station`: row.`Nearest Police Station` })
  SET n.`Nearest Police Station` = row.`Nearest Police Station`
  SET n.`Contact Number` = toInteger(trim(row.`Contact Number`))
  SET n.`Google Map Link` = row.`Google Map Link`
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_7) AS row
WITH row
WHERE NOT row.`Accommodation Place Name` IN $idsToSkip AND NOT row.`Accommodation Place Name` IS NULL
CALL {
  WITH row
  MERGE (n: `Accomadation` { `Accommodation Place Name`: row.`Accommodation Place Name` })
  SET n.`Accommodation Place Name` = row.`Accommodation Place Name`
  SET n.`Rating` = row.`Rating`
  SET n.`Type` = row.`Type`
  SET n.`Description` = row.`Description`
  SET n.`Nearby Places` = row.`Nearby Places`
  SET n.`Booking.com Booking Link` = row.`Booking.com Booking Link`
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_8) AS row
WITH row
WHERE NOT row.`Description` IN $idsToSkip AND NOT row.`Description` IS NULL
CALL {
  WITH row
  MERGE (n: `Weather` { `Description`: row.`Description` })
  SET n.`Description` = row.`Description`
  SET n.`Month` = row.`Month`
  SET n.`Season` = row.`Season`
} IN TRANSACTIONS OF 10000 ROWS;

/////////////////////////////////////////////////////////////////////////
// 3) LOAD RELATIONSHIPS FROM CSV
/////////////////////////////////////////////////////////////////////////
LOAD CSV WITH HEADERS FROM ($file_path_root + $file_1) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Country` { `Country`: row.`Country` })
  MATCH (target: `Province` { `Province`: row.`Province` })
  MERGE (source)-[r: `HAS_PROVINCE`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_1) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Province` { `Province`: row.`Province` })
  MATCH (target: `District` { `District`: row.`District` })
  MERGE (source)-[r: `HAS_DISTRICT`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_2) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Area` { `Areas`: row.`Areas` })
  MATCH (target: `District` { `District`: row.`District` })
  MERGE (source)-[r: `LOCATED_IN`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_9) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Area` { `Areas`: row.`Location 1` })
  MATCH (target: `Area` { `Areas`: row.`Location 2` })
  MERGE (source)-[r: `HAS_DISTANCE`]->(target)
  SET r.`Distance_in_KM` = toFloat(trim(row.`Distance_in_KM`))
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_4) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Area` { `Areas`: row.`Areas` })
  MATCH (target: `Hospital` { `Nearest Hospital`: row.`Nearest Hospital` })
  MERGE (source)-[r: `HAS_HOSPITAL`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_3) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Area` { `Areas`: row.`area` })
  MATCH (target: `Resturant` { `restaurant`: row.`restaurant` })
  MERGE (source)-[r: `HAS_RESTAURANT`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_5) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Area` { `Areas`: row.`Area` })
  MATCH (target: `Place` { `Place to Visit`: row.`Place to Visit` })
  MERGE (source)-[r: `CONSISTED_WITH`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_6) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Area` { `Areas`: row.`Areas` })
  MATCH (target: `PoliceStation` { `Nearest Police Station`: row.`Nearest Police Station` })
  MERGE (source)-[r: `HAS_POLICE`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_7) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Area` { `Areas`: row.`Area` })
  MATCH (target: `Accomadation` { `Accommodation Place Name`: row.`Accommodation Place Name` })
  MERGE (source)-[r: `HAS_ACCOMADATION`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_8) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Area` { `Areas`: row.`Area` })
  MATCH (target: `Weather` { `Description`: row.`Description` })
  MERGE (source)-[r: `HAS_WEATHER`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;
"""

def main():
    # Create a driver object for the given URI and credentials
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    try:
        # Open a session to the specified database
        with driver.session(database=DATABASE) as session:
            # Run the entire script with the parameters
            session.run(cypher_script, **params)
            print("Data load completed successfully!")
    finally:
        driver.close()

if __name__ == "__main__":
    main()
