import pymongo

database_url = "mongodb://localhost:27017"
database_name = "app_market_analasys"

def connect_to_db():
    try:
        client = pymongo.MongoClient(database_url)
        db = client[database_name]
        return db
    except Exception as e:
        print(f"Could not connect to MongoDB:")
        return None
