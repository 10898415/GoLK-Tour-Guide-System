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

         // Load Accommodation nodes
        LOAD CSV WITH HEADERS FROM 'file:///accomadation.csv' AS row 
        MERGE (a:Accomadation {Accommodation_Place_Name: row.Accommodation_Place_Name})
        ON CREATE SET 
           a.Accommodation_Place_Name = row.Accommodation_Place_Name,
           a.Rating = row.Rating, 
           a.Type = row.Type, 
           a.Description = row.Description, 
           a.Nearby_Places = row.Nearby_Places, 
           a.Booking_Com_Booking_Link = row.Booking_Com_Booking_Link;
        
        // Load Province nodes
        LOAD CSV WITH HEADERS FROM 'file:///DistrictEthnicity.csv' AS row 
        MERGE (p:Province {Province: row.Province})
        ON CREATE SET
           p.Province = row.Province;
        
        // Add Police Station nodes
        LOAD CSV WITH HEADERS FROM 'file:///PoliceStations.csv' AS row 
        MERGE (p:PoliceStation {Nearest_Police_Station: row.Nearest_Police_Station})
        ON CREATE SET 
           p.Nearest_Police_Station = row.Nearest_Police_Station,
           p.Contact_Number = toInteger(trim(row.Contact_Number)),
           p.Google_Map_Link = row.Google_Map_Link;
        
        // Add Hospital nodes
        LOAD CSV WITH HEADERS FROM 'file:///Hospitals.csv' AS row 
        MERGE (h:Hospital {Nearest_Hospital: row.Nearest_Hospital})
        ON CREATE SET 
           h.Nearest_Hospital = row.Nearest_Hospital,
           h.Contact_Number = toInteger(trim(row.Contact_Number)),
           h.Google_Map_Link = row.Google_Map_Link;
        
        // Add Country nodes
        LOAD CSV WITH HEADERS FROM 'file:///SriLanka.csv' AS row 
        MERGE (c:Country {Country: row.Country})
        ON CREATE SET 
           c.Country = row.Country,
           c.Suwa_Seriya_Ambulance = toInteger(trim(row.Suwa_Seriya_Ambulance)),
           c.Police_Emergency_Service = toInteger(trim(row.Police_Emergency_Service)),
           c.Description = row.Description,
           c.Nationality = row.Nationality,
           c.Currency = row.Currency;
        
        // Create relationships
        LOAD CSV WITH HEADERS FROM 'file:///areas.csv' AS row 
        MATCH (a:Area {Areas: row.Areas}) 
        MATCH (d:District {District: row.District}) 
        MERGE (a)-[:LOCATED_IN]->(d);
        
        LOAD CSV WITH HEADERS FROM 'file:///places.csv' AS row 
        MATCH (a:Area {Areas: row.Area}) 
        MATCH (p:Place {Place_To_Visit: row.Place_To_Visit}) 
        MERGE (a)-[:CONSISTED_WITH]->(p);
        
        LOAD CSV WITH HEADERS FROM 'file:///restaurants.csv' AS row 
        MATCH (a:Area {Areas: row.Area}) 
        MATCH (r:Restaurant {Restaurant: row.Restaurant}) 
        MERGE (a)-[:HAS_RESTAURANT]->(r);
        
        LOAD CSV WITH HEADERS FROM 'file:///weather.csv' AS row 
        MATCH (a:Area {Areas: row.Area}) 
        MATCH (w:Weather {Description: row.Description}) 
        MERGE (a)-[:HAS_WEATHER]->(w);
        
        LOAD CSV WITH HEADERS FROM 'file:///accomadation.csv' AS row 
        MATCH (a:Area {Areas: row.Area}) 
        MATCH (acc:Accomadation {Accommodation_Place_Name: row.Accommodation_Place_Name}) 
        MERGE (a)-[:HAS_ACCOMADATION]->(acc);
        
        LOAD CSV WITH HEADERS FROM 'file:///DistrictEthnicity.csv' AS row 
        MATCH (p:Province {Province: row.Province}) 
        MATCH (d:District {District: row.District}) 
        MERGE (p)-[:HAS_DISTRICT]->(d);
        
        // Distance between Areas
        LOAD CSV WITH HEADERS FROM 'file:///City_Distances.csv' AS row 
        MATCH (a1:Area {Areas: row.Location_1}) 
        MATCH (a2:Area {Areas: row.Location_2}) 
        MERGE (a1)-[:HAS_DISTANCE {Distance_in_km: toFloat(trim(row.Distance_in_km))}]->(a2);
        
        // Areas to Police Stations
        LOAD CSV WITH HEADERS FROM 'file:///PoliceStations.csv' AS row 
        MATCH (a:Area {Areas: row.Areas}) 
        MATCH (p:PoliceStation {Nearest_Police_Station: row.Nearest_Police_Station}) 
        MERGE (a)-[:HAS_POLICE]->(p);
        
        // Areas to Hospitals
        LOAD CSV WITH HEADERS FROM 'file:///Hospitals.csv' AS row 
        MATCH (a:Area {Areas: row.Areas}) 
        MATCH (h:Hospital {Nearest_Hospital: row.Nearest_Hospital}) 
        MERGE (a)-[:HAS_HOSPITAL]->(h);
        
        // Country to Province relationship
        LOAD CSV WITH HEADERS FROM 'file:///DistrictEthnicity.csv' AS row 
        MATCH (c:Country {Country: row.Country}) 
        MATCH (p:Province {Province: row.Province}) 
        MERGE (c)-[:HAS_PROVINCE]->(p);


        Note: When generating the cypher queries please make sure to do not return the nodes and relationships. please return the properties of the nodes and relationships.
        
        Here are the nodes used:
         
        Accomadation, Area, Country, District, Hospital, Place, PoliceStation, Province, Restaurant, Weather
        
        Here are the relationships used:
        
        CONSISTED_WITH, HAS_ACCOMADATION, HAS_DISTANCE, HAS_DISTRICT, HAS_HOSPITAL, HAS_POLICE, HAS_PROVINCE, HAS_RESTAURANT, HAS_WEATHER, LOCATED_IN
        
        Here are the node properties used:
        
            District Node:
                District (unique constraint)
                Sinhalese
                Sri_Lankan_Tamils
                Indian_Tamils
                Sri_Lankan_Moors
                Others
                Most_Used_Language
                
                
            Area Node:
                Areas (unique constraint)
                Description
                Population (Integer type)
                
                
            Place Node:
                Place_To_Visit (unique constraint)
                Activity_Type
                Description
                
                
            Restaurant Node (When user ask about restaurants use this):
                Restaurant (unique constraint)
                Ratings
                Google_map_link
                
                
            Weather Node:
                Description (unique constraint)
                Month
                Season
                
                
            Accommodation Node (When user ask about hotels/motels use this):
                Accommodation_Place_Name (unique constraint)
                Rating
                Type
                Description
                Nearby_Places
                Booking_Com_Booking_Link
                
                
            Province Node:
                Province (unique constraint)
                
                
            Police Station Node:
                Nearest_Police_Station (unique constraint)
                Contact_Number (Integer type)
                Google_Map_Link
                
                
            Hospital Node:
                Nearest_Hospital (unique constraint)
                Contact_Number (Integer type)
                Google_Map_Link
                
                
            Country Node:
                Country (unique constraint)
                Suwa_Seriya_Ambulance (Integer type)
                Police_Emergency_Service (Integer type)
                Description
                Nationality
                Currency
                
        Here are the relationship properties used:
        
            Area -> District
            Relationship type: LOCATED_IN
            Properties: None
            
            
            Area -> Place
            Relationship type: CONSISTED_WITH
            Properties: None
            
            
            Area -> Restaurant
            Relationship type: HAS_RESTAURANT
            Properties: None
            
            
            Area -> Weather
            Relationship type: HAS_WEATHER
            Properties: None
            
            
            Area -> Accommodation
            Relationship type: HAS_ACCOMADATION
            Properties: None
            
            
            Province -> District
            Relationship type: HAS_DISTRICT
            Properties: None
            
            
            Area -> Area (Distance relationship)
            Relationship type: HAS_DISTANCE
            Properties: Distance_in_km (Float type)
            
            
            Area -> Police Station
            Relationship type: HAS_POLICE
            Properties: None
            
            
            Area -> Hospital
            Relationship type: HAS_HOSPITAL
            Properties: None
            
            
            Country -> Province
            Relationship type: HAS_PROVINCE
            Properties: None
            
        Use only the relationship properties that are not None.
"""