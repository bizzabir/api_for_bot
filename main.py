from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error

app = FastAPI()

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456abcdef",
    "database": "sakila"
}

# Pydantic model for POST input
class QueryRequest(BaseModel):
    query: str

# Function to establish database connection
def get_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

# GET endpoint to retrieve all actors
@app.get("/actors/")
def get_actors():
    """Retrieve all actors from the database."""
    try:
        connection = get_connection()
        if connection is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        cursor = connection.cursor(dictionary=True)  # Dictionary cursor for JSON-like output
        cursor.execute("SELECT actor_id, first_name, last_name FROM actor")
        results = cursor.fetchall()

        cursor.close()
        connection.close()

        return {"success": True, "data": results}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve actors")

# POST endpoint to execute a dynamic query
@app.post("/execute-query/")
async def execute_query(request: QueryRequest):
    try:
        connection = get_connection()
        if connection is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        cursor = connection.cursor(dictionary=True)
        cursor.execute(request.query)
        result = cursor.fetchall()

        cursor.close()
        connection.close()

        return {"success": True, "data": result}

    except Error as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
