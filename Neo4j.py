from neo4j import GraphDatabase
import json

def create_driver():
    try:
        # Replace None with actual authentication details if needed
        return GraphDatabase.driver(uri="bolt://localhost:7687", auth=None)
    except Exception as e:
        print(f"Error creating the driver: {e}")
        return None

def fetch_relationships(driver):
    if not driver:
        print("No driver available")
        return []

    try:
        with driver.session() as session:
            result = session.run("""
            MATCH (i1:Ingredients)-[rel]->(i2:Ingredients)
            RETURN i1.name AS Ingredient1, i2.name AS Ingredient2, type(rel) AS RelationshipType
            """)
            relationships = []
            for record in result:
                relationships.append({
                    "Ingredient1": record["Ingredient1"],
                    "Ingredient2": record["Ingredient2"],
                    "RelationshipType": record["RelationshipType"]
                })
            return relationships
    except Exception as e:
        print(f"Error running the query: {e}")
        return []

def write_to_json(data, file_path):
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data successfully written to {file_path}")
    except Exception as e:
        print(f"Error writing to JSON file: {e}")

# Create the driver
driver = create_driver()

# Fetch the relationships
relationships = fetch_relationships(driver)

# Write the relationships to a JSON file
write_to_json(relationships, 'relationships.json')

# Close the driver connection if it was created successfully
if driver:
    driver.close()
