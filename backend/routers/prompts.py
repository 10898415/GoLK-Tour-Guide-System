db_structure = """
    The below is the cypher query to create the database structure for the prompts
    
        :param {
      // Define the file path root and the individual file names required for loading.
      // https://neo4j.com/docs/operations-manual/current/configuration/file-locations/
      file_path_root: 'file:///', // Change this to the folder your script can access the files at.
      file_0: 'DistrictEthnicity.csv',
      file_1: 'areas.csv',
      file_2: 'places.csv',
      file_3: 'restaurants.csv',
      file_4: 'weather.csv',
      file_5: 'accomadation.csv',
      file_6: 'PoliceStations.csv',
      file_7: 'Hospitals.csv',
      file_8: 'SriLanka.csv',
      file_9: 'City_Distances.csv'
    };
    
    // CONSTRAINT creation
    // -------------------
    //
    // Create node uniqueness constraints, ensuring no duplicates for the given node label and ID property exist in the database. This also ensures no duplicates are introduced in future.
    //
    // NOTE: The following constraint creation syntax is generated based on the current connected database version 5.27.0.
    CREATE CONSTRAINT `District_District_uniq` IF NOT EXISTS
    FOR (n: `District`)
    REQUIRE (n.`District`) IS UNIQUE;
    CREATE CONSTRAINT `Areas_Area_uniq` IF NOT EXISTS
    FOR (n: `Area`)
    REQUIRE (n.`Areas`) IS UNIQUE;
    CREATE CONSTRAINT `Place_To_Visit_Place_uniq` IF NOT EXISTS
    FOR (n: `Place`)
    REQUIRE (n.`Place_To_Visit`) IS UNIQUE;
    CREATE CONSTRAINT `Restaurant_Restaurant_uniq` IF NOT EXISTS
    FOR (n: `Restaurant`)
    REQUIRE (n.`Restaurant`) IS UNIQUE;
    CREATE CONSTRAINT `Description_Weather_uniq` IF NOT EXISTS
    FOR (n: `Weather`)
    REQUIRE (n.`Description`) IS UNIQUE;
    CREATE CONSTRAINT `Accommodation_Place_Name_Accomadation_uniq` IF NOT EXISTS
    FOR (n: `Accomadation`)
    REQUIRE (n.`Accommodation_Place_Name`) IS UNIQUE;
    CREATE CONSTRAINT `Province_Province_uniq` IF NOT EXISTS
    FOR (n: `Province`)
    REQUIRE (n.`Province`) IS UNIQUE;
    CREATE CONSTRAINT `Nearest_Police_Station_PoliceStation_uniq` IF NOT EXISTS
    FOR (n: `PoliceStation`)
    REQUIRE (n.`Nearest_Police_Station`) IS UNIQUE;
    CREATE CONSTRAINT `Nearest_Hospital_Hospital_uniq` IF NOT EXISTS
    FOR (n: `Hospital`)
    REQUIRE (n.`Nearest_Hospital`) IS UNIQUE;
    CREATE CONSTRAINT `Country_Country_uniq` IF NOT EXISTS
    FOR (n: `Country`)
    REQUIRE (n.`Country`) IS UNIQUE;
    
    :param {
      idsToSkip: []
    };
    
    // NODE load
    // ---------
    //
    // Load nodes in batches, one node label at a time. Nodes will be created using a MERGE statement to ensure a node with the same label and ID property remains unique. Pre-existing nodes found by a MERGE statement will have their other properties set to the latest values encountered in a load file.
    //
    // NOTE: Any nodes with IDs in the 'idsToSkip' list parameter will not be loaded.
    LOAD CSV WITH HEADERS FROM ($file_path_root + $file_0) AS row
    WITH row
    WHERE NOT row.`District` IN $idsToSkip AND NOT row.`District` IS NULL
    CALL {
      WITH row
      MERGE (n: `District` { `District`: row.`District` })
      SET n.`District` = row.`District`
      SET n.`Sinhalese` = row.`Sinhalese`
      SET n.`Others` = row.`Others`
      SET n.`Sri_Lankan_Tamils` = row.`Sri_Lankan_Tamils`
      SET n.`Indian_Tamils` = row.`District`
      SET n.`Sri_Lankan_Moors` = row.`Sri_Lankan_Moors`
      SET n.`Most_Used_Language` = row.`Most_Used_Language`
    } IN TRANSACTIONS OF 10000 ROWS;
    
    LOAD CSV WITH HEADERS FROM ($file_path_root + $file_1) AS row
    WITH row
    WHERE NOT row.`Areas` IN $idsToSkip AND NOT row.`Areas` IS NULL
    CALL {
      WITH row
      MERGE (n: `Area` { `Areas`: row.`Areas` })
      SET n.`Areas` = row.`Areas`
      SET n.`Description` = row.`Description`
      SET n.`Population` = toInteger(trim(row.`Population`))
    } IN TRANSACTIONS OF 10000 ROWS;
    
    LOAD CSV WITH HEADERS FROM ($file_path_root + $file_2) AS row
    WITH row
    WHERE NOT row.`Place_To_Visit` IN $idsToSkip AND NOT row.`Place_To_Visit` IS NULL
    CALL {
      WITH row
      MERGE (n: `Place` { `Place_To_Visit`: row.`Place_To_Visit` })
      SET n.`Place_To_Visit` = row.`Place_To_Visit`
      SET n.`Description` = row.`Description`
      SET n.`Activity_Type` = row.`Activity_Type`
    } IN TRANSACTIONS OF 10000 ROWS;
    
    LOAD CSV WITH HEADERS FROM ($file_path_root + $file_3) AS row
    WITH row
    WHERE NOT row.`Restaurant` IN $idsToSkip AND NOT row.`Restaurant` IS NULL
    CALL {
      WITH row
      MERGE (n: `Restaurant` { `Restaurant`: row.`Restaurant` })
      SET n.`Restaurant` = row.`Restaurant`
      SET n.`Ratings` = row.`Ratings`
      SET n.`Google_map_link` = row.`Google_map_link`
    } IN TRANSACTIONS OF 10000 ROWS;
    
    LOAD CSV WITH HEADERS FROM ($file_path_root + $file_4) AS row
    WITH row
    WHERE NOT row.`Description` IN $idsToSkip AND NOT row.`Description` IS NULL
    CALL {
      WITH row
      MERGE (n: `Weather` { `Description`: row.`Description` })
      SET n.`Description` = row.`Description`
      SET n.`Month` = row.`Month`
      SET n.`Season` = row.`Season`
    } IN TRANSACTIONS OF 10000 ROWS;
    
    LOAD CSV WITH HEADERS FROM ($file_path_root + $file_5) AS row
    WITH row
    WHERE NOT row.`Accommodation_Place_Name` IN $idsToSkip AND NOT row.`Accommodation_Place_Name` IS NULL
    CALL {
      WITH row
      MERGE (n: `Accomadation` { `Accommodation_Place_Name`: row.`Accommodation_Place_Name` })
      SET n.`Accommodation_Place_Name` = row.`Accommodation_Place_Name`
      SET n.`Rating` = row.`Rating`
      SET n.`Type` = row.`Type`
      SET n.`Description` = row.`Description`
      SET n.`Nearby_Places` = row.`Nearby_Places`
      SET n.`Booking_Com_Booking_Link` = row.`Booking_Com_Booking_Link`
    } IN TRANSACTIONS OF 10000 ROWS;
    
    LOAD CSV WITH HEADERS FROM ($file_path_root + $file_0) AS row
    WITH row
    WHERE NOT row.`Province` IN $idsToSkip AND NOT row.`Province` IS NULL
    CALL {
      WITH row
      MERGE (n: `Province` { `Province`: row.`Province` })
      SET n.`Province` = row.`Province`
    } IN TRANSACTIONS OF 10000 ROWS;
    
    LOAD CSV WITH HEADERS FROM ($file_path_root + $file_6) AS row
    WITH row
    WHERE NOT row.`Nearest_Police_Station` IN $idsToSkip AND NOT row.`Nearest_Police_Station` IS NULL
    CALL {
      WITH row
      MERGE (n: `PoliceStation` { `Nearest_Police_Station`: row.`Nearest_Police_Station` })
      SET n.`Nearest_Police_Station` = row.`Nearest_Police_Station`
      SET n.`Contact_Number` = toInteger(trim(row.`Contact_Number`))
      SET n.`Google_Map_Link` = row.`Google_Map_Link`
    } IN TRANSACTIONS OF 10000 ROWS;
    
    LOAD CSV WITH HEADERS FROM ($file_path_root + $file_7) AS row
    WITH row
    WHERE NOT row.`Nearest_Hospital` IN $idsToSkip AND NOT row.`Nearest_Hospital` IS NULL
    CALL {
      WITH row
      MERGE (n: `Hospital` { `Nearest_Hospital`: row.`Nearest_Hospital` })
      SET n.`Nearest_Hospital` = row.`Nearest_Hospital`
      SET n.`Contact_Number` = toInteger(trim(row.`Contact_Number`))
      SET n.`Google_Map_Link` = row.`Google_Map_Link`
    } IN TRANSACTIONS OF 10000 ROWS;
    
    LOAD CSV WITH HEADERS FROM ($file_path_root + $file_8) AS row
    WITH row
    WHERE NOT row.`Country` IN $idsToSkip AND NOT row.`Country` IS NULL
    CALL {
      WITH row
      MERGE (n: `Country` { `Country`: row.`Country` })
      SET n.`Country` = row.`Country`
      SET n.`Description` = row.`Description`
      SET n.`Nationality` = row.`Nationality`
      SET n.`Currency` = row.`Currency`
      SET n.`Suwa_Seriya_Ambulance` = toInteger(trim(row.`Suwa_Seriya_Ambulance`))
      SET n.`Police_Emergency_Service` = toInteger(trim(row.`Police_Emergency_Service`))
      SET n.`Government_Information_Center` = toInteger(trim(row.`Government_Information_Center`))
      SET n.`Bomb_Disposal_Unit` = toInteger(trim(row.`Bomb_Disposal_Unit`))
      SET n.`National_Help_Desk` = toInteger(trim(row.`National_Help_Desk`))
      SET n.`Sri_Lanka_Tourism_Development_Authority` = toInteger(trim(row.`Sri_Lanka_Tourism_Development_Authority`))
      SET n.`Bandaranaike_International_Airport` = toInteger(trim(row.`Bandaranaike_International_Airport`))
      SET n.`Department_Of_Immigration` = toInteger(trim(row.`Department_Of_Immigration`))
      SET n.`Srilankan_Airlines` = row.`Srilankan_Airlines`
      SET n.`Sri_Lanka_Railways` = toInteger(trim(row.`Department_Of_Immigration`))
      SET n.`Children_Helpline` = toInteger(trim(row.`Children_Helpline`))
      SET n.`Women_Helpline` = toInteger(trim(row.`Women_Helpline`))
      SET n.`Ministry_Of_Foreign_Affairs` = toInteger(trim(row.`Ministry_Of_Foreign_Affairs`))
      SET n.`Ministry_Of_Health` = toInteger(trim(row.`Ministry_Of_Health`))
      SET n.`Trilingual_Health_Line` = toInteger(trim(row.`Trilingual_Health_Line`))
      SET n.`Ceylon_Electricity_Board` = toInteger(trim(row.`Ceylon_Electricity_Board`))
      SET n.`National_Water_Supply_And_Drainage_Board` = toInteger(trim(row.`National_Water_Supply_And_Drainage_Board`))
      SET n.`National_Sport` = row.`National_Sport`
      SET n.`National_Bird` = row.`National_Bird`
      SET n.`National_Flower` = row.`National_Flower`
      SET n.`National_Tree` = row.`National_Tree`
      SET n.`Official_Languages` = row.`Official_Languages`
      SET n.`Major_Ethnic` = row.`Major_Ethnic`
    } IN TRANSACTIONS OF 10000 ROWS;
    
    
    // RELATIONSHIP load
    // -----------------
    //
    // Load relationships in batches, one relationship type at a time. Relationships are created using a MERGE statement, meaning only one relationship of a given type will ever be created between a pair of nodes.
    LOAD CSV WITH HEADERS FROM ($file_path_root + $file_1) AS row
    WITH row 
    CALL {
      WITH row
      MATCH (source: `Area` { `Areas`: row.`Areas` })
      MATCH (target: `District` { `District`: row.`District` })
      MERGE (source)-[r: `LOCATED_IN`]->(target)
    } IN TRANSACTIONS OF 10000 ROWS;
    
    LOAD CSV WITH HEADERS FROM ($file_path_root + $file_2) AS row
    WITH row 
    CALL {
      WITH row
      MATCH (source: `Area` { `Areas`: row.`Area` })
      MATCH (target: `Place` { `Place_To_Visit`: row.`Place_To_Visit` })
      MERGE (source)-[r: `CONSISTED_WITH`]->(target)
    } IN TRANSACTIONS OF 10000 ROWS;
    
    LOAD CSV WITH HEADERS FROM ($file_path_root + $file_3) AS row
    WITH row 
    CALL {
      WITH row
      MATCH (source: `Area` { `Areas`: row.`Area` })
      MATCH (target: `Restaurant` { `Restaurant`: row.`Restaurant` })
      MERGE (source)-[r: `HAS_RESTAURANT`]->(target)
    } IN TRANSACTIONS OF 10000 ROWS;
    
    LOAD CSV WITH HEADERS FROM ($file_path_root + $file_4) AS row
    WITH row 
    CALL {
      WITH row
      MATCH (source: `Area` { `Areas`: row.`Area` })
      MATCH (target: `Weather` { `Description`: row.`Description` })
      MERGE (source)-[r: `HAS_WEATHER`]->(target)
    } IN TRANSACTIONS OF 10000 ROWS;
    
    LOAD CSV WITH HEADERS FROM ($file_path_root + $file_5) AS row
    WITH row 
    CALL {
      WITH row
      MATCH (source: `Area` { `Areas`: row.`Area` })
      MATCH (target: `Accomadation` { `Accommodation_Place_Name`: row.`Accommodation_Place_Name` })
      MERGE (source)-[r: `HAS_ACCOMADATION`]->(target)
    } IN TRANSACTIONS OF 10000 ROWS;
    
    LOAD CSV WITH HEADERS FROM ($file_path_root + $file_0) AS row
    WITH row 
    CALL {
      WITH row
      MATCH (source: `Province` { `Province`: row.`Province` })
      MATCH (target: `District` { `District`: row.`District` })
      MERGE (source)-[r: `HAS_DISTRICT`]->(target)
    } IN TRANSACTIONS OF 10000 ROWS;
    
    LOAD CSV WITH HEADERS FROM ($file_path_root + $file_9) AS row
    WITH row 
    CALL {
      WITH row
      MATCH (source: `Area` { `Areas`: row.`Location_1` })
      MATCH (target: `Area` { `Areas`: row.`Location_2` })
      MERGE (source)-[r: `HAS_DISTANCE`]->(target)
      SET r.`Distance_in_km` = toFloat(trim(row.`Distance_in_km`))
    } IN TRANSACTIONS OF 10000 ROWS;
    
    LOAD CSV WITH HEADERS FROM ($file_path_root + $file_6) AS row
    WITH row 
    CALL {
      WITH row
      MATCH (source: `Area` { `Areas`: row.`Areas` })
      MATCH (target: `PoliceStation` { `Nearest_Police_Station`: row.`Nearest_Police_Station` })
      MERGE (source)-[r: `HAS_POLICE`]->(target)
    } IN TRANSACTIONS OF 10000 ROWS;
    
    LOAD CSV WITH HEADERS FROM ($file_path_root + $file_7) AS row
    WITH row 
    CALL {
      WITH row
      MATCH (source: `Area` { `Areas`: row.`Areas` })
      MATCH (target: `Hospital` { `Nearest_Hospital`: row.`Nearest_Hospital` })
      MERGE (source)-[r: `HAS_HOSPITAL`]->(target)
    } IN TRANSACTIONS OF 10000 ROWS;
    
    LOAD CSV WITH HEADERS FROM ($file_path_root + $file_0) AS row
    WITH row 
    CALL {
      WITH row
      MATCH (source: `Country` { `Country`: row.`Country` })
      MATCH (target: `Province` { `Province`: row.`Province` })
      MERGE (source)-[r: `HAS_PROVINCE`]->(target)
    } IN TRANSACTIONS OF 10000 ROWS;

        
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
        
        
        weather Node additionaly contain these details and these are the names of the variables.
        
        precipitation_prob  
        last_updated  
        Description  
        avg_temp  
        avg_precip  
        description  
        Month  
        precipitation  
        avg_wind  
        min_temp  
        current_temp  
        season  
        wind_speed  
        Season  
        max_temp  
        precip_prob
        
"""

settings_prompt = """
               Each setting text generation pattern explanation:
                   **Politeness Level**
                    Friendly - Warm, welcoming tone with personal touches and encouraging language
                    - Key terms: "Great to hear from you!", "I'd love to help", "That's wonderful"
                    - Emotionally engaging phrases: "I understand how you feel", "I'm excited to assist"
                    - Personal pronouns: frequent use of "you" and "we"
                    - Encouraging language: "You're doing great", "That's a fantastic approach"

                    Neutral - Balanced, straightforward communication without strong emotional elements
                    - Key terms: "Here is", "This shows", "The following"
                    - Matter-of-fact phrases: "Based on the information", "According to"
                    - Objective language: "The data indicates", "Results show"
                    - Clear statements: "This works by", "The process involves"

                    Professional - Courteous, respectful tone with proper etiquette and business-appropriate language
                    - Key terms: "I appreciate your inquiry", "Thank you for your consideration"
                    - Business phrases: "Per your request", "As discussed", "I am pleased to"
                    - Formal acknowledgments: "Kind regards \n TravelGuru", "Best regards \n TravelGuru" (Mention TravelGuru)
                    - Respectful language: "Would you please", "May I suggest"

                  **Tone**
                    Formal - Structured, sophisticated language with proper grammar and technical terminology
                    - Key terms: "Furthermore", "Nevertheless", "Subsequently"
                    - Complete sentences: No contractions, full proper nouns
                    - Technical terms: Industry-specific vocabulary, precise terminology
                    - Complex structures: "In accordance with", "With regard to"

                    Semi-formal - Balanced mix of professional and conversational elements, moderate use of contractions
                    - Key terms: "I'd suggest", "Let's consider", "We'll examine"
                    - Mixed contractions: Selective use of don't, can't, we'll
                    - Balanced phrases: "This means that", "In other words"
                    - Accessible terminology: Mix of technical and common terms

                    Informal - Casual, conversational style with common expressions and simplified language
                    - Key terms: "Yeah", "Sure thing", "No worries"
                    - Contractions: heavy use of don't, can't, won't, it's
                    - Casual phrases: "Basically", "Kind of", "Pretty much"
                    - Everyday language: Common expressions, simple terms

                  **responseLength**
                    Brief - Concise response focusing on essential information (50-100 words)
                    Medium - Balanced explanation with supporting details (100-250 words)
                    Detailed - Comprehensive coverage with examples and thorough explanations (250+ words)
               """