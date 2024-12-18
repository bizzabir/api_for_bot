from fastapi import FastAPI, HTTPException
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

# Create a reusable function to connect to the database
def get_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None


@app.get("/")
def read_root():
    return {"message": "Welcome to the Sakila API!"}


@app.get("/actors/")
def get_actors():
    """Retrieve all actors from the database."""
    try:
        connection = get_connection()
        if connection is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT actor_id, first_name, last_name FROM actor")
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve actors")


@app.get("/actor/{actor_id}")
def get_actor(actor_id: int):
    """Retrieve details of a specific actor by ID."""
    try:
        connection = get_connection()
        if connection is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT actor_id, first_name, last_name FROM actor WHERE actor_id = %s", (actor_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        if result is None:
            raise HTTPException(status_code=404, detail="Actor not found")
        return result

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve actor")


@app.get("/movies/")
def get_movies():
    """Retrieve all movies (films) from the database."""
    try:
        connection = get_connection()
        if connection is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT film_id, title, description FROM film")
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve movies")
