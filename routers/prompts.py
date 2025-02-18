db_structure = """
    The below is the cypher query to create the database structure for the prompts
    
        // Create unique constraints
        CREATE CONSTRAINT District_District_uniq IF NOT EXISTS 
        FOR (n:District) REQUIRE (n.District) IS UNIQUE;
        CREATE CONSTRAINT Areas_Area_uniq IF NOT EXISTS 
        FOR (n:Area) REQUIRE (n.Areas) IS UNIQUE;
"""