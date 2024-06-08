from neo4j import GraphDatabase

def create_driver():
    try:
        # Replace None with actual authentication details if needed
        return GraphDatabase.driver(uri="bolt://localhost:7687", auth=None)
    except Exception as e:
        print(f"Error creating the driver: {e}")
        return None

def test_connection(driver):
    if not driver:
        print("No driver available")
        return

    try:
       with driver.session() as session:
            result = session.run("""
            MATCH (i1:Ingredients) 
            MATCH (i2:Ingredients) 
            MATCH (r:Recipe) 
            WHERE EXISTS((r)-[:CONTAINS]->(i1)) AND EXISTS((i1)-[:SUBSTITUTE_Protein]->(i2)) 
            RETURN i1.name AS Ingredient1, i2.name AS Ingredient2, r.name
            """)
         # Fetch and print the result
            for record in result:
                print("Recipe:", record["r.name"])
                print("Ingredient 1:", record["Ingredient1"])
                print("Ingredient 2:", record["Ingredient2"])
                
    except Exception as e:
        print(f"Error running the test query: {e}")

# Create the driver
driver = create_driver()

# Test the connection
test_connection(driver)

# Close the driver connection if it was created successfully
if driver:
    driver.close()
