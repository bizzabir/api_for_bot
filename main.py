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

# Pydantic model for input
class QueryRequest(BaseModel):
    query: str

# API to execute a MySQL query
@app.post("/")
async def execute_query(request: QueryRequest):
    try:
        # Establish database connection
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)  # Use dictionary=True for JSON-friendly output

        # Execute the query
        cursor.execute(request.query)
        # Fetch all results
        result = cursor.fetchall()

        # Close connection
        cursor.close()
        connection.close()

        return {"success": True, "data": result}

    except Error as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
