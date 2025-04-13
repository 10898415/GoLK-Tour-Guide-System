db_structure = """
    The below is the cypher query to create the database structure for the prompts
    
        // Create unique constraints
        CREATE CONSTRAINT District_District_uniq IF NOT EXISTS 
        FOR (n:District) REQUIRE (n.District) IS UNIQUE;
        CREATE CONSTRAINT Areas_Area_uniq IF NOT EXISTS 
        FOR (n:Area) REQUIRE (n.Areas) IS UNIQUE;
        CREATE CONSTRAINT Place_To_Visit_Place_uniq IF NOT EXISTS 
        FOR (n:Place) REQUIRE (n.Place_To_Visit) IS UNIQUE;
        CREATE CONSTRAINT Restaurant_Restaurant_uniq IF NOT EXISTS 
        FOR (n:Restaurant) REQUIRE (n.Restaurant) IS UNIQUE;
        CREATE CONSTRAINT Description_Weather_uniq IF NOT EXISTS 
        FOR (n:Weather) REQUIRE (n.Description) IS UNIQUE;
        CREATE CONSTRAINT Accommodation_Place_Name_Accomadation_uniq IF NOT EXISTS 
        FOR (n:Accomadation) REQUIRE (n.Accommodation_Place_Name) IS UNIQUE;
        CREATE CONSTRAINT Province_Province_uniq IF NOT EXISTS 
        FOR (n:Province) REQUIRE (n.Province) IS UNIQUE;
        CREATE CONSTRAINT Nearest_Police_Station_PoliceStation_uniq IF NOT EXISTS 
        FOR (n:PoliceStation) REQUIRE (n.Nearest_Police_Station) IS UNIQUE;
        CREATE CONSTRAINT Nearest_Hospital_Hospital_uniq IF NOT EXISTS 
        FOR (n:Hospital) REQUIRE (n.Nearest_Hospital) IS UNIQUE;
        CREATE CONSTRAINT Country_Country_uniq IF NOT EXISTS 
        FOR (n:Country) REQUIRE (n.Country) IS UNIQUE;
        
        // Load District nodes
        LOAD CSV WITH HEADERS FROM 'file:///DistrictEthnicity.csv' AS row 
        MERGE (d:District {District: row.District})
        ON CREATE SET 
           d.District = row.District,
           d.Sinhalese = row.Sinhalese, 
           d.Sri_Lankan_Tamils = row.Sri_Lankan_Tamils, 
           d.Indian_Tamils = row.Indian_Tamils, 
           d.Sri_Lankan_Moors = row.Sri_Lankan_Moors, 
           d.Others = row.Others, 
           d.Most_Used_Language = row.Most_Used_Language;

        // Load Area nodes
        LOAD CSV WITH HEADERS FROM 'file:///areas.csv' AS row 
        MERGE (a:Area {Areas: row.Areas})
        ON CREATE SET 
           a.Areas = row.Areas,
           a.Description = row.Description, 
           a.Population = toInteger(trim(row.Population));
        
        // Load Place nodes
        LOAD CSV WITH HEADERS FROM 'file:///places.csv' AS row 
        MERGE (p:Place {Place_To_Visit: row.Place_To_Visit})
        ON CREATE SET 
           p.Place_To_Visit = row.Place_To_Visit,
           p.Activity_Type = row.Activity_Type, 
           p.Description = row.Description;

        // Load Restaurant nodes
        LOAD CSV WITH HEADERS FROM 'file:///restaurants.csv' AS row 
        MERGE (r:Restaurant {Restaurant: row.Restaurant})
        ON CREATE SET 
           r.Restaurant = row.Restaurant,
           r.Ratings = row.Ratings, 
           r.Google_map_link = row.Google_map_link;
        
        // Load Weather nodes
        LOAD CSV WITH HEADERS FROM 'file:///weather.csv' AS row 
        MERGE (w:Weather {Description: row.Description})
        ON CREATE SET 
           w.Description = row.Description,
           w.Month = row.Month, 
           w.Season = row.Season;
"""